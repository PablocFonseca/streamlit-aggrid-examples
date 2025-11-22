"""
Simple Streamlit interface for the FastAPI backend
"""
import streamlit as st
from backend_poc import start_backend, get_messages, clear_messages, get_message_count


# Start backend on first run
start_backend()

st.title("Message Accumulator")

# Display message count
count = get_message_count()
st.metric("Total Messages", count)

col1, col2 = st.columns(2)

with col1:
    if st.button("Show Messages"):
        messages = get_messages()
        if messages:
            st.json(messages)
        else:
            st.info("No messages yet")

with col2:
    if st.button("Clear Messages"):
        clear_messages()
        st.success("Messages cleared")
        st.rerun()

st.divider()

st.code("""
# Send a test message:
curl -X POST http://localhost:8000/message \\
  -H "Content-Type: application/json" \\
  -d '{"data": {"ticker": "BTC", "price": 50000}}'
""", language="bash")
