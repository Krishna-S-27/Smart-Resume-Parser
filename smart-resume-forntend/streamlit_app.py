import streamlit as st
import requests
import json
import re

# ─────────────────────────────────────────────
# Page Setup
# ─────────────────────────────────────────────
st.set_page_config(page_title="📄 Smart Resume Parser", layout="wide")

API_URL = "https://smart-resume-parser-backend-url.onrender.com" 

# ─────────────────────────────────────────────
# JSON Cleaner
# ─────────────────────────────────────────────
def clean_ai_json(raw_text):
    """Cleans/parses AI-generated JSON safely."""
    try:
        if not isinstance(raw_text, str):
            return {}

        # Extract inside ```json ... ```
        match = re.search(r"```json(.*?)```", raw_text, re.DOTALL | re.IGNORECASE)
        if match:
            raw_text = match.group(1).strip()
        else:
            # fallback: any fenced block
            match_any = re.search(r"```(.*?)```", raw_text, re.DOTALL)
            if match_any:
                raw_text = match_any.group(1).strip()

        raw_text = raw_text.replace("```", "").strip()
        raw_text = raw_text.replace("’", "'").replace("“", '"').replace("”", '"')
        raw_text = raw_text.replace("'", '"')
        raw_text = re.sub(r",\s*([}\]])", r"\1", raw_text)

        parsed = json.loads(raw_text)
        if isinstance(parsed, dict):
            return parsed
        else:
            return {"parsed_list": parsed}
    except Exception as e:
        return {"error": str(e), "raw_text": raw_text}

# ─────────────────────────────────────────────
# Styles
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp { background-color: #0f172a; color: #e5e7eb; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { color: #f3f4f6; font-weight: 600; }
    .profile-card { background: linear-gradient(135deg, #1e3a8a 0%, #0ea5e9 100%);
        padding: 20px; border-radius: 14px; color: white; margin: 8px 0 18px 0;
        box-shadow: 0 12px 30px rgba(14,165,233,0.25); }
    .section-card { background: #111827; border: 1px solid #1f2937; padding: 18px;
        border-radius: 12px; margin-bottom: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.35); }
    .section-card:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(0,0,0,0.45); }
    .skill-tag { display: inline-block; background: #0b1220; padding: 6px 12px;
        border-radius: 999px; margin: 4px 6px 0 0; font-size: 13px; color: #93c5fd;
        border: 1px solid #1d4ed8; }
    .timeline-item { padding: 12px; border-left: 3px solid #06b6d4;
        margin: 10px 0; background: #0b1220; border-radius: 8px; }
    .project-card { background: #1e293b; padding: 14px; border-radius: 10px; margin: 8px 0; }
    a { color: #93c5fd !important; text-decoration: none; }
    a:hover { color: #bfdbfe !important; text-decoration: underline; }
    .stButton > button { background: linear-gradient(90deg, #3b82f6, #06b6d4);
        color: white; border: none; border-radius: 10px; padding: 0.65rem 1.1rem;
        font-weight: 600; box-shadow: 0 8px 20px rgba(59,130,246,0.25); }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 10px 24px rgba(59,130,246,0.35); }
    .divider { height: 1px; background: #1f2937; margin: 10px 0 18px 0; }
    </style>
    """,
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# Header / Upload
# ─────────────────────────────────────────────
st.title("📄 Smart Resume Parser")
st.caption("Upload a resume and get clean, structured insights powered by AI and reload before or after every parsing.")

uploaded_file = st.file_uploader("📂 Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
if uploaded_file:
    st.success("✅ Selected file: {}".format(uploaded_file.name))

parse_clicked = st.button("🚀 Parse Resume", type="primary", disabled=not uploaded_file)

# ─────────────────────────────────────────────
# Processing
# ─────────────────────────────────────────────
if parse_clicked and uploaded_file:
    with st.spinner("Parsing resume... ⏳"):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            resp = requests.post("{}/upload".format(API_URL), files=files, timeout=120)
        except Exception as e:
            st.error("❌ Request failed: {}".format(e))
            st.stop()

    if resp.status_code != 200:
        st.error("❌ Backend error: {}\n\n{}".format(resp.status_code, resp.text))
        st.stop()

    result = resp.json()
    data = result.get("data", {}) or {}

    # Merge parsed raw_output JSON into main dict
    if "raw_output" in data and isinstance(data["raw_output"], str):
        parsed = clean_ai_json(data["raw_output"])
        if isinstance(parsed, dict):
            for k, v in parsed.items():
                if k not in data or not data[k]:
                    data[k] = v

    # ───────── Profile Card
    st.markdown(
        """
        <div class="profile-card">
            <h2 style="margin-bottom:8px;">{}</h2>
            <div>📧 {}</div>
            <div>📞 {}</div>
            <div class="divider"></div>
            <div>{}</div>
        </div>
        """.format(data.get('name', '—'), data.get('email', '—'), data.get('phone', '—'), data.get('summary', '') or ''),
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([2, 1], gap="large")

    with col_left:
        # ───────── Skills
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("🛠 Skills")
        skills = data.get("skills", []) or []
        if skills:
            st.markdown("".join(["<span class='skill-tag'>{}</span>".format(s) for s in skills]), unsafe_allow_html=True)
        else:
            st.write("—")
        st.markdown("</div>", unsafe_allow_html=True)

        # ───────── Education
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("🎓 Education")
        for e in data.get("education", []) or []:
            if isinstance(e, dict):
                st.markdown(
                    "<div class='timeline-item'><b>{}</b> in {}<br>📍 {}<br>📅 {}</div>".format(
                        e.get('degree', ''), e.get('subject', ''), e.get('college', ''), e.get('year', '')
                    ),
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("- {}".format(e))
        st.markdown("</div>", unsafe_allow_html=True)

        # ───────── Experience
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("💼 Experience")
        for e in data.get("experience", []) or []:
            if isinstance(e, dict):
                st.markdown(
                    "<div class='timeline-item'><b>{}</b><br>📌 {}</div>".format(
                        e.get('role', ''), e.get('project', '')
                    ),
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("- {}".format(e))
        st.markdown("</div>", unsafe_allow_html=True)

        # ───────── Extra Sections
        for section_name, items in (data.get("sections", {}) or {}).items():
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.subheader("📂 {}".format(section_name.capitalize()))
            if items:
                for item in items:
                    if isinstance(item, dict):
                        st.markdown(
                            "<div class='project-card'><b>{}</b><br>{}</div>".format(
                                item.get('title', 'Untitled'), item.get('description', '')
                            ),
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown("- {}".format(item))
            else:
                st.write("—")
            st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        # ───────── Links
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("🌐 Links")
        for l in data.get("links", []) or []:
            st.markdown("- [{}]({})".format(l, l))
        st.markdown("</div>", unsafe_allow_html=True)

        # ───────── Export
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("⬇️ Export")
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        st.download_button("Download JSON", data=json_data, file_name="parsed_resume.json", mime="application/json")

        try:
            import pandas as pd
            rows = []
            for sec in ["skills", "education", "experience"]:
                values = data.get(sec, [])
                if isinstance(values, list):
                    for item in values:
                        rows.append({
                            "section": sec,
                            "value": json.dumps(item, ensure_ascii=False) if isinstance(item, dict) else str(item)
                        })
            csv_data = pd.DataFrame(rows).to_csv(index=False)
            st.download_button("Download CSV", data=csv_data, file_name="parsed_resume.csv", mime="text/csv")
        except Exception as e:
            st.caption("CSV export unavailable: {}".format(e))
        st.markdown("</div>", unsafe_allow_html=True)

        # ───────── Backend Exports
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("📦 Backend Exports")
        for label, link in (result.get("downloads", {}) or {}).items():
            st.markdown("- [📥 {}]({}{})".format(label.upper(), API_URL, link))
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("🔍 Raw JSON (debug)"):
        st.json(data)
