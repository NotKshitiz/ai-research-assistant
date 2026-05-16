import streamlit as st
import tempfile
import agent as agent_module
from tools import load_document

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="centered"
)

st.markdown("""
<style>
.user-bubble {
    background-color: #2f6df5;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0;
    max-width: 75%;
    margin-left: auto;
    text-align: right;
}
.assistant-bubble {
    background-color: #1e1e2e;
    color: #e0e0e0;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 0;
    max-width: 75%;
    margin-right: auto;
}
</style>
""", unsafe_allow_html=True)

st.title("🔍 AI Research Assistant")
st.caption("Search the web · Calculate · Ask about your document")

with st.sidebar:
    st.header("📄 Document")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf", label_visibility="collapsed")
    if uploaded_file:
        with st.spinner("Loading document..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
                f.write(uploaded_file.read())
                temp_path = f.name
            agent_module.vector_store = load_document(temp_path)
        st.success(f"✅ {uploaded_file.name}")
    else:
        st.info("Upload a PDF to enable document search")

    st.markdown("---")
    st.markdown("**What I can do:**")
    st.markdown("🌐 Search the web for recent news")
    st.markdown("🧮 Calculate math expressions")
    st.markdown("📄 Answer questions from your PDF")
    st.markdown("---")
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

query = st.chat_input("Ask anything...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.markdown(f'<div class="user-bubble">{query}</div>', unsafe_allow_html=True)

    with st.spinner("Thinking..."):
        response = agent_module.agent.invoke({"messages": [("user", query)]})
        last_message = response["messages"][-1].content
        if isinstance(last_message, list):
            answer = last_message[0]["text"]
        else:
            answer = last_message

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.markdown(f'<div class="assistant-bubble">{answer}</div>', unsafe_allow_html=True)