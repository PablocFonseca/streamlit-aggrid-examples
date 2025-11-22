"""
FastAPI Backend POC - Message Accumulator

A simple FastAPI backend that runs in a separate thread and accumulates messages.
The main Streamlit thread can read accumulated messages via get_messages().

Usage in Streamlit:
    from backserver.backend_poc import start_backend, get_messages

    # Start the backend once (check if already running)
    start_backend()

    # Read accumulated messages
    messages = get_messages()
    st.write(messages)
"""

import threading
from typing import List, Dict, Any
from collections import deque
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


# Thread-safe message store
message_store = deque(maxlen=1000)  # Limit to last 1000 messages
store_lock = threading.Lock()


class Message(BaseModel):
    """Message model for POST requests"""
    data: Dict[str, Any]


# FastAPI app
app = FastAPI(title="Message Accumulator Backend")


@app.post("/message")
async def receive_message(message: Message):
    """
    POST endpoint to receive and accumulate messages.

    Example:
        curl -X POST http://localhost:8000/message \
             -H "Content-Type: application/json" \
             -d '{"data": {"ticker": "BTC", "price": 50000}}'
    """
    with store_lock:
        message_store.append(message.data)

    return {
        "status": "success",
        "message": "Message accumulated",
        "total_messages": len(message_store)
    }


# Helper functions for Streamlit integration


def get_messages(clear: bool = False) -> List[Dict[str, Any]]:
    """
    Get accumulated messages (thread-safe).

    Args:
        clear: If True, clear the message store after reading

    Returns:
        List of accumulated messages
    """
    with store_lock:
        messages = list(message_store)
        if clear:
            message_store.clear()

    return messages


def get_message_count() -> int:
    """Get the current count of accumulated messages (thread-safe)"""
    with store_lock:
        return len(message_store)


def clear_messages():
    """Clear all accumulated messages (thread-safe)"""
    with store_lock:
        message_store.clear()


# Backend thread management
_backend_thread = None
_backend_running = False


def _run_server():
    """Internal function to run the FastAPI server"""
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


def start_backend(host: str = "127.0.0.1", port: int = 8000):
    """
    Start the FastAPI backend in a daemon thread.

    Args:
        host: Host to bind to (default: 127.0.0.1)
        port: Port to bind to (default: 8000)

    Note:
        This function is idempotent - calling it multiple times won't
        start multiple servers.
    """
    global _backend_thread, _backend_running

    if _backend_running and _backend_thread and _backend_thread.is_alive():
        print("Backend is already running")
        return

    print(f"Starting FastAPI backend on {host}:{port}...")

    _backend_thread = threading.Thread(
        target=_run_server,
        daemon=True,
        name="FastAPIBackend"
    )
    _backend_thread.start()
    _backend_running = True

    print(f"Backend started! Access at http://{host}:{port}")
    print(f"POST messages to: http://{host}:{port}/message")


if __name__ == "__main__":
    # Run standalone for testing
    print("Running FastAPI backend in main thread (for testing)")
    print("POST messages to: http://127.0.0.1:8000/message")
    print("\nExample curl command:")
    print('curl -X POST http://localhost:8000/message \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"data": {"ticker": "BTC", "price": 50000}}\'')

    uvicorn.run(app, host="127.0.0.1", port=8000)
