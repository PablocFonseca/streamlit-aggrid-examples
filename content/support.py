"""
Support the Project
===================

Help keep streamlit-aggrid alive and thriving!
"""

import streamlit as st

st.set_page_config(page_title="Support the Project", layout="centered")

st.title("💝 Support the Project")

st.markdown(
    """
    ### Why Your Support Matters

    **streamlit-aggrid** is the result of countless hours of dedication by a solo Python developer.
    This project provides powerful data grid capabilities to the Streamlit community, completely free and open-source.

    If you find it useful, consider giving back to help keep it alive and thriving.
    """
)

st.divider()

st.markdown(
    """
    ### Show Your Appreciation
    Your donations directly support the continued development, maintenance, and improvement of streamlit-aggrid.
    Every contribution, no matter the size, makes a difference.
    """
)

# PayPal Donation Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.link_button(
        "Donate via PayPal",
        "https://www.paypal.com/donate?hosted_button_id=8HGLA4JZBYFPQ",
        use_container_width=True,
        type="primary"
    )

st.markdown("###")

st.markdown(
    """
    ### Professional Services & Custom Development

    Need something special? I'm available for custom features, priority support, or enterprise solutions.
    Whether it's tailored functionality, urgent bug fixes, or dedicated consulting, let's make streamlit-aggrid work perfectly for your needs.
    """
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.link_button(
        "Contact for Custom Development",
        "mailto:pablo.fonseca+staggrid@gmail.com",
        use_container_width=True
    )