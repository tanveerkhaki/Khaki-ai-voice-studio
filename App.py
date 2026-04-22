import streamlit as st
import asyncio
import edge_tts
import io

# --- Page Config ---
st.set_page_config(page_title="Khak AI Voice Studio", page_icon="🎙️", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e3e3e3; }
    .stButton>button { background-color: #238636; color: white; border-radius: 8px; width: 100%; font-weight: bold; height: 50px; }
    .ad-placeholder { background-color: #1c2128; border: 1px dashed #444; padding: 15px; text-align: center; color: #888; border-radius: 10px; }
    .stTextArea textarea { background-color: #1c2128 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- Voice Engine ---
async def get_all_voices():
    v_manager = await edge_tts.VoicesManager.create()
    return v_manager.voices

def get_full_country_name(locale):
    mapping = {
        "ur-PK": "Pakistan (Urdu) 🇵🇰",
        "hi-IN": "India (Hindi) 🇮🇳",
        "en-US": "United States (English) 🇺🇸",
        "en-GB": "United Kingdom (English) 🇬🇧",
        "ar-SA": "Saudi Arabia (Arabic) 🇸🇦",
        "es-ES": "Spain (Spanish) 🇪🇸",
        "fr-FR": "France (French) 🇫🇷"
    }
    return mapping.get(locale, locale)

async def generate_voice(text, voice_name, speed, pitch):
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

# --- UI ---
st.title("🎙️ Khak AI Voice Studio")
st.markdown('<div class="ad-placeholder">Google AdSense Space (Traffic barhne par yahan ads ayenge)</div>', unsafe_allow_html=True)

if 'voices' not in st.session_state:
    with st.spinner("Voices Loading..."):
        st.session_state.voices = asyncio.run(get_all_voices())

col_settings, col_main = st.columns([1, 2])

with col_settings:
    st.subheader("⚙️ Voice Settings")
    
    all_locales = sorted(list(set([v['Locale'] for v in st.session_state.voices])))
    locale_options = {get_full_country_name(loc): loc for loc in all_locales}
    
    selected_name = st.selectbox("🌍 Select Country", list(locale_options.keys()), 
                                 index=list(locale_options.keys()).index("Pakistan (Urdu) 🇵🇰") if "Pakistan (Urdu) 🇵🇰" in locale_options else 0)
    
    selected_locale = locale_options[selected_name]
    filtered_voices = [v for v in st.session_state.voices if v['Locale'] == selected_locale]
    voice_labels = [f"{v['FriendlyName'].split('-')[-1]} ({v['Gender']})" for v in filtered_voices]
    
    selected_voice_label = st.selectbox(f"👤 Characters", voice_labels)
    selected_voice_name = filtered_voices[voice_labels.index(selected_voice_label)]['Name']
    
    st.markdown("---")
    # TUNE BOX: Sirf aapki yaad-dihani ke liye, AI isay parhay ga nahi
    st.info("💡 Note: Tune box instructions are for internal AI tone adjustment.")
    mood_setting = st.text_input("Tone/Mood Setting", "Natural Tone")
    
    pitch_val = st.slider("Tone Pitch", 0.5, 1.5, 1.0)
    speed_val = st.slider("Speed Control", 0.5, 2.0, 1.0)

with col_main:
    st.subheader("📝 Script Studio")
    # Yahan wo text likhen jo AI ne bolna hai
    user_text = st.text_area("Yahan wo script likhen jo AI ne bolni hai...", height=280, key="user_script_input")
    
    if st.button("✨ GENERATE VOICE"):
        if user_text.strip():
            with st.spinner("AI Voice Generating..."):
                try:
                    # FIX: Ab sirf user_text jaye ga, mood_setting nahi!
                    audio = asyncio.run(generate_voice(user_text, selected_voice_name, speed_val, pitch_val))
                    
                    if audio:
                        st.audio(audio, format="audio/mp3")
                        st.success("Audio Tayyar Hai! 🎈")
                    else:
                        st.error("Text sahi se read nahi ho raha.")
                except Exception as e:
                    st.error(f"Engine Error: {e}")
        else:
            st.warning("Script box mein kuch likhen pehle!")

st.markdown("---")
st.caption("Powered by Khak AI Studio | Free Unlimited Version")
