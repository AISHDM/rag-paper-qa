import streamlit as st
import requests
import json
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChemRAG — Research Paper Q&A",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Fraunces:ital,wght@0,300;0,600;1,300&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Fraunces', Georgia, serif;
    background-color: #0d1117;
    color: #e6edf3;
}

/* Hide streamlit branding */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem; padding-bottom: 2rem;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #58a6ff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* Title */
.main-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 2.8rem;
    font-weight: 300;
    color: #e6edf3;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}
.main-title span {
    color: #58a6ff;
    font-style: italic;
}
.main-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #8b949e;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* Chat messages */
.user-msg {
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 12px 12px 4px 12px;
    padding: 1rem 1.25rem;
    margin: 0.75rem 0;
    margin-left: 15%;
    font-size: 0.95rem;
    line-height: 1.6;
}
.bot-msg {
    background: #161b22;
    border: 1px solid #21262d;
    border-left: 3px solid #58a6ff;
    border-radius: 4px 12px 12px 12px;
    padding: 1rem 1.25rem;
    margin: 0.75rem 0;
    margin-right: 15%;
    font-size: 0.95rem;
    line-height: 1.7;
}
.bot-msg .answer-text {
    color: #e6edf3;
    margin-bottom: 0.75rem;
}
.source-tag {
    display: inline-block;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 2px 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #8b949e;
    margin: 2px 4px 2px 0;
}
.source-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #58a6ff;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 4px;
}
.error-msg {
    background: #1a0f0f;
    border: 1px solid #f8514975;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    color: #f85149;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
}
.thinking {
    color: #8b949e;
    font-style: italic;
    font-size: 0.85rem;
    padding: 0.5rem 0;
}

/* Paper cards in sidebar */
.paper-card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 0.6rem 0.8rem;
    margin: 0.4rem 0;
    font-size: 0.8rem;
    color: #8b949e;
    font-family: 'JetBrains Mono', monospace;
}
.paper-card .paper-name {
    color: #e6edf3;
    font-weight: 600;
    font-size: 0.75rem;
}

/* Input box */
.stTextInput > div > div > input {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
    font-family: 'Fraunces', Georgia, serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.1) !important;
}

/* Buttons */
.stButton > button {
    background: #238636 !important;
    color: #ffffff !important;
    border: 1px solid #2ea043 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #2ea043 !important;
    border-color: #3fb950 !important;
}

/* Upload widget */
[data-testid="stFileUploader"] {
    background: #161b22;
    border: 2px dashed #30363d;
    border-radius: 12px;
    padding: 1rem;
}

/* Metric cards */
.metric-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.metric-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: #58a6ff;
}
.metric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 2px;
}

/* Divider */
hr {border-color: #21262d;}

/* Slider */
.stSlider > div > div > div {
    color: #58a6ff !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #161b22 !important;
    border-color: #30363d !important;
    color: #e6edf3 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
API_BASE = "http://localhost:8000"

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "papers" not in st.session_state:
    st.session_state.papers = []

# ── Helper functions ───────────────────────────────────────────────────────────
def ask_question(question: str, k: int = 4) -> dict:
    """Send question to FastAPI backend."""
    try:
        response = requests.post(
            f"{API_BASE}/ask",
            json={"question": question, "k": k},
            timeout=30,
        )
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to API. Make sure the server is running:\n`uvicorn src.api:app --reload --port 8000`"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. The model may be loading — try again."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_papers() -> list:
    """Fetch list of indexed papers from API."""
    try:
        response = requests.get(f"{API_BASE}/papers", timeout=5)
        response.raise_for_status()
        return response.json().get("papers", [])
    except:
        return []

def check_api_health() -> bool:
    """Check if API is running."""
    try:
        r = requests.get(f"{API_BASE}/", timeout=3)
        return r.status_code == 200
    except:
        return False

def format_source(source: str) -> str:
    """Clean up source path for display."""
    return source.split("/")[-1].replace(".pdf", "").replace("_", " ")

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚗️ ChemRAG")
    st.markdown("---")

    # API Status
    api_ok = check_api_health()
    if api_ok:
        st.success("● API connected", icon=None)
    else:
        st.error("● API offline")
        st.markdown("""
<div style='font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#8b949e;line-height:1.8'>
Start the server:<br>
<code style='color:#58a6ff'>uvicorn src.api:app --reload --port 8000</code>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # Retrieval settings
    st.markdown("### Settings")
    k_chunks = st.slider(
        "Chunks to retrieve (k)",
        min_value=1, max_value=10, value=4,
        help="More chunks = more context but slower"
    )

    st.markdown("---")

    # Indexed papers
    st.markdown("### Indexed Papers")
    if st.button("Refresh papers"):
        st.session_state.papers = get_papers()

    if not st.session_state.papers:
        st.session_state.papers = get_papers()

    if st.session_state.papers:
        for p in st.session_state.papers:
            name = format_source(p)
            st.markdown(f"""
<div class='paper-card'>
  <div class='paper-name'>📄 {name}</div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div style='font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#8b949e'>
No papers indexed yet.<br><br>
Add PDFs to <code>papers/</code> folder<br>
then run:<br>
<code style='color:#58a6ff'>python src/ingest.py</code>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # Clear chat
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
<div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#8b949e;margin-top:1rem;line-height:1.8'>
Built by Dheeraj Meena<br>
IIT Delhi · ChemE · 2026<br>
<a href='https://github.com/AISHDM' style='color:#58a6ff'>github.com/AISHDM</a>
</div>
""", unsafe_allow_html=True)

# ── Main area ──────────────────────────────────────────────────────────────────
# Header
st.markdown("""
<div class='main-title'>Chem<span>RAG</span></div>
<div class='main-subtitle'>Research Paper Q&A · LangChain · ChromaDB · Llama 3 · Groq</div>
""", unsafe_allow_html=True)

# Stats row
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
<div class='metric-card'>
  <div class='metric-val'>{len(st.session_state.papers)}</div>
  <div class='metric-label'>Papers indexed</div>
</div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
<div class='metric-card'>
  <div class='metric-val'>{len(st.session_state.messages)}</div>
  <div class='metric-label'>Questions asked</div>
</div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
<div class='metric-card'>
  <div class='metric-val'>{'🟢' if api_ok else '🔴'}</div>
  <div class='metric-label'>API status</div>
</div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Example questions
if not st.session_state.messages:
    st.markdown("""
<div style='font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#8b949e;
            text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.75rem'>
Try asking:
</div>
""", unsafe_allow_html=True)

    example_cols = st.columns(3)
    examples = [
        "What is multi-head attention?",
        "How does message passing work in GNNs?",
        "What datasets were used in the experiments?",
    ]
    for i, (col, ex) in enumerate(zip(example_cols, examples)):
        with col:
            if st.button(f'"{ex}"', key=f"ex_{i}"):
                st.session_state.messages.append({"role": "user", "content": ex})
                with st.spinner("Thinking..."):
                    result = ask_question(ex, k=k_chunks)
                if result["success"]:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["data"].get("answer", "No answer returned."),
                        "sources": result["data"].get("sources", []),
                    })
                else:
                    st.session_state.messages.append({
                        "role": "error",
                        "content": result["error"],
                    })
                st.rerun()

# Chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>🧑‍🔬 {msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        sources_html = ""
        if msg.get("sources"):
            tags = "".join(f"<span class='source-tag'>📄 {format_source(s)}</span>" for s in msg["sources"])
            sources_html = f"<div class='source-label'>Sources</div>{tags}"
        st.markdown(f"""
<div class='bot-msg'>
  <div class='answer-text'>⚗️ {msg['content']}</div>
  {sources_html}
</div>""", unsafe_allow_html=True)
    elif msg["role"] == "error":
        st.markdown(f"<div class='error-msg'>⚠ {msg['content']}</div>", unsafe_allow_html=True)

# Input
st.markdown("<br>", unsafe_allow_html=True)
with st.form("question_form", clear_on_submit=True):
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        question = st.text_input(
            "question",
            placeholder="Ask anything about the indexed papers...",
            label_visibility="collapsed",
        )
    with col_btn:
        submitted = st.form_submit_button("Ask →")

if submitted and question.strip():
    st.session_state.messages.append({"role": "user", "content": question.strip()})
    with st.spinner("Retrieving and generating answer..."):
        result = ask_question(question.strip(), k=k_chunks)
    if result["success"]:
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["data"].get("answer", "No answer returned."),
            "sources": result["data"].get("sources", []),
        })
    else:
        st.session_state.messages.append({
            "role": "error",
            "content": result["error"],
        })
    st.rerun()
elif submitted and not question.strip():
    st.warning("Please enter a question.")
