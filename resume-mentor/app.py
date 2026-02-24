import streamlit as st
import PyPDF2
import plotly.graph_objects as go
from utils import analyze_resume, chatbot_response

st.set_page_config(page_title="CareerPilot AI", layout="wide")

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#1f1c2c,#928DAB);
    color:white;
}
.section-box {
    background: rgba(255,255,255,0.1);
    padding:25px;
    border-radius:20px;
    margin-top:20px;
}
.stButton>button {
    background: linear-gradient(90deg,#00C9FF,#92FE9D);
    border-radius:12px;
    height:3em;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
st.sidebar.title("🚀 CareerPilot AI")

menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "📄 Resume Intelligence", "💬 AI Career Mentor"]
)

# =====================================================
# DASHBOARD
# =====================================================
if menu == "🏠 Dashboard":

    st.title("🎓 CareerPilot AI – Agentic Career Platform")

    st.markdown("""
    CareerPilot AI supports students with:
    - Resume Evaluation
    - Career Guidance
    - Skill Recommendations

    The AI agent provides personalized learning and career planning insights 
    based on user profiles.
    """)

    st.markdown("---")
    st.image("https://images.unsplash.com/photo-1522202176988-66273c2fd55f", use_container_width=True)

# =====================================================
# RESUME INTELLIGENCE
# =====================================================
elif menu == "📄 Resume Intelligence":

    st.title("📄 Resume Intelligence Engine")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    def extract_text(file):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
        return text

    if uploaded_file:
        resume_text = extract_text(uploaded_file)
        st.success("Resume Uploaded Successfully!")

        if st.button("🚀 Analyze Resume"):

            with st.spinner("Generating Career Insights..."):
                result, score = analyze_resume(resume_text)

            # SCORE SECTION
            st.markdown("<div class='section-box'>", unsafe_allow_html=True)
            st.subheader("📊 Resume Score")

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                gauge={'axis': {'range': [0, 100]}}
            ))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # FULL REPORT SECTION
            st.markdown("<div class='section-box'>", unsafe_allow_html=True)
            st.subheader("📑 Detailed Career Analysis")
            st.write(result)
            st.markdown("</div>", unsafe_allow_html=True)

            # BOTTOM INSIGHT SECTION
            st.markdown("<div class='section-box'>", unsafe_allow_html=True)
            st.subheader("💡 Understanding Your Report")
            st.write("""
            - Resume Score indicates overall profile strength.
            - Strengths show what gives you competitive advantage.
            - Weaknesses highlight improvement areas.
            - Skill Gap shows missing industry skills.
            - Roadmap gives structured growth direction.
            """)
            st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# AI CAREER MENTOR
# =====================================================
elif menu == "💬 AI Career Mentor":

    st.title("💬 CareerPilot AI Mentor")

    if "chat_stage" not in st.session_state:
        st.session_state.chat_stage = 1
        st.session_state.last_response = ""

    # FIRST QUESTION INPUT
    if st.session_state.chat_stage == 1:

        user_question = st.text_input("Ask your career question:")

        if st.button("Submit Question"):

            ai_response = chatbot_response(user_question)

            st.session_state.last_response = ai_response
            st.session_state.chat_stage = 2

    # SHOW RESPONSE
    if st.session_state.chat_stage == 2:

        st.markdown("### 🤖 AI Response")
        st.info(st.session_state.last_response)

        # SECOND INPUT BOX AFTER RESPONSE
        follow_up = st.text_input("Continue conversation:")

        if st.button("Reply to AI"):
            new_response = chatbot_response(follow_up)
            st.session_state.last_response = new_response
            st.success(new_response)