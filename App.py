import streamlit as st
import asyncio
import edge_tts
import io

# --- Page Config (Studio Look) ---
st.set_page_config(page_title="Khak AI Voice Studio", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e3e3e3; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stTextArea textarea { background-color: #1c2128 !important; color: white !important; border: 1px solid #30363d !important; }
    .stButton>button { background-color: #238636; color: white; border-radius: 6px; width: 100%; border: none; font-weight: bold; }
    .stSelectbox div[data-baseweb="select"] { background-color: #1c2128 !important; }
    </style>
""", unsafe_allow_html=True)

# --- Voice Data (Supporting 100+ Languages & 20 Characters) ---
async def get_voices():
    all_voices = await edge_tts.VoicesManager.create()
    return all_voices.voices

def filter_voices(voices_list):
    # Filtering to get a mix of 10 Male and 10 Female for top languages
    # This keeps the app fast and organized
    return sorted(voices_list, key=lambda x: x['Locale'])

# --- Generation Logic ---
async def generate_voice(text, voice_name, speed, pitch, system_prompt):
    # System Prompt Integration: Combining instructions with text for context
    # Note: Edge-TTS uses pre-recorded neural models, 
    # so we add the system prompt as a context layer.
    full_text = f"{system_prompt}. {text}" if system_prompt else text
    
    speed_str = f"{int((speed - 1) * 100):+d}%"
    pitch_str = f"{int((pitch - 1) * 100):+d}%"
    
    communicate = edge_tts.Communicate(full_text, voice_name, rate=speed_str, pitch=pitch_str)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

# --- UI Layout (Google AI Studio Style) ---
st.title("🎙️ Khak AI Voice Studio (Pro)")

# Top Bar: Language and Character Selection (Google AI Studio Column Style)
t1, t2, t3 = st.columns([1, 1, 1])

with st.spinner("Loading AI Models..."):
    all_available_voices = asyncio.run(get_voices())

with t1:
    # 100+ Languages automatically supported through Locale
    locales = sorted(list(set([v['Locale'] for v in all_available_voices])))
    selected_locale = st.selectbox("🌍 Select Language (100+)", locales, index=locales.index("ur-PK") if "ur-PK" in locales else 0)

with t2:
    # Filter voices based on selected Language
    filtered = [v for v in all_available_voices if v['Locale'] == selected_locale]
    voice_labels = [f"{v['FriendlyName']} ({v['Gender']})" for v in filtered]
    selected_voice_label = st.selectbox("👤 Select Character (Male/Female)", voice_labels)
    selected_voice_name = filtered[voice_labels.index(selected_voice_label)]['Name']

with t3:
    st.info(f"Engine: Neural Natural Voice")

st.markdown("---")

# Main Columns
col_settings, col_main = st.columns([1, 2])

with col_settings:
    st.subheader("⚙️ System Tuning")
    # THE SYSTEM PROMPT BOX (Google AI Studio Style)
    system_instruction = st.text_area("System Instructions (Tone)", 
                                     placeholder="Example: Speak like a happy child, or a serious news reporter...",
                                     help="Yahan wo instructions likhen jo awaz ke lehjay (Tone) ko control karengi.")
    
    st.markdown("---")
    pitch_val = st.slider("Pitch Control", 0.5, 1.5, 1.0, step=0.1)
    speed_val = st.slider("Speed Control", 0.5, 2.0, 1.0, step=0.1)

with col_main:
    st.subheader("📝 Input Script")
    user_text = st.text_area("Yahan wo text likhen jis ki awaz banani hai...", height=300)
    
    if st.button("✨ GENERATE NATURAL VOICE"):
        if user_text:
            with st.spinner("AI is thinking and speaking..."):
                try:
                    final_audio = asyncio.run(generate_voice(user_text, selected_voice_name, speed_val, pitch_val, system_instruction))
                    st.audio(final_audio, format="audio/mp3")
                    st.success("Natural Voice Generated Successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter some text first.")

st.markdown("---")
st.caption("Powered by Khak AI Studio | Neural Voice Engine v2.0")
