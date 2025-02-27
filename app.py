LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Marathi": "mr",
    "Telugu": "te",
    "Tamil": "ta",
    "Gujarati": "gu",
    "Urdu": "ur",
    "Kannada": "kn",
    "Odia": "or",
    "Malayalam": "ml"
}

import streamlit as st
from streamlit_mic_recorder import speech_to_text
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
    tts = gTTS(text=text, lang=LANGUAGE_CODES[lang])
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.getvalue()

# Streamlit app
st.title("Multi-Language Voice Translator using LLAMA3.2")

# Language selection
languages = list(LANGUAGE_CODES.keys())
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Select source language", languages, index=languages.index("English"))
    
with col2:
    target_lang = st.selectbox("Select target language", languages, index=languages.index("Hindi"))

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"{source_lang} to {target_lang}")
    source_speech = speech_to_text(language=LANGUAGE_CODES[source_lang], key='source_speech')
    if source_speech:
        st.write(f"{source_lang}: {source_speech}")
        translation = translate_text(source_speech, source_lang, target_lang)
        st.write(f"{target_lang}: {translation}")
        
        # Convert translation to speech
        audio = text_to_speech(translation, target_lang)
        st.audio(audio, format="audio/mp3")

with col2:
    st.subheader(f"{target_lang} to {source_lang}")
    target_speech = speech_to_text(language=LANGUAGE_CODES[target_lang], key='target_speech')
    if target_speech:
        st.write(f"{target_lang}: {target_speech}")
        translation = translate_text(target_speech, target_lang, source_lang)
        st.write(f"{source_lang}: {translation}")
        
        # Convert translation to speech
        audio = text_to_speech(translation, source_lang)
        st.audio(audio, format="audio/mp3")