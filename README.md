# 🐍 Python Coding Adventure

A gamified, CodeDex-inspired Streamlit app that teaches Python fundamentals through 5 interactive levels, quizzes, XP progression, and a certificate generator.

---

## ✨ Features

| Feature | Detail |
|---|---|
| 5 Curriculum Levels | Variables → Loops → Lists → Functions → Final Boss |
| XP & Rank System | Earn XP per quiz, rank up from Apprentice → Python Master |
| Milestone Badges | Balloon animations + badge card on level completion |
| Sequential Unlocking | Can't skip ahead — levels gate on completion |
| Certificate Generator | Downloadable HTML certificate with your name + stats |
| CodeDex Aesthetic | Dark theme, Neubrutalism buttons, neon green + deep purple |

---

## 🚀 Local Setup

### 1. Clone or create your repo

```bash
mkdir python-adventure && cd python-adventure
# paste app.py and requirements.txt here
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📦 Deploy to GitHub + Streamlit Cloud

### Step 1 — Push to GitHub

```bash
git init
git add app.py requirements.txt README.md
git commit -m "feat: initial Python Coding Adventure"
gh repo create python-adventure --public --push
# OR manually create a repo on github.com and follow the push instructions
```

Your repo should contain exactly:
```
python-adventure/
├── app.py
├── requirements.txt
└── README.md
```

### Step 2 — Deploy on Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
2. Click **"New app"**.
3. Select your repository (`python-adventure`), branch (`main`), and main file (`app.py`).
4. Click **"Deploy!"** — Streamlit Cloud installs dependencies from `requirements.txt` automatically.
5. Your app gets a public URL like: `https://your-username-python-adventure-app-xxxx.streamlit.app`

> **Note:** Streamlit Cloud free tier supports public repos and gives you 1 GB RAM. This app is well within those limits.

---

## 🏗️ Project Structure

```
app.py               # Single-file Streamlit application
requirements.txt     # Python dependencies
README.md            # This file
```

### Key architecture decisions

- **`st.session_state`** — All state (XP, completed levels, quiz answers) lives here. Streamlit reruns the script on every interaction; session state persists between reruns.
- **Single-file design** — Everything (CSS, data, logic, UI) is in `app.py` for simplicity and portability.
- **Certificate as HTML** — The certificate is a styled HTML file generated with Python's `base64` module (no extra dependencies). Users download and open it in any browser.
- **Neubrutalism CSS** — Injected via `st.markdown(..., unsafe_allow_html=True)` using Google Fonts loaded from CDN.

---

## 🎮 Curriculum Map

```
Level 1 — Variables & Data Types  (50 XP)   🔢
Level 2 — Logic & Loops           (60 XP)   ♾️
Level 3 — Lists & Dictionaries    (70 XP)   📦
Level 4 — Functions               (80 XP)   🪄
Level 5 — The Final Boss          (100 XP)  💀
─────────────────────────────────────────────
                         Total   360 XP max
```

### XP → Rank table

| XP Range | Rank |
|---|---|
| 0 – 49 | 🌱 Apprentice |
| 50 – 119 | 💻 Coder |
| 120 – 199 | 🧙 Wizard |
| 200 – 299 | 🔮 Sorcerer |
| 300+ | 🐍 Python Master |

---

## 🛠️ Customisation Tips

- **Add more levels:** Duplicate a level dict in the `LEVELS` dictionary and increment the key.
- **Change XP rewards:** Edit `"xp_reward"` in each level.
- **Swap quiz questions:** Edit the `"questions"` list in any level.
- **New rank tiers:** Add rows to the `XP_TIERS` list.
- **Change colours:** Update `--neon` and `--purple` CSS variables in `CUSTOM_CSS`.

---

## 📄 License

MIT — feel free to fork, extend, and share.
