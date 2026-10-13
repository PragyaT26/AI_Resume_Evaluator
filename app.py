import time

import streamlit as st

st.set_page_config(page_title="AI Resume Evaluator", page_icon="📄", layout="wide")

try:
    import resume_parser as rp
except ValueError:
    st.error("GROQ_API_KEY missing. Put it in a `.env` file next to app.py and restart.")
    st.stop()

st.markdown("""
<style>
.hero{padding:28px 32px;border-radius:18px;margin-bottom:18px;color:#fff;
background:linear-gradient(120deg,#6d28d9,#db2777 60%,#f59e0b)}
.hero h1{margin:0;font-size:2.1rem}.hero p{margin:6px 0 0;opacity:.9}
.card{background:#1a1b36;border:1px solid #2c2e57;border-radius:16px;padding:16px 20px;margin-bottom:12px}
.card .rank{font-size:1.6rem;margin-right:10px}
.badge{display:inline-block;padding:3px 12px;border-radius:999px;font-weight:700;color:#fff}
.chip{display:inline-block;padding:3px 10px;margin:3px 4px 3px 0;border-radius:999px;font-size:.82rem}
.ok{background:#14532d;color:#bbf7d0}.bad{background:#7f1d1d;color:#fecaca}
.bar{height:8px;border-radius:99px;background:#2c2e57;margin-top:10px}.bar>div{height:8px;border-radius:99px}
[data-testid=stMetric]{background:#1a1b36;border:1px solid #2c2e57;border-radius:14px;padding:12px 16px}
</style>
<div class="hero"><h1>📄 AI Resume Evaluator</h1>
<p>Upload resumes, paste a job description, get a ranked shortlist in minutes.</p></div>
""", unsafe_allow_html=True)

def color(score):
    return "#22c55e" if score >= 70 else "#f59e0b" if score >= 50 else "#ef4444"

def chips(items, cls):
    return "".join(f'<span class="chip {cls}">{x}</span>' for x in items) or "<i>none</i>"

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
    scores = [r["score"] for r in results]
    c1, c2, c3 = st.columns(3)
    c1.metric("Candidates", len(results))
    c2.metric("Top score", f"{max(scores):.0f}%")
    c3.metric("Average", f"{sum(scores) / len(scores):.0f}%")
    st.subheader("Ranking")
    medals = ["🥇", "🥈", "🥉"]
    for i, r in enumerate(results):
        col, d = color(r["score"]), r["details"]
        st.markdown(
            f'''<div class="card"><span class="rank">{medals[i] if i < 3 else i + 1}</span>
            <b style="font-size:1.15rem">{r["name"]}</b>
            <span class="badge" style="background:{col};float:right">{r["score"]:.0f}%</span>
            <div style="opacity:.6;font-size:.8rem">{r["file"]}</div>
            <div class="bar"><div style="width:{r["score"]}%;background:{col}"></div></div></div>''',
            unsafe_allow_html=True,
        )
        with st.expander("Details"):
            if d.get("verdict"):
                st.info(d["verdict"])
            st.markdown("**✅ Matching skills**", help=None)
            st.markdown(chips(d.get("matching_skills", []), "ok"), unsafe_allow_html=True)
            st.markdown("**❌ Missing skills**")
            st.markdown(chips(d.get("missing_important_skills", []), "bad"), unsafe_allow_html=True)
            st.markdown(f"**Experience requirement met:** {d.get('experience_requirement_met', 'n/a')}")
else:
    st.info("Add resumes and a job description in the sidebar, then hit Evaluate.")
