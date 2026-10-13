import time

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Resume Evaluator", page_icon="📄", layout="wide")

try:
    import resume_parser as rp
except ValueError:
    st.error("GROQ_API_KEY missing. Put it in a `.env` file next to app.py and restart.")
    st.stop()

st.title("📄 AI Resume Evaluator")
st.caption("Upload resumes, paste a job description, get a ranked shortlist.")

with st.sidebar:
    st.header("Job description")
    jd = st.text_area("Paste JD", rp.job_description.strip(), height=350)
    files = st.file_uploader("Resumes (PDF / DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
    run = st.button("Evaluate", type="primary", disabled=not (files and jd.strip()), use_container_width=True)

if run:
    results = []
    bar = st.progress(0.0, "Parsing job description…")
    job = rp.parse_job(jd)
    for i, f in enumerate(files):
        bar.progress(i / len(files), f"Evaluating {f.name}…")
        try:
            text = rp.read_pdf(f) if f.name.lower().endswith(".pdf") else rp.read_docx(f)
            resume = rp.parse_resume(text)
            time.sleep(2)  # ponytail: crude rate-limit guard, use retry/backoff if Groq limits bite
            m = rp.final_score(job, resume)
            results.append({"file": f.name, "name": resume.name or f.name, "score": m.score, "details": m.details})
        except Exception as e:
            st.warning(f"{f.name}: {e}")
    bar.empty()
    st.session_state["job"] = job
    st.session_state["results"] = sorted(results, key=lambda r: r["score"], reverse=True)

if "results" in st.session_state:
    results = st.session_state["results"]
    st.subheader("Ranking")
    df = pd.DataFrame(results)[["name", "score", "file"]]
    st.dataframe(
        df, hide_index=True, use_container_width=True,
        column_config={"score": st.column_config.ProgressColumn("Match %", min_value=0, max_value=100, format="%.0f")},
    )
    st.subheader("Details")
    for r in results:
        with st.expander(f"{r['name']} — {r['score']:.0f}%"):
            for k, v in r["details"].items():
                st.markdown(f"**{k.replace('_', ' ').title()}**")
                if isinstance(v, list):
                    st.markdown("\n".join(f"- {x}" for x in v) or "_none_")
                else:
                    st.write(v)
else:
    st.info("Add resumes and a job description in the sidebar, then hit Evaluate.")
