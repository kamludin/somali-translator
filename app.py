import streamlit as st
from deep_translator import GoogleTranslator, MyMemoryTranslator
import pyttsx3
import base64
import time
import random

def translate_text(text, target_lang="english"):
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        return translator.translate(text)
    except Exception:
        try:
            translator = MyMemoryTranslator(source='auto', target=target_lang)
            return translator.translate(text)
        except Exception:
            return "Translation not available. Please try again later."

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def loading_animation():
    with st.spinner("Processing..."):
        time.sleep(random.uniform(1, 3))

st.set_page_config(page_title="Somali Translator", page_icon="🌍")
st.title("🌍 Somali Language Translator")

dark_mode = st.checkbox("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
        <style>
            .main {background-color: #2c2f33; color: white;}
        </style>
    """, unsafe_allow_html=True)

target_language = st.selectbox("Select target language:", ["English", "French", "Spanish", "German", "Arabic", "Turkish", "Chinese", "Hindi", "Swahili"])

somali_text = st.text_area("✍️ Enter Somali text:")

translation = ""
if st.button("🔄 Translate"):
    loading_animation()
    translation = translate_text(somali_text, target_language.lower())
    st.markdown(f"### 📖 Translation:")
    st.success(translation)
    
    if st.button("🔊 Listen to Translation"):
        text_to_speech(translation)
    
    st.button("📋 Copy to Clipboard", on_click=lambda: st.session_state.update({'clipboard': translation}))
    
    b64 = base64.b64encode(translation.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="translation.txt">📥 Download Translation</a>'
    st.markdown(href, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

if somali_text and translation:
    st.session_state.history.append((somali_text, translation))

st.subheader("📜 Translation History")
for original, translated in st.session_state.history[-5:]:
    st.write(f"**Somali:** {original}")
    st.write(f"**Translation:** {translated}")
    st.markdown("---")

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if st.button("⭐ Save to Favorites"):
    st.session_state.favorites.append((somali_text, translation))

st.subheader("⭐ Favorite Translations")
for original, translated in st.session_state.favorites:
    st.write(f"**Somali:** {original}")
    st.write(f"**Translation:** {translated}")
    st.markdown("---")

st.sidebar.header("ℹ️ About the App")
st.sidebar.info("This app allows users to translate Somali text into multiple languages, listen to translations, save favorite translations, and more.")

st.sidebar.header("🛠 Features")
st.sidebar.markdown("- 🔄 Real-time Translation")
st.sidebar.markdown("- 🔊 Text-to-Speech")
st.sidebar.markdown("- 📜 Translation History")
st.sidebar.markdown("- ⭐ Save Favorite Translations")
st.sidebar.markdown("- 🌙 Dark Mode Support")
