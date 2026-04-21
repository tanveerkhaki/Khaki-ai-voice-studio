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

# --- Voice Engine & Mapping ---
async def get_all_voices():
    v_manager = await edge_tts.VoicesManager.create()
    return v_manager.voices

# Country code ko full name mein badalne ka function
def get_full_country_name(locale):
    mapping = {
        "ur-PK": "Pakistan (Urdu) 🇵🇰",
        "hi-IN": "India (Hindi) 🇮🇳",
        "en-US": "United States (English) 🇺🇸",
        "en-GB": "United Kingdom (English) 🇬🇧",
        "ar-SA": "Saudi Arabia (Arabic) 🇸🇦",
        "es-ES": "Spain (Spanish) 🇪🇸",
        "fr-FR": "France (French) 🇫🇷",
        "bn-IN": "India (Bengali) 🇮🇳",
        "bn-BD": "Bangladesh (Bengali) 🇧🇩"
    }
    return mapping.get(locale, locale) # Agar list mein nahi hai toh purana naam hi dikhaye

async def generate_voice(text, voice_name, speed, pitch):
    speed_str = f"{int((speed - 1) * 100):+d}%"
    pitch_str = f"{int((pitch - 1) * 100):+d}Hz"
    communicate = edge_tts.Communicate(text, voice_name, rate=speed_str, pitch=pitch_str)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

# --- UI ---
st.title("🎙️ Khak AI Voice Studio")
st.markdown('<div class="ad-placeholder">Ad Space - Google AdSense (Banner)</div>', unsafe_allow_html=True)

if 'voices' not in st.session_state:
    with st.spinner("Fetching All Global Voices..."):
        st.session_state.voices = asyncio.run(get_all_voices())

col_settings, col_main = st.columns([1, 2])

with col_settings:
    st.subheader("⚙️ Settings")
    
    # Locales with Full Names
    all_locales = sorted(list(set([v['Locale'] for v in st.session_state.voices])))
    # Dropdown mein full names dikhane ke liye map banaya
    locale_options = {get_full_country_name(loc): loc for loc in all_locales}
    
    selected_name = st.selectbox("🌍 Select Country/Language", list(locale_options.keys()), 
                                 index=list(locale_options.keys()).index("Pakistan (Urdu) 🇵🇰") if "Pakistan (Urdu) 🇵🇰" in locale_options else 0)
    
    selected_locale = locale_options[selected_name]
    
    # Filter voices for the selected locale
    filtered_voices = [v for v in st.session_state.voices if v['Locale'] == selected_locale]
    voice_labels = [f"{v['FriendlyName'].split('-')[-1]} ({v['Gender']})" for v in filtered_voices]
    
    selected_voice_label = st.selectbox(f"👤 Select Character ({len(filtered_voices)} available)", voice_labels)
    selected_voice_name = filtered_voices[voice_labels.index(selected_voice_label)]['Name']
    
    st.markdown("---")
    mood_prompt = st.text_area("System Prompt (Mood)", "Natural Tone", help="AI ko bataen kaisa bolna hai.")
    pitch_val = st.slider("Tone (Pitch)", 0.5, 1.5, 1.0, step=0.1)
    speed_val = st.slider("Speed", 0.5, 2.0, 1.0, step=0.1)

with col_main:
    st.subheader("📝 Script")
    user_text = st.text_area("Yahan wo likhen jo bolna hai...", height=250)
    
    if st.button("✨ GENERATE FREE VOICE"):
        if user_text:
            with st.spinner("AI is generating voice..."):
                try:
                    # Mood ko instruction ke taur par text ke shuru mein lagana
                    final_input = f"{mood_prompt}. {user_text}"
                    audio = asyncio.run(generate_voice(final_input, selected_voice_name, speed_val, pitch_val))
                    
                    if audio:
                        st.audio(audio, format="audio/mp3")
                        st.success("Success! Click three dots to download.")
                    else:
                        st.error("Engine failed to generate audio.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter some text.")

st.markdown("---")
st.caption("© 2026 Khak AI Studio | Multi-Language Support")
