# 🎧 Live Call Insights

**AI-powered audio call analysis dashboard** built using **OpenAI Whisper**, **Hugging Face Transformers**, and **Streamlit**.

Analyze call recordings to extract:
-  Transcriptions
-  Speaker Diarization
-  Emotion & Sentiment
-  Conversational Insights



---

##  Features

 1. Transcribe audio using Whisper  
 2. Detect speaker turns  
 3. Analyze emotions and sentiments using RoBERTa  
 4. Chat with an AI Assistant based on call content  
 5. Visualize key metrics with Plotly and Matplotlib

---

##  Tech Stack

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Hugging Face Transformers](https://huggingface.co/)
- spaCy, NLTK, Pandas, Plotly

---

##  Run Locally

```bash
# Clone the repo
git clone https://github.com/Jessicawadhwa/Live-Call-Insights.git
cd Live-Call-Insights

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py





