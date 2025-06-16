import streamlit as st
from view.styling import CHAT_STYLES


def configure_streamlit() -> None:
    st.set_page_config(layout='wide', page_title='ADK Chat UI')
    st.markdown(CHAT_STYLES, unsafe_allow_html=True)
