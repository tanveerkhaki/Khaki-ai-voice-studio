import streamlit as st
import asyncio
import edge_tts
import io

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Khak AI Voice Studio - Global TTS",
    page_icon="🎙️",
    layout="wide"
)

# --- 2. Advanced Styling (Modern & Clean) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e3e3e3; }
    .stButton>button { 
        background-color: #238636; color: white; border-radius: 8px; 
        width: 100%; font-weight: bold; height: 50px; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #2ea043; transform: scale(1.02); }
    .stTextArea textarea { background-color: #1c2128 !important; color: white !important; border: 1px solid #30363d !important; border-radius: 10px; }
    .stSelectbox div[data-baseweb="select"] { background-color: #1c2128 !important; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. Core Voice Engine ---
async def get_all_voices():
    v_manager = await edge_tts.VoicesManager.create()
    return v_manager.voices

async def generate_voice(text, voice_name, speed, pitch):
    # Calculations for Pitch and Speed
    speed_str = f"{int((speed - 1) * 100):+d}%"
    pitch_str = f"{int((pitch - 1) * 100):+d}Hz"
    
    if not text.strip():
        return None

    communicate = edge_tts.Communicate(text, voice_name, rate=speed_str, pitch=pitch_str)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

# --- 4. Main Interface ---
st.title("🎙️ Khak AI Voice Studio")
st.caption("Create Natural, High-Engagement AI Voices Globally")

if 'voices' not in st.session_state:
    with st.spinner("Initializing AI Voices..."):
        st.session_state.voices = asyncio.run(get_all_voices())

# Sidebar / Settings Column
col_settings, col_main = st.columns([1, 2])

with col_settings:
    st.markdown("### ⚙️ Voice Customization")
    
    # Updated Mapping with Portuguese Brazil
    mapping = {
        "ur-PK": "Pakistan (Urdu) 🇵🇰", 
        "hi-IN": "India (Hindi) 🇮🇳", 
        "en-US": "United States (English) 🇺🇸",
        "en-GB": "United Kingdom (English) 🇬🇧",
        "pt-BR": "Brazil (Portuguese) 🇧🇷",
        "ar-SA": "Saudi Arabia (Arabic) 🇸🇦",
        "es-ES": "Spain (Spanish) 🇪🇸"
    }
    
    all_locales = sorted(list(set([v['Locale'] for v in st.session_state.voices])))
    locale_options = {mapping.get(loc, loc): loc for loc in all_locales}
    
    selected_name = st.selectbox("🌍 Select Language", list(locale_options.keys()), index=0)
    selected_locale = locale_options[selected_name]
    
    filtered_voices = [v for v in st.session_state.voices if v['Locale'] == selected_locale]
    voice_labels = [f"{v['FriendlyName'].split('-')[-1]} ({v['Gender']})" for v in filtered_voices]
    
    selected_voice_label = st.selectbox("👤 Select AI Character", voice_labels)
    selected_voice_name = filtered_voices[voice_labels.index(selected_voice_label)]['Name']
    
    st.markdown("---")
    st.info("💡 **Tip:** For **Excited/Engaging** voice, keep Speed between 1.1x and 1.2x.")
    
    pitch_val = st.slider("Tone Pitch (Deep to High)", 0.5, 1.5, 1.0, help="Higher pitch sounds more youthful.")
    speed_val = st.slider("Voice Speed", 0.5, 2.0, 1.0, help="Increase for faster, energetic delivery.")

with col_main:
    st.markdown("### 📝 Script Studio")
    user_text = st.text_area("Yahan wo script likhen jisay AI awaz mein badalna hai...", height=300, placeholder="Example: Welcome to the world of Khak AI Studio!")
    
    if st.button("✨ GENERATE PROFESSIONAL AUDIO"):
        if user_text.strip():
            with st.spinner("Processing..."):
                try:
                    audio = asyncio.run(generate_voice(user_text, selected_voice_name, speed_val, pitch_val))
                    if audio:
                        st.audio(audio, format="audio/mp3")
                        
                        # Direct Download Button for User Convenience
                        st.download_button(
                            label="📥 DOWNLOAD MP3 (Save to Device)",
                            data=audio,
                            file_name="khak_ai_voice.mp3",
                            mime="audio/mp3"
                        )
                        st.success("Audio generated successfully! Click download to save.")
                except Exception as e:
                    st.error(f"Engine Error: {e}")
        else:
            st.warning("Please enter some text first!")

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>© 2026 Khak AI Studio | Fast • Free • Professional</p>", unsafe_allow_html=True)
