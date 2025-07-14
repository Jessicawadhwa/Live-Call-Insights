import streamlit as st

def login_ui():
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-color: #63C5DA !important;
        }

        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .login-box {
            background-color: white;
            padding: 40px;
            height: 300px;  
            width: 500px;   
            border-radius: 22px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            text-align: center;
        }

        .title {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 4px;
        }

        .subtitle {
            font-size: 16px;
            color: #555;
            margin-bottom: 15px;
        }

        .stTextInput input {
            height: 40px;
            border-radius: 10px;
            padding: 0 12px;
            font-size: 15px;
        }

        .stButton>button {
            background-color: #1E3A8A;
            color: white;
            height: 42px;
            border-radius: 10px;
            width: 100%;
            font-weight: bold;
            margin-top: 10px;
        }
        </style>

        <div class="container">
            <div class="login-box">
                <div class="title">
                    <img src="https://em-content.zobj.net/thumbs/240/apple/354/locked_1f512.png" width="26" style="vertical-align: middle; margin-right: 8px;" />
                    Live Call Insights
                </div>
                <div class="subtitle">Smart Call Transcription & Sentiment Dashboard</div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_clicked = st.button("Login")

    st.markdown("</div></div>", unsafe_allow_html=True)

    return username, password, login_clicked