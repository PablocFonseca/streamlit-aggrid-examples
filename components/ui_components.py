"""UI components for the streamlit-aggrid-examples app."""

import streamlit as st


def inject_banner_styles():
    """Inject CSS styles for the banner and premium button."""
    st.markdown("""
<style>
    .banner {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        color: white;
        text-align: center;
        padding: 8px 0;
        font-weight: bold;
        font-size: 14px;
        z-index: 9999;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        animation: slide 15s linear infinite;
    }

    @keyframes slide {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }

    .banner:hover {
        animation-play-state: paused;
    }

    /* Adjust main content to account for banner */
    .stApp > header {
        margin-top: 40px;
    }

    /* Alternative: push down the entire app */
    .stApp {
        margin-top: 40px;
    }

    /* Premium button styling */
    .premium-button {
        position: fixed;
        top: 50px;
        right: 20px;
        background: linear-gradient(45deg, #ff6b6b, #ffd700);
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        color: white;
        font-weight: bold;
        text-decoration: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        z-index: 9998;
        transition: transform 0.2s ease;
        cursor: pointer;
        font-size: 14px;
        display: inline-block;
    }

    .premium-button:hover {
        transform: scale(1.05);
        text-decoration: none;
        color: white;
        background: linear-gradient(45deg, #ff5555, #ffcc00);
    }
</style>
""", unsafe_allow_html=True)


def render_banner():
    """Render the promotional banner at the top of the page."""
    st.markdown("""
<div class="banner">
    🎉 Transform your data with the World's Most Powerful Grid Component for Streamlit!
    ✨ Enterprise-grade features • Lightning-fast performance • Beautiful UI 🚀
</div>
""", unsafe_allow_html=True)


def get_premium_button_js():
    """Get the JavaScript code for the premium button component."""
    return """
export default function(component) {
    const { parentElement } = component;

    console.log("Premium button component is running!");

    // Function to create button
    function createButton() {
        // Remove existing button if it exists
        const existingButton = document.getElementById('premium-button');
        if (existingButton) {
            existingButton.remove();
        }

        // Find the navigation overflow container
        const navContainer = document.querySelector('.rc-overflow.st-emotion-cache-qreyob.en0apyo13');
        if (!navContainer) {
            console.log("Navigation container not found, retrying...");
            return false;
        }

        // Create the button container similar to other nav items
        const buttonContainer = document.createElement('div');
        buttonContainer.className = 'rc-overflow-item';
        buttonContainer.style.opacity = '1';
        buttonContainer.style.order = '5'; // After demos (order 3)
        buttonContainer.id = 'premium-button-container';

        // Create inner structure similar to nav items
        const innerDiv = document.createElement('div');
        innerDiv.className = 'st-emotion-cache-1u3ygr en0apyo15';

        const linkContainer = document.createElement('div');
        linkContainer.className = 'st-emotion-cache-1gb1rig en0apyo2';
        linkContainer.setAttribute('data-testid', 'stTopNavLinkContainer');

        // Create the actual link button - match navigation styling
        const button = document.createElement('a');
        button.id = 'premium-button';
        button.className = 'st-emotion-cache-1erimsn en0apyo5';
        button.href = 'https://streamlitaggrid.com';
        button.target = '_blank';
        // Remove custom styling to match navigation
        button.style.textDecoration = 'none';
        button.style.display = 'flex';
        button.style.alignItems = 'center';
        button.style.gap = '8px';

        // Create icon span
        const iconSpan = document.createElement('span');
        iconSpan.className = 'st-emotion-cache-1dl0i61 en0apyo3';

        const colorSpan = document.createElement('span');
        colorSpan.className = 'st-emotion-cache-rwl0nn e1t4gh342';
        colorSpan.setAttribute('color', '#fafafa');

        const emojiSpan = document.createElement('span');
        emojiSpan.className = 'st-emotion-cache-119a5a9 e1t4gh344';
        emojiSpan.setAttribute('data-testid', 'stIconEmoji');
        emojiSpan.setAttribute('aria-hidden', 'true');
        emojiSpan.setAttribute('color', '#fafafa');
        emojiSpan.innerHTML = '💎';

        colorSpan.appendChild(emojiSpan);
        iconSpan.appendChild(colorSpan);

        // Create label span
        const labelSpan = document.createElement('span');
        labelSpan.className = 'st-emotion-cache-dua26v en0apyo6';
        labelSpan.setAttribute('label', 'Streamlit-Aggrid Premium');
        labelSpan.innerHTML = 'Streamlit-Aggrid Premium';

        // Create external link arrow icon
        const arrowSpan = document.createElement('span');
        arrowSpan.style.fontSize = '12px';
        arrowSpan.style.opacity = '0.7';
        arrowSpan.style.marginLeft = '0px';
        arrowSpan.innerHTML = '↗';

        // Remove custom hover effects to match navigation

        // Assemble the structure
        button.appendChild(iconSpan);
        button.appendChild(labelSpan);
        button.appendChild(arrowSpan);
        linkContainer.appendChild(button);
        innerDiv.appendChild(linkContainer);
        buttonContainer.appendChild(innerDiv);

        // Insert after the demos item (before the rest item)
        const restItem = navContainer.querySelector('.rc-overflow-item-rest');
        if (restItem) {
            navContainer.insertBefore(buttonContainer, restItem);
        } else {
            navContainer.appendChild(buttonContainer);
        }

        console.log("Premium button created successfully in navigation!");
        return true;
    }

    // Try to create button multiple times with delays
    let attempts = 0;
    const maxAttempts = 10;

    function tryCreateButton() {
        if (createButton() || attempts >= maxAttempts) {
            return;
        }
        attempts++;
        setTimeout(tryCreateButton, 200);
    }

    // Start trying to create the button
    tryCreateButton();

    // Cleanup function
    return () => {
        const buttonContainer = document.getElementById('premium-button-container');
        if (buttonContainer) {
            buttonContainer.remove();
        }
    };
}
"""


def get_premium_button_component():
    """Create and return the premium button component."""
    return st.components.v2.component(
        "premium_button",
        js=get_premium_button_js(),
    )


def render_premium_button():
    """Render the premium button component in the navigation."""
    premium_button_component = get_premium_button_component()
    premium_button_component()
