 # 🔍 Code Review Assistant

An intelligent, interactive **Streamlit app** powered by **Hugging Face** models for automated code analysis and review.  
It helps developers quickly assess **code quality, performance, security, and readability** using AI.

**Demo:** [Watch the Code Review Assistant video](https://drive.google.com/file/d/16bQbK4Xxr8IAKxyq1K9Xhij0aiVj5B68/view?usp=sharing)

---

## 🚀 Features

- **Automatic Code Review** — Upload or paste your code and get a structured review instantly.  
- **AI-Powered Analysis** — Uses the `meta-llama/Llama-3.2-3B-Instruct` model via Hugging Face Inference API.  
- **Multi-Language Support** — Python, JavaScript, TypeScript, Java, C/C++, Go, Rust, Ruby, PHP, JSX/TSX, HTML, CSS  
- **Detailed Evaluation**: Code Quality (0–10), Readability, Best Practices, Bugs, Security, Performance, Modularity  
- **Downloadable Reports** in Markdown  
- **Review History** — Stores your last 10 reviews  
- **Modern Streamlit UI** — Tabs for New Review, History, and Guide

---

## 🧩 Tech Stack

| Component | Technology |
| --- | --- |
| Frontend / UI | Streamlit |
| AI Model | meta-llama/Llama-3.2-3B-Instruct |
| Backend API | Hugging Face Inference API |
| Storage | Streamlit session state (in-memory) |

---

## ⚙️ Installation & Setup

### 1) Clone
```bash
git clone https://github.com/your-username/code-review-assistant.git
cd code-review-assistant
2) Install
pip install streamlit huggingface_hub
3) Configure API Key
Open app.py and set your token:
HF_API_KEY = "your_huggingface_api_key_here"
Create/get a token here: https://huggingface.co/settings/tokens
▶️ Run
streamlit run app.py
App URL: http://localhost:8501
🧭 App Layout
📝 New Review — Upload/paste code, choose language, set focus, analyze
📚 Review History — View, delete, and download previous reports
📖 Guide — Usage, supported languages, troubleshooting
📋 Output Example
# Code Review Summary
**Code Quality Score:** 8/10
**Readability:** Clear, consistent naming
**Best Practices:** Mostly follows conventions
**Potential Bugs:** Edge case on empty input
**Security:** No obvious vulnerabilities
**Performance:** Consider caching heavy calls
**Modularity:** Break large functions into smaller units
**Improvements:** Add docstrings and type hints
💾 Downloads
Each analysis can be saved as:
review_<filename>_<timestamp>.md (includes code, metadata, and full AI review)
🧑‍💻 Notes
Uses Streamlit caching and session state
Handles common errors: model warm-up, invalid token, rate limits
Keeps only the last 10 reviews for performance
🛣️ Roadmap
PDF/HTML report export
Batch/multi-file analysis
GitHub repo integration
Model selector (e.g., Mixtral/GPT variants)
📽️ Demo
Watch the Code Review Assistant video:
https://drive.google.com/file/d/16bQbK4Xxr8IAKxyq1K9Xhij0aiVj5B68/view?usp=sharing
