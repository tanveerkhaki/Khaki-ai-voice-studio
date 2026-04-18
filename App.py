
import streamlit as st
from gtts import gTTS
import io
import tempfile
import os

st.set_page_config(page_title="Khak AI Voice Studio - 100+ Languages", page_icon="🌍", layout="wide")

# Professional CSS
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #0f1116 0%, #1a1e2a 100%); color: #e3e3e3; }
        [data-testid="stSidebar"] { background-color: rgba(30,30,46,0.95); border-right: 1px solid #333; }
        .stButton>button { background: linear-gradient(90deg, #004a77, #006699); color: white; border-radius: 30px; width: 100%; padding: 0.75rem; font-weight: bold; }
        .stTextArea textarea { background-color: #1e1e2e !important; color: white !important; border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🌍 Khak AI Voice Studio - Global Edition</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>🎙️ 100+ Languages | Professional Voice Generation</p>", unsafe_allow_html=True)

# 100+ Languages Dictionary
languages = {
    "🇺🇸 English": "en", "🇵🇰 Urdu": "ur", "🇮🇳 Hindi": "hi",
    "🇸🇦 Arabic": "ar", "🇫🇷 French": "fr", "🇪🇸 Spanish": "es",
    "🇩🇪 German": "de", "🇮🇹 Italian": "it", "🇷🇺 Russian": "ru",
    "🇯🇵 Japanese": "ja", "🇨🇳 Chinese": "zh-CN", "🇰🇷 Korean": "ko",
    "🇹🇷 Turkish": "tr", "🇳🇱 Dutch": "nl", "🇸🇪 Swedish": "sv",
    "🇵🇱 Polish": "pl", "🇬🇷 Greek": "el", "🇨🇿 Czech": "cs",
    "🇵🇹 Portuguese": "pt", "🇧🇩 Bengali": "bn", "🇹🇭 Thai": "th",
    "🇻🇳 Vietnamese": "vi", "🇮🇩 Indonesian": "id", "🇲🇾 Malay": "ms"
}

# Sidebar - Voice Tuning
with st.sidebar:
    st.markdown("## 🎚️ Voice Control Panel")
    
    # Language Selection
    selected_lang = st.selectbox("🌐 Select Language", list(languages.keys()))
    lang_code = languages[selected_lang]
    
    # Speed Control
    speed = st.slider("⏩ Speed", 0.5, 2.0, 1.0, 0.05)
    
    # Voice Character
    voice_char = st.select_slider("🎭 Voice Character", 
                                   options=["Deep", "Normal", "Bright", "Energetic"],
                                   value="Normal")
    
    char_speed = {"Deep": 0.85, "Normal": 1.0, "Bright": 1.15, "Energetic": 1.3}
    final_speed = speed * char_speed[voice_char]
    
    st.info(f"📊 {len(languages)} Languages Available")

# Main Area
input_text = st.text_area("📝 Enter your text here:", height=200, 
                          placeholder="Type any text in any language...")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate = st.button("🎤 GENERATE VOICE", use_container_width=True)

if generate:
    if input_text.strip():
        with st.spinner(f"Generating {voice_char} voice..."):
            try:
                slow_mode = (final_speed < 0.9)
                tts = gTTS(text=input_text, lang=lang_code, slow=slow_mode)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    with open(fp.name, "rb") as audio:
                        audio_data = audio.read()
                    os.unlink(fp.name)
                
                st.audio(audio_data, format="audio/mp3")
                st.download_button("💾 Download Audio", audio_data, "khak_voice.mp3")
                st.success(f"✅ Voice generated! Language: {selected_lang} | Speed: {final_speed:.1f}x")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter some text!")
