# ⛩️ Momin's JLPT Mock Test Platform — AI Agent Handover & Context Guide

> **Note for AI Assistant:** This document provides full contextual memory of this repository, its architecture, datasets, Telegram integration, and Vercel 24/7 hosting workflow. Read this file to instantly resume development or support the user.

---

## 📌 1. Project Overview & Repository
- **GitHub Repository:** [https://github.com/noerror-web/momin-jlpt-mock.git](https://github.com/noerror-web/momin-jlpt-mock.git)
- **Application Type:** JLPT Online Mock Examination System (N5, N4, N3, N2, N1) with timed exam mode, practice mode, instant explanation popups, and automated teacher notifications via Telegram.
- **Tech Stack:**
  - **Frontend:** HTML5, Vanilla JavaScript (`app.js`), Modern Responsive Dark CSS (`styles.css`).
  - **Backend / Serverless:** Vercel Node.js Serverless Function (`api/send-score.js`).
  - **Dataset Generators:** Python scripts (`build_full_n5_dataset.py`, `build_n5_mock_test_2.py`, `build_particle_furigana_dataset.py`).
  - **Local Development Server:** Python standard library server (`server.py`).

---

## 📂 2. Directory & File Structure
```text
momin-jlpt-mock/
├── index.html                     # Main application UI & student registration
├── styles.css                     # Modern dark-theme Japanese aesthetic styles
├── app.js                         # Exam runner, timer, scoring engine & Telegram API client
├── server.py                      # Local dev server & Telegram proxy
├── vercel.json                    # Vercel deployment configuration
├── PROJECT_AI_INSTRUCTIONS.md     # AI context handover document (this file)
├── api/
│   └── send-score.js              # Serverless API endpoint forwarding scores to Telegram
├── data/
│   ├── n5_mock_test_2.json        # Official JLPT N5 Mock Exam Set 2 (PDF extracted)
│   ├── n5_particles_furigana.json # N5 Particle Special Exam with HTML Furigana ruby tags
│   └── n5_practice_set_9.json     # Full JLPT N5 Practice Dataset
└── scripts/
    └── parse_pdf.py               # Tool for converting PDF test papers into JSON
```

---

## 🌐 3. Vercel 24/7 Online Deployment & Telegram Integration

### How Vercel Deployment Works:
1. **GitHub Continuous Deployment:** The repo is linked to Vercel (`noerror-web/momin-jlpt-mock`). Every push to `master` automatically triggers a live deployment.
2. **Serverless Endpoint:** `/api/send-score` forwards student exam reports securely to Telegram without exposing bot tokens to students.
3. **Environment Variables on Vercel:**
   - `TELEGRAM_BOT_TOKEN`: Token from Telegram's `@BotFather`.
   - `TELEGRAM_CHAT_ID`: Teacher's Telegram Chat ID or Group ID.

---

## 🤖 4. Instructions for AI Assistant (Post-PC Reset / New Session)

When a user starts a new conversation after restoring or cloning this workspace:
1. **Verify Workspace State:** Run `git status` to ensure working directory is clean and up to date with `origin/master`.
2. **Inspect Datasets:** Check files in `data/` to verify available mock tests.
3. **Check Deployments / Endpoints:** Ensure `app.js` and `api/send-score.js` routes are intact.
4. **Prompt the User:** Ask the user if they want to create new test datasets, refine existing questions, update UI styles, or check Vercel 24/7 hosting status.
