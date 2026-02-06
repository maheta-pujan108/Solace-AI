import streamlit as st
from text_model import analyze_text
from voice_model import start_recording, stop_and_transcribe, analyze_voice

st.set_page_config(page_title="Solace AI 🌱", layout="centered")

st.markdown("""
<style>
body { background-color: #0f1117; color:white; }
.big { font-size:48px; font-weight:700; text-align:center; }
.sub { text-align:center; color:#aaa; }
.card { background:#1c1f26; padding:25px; border-radius:12px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big">🌱 Solace AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">A gentle space to understand your emotions</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Text", "🎤 Voice", "📷 Webcam"])

# ---------------- TEXT ----------------
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Talk to me")

    text = st.text_area("How are you feeling today?")

    if st.button("✨ Understand my feelings"):
        label, score = analyze_text(text)
        depression = score if label == "NEGATIVE" else 1 - score

        st.subheader("Your emotional state")
        st.write("Tone:", label)
        st.write("Intensity:", round(depression, 2))

        if depression > 0.7:
            st.info("💙 You're carrying a lot. You're not alone.")
        elif depression > 0.4:
            st.info("🌤 You're feeling some stress. Be gentle with yourself.")
        else:
            st.success("🌼 You seem emotionally balanced.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- VOICE ----------------
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Speak freely")

    if "stream" not in st.session_state:
        st.session_state.stream = None

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎙 Start recording"):
            st.session_state.stream = start_recording()
            st.info("I'm listening...")

    with col2:
        if st.button("🛑 Stop & analyze"):
            if st.session_state.stream is None:
                st.warning("Please start recording first.")
            else:
                with st.spinner("Understanding your emotions..."):
                    text = stop_and_transcribe(st.session_state.stream)
                    label, depression = analyze_voice(text)

                st.subheader("What you said")
                st.write(text)

                st.subheader("Your emotional state")
                st.write("Tone:", label)
                st.write("Intensity:", round(depression, 2))

                if depression > 0.7:
                    st.info("💙 It sounds heavy. You deserve support.")
                elif depression > 0.4:
                    st.info("🌤 You're feeling a bit overwhelmed.")
                else:
                    st.success("🌼 You sound emotionally okay.")

                st.session_state.stream = None

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- WEBCAM ----------------
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Facial emotions")

    if st.button("📷 Start camera"):
        st.info("Press Q to stop camera")
        import webcam

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<hr>
<div style="text-align:center;color:#777;">
Solace AI is a supportive tool, not a diagnosis.<br>
If you're struggling, talking to a real person really helps 💙
</div>
""", unsafe_allow_html=True)