import streamlit as st
import asyncio
import edge_tts

# --- 1. Page Configuration (Sirf EK dafa poore code mein) ---
st.set_page_config(
    page_title="Khak AI Voice Studio",
    page_icon="🎙️",
    layout="wide"
)

# --- 2. Google Search Console Verification ---
# Is se Google ko pata chal jaye ga ke ye aap ki app hai
st.markdown('<meta name="google-site-verification" content="XMevMtwIoHVhCraYTMo_1miegWUMRu_ISGQGoT6qQKQ" />', unsafe_allow_html=True)

# --- 3. Professional Dark Theme Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e3e3e3; }
    .stButton>button { 
        background-color: #238636; color: white; border-radius: 8px; 
        width: 100%; font-weight: bold; height: 45px; border: none;
    }
    .stTextArea textarea { background-color: #1c2128 !important; color: white !important; border: 1px solid #30363d !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. Core Engine Functions ---
async def get_all_voices():
    v_manager = await edge_tts.VoicesManager.create()
    return v_manager.voices

async def generate_voice(text, voice_name, speed, pitch):
    # Calculation for rate and pitch compatible with edge-tts
    rate = f"{int((speed - 1) * 100):+d}%"
    ptch = f"{int((pitch - 1) * 100):+d}Hz"
    communicate = edge_tts.Communicate(text, voice_name, rate=rate, pitch=ptch)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

# --- 5. All 14 Professional Styles ---
styles = {
    "Default (Normal)": {"pitch": 1.0, "speed": 1.0},
    "Motivational (Energetic)": {"pitch": 1.1, "speed": 1.15},
    "Educational (Clear)": {"pitch": 1.0, "speed": 0.95},
    "Storytelling (Deep & Slow)": {"pitch": 0.9, "speed": 0.85},
    "Quotes (Soft & Calm)": {"pitch": 0.95, "speed": 0.8},
    "News Reporter (Fast)": {"pitch": 1.15, "speed": 1.2},
    "Low Bass (Deep Voice)": {"pitch": 0.7, "speed": 0.9},
    "High Energy (Excited)": {"pitch": 1.2, "speed": 1.25},
    "Whispering (Mystery)": {"pitch": 1.1, "speed": 0.75},
    "Angry (Shouting)": {"pitch": 1.3, "speed": 1.3},
    "Funny (Kids/Cartoon)": {"pitch": 1.5, "speed": 1.1},
    "Podcast (Deep & Rich)": {"pitch": 0.85, "speed": 1.0},
    "Tech Robot (Flat)": {"pitch": 1.0, "speed": 1.1},
    "Sales/Ad (Fast Selling)": {"pitch": 1.1, "speed": 1.3}
}

# --- 6. Data Initialization (Session State) ---
if 'voices' not in st.session_state:
    with st.spinner("Loading Studio..."):
        st.session_state.voices = asyncio.run(get_all_voices())

# --- 7. Sidebar (Settings) ---
with st.sidebar:
    st.title("🎙️ Khak AI Settings")
    st.markdown("---")
    
    lang_map = {
        "en-US": "English (US) 🇺🇸", "ur-PK": "Urdu (Pakistan) 🇵🇰", "hi-IN": "Hindi (India) 🇮🇳",
        "zh-CN": "Mandarin Chinese 🇨🇳", "es-ES": "Spanish 🇪🇸", "ar-SA": "Arabic 🇸🇦",
        "pt-BR": "Portuguese (Brazil) 🇧🇷", "bn-BD": "Bengali 🇧🇩", "ru-RU": "Russian 🇷🇺",
        "ja-JP": "Japanese 🇯🇵", "de-DE": "German 🇩🇪", "fr-FR": "French 🇫🇷",
        "it-IT": "Italian 🇮🇹", "tr-TR": "Turkish 🇹🇷", "vi-VN": "Vietnamese 🇻🇳",
        "ko-KR": "Korean 🇰🇷", "pl-PL": "Polish 🇵🇱", "uk-UA": "Ukrainian 🇺🇦",
        "ms-MY": "Malay 🇲🇾", "th-TH": "Thai 🇹🇭", "kn-IN": "Kannada 🇮🇳",
        "fa-IR": "Persian (Farsi) 🇮🇷", "nl-NL": "Dutch 🇳🇱"
    }
    
    available_locales = {lang_map.get(v['Locale'], v['Locale']): v['Locale'] for v in st.session_state.voices if v['Locale'] in lang_map}
    selected_lang = st.selectbox("🌍 Select Language", list(available_locales.keys()), index=1) # Urdu by default
    locale = available_locales[selected_lang]
    
    v_list = [v for v in st.session_state.voices if v['Locale'] == locale]
    v_labels = [f"{v['FriendlyName'].split(' ')[1].replace('Neural', '')} ({v['Gender']})" for v in v_list]
    selected_v_label = st.selectbox("👤 Select Character", v_labels)
    voice_name = v_list[v_labels.index(selected_v_label)]['Name']

    st.markdown("<br><br>" * 3, unsafe_allow_html=True)
    st.markdown("---")
    st.link_button("⭐ Star on GitHub", "https://github.com/tanveerkhaki/khak-ai-voice-studio")
    st.link_button("💬 Report an Issue", "https://github.com/tanveerkhaki/khak-ai-voice-studio/issues")

# --- 8. Main Interface ---
st.title("Pro AI Voice Studio")

col1, col2 = st.columns(2)
with col1:
    style_name = st.selectbox("🎭 Select Voice Style", list(styles.keys()))
    style = styles[style_name]
with col2:
    speed = st.slider("Fine-tune Speed", 0.5, 2.0, float(style["speed"]))
    pitch = st.slider("Fine-tune Pitch", 0.5, 1.5, float(style["pitch"]))

user_text = st.text_area("📝 Your Script", height=250, placeholder="Yahan apna text likhen...")

if st.button("✨ GENERATE AI VOICE"):
    if user_text.strip():
        with st.spinner(f"Generating {style_name} voice..."):
            try:
                audio = asyncio.run(generate_voice(user_text, voice_name, speed, pitch))
                if audio:
                    st.audio(audio)
                    st.download_button("📥 Download MP3", data=audio, file_name=f"khak_ai_voice.mp3")
                    st.success(f"Generated with {selected_v_label} in {style_name} style!")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter text first.")
