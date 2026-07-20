# 📄 AI Resume Parser & Candidate Ranker

An AI-powered resume screening tool that automatically parses resumes (PDF & DOCX), extracts structured data using LLMs, and ranks candidates against a job description — saving hours of manual HR work.

Built with **Groq API**, **Pydantic**, and **Python 3.11+**.

---

## ✨ Features

- 🔍 **Smart Resume Parsing** — Extracts name, email, phone, skills, experience, education, projects, and certifications from resumes using LLM-powered analysis.
- 📑 **Multi-Format Support** — Reads both `.pdf` and `.docx` resume files.
- 🎯 **Job Description Matching** — Compares each candidate against a target job description and generates a match score (0–100%).
- 📊 **Candidate Ranking** — Automatically sorts candidates by score and highlights the **Top 2** and **Lowest 2** performers.
- 🧠 **Structured Output** — Uses Pydantic models for type-safe, validated data extraction.
- ⚡ **Rate-Limit Friendly** — Built-in delays between API calls to respect rate limits.

---

## 🏗️ How It Works

```
resumes/                     Job Description (hardcoded)
   │                                │
   ▼                                ▼
┌──────────────┐           ┌──────────────────┐
│ Read PDF/DOCX│           │ Parse JD → JobD  │
│ extract text │           │ (Pydantic model) │
└──────┬───────┘           └────────┬─────────┘
       │                            │
       ▼                            │
┌──────────────────┐                │
│ LLM: Parse Resume│                │
│ → Resume model   │                │
└──────┬───────────┘                │
       │                            │
       ▼                            ▼
   ┌──────────────────────────────────┐
   │ LLM: Compare Resume vs Job Desc │
   │ → MatchResult (score + details) │
   └──────────────┬───────────────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ Rank & Display    │
        │ Top 2 / Lowest 2  │
        └───────────────────┘
```

---

## 📁 Project Structure

```
day5/
├── resume_parser.py      # Main script — parsing, matching, ranking
├── main.py               # Entry point (hello world placeholder)
├── resumes/              # Drop your PDF/DOCX resumes here
│   ├── candidate1.pdf
│   ├── candidate2.docx
│   └── ...
├── .env                  # Groq API key (not committed)
├── pyproject.toml        # Project config & dependencies
├── uv.lock               # Lockfile
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **[uv](https://docs.astral.sh/uv/)** (recommended) or pip
- **Groq API Key** — Get one at [console.groq.com](https://console.groq.com)

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/ai-resume-parser.git
cd ai-resume-parser
```

### 2. Set up environment

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install groq pydantic pypdf python-docx python-dotenv
```

### 3. Add your API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Add resumes

Drop your `.pdf` or `.docx` resume files into the `resumes/` folder.

### 5. Run

```bash
uv run resume_parser.py
```

---

## 📋 Sample Output

```
None
['Bachelor's degree in Computer Science, Computer Engineering, ...']

Processing: abhay resume new - Abhay Singh.pdf
Score: 60.0

Processing: anshit verma resume word - Anshit Verma.docx
Score: 35.0

Processing: Ashish Raj 24PCS007 (1) - Ashish Raj.pdf
Score: 52.0

Processing: Resume for Freshers - Priyanshu Singh.docx
Score: 62.0

TOP 2 CANDIDATES
Ashish Raj - 65.0 %
{'matching_skills': ['C++', 'Python', 'AWS', 'Docker', ...], 'verdict': 'Good fit...'}

Priyanshu Singh - 62.0 %
{'matching_skills': ['Java', 'SQL', 'MongoDB', 'React', ...], 'verdict': 'Good foundational...'}

LOWEST 2 CANDIDATES
Abhay Pratap Singh - 60.0 %
...
Anshit Verma - 35.0 %
...
```

> **Note:** Scores may vary between runs since the LLM's output is non-deterministic.

---

## 🧩 Data Models

### `JobD` — Parsed Job Description
| Field | Type |
|---|---|
| `role` | `str` |
| `required_skills` | `list[str]` |
| `preferred_skills` | `list[str]` |
| `minimum_experience` | `float \| None` |
| `education_requirements` | `list[str]` |
| `responsibilities` | `list[str]` |

### `Resume` — Parsed Resume
| Field | Type |
|---|---|
| `name` | `str \| None` |
| `email` | `str \| None` |
| `phone` | `str \| None` |
| `total_experience_years` | `float \| None` |
| `skills` | `list[str]` |
| `experiences` | `list[Experience]` |
| `education` | `list[str]` |
| `projects` | `list[str]` |
| `certifications` | `list[str]` |

### `MatchResult` — Scoring Output
| Field | Type |
|---|---|
| `score` | `float` |
| `details` | `dict` |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Groq](https://groq.com/) | Ultra-fast LLM inference API |
| [Pydantic](https://docs.pydantic.dev/) | Data validation & structured output |
| [PyPDF](https://pypdf.readthedocs.io/) | PDF text extraction |
| [python-docx](https://python-docx.readthedocs.io/) | DOCX text extraction |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment variable management |

---

## ⚠️ Important Notes

- The job description is currently **hardcoded** in `resume_parser.py`. Modify the `job_description` variable to match your target role.
- API calls have **5-second delays** to avoid rate limiting.
- The model used is `openai/gpt-oss-120b` via Groq. You can change this in the `model` variable.
- Make sure your `.env` file is listed in `.gitignore` to avoid leaking your API key.

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ using Groq + Python
</p>
