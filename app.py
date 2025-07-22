import streamlit as st
import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv
import os

# Load API key securely
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("🚨 API Key is missing! Set it in Streamlit Secrets or a .env file.")
    st.stop()

# Streamlit UI
st.set_page_config(page_title="🎙️ Arabic to English Voice Translator", page_icon="🗣️", layout="centered")
st.title("🎙️ Arabic to English Voice Translator")
st.markdown("Press the button to speak Arabic. Your speech will be translated to English using AI.")

# Create Groq Client
client = Groq(api_key=GROQ_API_KEY)

# Microphone button
if st.button("🎤 Start Listening (Speak Arabic Now)"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎧 Listening... Speak now")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

    try:
        # Transcribe Arabic speech to text
        arabic_text = recognizer.recognize_google(audio, language="ar")
        st.success(f"🗣️ Detected Arabic: {arabic_text}")

        # Translate using GROQ LLM
        prompt = f"Translate this Arabic sentence into English: {arabic_text}"
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional Arabic-to-English translator."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192"
        )

        translation = response.choices[0].message.content.strip()
        st.subheader("✅ English Translation:")
        st.success(translation)

    except sr.UnknownValueError:
        st.error("❌ Sorry, could not understand your speech.")
    except sr.RequestError as e:
        st.error(f"❌ Error from speech recognition service: {e}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
