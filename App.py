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
        "es-ES": "Spain (Spanish) 🇪🇸"
    }
    return mapping.get(locale, locale)

async def generate_voice(text, voice_name, speed, pitch):
    speed_str = f"{int((speed - 1) * 100):+d}%"
    pitch_str = f"{int((pitch - 1) * 100):+d}Hz"
    
    # Text validation to fix "No audio received" error
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
st.markdown('<div class="ad-placeholder">Ad Space - Traffic barhne par yahan ads lagayen</div>', unsafe_allow_html=True)

if 'voices' not in st.session_state:
    with st.spinner("Voices load ho rahi hain..."):
        st.session_state.voices = asyncio.run(get_all_voices())

col_settings, col_main = st.columns([1, 2])

with col_settings:
    st.subheader("⚙️ Settings")
    
    all_locales = sorted(list(set([v['Locale'] for v in st.session_state.voices])))
    locale_options = {get_full_country_name(loc): loc for loc in all_locales}
    
    selected_name = st.selectbox("🌍 Select Country", list(locale_options.keys()), 
                                 index=list(locale_options.keys()).index("Pakistan (Urdu) 🇵🇰") if "Pakistan (Urdu) 🇵🇰" in locale_options else 0)
    
    selected_locale = locale_options[selected_name]
    filtered_voices = [v for v in st.session_state.voices if v['Locale'] == selected_locale]
    voice_labels = [f"{v['FriendlyName'].split('-')[-1]} ({v['Gender']})" for v in filtered_voices]
    
    selected_voice_label = st.selectbox(f"👤 Characters ({len(filtered_voices)})", voice_labels)
    selected_voice_name = filtered_voices[voice_labels.index(selected_voice_label)]['Name']
    
    st.markdown("---")
    # Instruction box - Ab hum isay alag rakhen ge
    mood_prompt = st.text_input("Voice Tone (Optional)", "Natural")
    
    pitch_val = st.slider("Tone Pitch", 0.5, 1.5, 1.0)
    speed_val = st.slider("Speed", 0.5, 2.0, 1.0)

with col_main:
    st.subheader("📝 Script (Is box mein likhen)")
    user_text = st.text_area("Yahan wo kahani ya text likhen jo bolna hai...", height=250, key="main_script")
    
    if st.button("✨ GENERATE VOICE"):
        if user_text.strip():
            with st.spinner("AI Voice ban rahi hai..."):
                try:
                    # YAHAN FIX HAI: Mood aur Script ko sahi se jora hai
                    final_content = f"{user_text}" 
                    audio = asyncio.run(generate_voice(final_content, selected_voice_name, speed_val, pitch_val))
                    
                    if audio:
                        st.audio(audio, format="audio/mp3")
                        st.success("Balloons! 🎈 Audio tayyar hai.")
                    else:
                        st.error("Error: Script sahi se parhi nahi gayi.")
                except Exception as e:
                    st.error(f"Engine Error: {e}")
        else:
            st.warning("Script wala box khali hai! Pehle wahan text likhen.")

# --- Voice Cloning Note ---
st.markdown("---")
with st.expander("🛡️ Voice Cloning (Apni Awaz Clone Karen)"):
    st.write("Voice Cloning feature ke liye ElevenLabs ka Pro account chahiye hota hai. Agle update mein hum 'Upload Your Voice' ka option add karenge (Sirf Premium Users ke liye).")
