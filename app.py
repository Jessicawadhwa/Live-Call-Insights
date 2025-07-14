import streamlit as st
from login import login_ui
from dashboard import show_dashboard

st.set_page_config(page_title="Live Call Insights", layout="wide")

# If not logged in, show login UI
if "logged_in" not in st.session_state:
    username, password, clicked = login_ui()

    if clicked:
        # Accept any username/password, store in session for further use
        st.session_state.logged_in = True
        st.session_state.username = username.strip()
        st.session_state.password = password.strip()
        st.rerun()
else:
    show_dashboard()
