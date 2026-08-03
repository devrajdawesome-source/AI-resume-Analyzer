# 📄 AI Resume & ATS Analyzer

A full-stack, domain-agnostic **ATS (Applicant Tracking System) Resume Analyzer** built with **Django REST Framework**, **Tailwind CSS**, **Google Gemini AI**, and **JWT Authentication**.

This application allows job seekers from any industry (Software Engineering, Marketing, Finance, Healthcare, HR, etc.) to upload their PDF resume alongside a target Job Description to receive an instant ATS match score, extracted matching & missing skill keywords, and actionable AI recommendations to optimize their resume.

---

## 🌟 Key Features

* **🤖 Universal Gemini AI Integration:** Evaluates candidate suitability and relevance across any job domain using LLM-based semantic reasoning rather than hardcoded skill dictionaries.
* **🔐 JWT Authentication & Guest Mode:** Users can create an account and log in securely via JSON Web Tokens (`simplejwt`) to save personal history, or test the app instantly in **Guest Mode**.
* **📄 In-Memory PDF Processing:** Uses `pypdf` to parse and extract text directly from uploaded PDF files in memory without storing raw files on disk.
* **📊 ATS Match Scoring:** Computes an intuitive suitability score (0–100%) along with extracted key qualification tags.
* **💡 Actionable AI Advice:** Generates tailored bullet-point suggestions explaining specific improvements needed to increase match likelihood for a target role.
* **📜 User-Specific Database History:** Persists past evaluation runs to SQLite/PostgreSQL with Foreign Key links to authenticated users.
* **🎨 Modern Responsive UI:** Built with clean Tailwind CSS featuring tab navigation, modal login/register popups, dark-mode styling, loading spinners, and skill badges.

---

## 🛠️ Tech Stack

* **Backend:** Python 3, Django, Django REST Framework, Django SimpleJWT, `pypdf`
* **AI Engine:** Google Gemini API (`google-genai` SDK)
* **Frontend:** HTML5, Tailwind CSS (via CDN), Vanilla JavaScript (`fetch` API, `localStorage`)
* **Database:** SQLite (Development / Ephemeral Cloud)
* **Production Deployment:** Gunicorn, Render, GitHub CI/CD

---

## 🚀 Live Demo

* **Live Web Application:** [https://ai-resume-analyzer.onrender.com](https://ai-resume-analyzer.onrender.com)
* **GitHub Repository:** [https://github.com/devrajdawesome-source/AI-resume-Analyzer](https://github.com/devrajdawesome-source/AI-resume-Analyzer)

---

## 🔑 Authentication Architecture

The application implements **Stateless JWT (JSON Web Token)** authentication:
1. User registers via `/api/register/` or logs in via `/api/token/`.
2. The server returns an `access_token` and `refresh_token`.
3. The frontend stores `access_token` in `localStorage` and attaches it to request headers (`Authorization: Bearer <token>`).
4. Django REST Framework automatically decodes the token and attaches `request.user` to isolate analysis history per user.

---

## 💻 Local Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/devrajdawesome-source/AI-resume-Analyzer.git](https://github.com/devrajdawesome-source/AI-resume-Analyzer.git)
cd AI-resume-Analyzer
