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
    .ad-placeholder { background-color: #1c2128; border: 1px dashed #444; padding: 20px; text-align: center; color: #888; border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- Voice Engine ---
async def get_all_voices():
    voices = await edge_tts.VoicesManager.create()
    return voices.voices

async def generate_voice(text, voice_name, speed, pitch):
    # Free engine doesn't read instructions separately, so we only process script
    speed_str = f"{int((speed - 1) * 100):+d}%"
    pitch_str = f"{int((pitch - 1) * 100):+d}Hz"
    communicate = edge_tts.Communicate(text, voice_name, rate=speed_str, pitch=pitch_str)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

# --- UI Layout ---
st.title("🎙️ Khak AI Voice Studio")

# --- Top Ad Space ---
st.markdown('<div class="ad-placeholder">Google AdSense Space (Banner Ad)</div>', unsafe_allow_html=True)

# Loading Voices
if 'voices' not in st.session_state:
    with st.spinner("AI Models Loading..."):
        st.session_state.voices = asyncio.run(get_all_voices())

col_settings, col_main = st.columns([1, 2])

with col_settings:
    st.subheader("🎚️ Studio Settings")
    
    # Language Selection (100+)
    locales = sorted(list(set([v['Locale'] for v in st.session_state.voices])))
    selected_locale = st.selectbox("🌍 Select Language", locales, index=locales.index("ur-PK") if "ur-PK" in locales else 0)
    
    # Character Selection
    filtered = [v for v in st.session_state.voices if v['Locale'] == selected_locale]
    voice_labels = [f"{v['FriendlyName']} ({v['Gender']})" for v in filtered]
    selected_voice_label = st.selectbox("👤 Select Character", voice_labels)
    selected_voice_name = filtered[voice_labels.index(selected_voice_label)]['Name']
    
    st.markdown("---")
    # Tone Box (System Prompt for user's reference)
    st.text_area("System Prompt (Mood)", "Example: Happy, Educational, Serious...", help="Yeh box sirf aapki setting yaad rakhne ke liye hai.")
    
    pitch_val = st.slider("Pitch (Tone)", 0.5, 1.5, 1.0, step=0.1)
    speed_val = st.slider("Speed", 0.5, 2.0, 1.0, step=0.1)

with col_main:
    st.subheader("📝 Script Input")
    user_text = st.text_area("Yahan wo likhen jo bolna hai...", height=300, placeholder="Assalam-o-Alaikum! Main Khak AI Studio hoon.")
    
    if st.button("✨ GENERATE FREE VOICE"):
        if user_text:
            with st.spinner("AI is generating your voice..."):
                try:
                    audio = asyncio.run(generate_voice(user_text, selected_voice_name, speed_val, pitch_val))
                    st.audio(audio, format="audio/mp3")
                    st.success("Balloons! 🎈 Tayyar hai.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Pehle text likhen!")

# --- Sidebar Ad/Info ---
with st.sidebar:
    st.markdown("### 🏆 Premium Voice")
    st.write("Professional ElevenLabs voices coming soon for members!")
    st.markdown("---")
    st.markdown('<div class="ad-placeholder" style="height:300px;">Sidebar Ad (Vertical)</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 Khak AI Studio | Unlimited Free AI Voices")
