import streamlit as st
import whisper
import os
import requests
import time
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from transformers import pipeline
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Hugging Face Emotion Classifier
emotion_classifier = pipeline("text-classification", 
                              model="j-hartmann/emotion-english-distilroberta-base",
                              top_k=1)

# Set ffmpeg path manually
os.environ["PATH"] += os.pathsep + r"C:\\Users\\DELL\\Downloads\\ffmpeg-7.0.2-full_build\\bin"

# AssemblyAI API Key
ASSEMBLYAI_API_KEY = "9c4c469dbb5b4679a357429970291cfd"

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    if not os.path.exists("temp"):
        os.makedirs("temp")
    audio_path = os.path.join("temp", audio_file.name)
    with open(audio_path, "wb") as f:
        f.write(audio_file.getbuffer())
    result = model.transcribe(audio_path)
    return result["text"], audio_path

def transcribe_with_diarization(file_path):
    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }
    try:
        with open(file_path, 'rb') as f:
            upload_response = requests.post(
                'https://api.assemblyai.com/v2/upload',
                headers={"authorization": ASSEMBLYAI_API_KEY},
                data=f
            )
        upload_response.raise_for_status()
        upload_url = upload_response.json().get("upload_url")
        if not upload_url:
            st.error("Upload failed: No URL returned.")
            st.stop()
        json_data = {
            "audio_url": upload_url,
            "speaker_labels": True,
            "sentiment_analysis": True
        }
        transcript_response = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            json=json_data,
            headers=headers
        )
        transcript_id = transcript_response.json()['id']
        while True:
            polling_response = requests.get(
                f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
                headers=headers
            )
            status = polling_response.json()['status']
            if status == 'completed':
                return polling_response.json()
            elif status == 'error':
                raise Exception("Transcription failed:", polling_response.json())
            time.sleep(3)
    except Exception as e:
        st.error(f"Upload or transcription failed: {str(e)}")
        st.stop()

def segment_sentences(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

def analyze_emotions(text):
    segments = segment_sentences(text)
    emotions = []
    for seg in segments:
        result = emotion_classifier(seg)
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], list) and len(result[0]) > 0:
                label = result[0][0].get("label")
            elif isinstance(result[0], dict):
                label = result[0].get("label")
            else:
                label = None
            if label:
                emotions.append(label)
    return emotions

def plot_emotion_pie_chart(emotions):
    counts = Counter(emotions)
    df = pd.DataFrame(counts.items(), columns=['Emotion', 'Count'])
    fig = px.pie(df, names='Emotion', values='Count', title='Emotion Distribution', hole=0.3)
    st.plotly_chart(fig, use_container_width=True, key="emotion_pie")

def plot_top_3_bar_chart(emotions):
    counts = Counter(emotions)
    top3 = counts.most_common(3)
    if not top3:
        st.warning("⚠️ Not enough emotion data to plot Top 3 Bar Chart.")
        return
    labels, values = zip(*top3)
    fig = go.Figure([go.Bar(x=labels, y=values, marker_color='indianred')])
    fig.update_layout(title="Top 3 Emotions (Bar Chart)", xaxis_title="Emotion", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True, key="emotion_bar")

def show_dashboard():
    st.set_page_config(layout="wide")
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] { background-color: white !important; color: black; }
        .stApp { background: linear-gradient(to right, #63C5DA, #e6f7ff); }
        .welcome-box { background-color: #d4edda; color: #155724; padding: 10px; border-radius: 8px; font-weight: bold; }
        .assistant-box { background-color: #9b59b6; color: white; padding: 8px; border-radius: 6px; font-weight: bold; text-align: center; margin-top: 10px; margin-bottom: 10px; }
        .black-box { background-color: black; height: 40px; border-radius: 6px; margin-bottom: 10px; }
        .chat-bubble { background: linear-gradient(to right, #f77062, #fe5196); color: white; padding: 12px; border-radius: 10px; font-size: 14px; margin-bottom: 10px; }
        .upload-instruction { margin-top: 10px; color: #555; }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        username = "Jessica"
        st.markdown(f'<div class="welcome-box">Welcome {username}!</div>', unsafe_allow_html=True)
        st.markdown('<div class="assistant-box">🤖 Assistant</div>', unsafe_allow_html=True)
        st.markdown('<div class="black-box"></div>', unsafe_allow_html=True)
        st.markdown('<div class="chat-bubble">👋 Hi! I\'m your Call Insights AI assistant. I can help you analyze call data, explain sentiment trends, and answer questions about your dashboard.</div>', unsafe_allow_html=True)
        user_question = st.text_input("Ask a question...", key="chat_input")
        if st.button("Send", type="primary"):
            response = ""
            query = user_question.strip().lower()
            summary = st.session_state.get("emotion_summary")
            if "emotion" in query and summary:
                response += "Detected emotions are:\n"
                for emo, count in summary.items():
                    response += f"- {emo}: {count}\n"
            elif not summary:
                response = "Emotion analysis not available yet. Upload and analyze an audio file first."
            else:
                response = "Sorry, I can only answer emotion-related questions right now."
            st.markdown(f"<div class='chat-bubble'>{response}</div>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: left;'>📞 Live Call Insights Dashboard</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a"], label_visibility="collapsed")
    st.markdown('<p class="upload-instruction">Limit: 200MB per file • MP3, WAV, M4A</p>', unsafe_allow_html=True)

    if uploaded_file:
        st.success("File uploaded successfully!")
        st.audio(uploaded_file, format="audio/wav")

        with st.spinner("Transcribing using Whisper..."):
            transcript, audio_path = transcribe_audio(uploaded_file)
            st.subheader("📝 Transcription:")
            st.write(transcript)

        with st.spinner("Running speaker diarization and sentiment analysis using AssemblyAI..."):
            result = transcribe_with_diarization(audio_path)
            utterances = result.get("utterances", [])
            st.subheader("🧑‍🧑 Speaker Diarization:")
            if utterances:
                for utt in utterances:
                    speaker = utt.get("speaker", "Unknown")
                    start_time = round(utt.get("start", 0) / 1000, 2)
                    text = utt.get("text", "").strip()
                    if text:
                        st.markdown(f"""
                            <div style="padding: 10px; margin-bottom: 10px; border-radius: 10px; background-color: #f9f9f9; border-left: 6px solid #6c63ff;">
                                <strong>🗣️ Speaker {speaker}</strong> <span style="color: gray;">({start_time}s)</span><br>
                                <span style="font-size: 15px;">{text}</span>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No speaker diarization data found.")

        total_words = result.get("words", [])
        wpm = result.get("audio_duration", 0) / 60

        st.subheader("📈 Metrics:")
        st.metric("Words/Min", round(len(total_words) / wpm, 2))
        st.metric("Total Words", len(total_words))

        with st.spinner("🔍 Running Emotion Detection using RoBERTa..."):
            emotions = analyze_emotions(transcript)
            st.session_state["emotions"] = emotions
            st.session_state["emotion_summary"] = Counter(emotions)

            st.metric("Emotions", len(emotions))
            st.markdown("### 🎯 Emotion Summary (Pie Chart):")
            plot_emotion_pie_chart(emotions)

            st.markdown("### 🏆 Top 3 Emotions (Bar Chart):")
            plot_top_3_bar_chart(emotions)
