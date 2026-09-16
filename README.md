# ⛩️ JLPT Mock Test Platform & Telegram Score Reporter

An interactive, full-featured **JLPT (Japanese Language Proficiency Test) Mock Exam System** designed for students and teachers. Students can take online exams on mobile or desktop, view detailed scorecards, and automatically push their scores to your **Telegram Bot**.

---

## ✨ Features

- 🎌 **Official JLPT Levels Supported**: N5, N4, N3, N2, N1 mock exam templates.
- ⏱️ **Exam Mode & Practice Mode**:
  - **Exam Mode**: Official timed countdown, section breakdown, auto-submit on time expiration.
  - **Practice Mode**: Immediate answer validation and vocabulary/grammar explanations.
- 👤 **Student Identification**: Prompts students for Name and Student ID before starting.
- 📊 **Detailed Analytics**: Overall score, Pass/Fail status (合格 / 不合格), and percentage breakdown per section (Vocabulary, Grammar, Reading).
- 📲 **Telegram Bot Integration**: Automatically pushes student score reports to your Telegram chat or group.
- 📄 **PDF Question Converter**: Includes a script to extract questions from your PDFs into clean JSON test files.
- 🚀 **100% Free Vercel Hosting Ready**: Serverless API route keeps your Telegram Bot Token hidden securely on the server.

---

## 🚀 Quick Start (Run Locally)

You can run and test the complete system on your computer right away:

1. Open your terminal in this directory.
2. Run the local Python server:
   ```bash
   python server.py
   ```
3. Open your browser and navigate to:
   ```text
   http://localhost:8000
   ```

---

## 🤖 Setting Up Telegram Bot Alerts

1. **Create a Telegram Bot**:
   - Open Telegram and search for `@BotFather`.
   - Send `/newbot` and follow the prompts to create your bot.
   - Copy your **Bot Token** (e.g. `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).

2. **Get Your Telegram Chat ID**:
   - Open Telegram and search for `@userinfobot` or add your new bot to your Telegram group.
   - Copy your **Chat ID** (e.g. `987654321` or group ID `-100123456789`).

3. **Configure Credentials in App**:
   - Open the web app -> Click the **Telegram Icon (Paper Plane)** in the top right header.
   - Paste your **Bot Token** and **Chat ID** -> Click **Test Connection** -> Click **Save Credentials**.

---

## 📄 Converting Your PDFs to Test JSON

Use the included PDF parser script to convert your test PDFs into quiz JSON datasets:

```bash
python scripts/parse_pdf.py --pdf my_n4_test.pdf --output data/sample_n4.json --level N4 --title "JLPT N4 Mock Test 01"
```

You can also directly create or edit JSON files inside the `data/` folder following the `sample_n5.json` format.

---

## 🌐 Deploying to Vercel (Free Online Link for Students)

To give students a permanent public link (`https://your-jlpt-test.vercel.app`):

### Method A: Deploy via GitHub (Recommended)
1. Push this folder to a GitHub repository.
2. Go to [Vercel.com](https://vercel.com) and log in.
3. Click **Add New Project** -> Select your GitHub repository.
4. Add Environment Variables (Optional for extra security):
   - `TELEGRAM_BOT_TOKEN` = `your_bot_token`
   - `TELEGRAM_CHAT_ID` = `your_chat_id`
5. Click **Deploy**. Vercel will give you a live shareable HTTPS link!

### Method B: Deploy via Vercel CLI
```bash
npm i -g vercel
vercel
```

---

## 📁 File Structure

```text
├── index.html            # Main User Interface
├── styles.css            # Responsive Dark/Light Japanese Design System
├── app.js                # Quiz runner, timer, scoring, Telegram client
├── server.py             # Local dev server with Telegram proxy
├── vercel.json           # Vercel deployment configuration
├── api/
│   └── send-score.js     # Secure Vercel Serverless function for Telegram
├── data/
│   ├── sample_n5.json    # N5 Mock Test Dataset
│   └── sample_n3.json    # N3 Mock Test Dataset
└── scripts/
    └── parse_pdf.py      # PDF text extractor tool
```
