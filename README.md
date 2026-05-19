# ◈ QuizVerse — Enhanced Online Quiz System

A feature-rich online quiz application built with **Flask** and **SQLite**, featuring a stunning dark space UI, countdown timers, categories, difficulty levels, and a global leaderboard.

---

## 🚀 Features

| Feature | Details |
|---|---|
| 🎨 **Modern UI** | Dark space theme, glassmorphism cards, smooth animations |
| ⏱️ **Timer** | 20-second countdown per question; auto-submits on timeout |
| 📂 **Categories** | Geography, Science, Mathematics, History, Technology |
| 🎯 **Difficulty** | Easy / Medium / Hard filtering |
| 🏆 **Leaderboard** | Persistent top-20 scores with category filter |
| 📊 **Score Review** | Full answer breakdown after each quiz |
| 🔀 **Randomisation** | Questions and options shuffled each game |
| 📱 **Responsive** | Works on mobile and desktop |

---

## 🛠️ Quick Start

### 1. Local (Python)

```bash
pip install -r requirements.txt
python init_db.py          # seed the database
python app.py              # runs on http://localhost:5000
```

### 2. Docker

```bash
docker build -t quizverse .
docker run -d -p 5000:5000 quizverse
# Open http://localhost:5000
```

### 3. Docker Compose (optional)

```yaml
version: '3.9'
services:
  quiz:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=your-secret-here
    volumes:
      - quiz_data:/app
volumes:
  quiz_data:
```

---

## 📁 Project Structure

```
enhanced_quiz_system/
├── app.py              # Flask routes (home, quiz, result, leaderboard, timeout)
├── init_db.py          # DB seed — 35+ questions across 5 categories
├── requirements.txt    # Pinned dependencies
├── Dockerfile          # Two-stage, non-root build
├── Jenkinsfile         # CI/CD pipeline (build → health-check → deploy)
└── templates/
    ├── base.html       # Shared layout (nav, starfield, fonts, CSS vars)
    ├── index.html      # Landing page — name + category + difficulty selector
    ├── quiz.html       # Quiz page — timer ring, progress bar, option picker
    ├── result.html     # Score gauge, grade badge, full answer review
    └── leaderboard.html # Top 20 with category filter tabs
```

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `quiz-secret-2024-change-in-prod` | Flask session secret |
| `DB_PATH` | `quiz.db` | Path to SQLite database |

---

## 🗄️ Database Schema

**`questions`** — `id, question, opt1, opt2, opt3, opt4, answer, category, difficulty`

**`scores`** — `id, player_name, score, total, percentage, category, difficulty, time_secs, played_at`

---

## 📈 CI/CD (Jenkinsfile)

Stages: **Checkout → Lint → Build Docker Image → Stop Old Container → Deploy → Health Check**

Update `YOUR_GITHUB_REPO_URL` in the Jenkinsfile before use.
