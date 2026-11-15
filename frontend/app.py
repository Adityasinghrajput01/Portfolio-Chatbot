import re
import time
import uuid

import requests
import streamlit as st

API_URL = "https://portfolio-chatbot-t30b.onrender.com/chat"

st.set_page_config(page_title="Aditya Kumar Singh · AI Portfolio", page_icon="✦", layout="wide")

# ───────────────────────── Styles ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Syne:wght@600;700;800&family=Cormorant+Garamond:ital,wght@1,500&display=swap');

:root { --bg:#0b0c10; --panel:#13151c; --line:#262932; --text:#ece7df; --muted:#8d8b96; --gold:#f5c97a; --gold-d:#a8823a; }

html, body, .stApp, p, li, label, input, textarea, button { font-family:'DM Sans', sans-serif; }
.stApp { background: radial-gradient(900px 420px at 85% -5%, #2a2118 0%, transparent 60%), var(--bg); color:var(--text); }

/* hide streamlit chrome */
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display:none !important; }
header[data-testid="stHeader"] { background:transparent; }
.block-container { max-width:820px; padding-top:2.2rem; padding-bottom:7rem; }

h1,h2,h3 { font-family:'Syne', sans-serif !important; color:var(--text) !important; letter-spacing:-.5px; }

/* sidebar */
[data-testid="stSidebar"] { background:#0f1117; border-right:1px solid var(--line); }
[data-testid="stSidebar"] .stButton button { text-align:left; justify-content:flex-start; background:transparent;
    color:var(--muted); border:1px solid transparent; border-radius:10px; padding:.5rem .7rem; font-size:14px; }
[data-testid="stSidebar"] .stButton button:hover { background:var(--panel); color:var(--text); border-color:var(--line); }
[data-testid="stSidebar"] .stButton:first-of-type button { background:var(--gold); color:#14110b; font-weight:600; justify-content:center; }
[data-testid="stSidebar"] .stButton:first-of-type button:hover { background:#ffd994; color:#14110b; }

.profile { display:flex; gap:12px; align-items:center; padding:6px 0 14px; }
.avatar { width:42px; height:42px; border-radius:12px; background:linear-gradient(135deg,var(--gold),#b8843a);
    color:#14110b; display:grid; place-items:center; font-weight:800; font-family:'Syne'; font-size:18px; }
.pname { font-family:'Syne'; font-weight:700; font-size:15px; color:var(--text); line-height:1.2; }
.prole { font-size:12px; color:var(--muted); }
.links a { color:var(--muted); font-size:13px; text-decoration:none; margin-right:14px; }
.links a:hover { color:var(--gold); }

/* chat messages */
[data-testid="stChatMessage"] { background:transparent; border:none; padding:.6rem 0; gap:.9rem; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:.8rem 1rem; }
[data-testid="stChatMessageAvatarAssistant"] { background:linear-gradient(135deg,var(--gold),#b8843a) !important; color:#14110b !important; }
[data-testid="stChatMessageAvatarUser"] { background:#2b2e3a !important; }
[data-testid="stChatMessage"] p { font-size:15.5px; line-height:1.75; }

/* input */
[data-testid="stBottom"] > div { background:transparent !important; }
[data-testid="stChatInput"] { border-radius:18px; border:1px solid var(--line); background:var(--panel); }
[data-testid="stChatInput"]:focus-within { border-color:var(--gold-d); box-shadow:0 0 0 3px rgba(245,201,122,.12); }
[data-testid="stChatInput"] textarea { background:transparent !important; color:var(--text) !important; }

/* welcome */
.greet { font-family:'Syne'; font-size:clamp(34px,6vw,54px); font-weight:700; letter-spacing:-2px; line-height:1.05; margin:3.5rem 0 .6rem; }
.greet em { font-family:'Cormorant Garamond',serif; font-weight:500; color:var(--gold); letter-spacing:0; }
.sub { color:var(--muted); font-size:15.5px; line-height:1.7; max-width:560px; margin-bottom:2rem; }

/* suggestion cards (main area buttons) */
.main .stButton button, section.main .stButton button, [data-testid="stMain"] .stButton button {
    background:var(--panel); color:var(--text); border:1px solid var(--line); border-radius:14px;
    padding:1rem 1.1rem; text-align:left; justify-content:flex-start; min-height:72px; font-size:14.5px; transition:border-color .2s, background .2s; }
[data-testid="stMain"] .stButton button:hover { border-color:var(--gold-d); background:#181b24; color:var(--gold); }

/* cards */
.card { background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:20px 22px; margin-bottom:14px; }
.card h4 { font-family:'Syne'; font-size:18px; margin:0 0 8px; color:var(--text); }
.card p { color:var(--muted); font-size:14px; line-height:1.7; margin:0; }
.card a { color:var(--gold); text-decoration:none; font-size:13.5px; font-weight:500; }
.chip { display:inline-block; font-size:12px; color:#c9bde3; background:#1c1a26; border:1px solid #3a3350;
    border-radius:999px; padding:3px 10px; margin:12px 6px 10px 0; }
.stat { font-family:'Syne'; font-size:30px; font-weight:700; color:var(--gold); }
.status { font-size:12px; color:var(--muted); }
.dot { display:inline-block; width:7px; height:7px; border-radius:50%; background:#62d08b; margin-right:6px; }
</style>
""", unsafe_allow_html=True)

# ───────────────────────── State ─────────────────────────
st.session_state.setdefault("session_id", str(uuid.uuid4()))
st.session_state.setdefault("messages", [])
st.session_state.setdefault("pending", None)
st.session_state.setdefault("view", "Chat")

SUGGESTIONS = [
    ("Projects", "Tell me about your projects."),
    ("Skills", "What are your technical skills?"),
    ("Education", "Tell me about your education."),
    ("Achievements", "What are your achievements?"),
]


def ask(question: str):
    st.session_state.pending = question
    st.session_state.view = "Chat"


def new_chat():
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.view = "Chat"


def call_backend(question: str) -> str:
    """Call the API; retries once because free Render servers sleep and wake slowly."""
    for attempt in range(2):
        try:
            r = requests.post(
                API_URL,
                json={"session_id": st.session_state.session_id, "question": question},
                timeout=90,
            )
            r.raise_for_status()
            return r.json()["answer"]
        except requests.exceptions.Timeout:
            if attempt == 1:
                return "The server took too long to respond. Please try again in a moment."
        except requests.exceptions.RequestException:
            if attempt == 1:
                return "I couldn't reach the backend. Please try again in a moment."
            time.sleep(2)
        except (ValueError, KeyError):
            return "The backend returned an unexpected response."
    return "Something went wrong. Please try again."


def stream_words(text: str):
    for token in re.split(r"(\s+)", text):
        yield token
        time.sleep(0.012)


# Read chat input first so it can switch the view before the sidebar radio is built
typed = st.chat_input("Message Aditya's AI assistant…")
prompt = typed or st.session_state.pending
st.session_state.pending = None
if typed:
    st.session_state.view = "Chat"

# ───────────────────────── Sidebar ─────────────────────────
with st.sidebar:
    st.button("＋  New chat", on_click=new_chat, use_container_width=True)
    st.write("")
    st.radio("View", ["Chat", "Projects", "About"], key="view", label_visibility="collapsed")
    st.write("")
    st.caption("Quick questions")
    for label, q in SUGGESTIONS:
        st.button(label, key=f"side_{label}", on_click=ask, args=(q,), use_container_width=True)
    st.divider()
    st.markdown("""
    <div class="profile"><div class="avatar">A</div>
      <div><div class="pname">Aditya Kumar Singh</div>
      <div class="prole">CS student · Lovely Professional University</div></div></div>
    <div class="links">
      <a href="https://github.com/Adityasinghrajput01" target="_blank">GitHub</a>
      <a href="https://www.linkedin.com/in/aditya-kumar-singh-173911321/" target="_blank">LinkedIn</a>
      <a href="mailto:adityasingh452452@gmail.com">Email</a>
    </div>
    """, unsafe_allow_html=True)

view = st.session_state.view

# ───────────────────────── Chat view ─────────────────────────
if view == "Chat":
    if not st.session_state.messages and not prompt:
        st.markdown("""
        <div class="greet">Hi, I'm Aditya's<br><em>portfolio assistant.</em></div>
        <div class="sub">Ask me about his projects, skills, education or achievements.
        He builds machine learning and data tools, and I can walk you through any of them.</div>
        """, unsafe_allow_html=True)
        cols = st.columns(2)
        for i, (label, q) in enumerate(SUGGESTIONS):
            with cols[i % 2]:
                st.button(q, key=f"main_{label}", on_click=ask, args=(q,), use_container_width=True)
        st.markdown('<div class="status" style="margin-top:1.5rem"><span class="dot"></span>Online</div>',
                    unsafe_allow_html=True)

    for m in st.session_state.messages:
        with st.chat_message(m["role"],  avatar="✨" if m["role"] == "assistant" else "🙂"):
            st.markdown(m["content"])

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🙂"):
            st.markdown(prompt)
        with st.chat_message("assistant",  avatar="✨"):
            with st.spinner("Thinking…"):
                answer = call_backend(prompt)
            st.write_stream(stream_words(answer))
        st.session_state.messages.append({"role": "assistant", "content": answer})

# ───────────────────────── Projects view ─────────────────────────
elif view == "Projects":
    st.markdown("## Projects")
    st.caption("Open-source work. Click through for the code.")
    projects = [
        ("AutoForge Engine",
         "Open-source AutoML framework published on PyPI. Includes preprocessing, model evaluation, cross-validation, hyperparameter tuning and a CLI.",
         ["Python", "Scikit-learn", "PyPI"], "https://github.com/Adityasinghrajput01/ModelForge"),
        ("NYC Taxi Prediction",
         "End-to-end ML pipeline trained on 1.45M+ records. A Random Forest model reached R² 0.7674 and is served through FastAPI.",
         ["Python", "FastAPI", "Docker"], "https://github.com/Adityasinghrajput01/NYC-Taxi-Trip-Duration-Prediction"),
        ("EV Range Prediction",
         "Model comparison for predicting electric vehicle range, with an interactive Power BI dashboard covering 500+ vehicles.",
         ["Python", "ML", "Power BI"], "https://github.com/Adityasinghrajput01/Electric-Vehicle-range-prediction"),
    ]
    for title, desc, tags, link in projects:
        chips = "".join(f'<span class="chip">{t}</span>' for t in tags)
        st.markdown(f'<div class="card"><h4>{title}</h4><p>{desc}</p>{chips}<br>'
                    f'<a href="{link}" target="_blank">View source ↗</a></div>', unsafe_allow_html=True)
    st.button("Ask the assistant about these projects", on_click=ask,
              args=("Tell me about your projects.",))

# ───────────────────────── About view ─────────────────────────
else:
    st.markdown("## About")
    st.markdown('<p class="sub" style="margin-bottom:1.2rem">I\'m Aditya Kumar Singh, a Computer Science student at '
                'Lovely Professional University, interested in machine learning, data science and practical AI tools.</p>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, num, label in [(c1, "1,000+", "DSA problems solved"),
                            (c2, "0.7674", "NYC taxi model R²"),
                            (c3, "v1.0.2", "autoforge-engine latest release on PyPI")]:
        col.markdown(f'<div class="card"><div class="stat">{num}</div><p>{label}</p></div>', unsafe_allow_html=True)

    st.markdown("### Skills")
    for title, items in [
        ("Languages & data", "Python, Java, C++, SQL, R, Pandas, NumPy"),
        ("Machine learning", "Scikit-learn, XGBoost, LightGBM, TensorFlow, PyTorch"),
        ("Engineering & BI", "FastAPI, Docker, Git, AWS, Power BI, Tableau"),
    ]:
        st.markdown(f'<div class="card"><h4>{title}</h4><p>{items}</p></div>', unsafe_allow_html=True)


    st.markdown("### Open-source package")
    st.markdown(
        '<div class="card"><h4>autoforge-engine on PyPI</h4>'
        '<p>My open-source AutoML framework for Python. It covers preprocessing, 10-fold cross-validation, '
        'hyperparameter tuning and model persistence, with a CLI and Python API tested with pytest. '
        'Author and maintainer: Aditya Kumar Singh.</p>'
        '<span class="chip">Python</span><span class="chip">Scikit-learn</span><span class="chip">pytest</span><br>'
        '<a href="https://pypi.org/project/autoforge-engine/" target="_blank">View on PyPI ↗</a> &nbsp;·&nbsp; '
        '<a href="https://github.com/Adityasinghrajput01/ModelForge" target="_blank">Source on GitHub ↗</a></div>',
        unsafe_allow_html=True)

    st.markdown("### Links and resume")
    st.markdown(
        '<div class="card"><p>'
        '<a href="https://github.com/Adityasinghrajput01" target="_blank">GitHub ↗</a> &nbsp;·&nbsp; '
        '<a href="https://www.linkedin.com/in/aditya-kumar-singh-173911321/" target="_blank">LinkedIn ↗</a> &nbsp;·&nbsp; '
        '<a href="https://pypi.org/project/autoforge-engine/" target="_blank">PyPI ↗</a></p></div>',
        unsafe_allow_html=True)
    import pathlib
    resume = pathlib.Path(__file__).parent / "Aditya_resume.pdf"
    if resume.exists():
        st.download_button("Download my resume (PDF)", resume.read_bytes(),
                           file_name="Aditya_Kumar_Singh_Resume.pdf", mime="application/pdf")
