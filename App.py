import streamlit as st
import asyncio
import edge_tts
import io

# --- Page Config ---
st.set_page_config(page_title="Khak AI Voice Studio", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e3e3e3; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stTextArea textarea { background-color: #1c2128 !important; color: white !important; border: 1px solid #30363d !important; }
    .stButton>button { background-color: #238636; color: white; border-radius: 6px; width: 100%; border: none; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- Voice Data ---
async def get_voices():
    all_voices = await edge_tts.VoicesManager.create()
    return all_voices.voices

# --- Updated Generation Logic (Pitch Error Fixed) ---
async def generate_voice(text, voice_name, speed, pitch, system_prompt):
    # System Prompt ko text ke saath jorna
    full_text = f"{system_prompt}. {text}" if system_prompt else text
    
    # Speed aur Pitch ko Edge-TTS ke mutabiq format karna
    # Speed: +0%, -20%, etc.
    speed_str = f"{int((speed - 1) * 100):+d}%"
    
    # Pitch: Isay Hz mein convert karna parta hai ya specific format mein
    # Hum yahan Hz (Hertz) wala asaan format use karenge jo error nahi deta
    pitch_change = int((pitch - 1) * 50) # Pitch range adjustment
    pitch_str = f"{pitch_change:+d}Hz"
    
    communicate = edge_tts.Communicate(full_text, voice_name, rate=speed_str, pitch=pitch_str)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

# --- UI Layout ---
st.title("🎙️ Khak AI Voice Studio (Pro)")

t1, t2 = st.columns([1, 1])

with st.spinner("Loading AI Models..."):
    all_available_voices = asyncio.run(get_voices())

with t1:
    locales = sorted(list(set([v['Locale'] for v in all_available_voices])))
    # Default Urdu set karna
    default_lang = "ur-PK" if "ur-PK" in locales else locales[0]
    selected_locale = st.selectbox("🌍 Select Language", locales, index=locales.index(default_lang))

with t2:
    filtered = [v for v in all_available_voices if v['Locale'] == selected_locale]
    voice_labels = [f"{v['FriendlyName']} ({v['Gender']})" for v in filtered]
    selected_voice_label = st.selectbox("👤 Select Character", voice_labels)
    selected_voice_name = filtered[voice_labels.index(selected_voice_label)]['Name']

st.markdown("---")

col_settings, col_main = st.columns([1, 2])

with col_settings:
    st.subheader("⚙️ System Tuning")
    system_instruction = st.text_area("System Instructions (Tone)", 
                                     placeholder="Example: Speak like a serious news reporter...")
    
    st.markdown("---")
    # Pitch Slider (Ab yeh Hz mein change laye ga jo error nahi deta)
    pitch_val = st.slider("Pitch Control", 0.5, 1.5, 1.0, step=0.1)
    speed_val = st.slider("Speed Control", 0.5, 2.0, 1.0, step=0.1)

with col_main:
    st.subheader("📝 Input Script")
    user_text = st.text_area("Yahan text likhen...", height=250)
    
    if st.button("✨ GENERATE NATURAL VOICE"):
        if user_text:
            with st.spinner("AI is generating voice..."):
                try:
                    final_audio = asyncio.run(generate_voice(user_text, selected_voice_name, speed_val, pitch_val, system_instruction))
                    st.audio(final_audio, format="audio/mp3")
                    st.success("Success!")
                except Exception as e:
                    st.error(f"Engine Error: {e}")
        else:
            st.warning("Text box khali hai!")

st.caption("Powered by Khak AI Studio")
