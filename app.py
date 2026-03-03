import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CartIQ",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, header, footer, .stDeployButton, [data-testid="stToolbar"] { display: none !important; }
    .main .block-container { padding: 0 !important; max-width: 100% !important; }
    section[data-testid="stSidebar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

with open("cartiq.html", "r") as f:
    html_content = f.read()

components.html(html_content, height=1400, scrolling=True)
