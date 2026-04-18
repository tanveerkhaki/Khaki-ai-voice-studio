import streamlit as st
‎
‎def check_password():
‎    """Returns True if the user had the correct password."""
‎    def password_entered():
‎        if st.session_state["password"] == "khak123": # Yahan apna password rakhen
‎            st.session_state["password_correct"] = True
‎            del st.session_state["password"]
‎        else:
‎            st.session_state["password_correct"] = False
‎
‎    if "password_correct" not in st.session_state:
‎        st.text_input("Please enter your access password", type="password", on_change=password_entered, key="password")
‎        return False
‎    elif not st.session_state["password_correct"]:
‎        st.text_input("Password incorrect, try again", type="password", on_change=password_entered, key="password")
‎        return False
‎    else:
‎        return True
‎
‎if check_password():
‎    # Aapka baqi saara app ka code yahan aaye ga
‎    st.write("Welcome to Khak AI Voice Studio!")
‎    # ... 
‎import streamlit as st
‎from gtts import gTTS
‎from openai import OpenAI
‎import io
‎from pydub import AudioSegment
‎
‎# --- Page Configuration ---
‎st.set_page_config(
‎    page_title="Pro Voice Studio",
‎    page_icon="🎙️",
‎    layout="wide"
‎)
‎
‎# --- Custom CSS for Studio Look ---
‎st.markdown("""
‎    <style>
‎        .stApp { background-color: #0f1116; color: #e3e3e3; }
‎        [data-testid="stSidebar"] { background-color: #1e1e1e; border-right: 1px solid #333; }
‎        .stButton>button {
‎            background-color: #004a77; color: white; border-radius: 20px;
‎            width: 100%; border: none; padding: 0.6rem;
‎        }
‎        .stTextArea textarea { background-color: #1e1e1e !important; color: white !important; }
‎    </style>
‎""", unsafe_allow_html=True)
‎
‎# --- Audio Processing Logic ---
‎def adjust_audio(audio_bytes, pitch_level):
‎    # Convert bytes to AudioSegment
‎    sound = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
‎    
‎    # Pitch adjustment logic
‎    new_sample_rate = int(sound.frame_rate * pitch_level)
‎    pitched_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
‎    pitched_sound = pitched_sound.set_frame_rate(sound.frame_rate)
‎    
‎    # Export back to bytes
‎    out_buf = io.BytesIO()
‎    pitched_sound.export(out_buf, format="mp3")
‎    return out_buf.getvalue()
‎
‎def generate_voice(text, lang, speed, pitch, provider, api_key):
‎    try:
‎        if provider == "OpenAI TTS":
‎            client = OpenAI(api_key=api_key)
‎            response = client.audio.speech.create(
‎                model="tts-1", voice="alloy", input=text, speed=speed
‎            )
‎            audio_data = response.content
‎        else:
‎            # gTTS Generation
‎            tts = gTTS(text=text, lang=lang, slow=(speed < 1.0))
‎            fp = io.BytesIO()
‎            tts.write_to_fp(fp)
‎            audio_data = fp.getvalue()
‎
‎        # Apply Pitch Tuning
‎        if pitch != 1.0:
‎            audio_data = adjust_audio(audio_data, pitch)
‎            
‎        return audio_data
‎    except Exception as e:
‎        st.error(f"Error: {e}")
‎        return None
‎
‎# --- UI Layout ---
‎st.title("🎙️ AI Voice Generation Studio")
‎
‎# Top Settings Bar
‎t1, t2, t3 = st.columns(3)
‎with t1:
‎    lang_opt = {"Urdu": "ur", "English": "en", "Hindi": "hi", "Arabic": "ar", "French": "fr"}
‎    selected_lang = st.selectbox("Language Selection", list(lang_opt.keys()))
‎with t2:
‎    provider = st.selectbox("AI Engine", ["gTTS (Free)", "OpenAI TTS"])
‎with t3:
‎    st.info("Status: Ready to Generate")
‎
‎# Sidebar for Tuning
‎with st.sidebar:
‎    st.header("🎚️ Voice Tuning")
‎    if provider == "OpenAI TTS":
‎        api_key = st.text_input("OpenAI Key", type="password")
‎    else:
‎        api_key = None
‎    
‎    st.markdown("---")
‎    pitch = st.slider("Pitch (Tone)", 0.5, 2.0, 1.0, step=0.1, help="Higher = Squeaky, Lower = Deep")
‎    speed = st.slider("Speed (Tempo)", 0.5, 2.0, 1.0, step=0.1)
‎
‎# Main Work Area
‎input_text = st.text_area("Yahan apna text likhen...", height=250)
‎
‎if st.button("Generate & Tune Voice"):
‎    if input_text:
‎        with st.spinner("Processing your voice..."):
‎            final_audio = generate_voice(input_text, lang_opt[selected_lang], speed, pitch, provider, api_key)
‎            if final_audio:
‎                st.audio(final_audio, format="audio/mp3")
‎                st.download_button("Download Audio", final_audio, "voice.mp3")
‎    else:
‎        st.warning("Please enter text first!")
‎
