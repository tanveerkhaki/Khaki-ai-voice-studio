
import streamlit as st
from gtts import gTTS
import tempfile
import os
import io
from pydub import AudioSegment
import numpy as np

st.set_page_config(page_title="Khak AI Voice Studio Pro", page_icon="🎚️", layout="wide")

# Professional CSS - Google AI Studio Style
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #0a0a0f 0%, #12121a 100%); color: #e3e3e3; }
        [data-testid="stSidebar"] { background-color: rgba(20,20,30,0.98); border-right: 1px solid #2a2a3a; }
        .stButton>button { background: linear-gradient(90deg, #006699, #00aacc); color: white; border-radius: 25px; width: 100%; padding: 0.8rem; font-weight: bold; border: none; transition: all 0.3s; }
        .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 25px rgba(0,170,204,0.4); }
        .stTextArea textarea { background-color: #1a1a2a !important; color: white !important; border-radius: 15px; border: 1px solid #2a2a3a; }
        .stSlider [data-baseweb="slider"] { background-color: #006699; }
        .studio-card { background: linear-gradient(135deg, #1a1a2a, #0f0f1a); border-radius: 20px; padding: 20px; border: 1px solid #2a2a3a; margin: 10px 0; }
        h1 { text-align: center; background: linear-gradient(90deg, #00aacc, #006699); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>🎚️ Khak AI Voice Studio Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #888;'>Professional Voice Tuning | Pitch + Speed + Voice Characters</p>", unsafe_allow_html=True)

# Voice Characters Library
voice_characters = {
    "🎙️ Studio Narrator": 1.0,
    "🎧 Radio Host": 1.15,
    "🤖 AI Assistant": 1.05,
    "🦁 Deep Voice": 0.8,
    "🐭 Cute Character": 1.4,
    "👑 Royal Voice": 0.9,
    "⚡ Fast Talker": 1.2,
    "🎭 Dramatic Actor": 0.95,
    "📢 News Anchor": 1.0,
    "❤️ Soft & Warm": 0.85,
    "🔥 Motivational": 1.1,
    "😊 Happy Voice": 1.2,
    "🔊 Deep Bass": 0.7,
    "🎪 Announcer": 1.0,
    "🌙 Night Mode": 0.88
}

# Languages Dictionary
lang_codes = {
    "🇺🇸 English": "en",
    "🇵🇰 Urdu": "ur",
    "🇮🇳 Hindi": "hi",
    "🇪🇸 Spanish": "es",
    "🇧🇷 Portuguese (Brazil)": "pt",
    "🇫🇷 French": "fr",
    "🇩🇪 German": "de",
    "🇸🇦 Arabic": "ar",
    "🇷🇺 Russian": "ru"
}

# Pitch adjustment function
def adjust_pitch(audio_bytes, pitch_factor):
    try:
        sound = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
        new_sample_rate = int(sound.frame_rate * pitch_factor)
        pitched_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        pitched_sound = pitched_sound.set_frame_rate(sound.frame_rate)
        out_buf = io.BytesIO()
        pitched_sound.export(out_buf, format="mp3")
        return out_buf.getvalue()
    except:
        return audio_bytes

# Sidebar - Professional Tuning Panel
with st.sidebar:
    st.markdown("## 🎚️ Voice Tuning Studio")
    st.markdown("---")
    
    # Voice Character Selection
    st.markdown("### 🎭 Voice Character")
    selected_character = st.selectbox("Choose voice style", list(voice_characters.keys()))
    base_pitch = voice_characters[selected_character]
    
    st.markdown("---")
    
    # Advanced Tuning
    st.markdown("### 🎛️ Advanced Tuning")
    
    # Pitch Control
    pitch = st.slider("🎵 Pitch (Tone)", 0.5, 2.0, base_pitch, 0.01,
                      help="Lower = Deep voice, Higher = Squeaky voice")
    
    # Speed Control
    speed = st.slider("⏩ Speed (Tempo)", 0.5, 2.0, 1.0, 0.02,
                      help="Control speaking speed")
    
    # Speed Presets
    st.markdown("**Quick Presets:**")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("🐢 Slow"):
            speed = 0.75
    with col_b:
        if st.button("⚡ Normal"):
            speed = 1.0
    with col_c:
        if st.button("🚀 Fast"):
            speed = 1.5
    
    st.markdown("---")
    
    # Language Selection
    st.markdown("### 🌐 Language")
    selected_lang = st.selectbox("Select Language", list(lang_codes.keys()))
    
    st.markdown("---")
    
    # Current Settings Display
    st.markdown("### 📊 Current Setup")
    st.info(f"""
    🎭 Voice: {selected_character}
    🎵 Pitch: {pitch:.2f}x
    ⏩ Speed: {speed:.2f}x
    🌐 Lang: {selected_lang}
    """)

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Input Text")
    input_text = st.text_area("Enter your text here...", height=200,
                              placeholder="Type any text in any language...")

with col2:
    st.markdown("### 🎛️ Voice Preview")
    st.markdown(f"""
    <div class="studio-card">
        <p style="color: #00aacc;">🎯 Active Settings</p>
        <hr>
        <p>🎭 <strong>Character:</strong> {selected_character}</p>
        <p>🎵 <strong>Pitch:</strong> {pitch:.2f}x | ⏩ <strong>Speed:</strong> {speed:.2f}x</p>
        <p>🌐 <strong>Language:</strong> {selected_lang}</p>
    </div>
    """, unsafe_allow_html=True)

# Generate Button
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generate = st.button("🎤 GENERATE PROFESSIONAL VOICE", use_container_width=True)

# Voice Generation
if generate:
    if input_text and input_text.strip():
        with st.spinner(f"🎧 Processing {selected_character} voice..."):
            try:
                lang_code = lang_codes[selected_lang]
                slow_mode = (speed < 0.9)
                
                # Generate base voice with gTTS
                tts = gTTS(text=input_text, lang=lang_code, slow=slow_mode)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    temp_path = fp.name
                    tts.save(temp_path)
                
                with open(temp_path, "rb") as audio_file:
                    audio_data = audio_file.read()
                
                os.unlink(temp_path)
                
                # Apply pitch adjustment
                if pitch != 1.0:
                    audio_data = adjust_pitch(audio_data, pitch)
                
                # Success Display
                st.markdown("---")
                st.markdown("### ✅ Professional Voice Generated!")
                
                # Audio Player
                col_audio, col_download = st.columns([3, 1])
                with col_audio:
                    st.audio(audio_data, format="audio/mp3")
                with col_download:
                    st.download_button(
                        label="💾 Download Studio Audio",
                        data=audio_data,
                        file_name=f"khak_studio_{lang_code}.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
                
                st.success(f"✅ Voice ready! Character: {selected_character} | Pitch: {pitch:.2f}x | Speed: {speed:.2f}x")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure pydub and ffmpeg are installed correctly.")
    else:
        st.warning("⚠️ Please enter text to convert to speech!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🎚️ Khak AI Voice Studio Pro | Google AI Studio Style Interface</p>
    <p>🎭 15+ Voice Characters | 🎛️ Pitch + Speed Control | 9 Languages</p>
</div>
""", unsafe_allow_html=True)
