import streamlit as st
import asyncio
import edge_tts
import io

# --- 1. SEO & Page Config ---
st.set_page_config(
    page_title="Khak AI Voice Studio - Global Pro TTS",
    page_icon="🎙️",
    layout="wide"
)

# --- 2. Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e3e3e3; }
    .stButton>button { 
        background-color: #238636; color: white; border-radius: 8px; 
        width: 100%; font-weight: bold; height: 50px; border: none;
    }
    .stTextArea textarea { background-color: #1c2128 !important; color: white !important; border: 1px solid #30363d !important; border-radius: 10px; }
    .stSelectbox div[data-baseweb="select"] { background-color: #1c2128 !important; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. Core Voice Engine ---
async def get_all_voices():
    v_manager = await edge_tts.VoicesManager.create()
    return v_manager.voices

async def generate_voice(text, voice_name, speed, pitch):
    speed_str = f"{int((speed - 1) * 100):+d}%"
    pitch_str = f"{int((pitch - 1) * 100):+d}Hz"
    if not text.strip(): return None
    communicate = edge_tts.Communicate(text, voice_name, rate=speed_str, pitch=pitch_str)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio": audio_data += chunk["data"]
    return audio_data

# --- 4. 14 Professional Styles Presets ---
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

# --- 5. Main UI ---
st.title("🎙️ Khak AI Voice Studio")
st.write("Professional Multilingual AI Voice Generator with Smart Styles")

if 'voices' not in st.session_state:
    with st.spinner("Loading Global Voices..."):
        st.session_state.voices = asyncio.run(get_all_voices())

col_settings, col_main = st.columns([1, 2])

with col_settings:
    st.markdown("### ⚙️ Voice Settings")
    
    # 23 Requested Languages Mapping
    lang_map = {
        "en-US": "English (US) 🇺🇸",
        "ur-PK": "Urdu (Pakistan) 🇵🇰",
        "hi-IN": "Hindi (India) 🇮🇳",
        "zh-CN": "Mandarin Chinese 🇨🇳",
        "es-ES": "Spanish 🇪🇸",
        "ar-SA": "Arabic 🇸🇦",
        "pt-BR": "Portuguese (Brazil) 🇧🇷",
        "bn-BD": "Bengali 🇧🇩",
        "ru-RU": "Russian 🇷🇺",
        "ja-JP": "Japanese 🇯🇵",
        "de-DE": "German 🇩🇪",
        "fr-FR": "French 🇫🇷",
        "it-IT": "Italian 🇮🇹",
        "tr-TR": "Turkish 🇹🇷",
        "vi-VN": "Vietnamese 🇻🇳",
        "ko-KR": "Korean 🇰🇷",
        "pl-PL": "Polish 🇵🇱",
        "uk-UA": "Ukrainian 🇺🇦",
        "ms-MY": "Malay 🇲🇾",
        "th-TH": "Thai 🇹🇭",
        "kn-IN": "Kannada 🇮🇳",
        "fa-IR": "Persian (Farsi) 🇮🇷",
        "nl-NL": "Dutch 🇳🇱"
    }

    all_locales = sorted(list(set([v['Locale'] for v in st.session_state.voices])))
    available_locales = {lang_map.get(loc, loc): loc for loc in all_locales if loc in lang_map}
    
    # English (US) set as Default
    default_lang = "English (US) 🇺🇸"
    lang_list = list(available_locales.keys())
    selected_lang_name = st.selectbox("🌍 Select Language", lang_list, index=lang_list.index(default_lang) if default_lang in lang_list else 0)
    selected_locale = available_locales[selected_lang_name]
    
    # Character Selection
    filtered_voices = [v for v in st.session_state.voices if v['Locale'] == selected_locale]
    voice_display_names = [f"{v['FriendlyName'].split(' ')[1].replace('Neural', '')} ({v['Gender']})" for v in filtered_voices]
    
    selected_voice_label = st.selectbox("👤 Select Character", voice_display_names)
    selected_voice_name = filtered_voices[voice_display_names.index(selected_voice_label)]['Name']
    
    st.markdown("---")
    
    # 🎭 Style Presets (Pehle wala function barqarar hai)
    selected_style = st.selectbox("🎭 Select Voice Style", list(styles.keys()))
    preset = styles[selected_style]
    
    pitch_val = st.slider("Fine-tune Pitch", 0.5, 1.5, float(preset["pitch"]))
    speed_val = st.slider("Fine-tune Speed", 0.5, 2.0, float(preset["speed"]))

with col_main:
    st.markdown("### 📝 Script Studio")
    user_text = st.text_area("Yahan apni script likhen...", height=350, placeholder="Type your text here to generate AI voice...")
    
    if st.button("✨ GENERATE AI VOICE"):
        if user_text.strip():
            with st.spinner(f"Generating {selected_style} voice..."):
                try:
                    audio = asyncio.run(generate_voice(user_text, selected_voice_name, speed_val, pitch_val))
                    if audio:
                        st.audio(audio, format="audio/mp3")
                        st.download_button(
                            label="📥 DOWNLOAD MP3", 
                            data=audio, 
                            file_name=f"khak_ai_{selected_voice_label.split(' ')[0]}.mp3", 
                            mime="audio/mp3"
                        )
                        st.success(f"Character '{selected_voice_label}' generated in '{selected_style}' style!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter text first.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2026 Khak AI Studio | 14 Pro Styles | Unlimited Free Use</p>", unsafe_allow_html=True)
