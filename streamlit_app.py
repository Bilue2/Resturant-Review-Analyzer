# streamlit_app.py
# 🍗 Customer Review Insights Bot — Chat UI + Conversation Dashboard
#
# Sidebar:
#   - New chat
#   - Conversation history (click to open)
#   - Rename + Delete
# Main page:
#   - Chat
#   - Advanced settings (collapsed)
#   - Debug (collapsed, optional)

import json
import time
import uuid
import streamlit as st
from app.rag import generate_grounded_response

st.set_page_config(
    page_title="🍗 Customer Review Insights Bot",
    page_icon="🍗",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _apply_professional_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
            color: #f8fafc;
        }
        [data-testid="stSidebar"] .stButton > button {
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 0.75rem;
            background: rgba(255,255,255,0.12);
            color: #ffffff;
            font-weight: 600;
            transition: 180ms ease-in-out;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            border-color: rgba(255,255,255,0.28);
            background: rgba(255,255,255,0.18);
        }
        [data-testid="stSidebar"] .stTextInput > div > div > input {
            background: rgba(255,255,255,0.95);
            color: #0f172a;
            border: 1px solid rgba(255,255,255,0.2);
        }
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .st-bd,
        [data-testid="stSidebar"] .st-emotion-cache-1jicfl2,
        [data-testid="stSidebar"] .st-emotion-cache-10trblm {
            color: #f8fafc !important;
        }
        [data-testid="stSidebar"] .stRadio > label,
        [data-testid="stSidebar"] .stSelectbox > label {
            color: #f8fafc;
        }
        [data-testid="stSidebar"] .stRadio > div {
            background: rgba(255,255,255,0.04);
            border-radius: 0.6rem;
            padding: 0.4rem 0.5rem;
        }
        .hero-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 1rem;
            padding: 1.2rem 1.3rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
            margin-bottom: 1rem;
        }
        .hero-kicker {
            display: inline-block;
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            background: #eff6ff;
            color: #1d4ed8;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }
        .info-box {
            background: rgba(248, 250, 252, 0.9);
            border: 1px solid rgba(148, 163, 184, 0.28);
            border-radius: 0.9rem;
            padding: 0.9rem 1rem;
            color: #334155;
        }
        .stChatMessage {
            border-radius: 0.8rem;
            padding: 0.4rem 0.6rem;
        }
        div[data-testid="stExpander"] {
            border: 1px solid rgba(148, 163, 184, 0.24);
            border-radius: 0.8rem;
            padding: 0.2rem 0.25rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


_apply_professional_styles()

# =========================
# Session state helpers
# =========================
def _init_state() -> None:
    if "conversations" not in st.session_state:
        # { chat_id: { "title": str, "messages": [{"role": "user|assistant", "content": str}], "created": float } }
        st.session_state.conversations = {}

    if "active_chat_id" not in st.session_state:
        st.session_state.active_chat_id = None

    if "settings" not in st.session_state:
        st.session_state.settings = {
            "top_k": 12,
            "min_recurring_reviews": 2,
            "debug_on": False,
        }

def _new_chat() -> None:
    chat_id = str(uuid.uuid4())
    st.session_state.conversations[chat_id] = {
        "title": "New chat",
        "messages": [],
        "created": time.time(),
    }
    st.session_state.active_chat_id = chat_id

def _ensure_active_chat() -> None:
    if not st.session_state.conversations:
        _new_chat()
        return
    if st.session_state.active_chat_id not in st.session_state.conversations:
        # Fall back to newest chat
        newest = max(st.session_state.conversations.items(), key=lambda kv: kv[1]["created"])[0]
        st.session_state.active_chat_id = newest

def _set_title_from_first_user_message(chat_id: str) -> None:
    convo = st.session_state.conversations[chat_id]
    if convo["title"] != "New chat":
        return
    for m in convo["messages"]:
        if m["role"] == "user" and m["content"].strip():
            t = m["content"].strip()
            convo["title"] = t[:40] + ("…" if len(t) > 40 else "")
            return

def _delete_chat(chat_id: str) -> None:
    st.session_state.conversations.pop(chat_id, None)
    if not st.session_state.conversations:
        _new_chat()
    else:
        newest = max(st.session_state.conversations.items(), key=lambda kv: kv[1]["created"])[0]
        st.session_state.active_chat_id = newest

def _sorted_chat_ids_newest_first():
    items = sorted(
        st.session_state.conversations.items(),
        key=lambda kv: kv[1]["created"],
        reverse=True,
    )
    return [cid for cid, _ in items]


# =========================
# Init
# =========================
_init_state()
if st.session_state.active_chat_id is None:
    _new_chat()
_ensure_active_chat()

# =========================
# Sidebar — Conversation dashboard
# =========================
with st.sidebar:
    st.markdown("### 💬 Conversation workspace")
    st.caption("Organize review analyses and switch between topics effortlessly.")

    # New chat button
    if st.button("➕ New chat", use_container_width=True):
        _new_chat()
        st.rerun()

    st.divider()

    chat_ids = _sorted_chat_ids_newest_first()
    active = st.session_state.active_chat_id

    # Conversation list (click to open)
    selected = st.radio(
        "History",
        options=chat_ids,
        index=chat_ids.index(active) if active in chat_ids else 0,
        format_func=lambda cid: st.session_state.conversations[cid]["title"],
        label_visibility="collapsed",
    )
    st.session_state.active_chat_id = selected
    _ensure_active_chat()

    st.divider()

    # Optional rename
    convo = st.session_state.conversations[st.session_state.active_chat_id]
    with st.expander("✏️ Rename / Manage", expanded=False):
        new_title = st.text_input("Conversation title", value=convo["title"])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save title", use_container_width=True):
                convo["title"] = (new_title.strip() or "Untitled")
                st.rerun()
        with col2:
            if st.button("Delete chat", use_container_width=True):
                _delete_chat(st.session_state.active_chat_id)
                st.rerun()

# =========================
# Main — Chat UI
# =========================
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-kicker">Grounded review analysis</div>
        <h1 style="margin:0 0 0.25rem 0;">Customer Review Insights Bot</h1>
        <p style="margin:0; color:#475569;">Ask about sentiment, recurring issues, operational opportunities, and draft follow-ups with evidence-backed answers.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_intro, col_tip = st.columns([2, 1], gap="medium")
with col_intro:
    st.info("Use this workspace to inspect customer feedback, identify recurring themes, and turn observations into practical actions.")
with col_tip:
    st.markdown(
        """
        <div class="info-box">
            <strong>Try asking:</strong><br>
            • What are the most common complaints?<br>
            • Draft an SMS response for unhappy guests.<br>
            • Which issues should operations prioritize?
        </div>
        """,
        unsafe_allow_html=True,
    )

cid = st.session_state.active_chat_id
convo = st.session_state.conversations[cid]

# Advanced settings expander (collapsed by default)
with st.expander("⚙️ Advanced settings", expanded=False):
    st.session_state.settings["top_k"] = st.slider(
        "Retrieved chunks (top_k)",
        min_value=3,
        max_value=50,
        value=int(st.session_state.settings["top_k"]),
        step=1,
    )
    st.session_state.settings["min_recurring_reviews"] = st.slider(
        "Min recurring reviews",
        min_value=1,
        max_value=10,
        value=int(st.session_state.settings["min_recurring_reviews"]),
        step=1,
    )
    st.session_state.settings["debug_on"] = st.toggle(
        "Enable debug output",
        value=bool(st.session_state.settings["debug_on"]),
    )

# Render history
for msg in convo["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Ask a question about the reviews…")

def _render_details(out: dict) -> None:
    """Collapsed details (themes/issues/SMS/ops + sources)."""
    with st.expander("Details (themes, issues, SMS, ops)", expanded=False):
        # Overall sentiment
        osent = out.get("overall_sentiment") or {}
        st.markdown(f"**Overall sentiment:** `{osent.get('label', 'mixed')}`")
        if osent.get("rationale"):
            st.write(osent["rationale"])

        # Themes
        st.subheader("Themes")
        themes = out.get("top_themes", []) or []
        if not themes:
            st.write("_No themes returned._")
        else:
            for th in themes:
                st.markdown(f"**{th.get('theme', 'Theme')}** • sentiment: `{th.get('sentiment', 'mixed')}`")
                for ev in th.get("evidence", []) or []:
                    st.markdown(f"- `{ev.get('chunk_id','')}` — {ev.get('excerpt','')}")

        # Issues
        st.subheader("Recurring issues")
        rec = out.get("recurring_issues", []) or []
        if not rec:
            st.write("_None._")
        else:
            for i, it in enumerate(rec, start=1):
                st.markdown(f"**{i}. {it.get('issue','')}**")
                ids = it.get("evidence_chunk_ids", []) or []
                if ids:
                    st.code("\n".join(ids))

        iso = out.get("isolated_issues", []) or []
        if iso:
            st.subheader("Isolated issues")
            for i, it in enumerate(iso, start=1):
                st.markdown(f"**{i}. {it.get('issue','')}**")
                ids = it.get("evidence_chunk_ids", []) or []
                if ids:
                    st.code("\n".join(ids))

        # SMS
        st.subheader("Draft SMS")
        sms = out.get("sms_draft") or {}
        msgs = sms.get("messages", []) or []
        if not msgs:
            st.write("_None._")
        else:
            for i, m in enumerate(msgs, start=1):
                st.markdown(f"**Message {i}**")
                st.code(m)

        # Ops recommendations
        st.subheader("Ops recommendations")
        recs = out.get("ops_recommendations", []) or []
        if not recs:
            st.write("_None._")
        else:
            for i, r in enumerate(recs, start=1):
                st.markdown(f"**{i}. {r.get('recommendation','')}**")
                ids = r.get("grounding_chunk_ids", []) or []
                if ids:
                    st.caption("Grounding chunk IDs")
                    st.code("\n".join(ids))

        # Sources
        st.subheader("Sources (chunk IDs)")
        src = set()
        for th in out.get("top_themes", []) or []:
            for ev in th.get("evidence", []) or []:
                if ev.get("chunk_id"):
                    src.add(ev["chunk_id"])
        for r in out.get("ops_recommendations", []) or []:
            for x in r.get("grounding_chunk_ids", []) or []:
                src.add(x)
        for it in out.get("recurring_issues", []) or []:
            for x in it.get("evidence_chunk_ids", []) or []:
                src.add(x)
        if src:
            st.code("\n".join(sorted(src)))
        else:
            st.write("_No sources provided._")

def _render_debug(out: dict) -> None:
    """Collapsed debug expander (only if enabled)."""
    if not st.session_state.settings["debug_on"]:
        return
    with st.expander("🧪 Debug", expanded=False):
        st.code(json.dumps(out, ensure_ascii=False, indent=2), language="json")

if prompt:
    # Append user message
    convo["messages"].append({"role": "user", "content": prompt})
    _set_title_from_first_user_message(cid)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving + generating grounded insights…"):
            out = generate_grounded_response(
                query=prompt,
                top_k=int(st.session_state.settings["top_k"]),
                min_recurring_reviews=int(st.session_state.settings["min_recurring_reviews"]),
                include_debug=bool(st.session_state.settings["debug_on"]),
            )

        if not isinstance(out, dict):
            st.error("Unexpected output type from backend (expected dict).")
            st.write(out)
        else:
            # Main assistant reply: keep it clean
            answer = out.get("answer_summary", "").strip() or "No answer summary returned."
            st.markdown(answer)

            # Details + debug collapsed
            _render_details(out)
            _render_debug(out)

            # Store assistant message in history (store clean text, not the whole JSON)
            convo["messages"].append({"role": "assistant", "content": answer})
