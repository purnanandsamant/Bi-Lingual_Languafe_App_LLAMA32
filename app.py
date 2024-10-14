import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import re

# Initialize Groq client
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

# Function to translate text using LLAMA3.2
def translate_text(text, source_lang, target_lang):
    try:
        prompt = f"Translate the following {source_lang} text to {target_lang}. Provide only the translation without any additional information: '{text}'"
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a translator. Provide only the translation without any explanations or additional text."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-70b-8192",
            temperature=0.3,
            max_tokens=1024,
        )
        translation = chat_completion.choices[0].message.content.strip()
        
        # Remove any quotation marks or extra spaces
        translation = re.sub(r'^["\']|["\']$', '', translation).strip()
        
        return translation
    except Exception as e:
        return f"Translation error: {str(e)}"

# Function to convert text to speech
def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.getvalue()

# Streamlit app
st.title("Marathi-English Voice Translator using LLAMA3.2")

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("Marathi to English")
    marathi_speech = speech_to_text(language='mr', key='marathi_speech')
    if marathi_speech:
        st.write(f"Marathi: {marathi_speech}")
        english_translation = translate_text(marathi_speech, 'Marathi', 'English')
        st.write(f"English: {english_translation}")
        
        # Convert translation to speech
        english_audio = text_to_speech(english_translation, 'en')
        st.audio(english_audio, format="audio/mp3")

with col2:
    st.subheader("English to Marathi")
    english_speech = speech_to_text(language='en', key='english_speech')
    if english_speech:
        st.write(f"English: {english_speech}")
        marathi_translation = translate_text(english_speech, 'English', 'Marathi')
        st.write(f"Marathi: {marathi_translation}")
        
        # Convert translation to speech
        marathi_audio = text_to_speech(marathi_translation, 'mr')
        st.audio(marathi_audio, format="audio/mp3")