
import streamlit as st
from gtts import gTTS
import tempfile
import os
import io
from pydub import AudioSegment

st.set_page_config(page_title="Khak AI Voice Studio Pro", page_icon="🎚️", layout="wide")

# Professional CSS
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #0a0a0f 0%, #12121a 100%); color: #e3e3e3; }
        [data-testid="stSidebar"] { background-color: rgba(20,20,30,0.98); border-right: 1px solid #2a2a3a; }
        .stButton>button { background: linear-gradient(90deg, #006699, #00aacc); color: white; border-radius: 25px; width: 100%; padding: 0.8rem; font-weight: bold; }
        .stTextArea textarea { background-color: #1a1a2a !important; color: white !important; border-radius: 15px; }
        h1 { text-align: center; background: linear-gradient(90deg, #00aacc, #006699); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎚️ Khak AI Voice Studio Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Professional Voice Tuning | 20+ Voice Characters | 50+ Languages</p>", unsafe_allow_html=True)

# ========== VOICE CHARACTERS (20+ Male/Female) ==========
voice_characters = {
    "👨 Male - Deep Narrator": 0.75,
    "👨 Male - Professional": 0.85,
    "👨 Male - Normal": 1.0,
    "👨 Male - Energetic": 1.15,
    "👨 Male - Radio Host": 1.2,
    "👨 Male - Announcement": 1.05,
    "👨 Male - Soft Spoken": 0.9,
    "👩 Female - Soft & Warm": 0.8,
    "👩 Female - Professional": 0.9,
    "👩 Female - Normal": 1.0,
    "👩 Female - Bright": 1.1,
    "👩 Female - Energetic": 1.2,
    "👩 Female - News Anchor": 1.05,
    "👩 Female - Sweet Voice": 0.95,
    "👩 Female - Authoritative": 1.15,
    "🤖 Robot - Mechanical": 1.3,
    "🤖 Robot - Digital": 1.4,
    "🎭 Echo - Deep Hall": 0.7,
    "🎭 Echo - Cave": 0.8,
    "🎭 Helium - Cartoon": 1.5,
    "🎭 Helium - Chipmunk": 1.6,
    "👻 Ghost - Whisper": 0.85
}

# ========== 50+ LANGUAGES ==========
lang_codes = {
    "🇺🇸 English": "en",
    "🇬🇧 English (UK)": "en",
    "🇵🇰 Urdu": "ur",
    "🇮🇳 Hindi": "hi",
    "🇪🇸 Spanish": "es",
    "🇫🇷 French": "fr",
    "🇩🇪 German": "de",
    "🇮🇹 Italian": "it",
    "🇵🇹 Portuguese": "pt",
    "🇧🇷 Portuguese (Brazil)": "pt",
    "🇷🇺 Russian": "ru",
    "🇯🇵 Japanese": "ja",
    "🇨🇳 Chinese (Simplified)": "zh-CN",
    "🇨🇳 Chinese (Traditional)": "zh-TW",
    "🇰🇷 Korean": "ko",
    "🇹🇷 Turkish": "tr",
    "🇳🇱 Dutch": "nl",
    "🇸🇪 Swedish": "sv",
    "🇵🇱 Polish": "pl",
    "🇬🇷 Greek": "el",
    "🇨🇿 Czech": "cs",
    "🇩🇰 Danish": "da",
    "🇫🇮 Finnish": "fi",
    "🇳🇴 Norwegian": "no",
    "🇭🇺 Hungarian": "hu",
    "🇮🇩 Indonesian": "id",
    "🇲🇾 Malay": "ms",
    "🇹🇭 Thai": "th",
    "🇻🇳 Vietnamese": "vi",
    "🇮🇱 Hebrew": "iw",
    "🇦🇪 Arabic": "ar",
    "🇧🇩 Bengali": "bn",
    "🇱🇰 Sinhala": "si",
    "🇳🇵 Nepali": "ne",
    "🇰🇭 Khmer": "km",
    "🇲🇲 Burmese": "my",
    "🇲🇳 Mongolian": "mn",
    "🇰🇿 Kazakh": "kk",
    "🇺🇿 Uzbek": "uz"
}

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

# ========== SIDEBAR - VOICE TUNING COLUMN ==========
with st.sidebar:
    st.markdown("## 🎚️ Voice Tuning Studio")
    st.markdown("---")
    
    # Voice Character Selection
    st.markdown("### 🎭 Voice Character")
    selected_character = st.selectbox("Choose Male/Female/Effect voice", list(voice_characters.keys()))
    base_pitch = voice_characters[selected_character]
    
    st.markdown("---")
    
    # Pitch Control
    st.markdown("### 🎵 Pitch Control")
    pitch = st.slider("Adjust Tone (Higher = Female/Cartoon, Lower = Male/Deep)", 
                      0.5, 2.0, base_pitch, 0.01)
    
    # Speed Control
    st.markdown("### ⏩ Speed Control")
    speed = st.slider("Speaking Speed", 0.5, 2.0, 1.0, 0.05)
    
    st.markdown("---")
    
    # Language Selection
    st.markdown("### 🌐 Language")
    selected_lang = st.selectbox("Select from 40+ languages", list(lang_codes.keys()))
    
    st.markdown("---")
    
    # Current Settings Display
    st.markdown("### 📊 Current Setup")
    st.info(f"""
    🎭 {selected_character}
    🎵 Pitch: {pitch:.2f}x
    ⏩ Speed: {speed:.2f}x
    🌐 {selected_lang}
    """)

# ========== MAIN CONTENT ==========
st.markdown("### 📝 Enter Your Text")
input_text = st.text_area("", height=150, placeholder="Type anything in any language...\n\nExample: Assalam-o-Alaikum! Welcome to Khak AI Voice Studio")

# Generate Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate = st.button("🎤 GENERATE PROFESSIONAL VOICE", use_container_width=True)

if generate:
    if input_text.strip():
        with st.spinner(f"🎧 Generating {selected_character} voice..."):
            try:
                lang_code = lang_codes[selected_lang]
                slow_mode = (speed < 0.9)
                
                # Generate base voice
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
                
                st.markdown("---")
                st.markdown("### ✅ Voice Generated Successfully!")
                
                col_audio, col_download = st.columns([3, 1])
                with col_audio:
                    st.audio(audio_data, format="audio/mp3")
                with col_download:
                    st.download_button(
                        label="💾 Download Audio",
                        data=audio_data,
                        file_name=f"khak_voice.mp3",
                        use_container_width=True
                    )
                
                st.success(f"✅ Voice ready! Character: {selected_character} | Pitch: {pitch:.2f}x | Speed: {speed:.2f}x")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure your text matches the selected language script.")
    else:
        st.warning("⚠️ Please enter text to convert to speech!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🎚️ Khak AI Voice Studio Pro | 20+ Voice Characters | 40+ Languages</p>
    <p>Professional Text-to-Speech with Pitch Control & Speed Adjustment</p>
</div>
""", unsafe_allow_html=True)
