import streamlit as st
from ai_suggestor import generate_ai_suggestion, chat_with_ai
from error_dectector import detect_code_issues

# MUST BE FIRST
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="logo.png",
    layout="wide"
)

st.image("logo.png", width=180)
st.title("🤖 AI Code Reviewer")

# ---------------- SESSION STATE ----------------
if "code_input" not in st.session_state:
    st.session_state.code_input = ""

if "ai_suggestion" not in st.session_state:
    st.session_state.ai_suggestion = ""

if "chat_reply" not in st.session_state:
    st.session_state.chat_reply = ""

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["Code Input", "AI Suggestions"])

# ================= TAB 1 =================
with tab1:
    st.subheader("📝 Your Code")

    st.session_state.code_input = st.text_area(
        "Paste your Python code here:",
        value=st.session_state.code_input,
        height=400
    )

    if st.button("Detect Errors", key="detect_errors"):
        if not st.session_state.code_input.strip():
            st.warning("Please enter Python code.")
        else:
            issues = detect_code_issues(st.session_state.code_input)

            if issues["unused_variables"]:
                st.warning("Unused Variables: " + ", ".join(issues["unused_variables"]))
            else:
                st.success("No unused variables found.")

            if issues["unused_imports"]:
                st.warning("Unused Imports: " + ", ".join(issues["unused_imports"]))
            else:
                st.success("No unused imports found.")

            if issues.get("python_errors"):
                st.error("Python Errors Detected:\n" + "\n".join(issues["python_errors"]))
            else:
                st.success("No Python errors detected!")

# ================= TAB 2 =================
with tab2:
    st.subheader("💡 AI Suggestions")

    if st.button("Get AI Suggestion", key="get_ai"):
        if not st.session_state.code_input.strip():
            st.warning("Please enter Python code in Tab-1.")
        else:
            with st.spinner("AI is reviewing your code..."):
                st.session_state.ai_suggestion = generate_ai_suggestion(
                    st.session_state.code_input
                )

    if st.session_state.ai_suggestion:
        st.text_area(
            "AI Suggestion",
            value=st.session_state.ai_suggestion,
            height=400,
            disabled=True
        )

    if st.button("🔄 Refresh Suggestion", key="refresh_ai"):
        if st.session_state.code_input.strip():
            with st.spinner("Regenerating suggestion..."):
                st.session_state.ai_suggestion = generate_ai_suggestion(
                    st.session_state.code_input
                )

    st.subheader("💬 Ask AI about this suggestion")

    user_question = st.text_input(
        "Your question:",
        placeholder="e.g., Why should I remove this import?",
        key="user_question"
    )

    if st.button("Send Question", key="send_question"):
        if not st.session_state.ai_suggestion:
            st.warning("Please generate AI suggestion first.")
        else:
            with st.spinner("AI is responding..."):
                st.session_state.chat_reply = chat_with_ai(
                    st.session_state.ai_suggestion,
                    user_question
                )

    if st.session_state.chat_reply:
        st.text_area(
            "AI Reply",
            value=st.session_state.chat_reply,
            height=250,
            disabled=True
        )
