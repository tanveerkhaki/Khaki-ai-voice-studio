import streamlit as st
import asyncio
import edge_tts
import io

# --- 1. SEO & Page Config (Ranking ke liye aham) ---
st.set_page_config(
    page_title="Khak AI Voice Studio - Free Unlimited AI Voices",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://khak-ai-voice-studio.streamlit.app/',
        'Report a bug': "https://khak-ai-voice-studio.streamlit.app/",
        'About': "# Khak AI Voice Studio \nBest Free AI Text-to-Speech Tool for Urdu, Hindi, and English."
    }
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e3e3e3; }
    .stButton>button { background-color: #238636; color: white; border-radius: 8px; width: 100%; font-weight: bold; height: 50px; border: none; }
    .stButton>button:hover { background-color: #2ea043; border: none; }
    .ad-placeholder { background-color: #1c2128; border: 1px dashed #444; padding: 15px; text-align: center; color: #888; border-radius: 10px; margin-bottom: 20px; }
    .stTextArea textarea { background-color: #1c2128 !important; color: white !important; border: 1px solid #30363d !important; }
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
        "fr-FR": "France (French) 🇫🇷",
        "bn-BD": "Bangladesh (Bengali) 🇧🇩"
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

# --- Main UI ---
st.title("🎙️ Khak AI Voice Studio")
st.subheader("Create Natural AI Voices for Free")

# Top Ad Space
st.markdown('<div class="ad-placeholder">Google AdSense Space - Banner Ad</div>', unsafe_allow_html=True)

if 'voices' not in st.session_state:
    with st.spinner("AI Engine loading..."):
        st.session_state.voices = asyncio.run(get_all_voices())

col_settings, col_main = st.columns([1, 2])

with col_settings:
    st.markdown("### ⚙️ Adjust Settings")
    
    all_locales = sorted(list(set([v['Locale'] for v in st.session_state.voices])))
    locale_options = {get_full_country_name(loc): loc for loc in all_locales}
    
    selected_name = st.selectbox("🌍 Select Language", list(locale_options.keys()), 
                                 index=list(locale_options.keys()).index("Pakistan (Urdu) 🇵🇰") if "Pakistan (Urdu) 🇵🇰" in locale_options else 0)
    
    selected_locale = locale_options[selected_name]
    filtered_voices = [v for v in st.session_state.voices if v['Locale'] == selected_locale]
    voice_labels = [f"{v['FriendlyName'].split('-')[-1]} ({v['Gender']})" for v in filtered_voices]
    
    selected_voice_label = st.selectbox(f"👤 Select AI Character", voice_labels)
    selected_voice_name = filtered_voices[voice_labels.index(selected_voice_label)]['Name']
    
    st.markdown("---")
    st.info("💡 Use Pitch & Speed to make the voice more natural.")
    pitch_val = st.slider("Tone Pitch", 0.5, 1.5, 1.0)
    speed_val = st.slider("Voice Speed", 0.5, 2.0, 1.0)

with col_main:
    st.markdown("### 📝 Enter Your Script")
    user_text = st.text_area("Yahan wo text likhen jo AI ne bolna hai...", height=280, key="user_script_v3", placeholder="Example: Assalam-o-Alaikum, aap kaise hain?")
    
    if st.button("✨ GENERATE PROFESSIONAL VOICE"):
        if user_text.strip():
            with st.spinner("Generating High-Quality Audio..."):
                try:
                    audio = asyncio.run(generate_voice(user_text, selected_voice_name, speed_val, pitch_val))
                    if audio:
                        st.audio(audio, format="audio/mp3")
                        st.success("Your voice is ready! Use the menu to download.")
                    else:
                        st.error("Technical error in generating audio.")
                except Exception as e:
                    st.error(f"Engine Error: {e}")
        else:
            st.warning("Please enter your script first!")

# --- Footer & Extra Info (For SEO) ---
st.markdown("---")
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("**Unlimited Characters**\nNo limit on word count.")
with f2:
    st.markdown("**100+ Languages**\nUrdu, Hindi, English & more.")
with f3:
    st.markdown("**Free Forever**\nPowered by Khak AI Studio.")

st.sidebar.markdown("### 🚀 About Khak AI")
st.sidebar.info("Khak AI Studio provides high-quality text-to-speech services for content creators worldwide.")
st.sidebar.markdown('<div class="ad-placeholder" style="height:200px;">Sidebar Ad</div>', unsafe_allow_html=True)
