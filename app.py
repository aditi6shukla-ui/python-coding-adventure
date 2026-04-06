import streamlit as st
import hashlib
import base64
import random
import json
import os
import sys
import io
from datetime import datetime, date

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Python Coding Adventure",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PERSISTENT STORAGE  (JSON file — survives server restarts)
# ============================================================
USERS_FILE = "python_adventure_users.json"

def _load_raw() -> dict:
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"users": {}, "progress": {}}

def _save_raw(data: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── cache in st module-level dict so we don't hit disk every rerun ──
if "_DB_CACHE" not in st.__dict__:
    st._DB_CACHE = _load_raw()

def get_db() -> dict:
    return st._DB_CACHE

def flush_db():
    _save_raw(st._DB_CACHE)


# ============================================================
# CUSTOM CSS
# ============================================================
CUSTOM_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Press+Start+2P&family=DM+Sans:wght@400;500;700&display=swap');

  :root {
    --neon:    #00FF41;
    --purple:  #6200EE;
    --purple2: #9D46FF;
    --bg:      #0D0D0D;
    --card:    #181818;
    --card2:   #1F1F1F;
    --border:  #2A2A2A;
    --text:    #E8E8E8;
    --muted:   #888;
    --shadow:        4px 4px 0px #000;
    --shadow-neon:   4px 4px 0px #00FF41;
    --shadow-purple: 4px 4px 0px #6200EE;
    --radius:  8px;
  }

  .stApp { background: var(--bg) !important; font-family: 'DM Sans', sans-serif; color: var(--text); }
  .block-container { padding: 1.5rem 2rem !important; max-width: 1100px; }
  #MainMenu, footer, header { visibility: hidden; }
  .stDeployButton { display: none; }

  [data-testid="stSidebar"] { background: #0A0A0A !important; border-right: 2px solid var(--border); }
  [data-testid="stSidebar"] .block-container { padding: 1rem !important; }

  h1, h2, h3 { font-family: 'Space Mono', monospace !important; }
  .pixel-font { font-family: 'Press Start 2P', monospace !important; }

  .stButton > button {
    background: var(--neon) !important; color: #000 !important;
    font-family: 'Space Mono', monospace !important; font-weight: 700 !important;
    font-size: 0.85rem !important; border: 2px solid #000 !important;
    border-radius: var(--radius) !important; box-shadow: var(--shadow) !important;
    padding: 0.6rem 1.4rem !important; transition: all 0.1s ease !important; letter-spacing: 0.04em;
  }
  .stButton > button:hover  { transform: translate(-2px,-2px) !important; box-shadow: 6px 6px 0px #000 !important; }
  .stButton > button:active { transform: translate(2px,2px)   !important; box-shadow: 2px 2px 0px #000 !important; }
  .stButton > button:disabled { background: #333 !important; color: #666 !important; box-shadow: none !important; }

  .stRadio > label { color: var(--text) !important; }
  .stRadio [data-testid="stMarkdownContainer"] p { color: var(--text) !important; }

  .card        { background:var(--card);  border:2px solid var(--border); border-radius:var(--radius); padding:1.5rem; box-shadow:var(--shadow);        margin-bottom:1rem; }
  .card-purple { background:var(--card);  border:2px solid var(--purple); border-radius:var(--radius); padding:1.5rem; box-shadow:var(--shadow-purple);  margin-bottom:1rem; }
  .card-neon   { background:var(--card);  border:2px solid var(--neon);   border-radius:var(--radius); padding:1.5rem; box-shadow:var(--shadow-neon);    margin-bottom:1rem; }

  .stProgress > div > div { background: var(--neon) !important; }
  .stProgress { filter: drop-shadow(0 0 6px var(--neon)); }

  .xp-badge {
    display:inline-block; background:var(--purple); color:#fff;
    font-family:'Space Mono',monospace; font-size:0.7rem; font-weight:700;
    padding:0.3rem 0.8rem; border:2px solid #000; border-radius:4px; box-shadow:2px 2px 0 #000;
  }

  .milestone {
    background:linear-gradient(135deg,#6200EE,#9D46FF);
    border:3px solid var(--neon); border-radius:12px; padding:1.5rem;
    text-align:center; box-shadow:0 0 30px rgba(0,255,65,0.3),6px 6px 0 #000; margin:1rem 0;
  }

  .info-box {
    background:rgba(98,0,238,0.12); border-left:4px solid var(--purple2);
    border-radius:0 var(--radius) var(--radius) 0; padding:0.9rem 1.2rem; margin:0.8rem 0; font-size:0.92rem;
  }
  .success-box {
    background:rgba(0,255,65,0.08); border-left:4px solid var(--neon);
    border-radius:0 var(--radius) var(--radius) 0; padding:0.9rem 1.2rem; margin:0.8rem 0; font-size:0.92rem; color:var(--neon);
  }
  .locked-box {
    background:rgba(255,100,0,0.08); border:2px dashed #FF6400;
    border-radius:var(--radius); padding:1rem 1.2rem; text-align:center; color:#FF6400;
  }
  .stat-row {
    display:flex; justify-content:space-between; align-items:center;
    padding:0.5rem 0; border-bottom:1px solid var(--border);
    font-family:'Space Mono',monospace; font-size:0.78rem;
  }
  .divider { border:none; border-top:2px solid var(--border); margin:1.5rem 0; }
  .neon-heading { color:var(--neon); text-shadow:0 0 12px rgba(0,255,65,0.5); font-family:'Space Mono',monospace; }
  .chapter-section { background:#111; border:1px solid #2A2A2A; border-radius:8px; padding:1.2rem 1.4rem; margin:0.8rem 0; }
  .chapter-title { font-family:'Space Mono',monospace; font-size:0.9rem; color:#9D46FF; margin-bottom:0.5rem; font-weight:700; }

  .stTextInput > div > div > input {
    background:var(--card) !important; border:2px solid var(--border) !important;
    color:var(--text) !important; border-radius:var(--radius) !important;
    font-family:'Space Mono',monospace !important;
  }
  .stTextInput > div > div > input:focus { border-color:var(--neon) !important; box-shadow:0 0 0 1px var(--neon) !important; }
  .stTextInput > label { color:var(--muted) !important; font-family:'Space Mono',monospace !important; font-size:0.78rem !important; }

  .stTabs [data-baseweb="tab-list"] { background:transparent; gap:0.5rem; }
  .stTabs [data-baseweb="tab"] {
    background:var(--card2) !important; border:2px solid var(--border) !important;
    border-radius:var(--radius) !important; color:var(--muted) !important;
    font-family:'Space Mono',monospace !important; font-size:0.78rem !important;
  }
  .stTabs [aria-selected="true"] { background:var(--purple) !important; border-color:var(--purple) !important; color:#fff !important; }
  .stTabs [data-baseweb="tab-panel"] { background:transparent !important; padding:1rem 0 !important; }

  .stSelectbox > div > div { background:var(--card) !important; border:2px solid var(--border) !important; color:var(--text) !important; border-radius:var(--radius) !important; }
  .stCodeBlock, pre, code { font-family:'Space Mono',monospace !important; background:#111 !important; border:1px solid #2A2A2A !important; border-radius:var(--radius) !important; }

  .pass-badge { color:#00FF41; font-family:'Space Mono',monospace; font-size:0.8rem; }
  .fail-badge { color:#FF4444; font-family:'Space Mono',monospace; font-size:0.8rem; }

  /* ── Practice Lab Panel ── */
  .lab-panel {
    background: #0C0C0C;
    border: 1.5px solid #1E3A2F;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 40px rgba(0,255,65,0.08), 6px 6px 0 #000;
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 600px;
  }
  .lab-header {
    background: linear-gradient(135deg, #0D1F17, #111A14);
    border-bottom: 1.5px solid #1E3A2F;
    padding: 0.75rem 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }
  .lab-header-dot {
    width: 10px; height: 10px; border-radius: 50%;
    display: inline-block;
  }
  .lab-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #00FF41;
    letter-spacing: 0.18em;
    text-shadow: 0 0 8px rgba(0,255,65,0.5);
    margin-left: 0.3rem;
  }
  .lab-filename {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #3A5A47;
    margin-left: auto;
  }
  .lab-editor-wrap {
    padding: 0.6rem 0.8rem 0 0.8rem;
    flex: 1;
  }
  .lab-editor-wrap .stTextArea textarea {
    background: #080E0A !important;
    border: 1.5px solid #1A3028 !important;
    border-radius: 8px !important;
    color: #A8FFB8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    line-height: 1.6 !important;
    caret-color: #00FF41;
    resize: none !important;
  }
  .lab-editor-wrap .stTextArea textarea:focus {
    border-color: #00FF41 !important;
    box-shadow: 0 0 0 2px rgba(0,255,65,0.15) !important;
  }
  .lab-editor-wrap .stTextArea label { display: none !important; }
  .lab-run-wrap {
    padding: 0.6rem 0.8rem;
  }
  .lab-run-wrap .stButton > button {
    background: linear-gradient(135deg, #00C936, #00FF41) !important;
    color: #000 !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.1em !important;
    border: 2px solid #000 !important;
    border-radius: 8px !important;
    box-shadow: 0 0 16px rgba(0,255,65,0.35), 3px 3px 0 #000 !important;
    padding: 0.65rem !important;
    width: 100% !important;
    transition: all 0.1s ease !important;
  }
  .lab-run-wrap .stButton > button:hover {
    transform: translate(-1px,-1px) !important;
    box-shadow: 0 0 24px rgba(0,255,65,0.5), 5px 5px 0 #000 !important;
  }
  .lab-console-wrap {
    padding: 0 0.8rem 0.8rem 0.8rem;
  }
  .lab-console-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #2A5C40;
    letter-spacing: 0.2em;
    margin-bottom: 0.35rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }
  .lab-console {
    background: #060D09;
    border: 1px solid #132B1E;
    border-radius: 6px;
    padding: 0.7rem 0.9rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #00FF41;
    white-space: pre-wrap;
    word-break: break-all;
    min-height: 90px;
    max-height: 180px;
    overflow-y: auto;
    line-height: 1.5;
  }
  .lab-console-idle {
    color: #1E4030;
    font-style: italic;
  }
  .lab-console-error {
    color: #FF6666;
  }

  .boss-box {
    background: linear-gradient(135deg, rgba(255,68,68,0.15), rgba(255,100,0,0.1));
    border: 2px solid #FF4444; border-radius: var(--radius); padding: 1.5rem;
    box-shadow: 0 0 20px rgba(255,68,68,0.25), 4px 4px 0 #000; margin: 1rem 0;
  }
  .leaderboard-row {
    display: flex; align-items: center; gap: 0.8rem;
    padding: 0.55rem 0.8rem; border-bottom: 1px solid var(--border);
    font-family: 'Space Mono', monospace; font-size: 0.76rem;
  }
  .leaderboard-row:last-child { border-bottom: none; }
  .streak-badge {
    display: inline-block; background: rgba(255,160,0,0.15);
    border: 2px solid #FFA000; border-radius: 6px;
    padding: 0.25rem 0.7rem; font-family: 'Space Mono', monospace;
    font-size: 0.72rem; color: #FFA000; box-shadow: 2px 2px 0 #000;
  }
  .stTextArea textarea {
    background: #111 !important; border: 2px solid var(--border) !important;
    color: var(--text) !important; border-radius: var(--radius) !important;
    font-family: 'Space Mono', monospace !important; font-size: 0.82rem !important;
  }
  .stTextArea textarea:focus { border-color: var(--neon) !important; box-shadow: 0 0 0 1px var(--neon) !important; }
  .stTextArea label { color: var(--muted) !important; font-family: 'Space Mono', monospace !important; font-size: 0.78rem !important; }
  .output-box {
    background: #0A0A0A; border: 1px solid #2A2A2A; border-radius: var(--radius);
    padding: 0.8rem 1rem; font-family: 'Space Mono', monospace; font-size: 0.78rem;
    color: #00FF41; white-space: pre-wrap; word-break: break-all; max-height: 260px; overflow-y: auto;
  }
  .error-output { color: #FF6666; }
</style>
"""

# ============================================================
# CURRICULUM DATA  — 5 levels, 20 questions each
# ============================================================
LEVELS = {
    1: {
        "title": "Variables & Data Types", "subtitle": "The Foundation",
        "icon": "🧱", "pixel_art": "🔢", "color": "#00FF41", "xp_reward": 100,
        "description": """
## 🧱 Chapter 1 — Variables & Data Types

Variables are **named containers** that hold data. Think of them as labeled boxes in your inventory. Python uses **dynamic typing** — you never need to declare the type; Python infers it automatically.

---

### 📦 Declaring Variables
```python
name = "Alex"       # assign with =
level = 1
xp = 0
name = "Jordan"     # reassign anytime
x = y = z = 0       # multiple assignment
a, b, c = 1, 2, 3   # tuple unpacking
```

**Naming Rules:**
- Must start with a letter or underscore `_`
- Can contain letters, digits, underscores
- Case-sensitive (`score` ≠ `Score`)
- Cannot use reserved keywords (`if`, `for`, `class`, etc.)
- Convention: use `snake_case` for variables

---

### 🔢 Core Data Types

| Type | Example | Description |
|------|---------|-------------|
| `int` | `42`, `-7`, `0` | Whole numbers |
| `float` | `3.14`, `-0.5` | Decimal numbers |
| `str` | `"Hello"`, `'World'` | Text (immutable) |
| `bool` | `True`, `False` | Truth values |
| `NoneType` | `None` | Absence of a value |

---

### 🔄 Type Conversion
```python
int("42")      # → 42
float("3.14")  # → 3.14
str(100)       # → "100"
bool(0)        # → False   (0, "", [], None are all False)
bool("hi")     # → True    (non-empty = True)
```

---

### ✏️ String Operations
```python
name = "python"
name.upper()         # "PYTHON"
name.capitalize()    # "Python"
name.replace("p","P")# "Python"
name.split("t")      # ["py", "hon"]
len(name)            # 6
name[0]              # "p"  (indexing)
name[-1]             # "n"  (negative index)
name[0:3]            # "pyt" (slicing)

# f-strings (best way to embed variables)
score = 95
msg = f"Player scored {score} points!"
msg2 = f"Double: {score * 2}"
```

---

### ➗ Arithmetic Operators
```python
10 + 3   # 13  (addition)
10 - 3   # 7   (subtraction)
10 * 3   # 30  (multiplication)
10 / 3   # 3.333... (float division)
10 // 3  # 3   (floor/integer division)
10 % 3   # 1   (modulo — remainder)
2 ** 10  # 1024 (exponentiation)
```

---

### 🔍 Checking Types
```python
type(42)        # <class 'int'>
type("hello")   # <class 'str'>
type(3.14)      # <class 'float'>
type(True)      # <class 'bool'>
type(None)      # <class 'NoneType'>

isinstance(42, int)    # True
isinstance("hi", str)  # True
```

---

> 💡 **Pro Tip:** Use `SCREAMING_SNAKE_CASE` for constants: `MAX_HEALTH = 100`
        """,
        "code_example": '''# 🐍 Variables & Data Types — Full Demo

# Basic assignment
name = "Alex"
level = 1
xp_multiplier = 1.5
is_hero = True
lives = None

print(f"Player: {name}")
print(f"Level:  {level}")
print(f"XP Mult:{xp_multiplier}")
print(f"Hero?   {is_hero}")
print(f"Lives:  {lives}")

# Type inspection
print(f"\\nType checks:")
print(f"  type(level):         {type(level)}")
print(f"  type(xp_multiplier): {type(xp_multiplier)}")
print(f"  isinstance(name,str):{isinstance(name, str)}")

# Type conversion
score_str = "250"
score_int = int(score_str)
print(f"\\nConverted score: {score_int}")
print(f"Doubled:         {score_int * 2}")
print(f"As float:        {float(score_str)}")

# String operations
tag = "python_master"
print(f"\\nString ops:")
print(f"  Upper:   {tag.upper()}")
print(f"  Length:  {len(tag)}")
print(f"  Slice:   {tag[0:6]}")
print(f"  Replace: {tag.replace('_',' ').title()}")

# Arithmetic
print(f"\\nArithmetic:")
print(f"  7 // 2 = {7 // 2}   (floor div)")
print(f"  7 %  2 = {7 %  2}   (remainder)")
print(f"  2**8   = {2**8}   (power)")

# Multiple assignment
x, y, z = 10, 20, 30
x, y = y, x          # swap!
print(f"\\nAfter swap: x={x}, y={y}")
''',
        "questions": [
            {"q": "What data type is the value `3.14` in Python?",
             "options": ["int", "float", "str", "bool"], "answer": "float"},
            {"q": "Which of the following is a valid Python variable name?",
             "options": ["2nd_player", "player-name", "player_name", "class"], "answer": "player_name"},
            {"q": "What does `type('Hello')` return?",
             "options": ["<class 'str'>", "<class 'int'>", "str", "String"], "answer": "<class 'str'>"},
            {"q": "What is the result of `int('42')`?",
             "options": ["'42'", "42.0", "42", "Error"], "answer": "42"},
            {"q": "What does `bool(0)` return?",
             "options": ["True", "False", "None", "0"], "answer": "False"},
            {"q": "Which of these is NOT a valid variable name?",
             "options": ["_score", "score1", "my_score", "2score"], "answer": "2score"},
            {"q": "What does `len('Python')` return?",
             "options": ["5", "6", "7", "Error"], "answer": "6"},
            {"q": "What is `'Hello' + ' ' + 'World'`?",
             "options": ["Hello World", "'Hello World'", "HelloWorld", "Error"], "answer": "Hello World"},
            {"q": "What is the result of `7 // 2`?",
             "options": ["3.5", "4", "3", "2"], "answer": "3"},
            {"q": "What is `10 % 3`?",
             "options": ["3", "1", "0", "2"], "answer": "1"},
            {"q": "What does `str(100)` return?",
             "options": ["100", "'100'", "int", "Error"], "answer": "'100'"},
            {"q": "What is `type(None)`?",
             "options": ["<class 'NoneType'>", "<class 'null'>", "<class 'none'>", "None"], "answer": "<class 'NoneType'>"},
            {"q": "What is `2 ** 10`?",
             "options": ["20", "512", "1024", "100"], "answer": "1024"},
            {"q": "What does `bool('hello')` return?",
             "options": ["False", "True", "None", "Error"], "answer": "True"},
            {"q": "What is `'Python'[0]`?",
             "options": ["'P'", "'y'", "'Python'", "Error"], "answer": "'P'"},
            {"q": "After `x = 5; x += 3`, what is `x`?",
             "options": ["5", "3", "8", "15"], "answer": "8"},
            {"q": "What is `f'{3 + 4}'`?",
             "options": ["7", "'7'", "3 + 4", "Error"], "answer": "'7'"},
            {"q": "Which method converts a string to uppercase?",
             "options": [".upper()", ".toUpper()", ".capitalize()", ".UPPER()"], "answer": ".upper()"},
            {"q": "What is `'Python'[-1]`?",
             "options": ["'P'", "'n'", "'o'", "Error"], "answer": "'n'"},
            {"q": "What is `isinstance(42, int)`?",
             "options": ["True", "False", "42", "Error"], "answer": "True"},
        ],
    },
    2: {
        "title": "Logic & Loops", "subtitle": "The Path",
        "icon": "🔀", "pixel_art": "♾️", "color": "#9D46FF", "xp_reward": 120,
        "description": """
## 🔀 Chapter 2 — Logic & Loops

Control flow lets your program **make decisions** and **repeat actions**. These are the building blocks of all logic in programming.

---

### ⚖️ Comparison Operators
```python
5 == 5     # True  (equal)
5 != 3     # True  (not equal)
5 > 3      # True  (greater than)
5 < 3      # False (less than)
5 >= 5     # True  (greater or equal)
5 <= 4     # False (less or equal)
5 == 5.0   # True  (int == float is OK)
"a" < "b"  # True  (alphabetical order)
```

---

### 🔗 Logical Operators
```python
True and True   # True  (both must be True)
True and False  # False
True or False   # True  (at least one True)
False or False  # False
not True        # False
not False       # True

# Short-circuit evaluation
x = 5
x > 0 and x < 10   # True (both checks pass)
x < 0 or x > 3     # True (second is True)
```

---

### 🌿 if / elif / else
```python
score = 85

if score >= 90:
    grade = "S-Rank"
elif score >= 70:
    grade = "A-Rank"
elif score >= 50:
    grade = "B-Rank"
else:
    grade = "Try Again"

print(grade)   # A-Rank

# Ternary (one-liner if)
label = "Pass" if score >= 60 else "Fail"
```

**Nesting conditionals:**
```python
if hp > 0:
    if mana > 10:
        print("Cast spell!")
    else:
        print("Not enough mana.")
else:
    print("You are defeated!")
```

---

### 🔁 for Loops
```python
# Basic range
for i in range(5):        # 0,1,2,3,4
    print(i)

for i in range(1, 6):     # 1,2,3,4,5
    print(i)

for i in range(0, 10, 2): # 0,2,4,6,8 (step 2)
    print(i)

# Iterating a list
items = ["sword", "shield", "potion"]
for item in items:
    print(item)

# enumerate — get index AND value
for idx, item in enumerate(items):
    print(f"{idx}: {item}")

# zip — iterate two lists together
names  = ["Alex", "Sam"]
scores = [90, 75]
for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

---

### 🔄 while Loops
```python
health = 100
rounds = 0

while health > 0:
    health -= 25
    rounds += 1
    print(f"Round {rounds}, HP: {health}")

print("Defeated!")

# Infinite loop with break
attempts = 0
while True:
    attempts += 1
    if attempts >= 3:
        break       # exit the loop
print(f"Broke after {attempts} attempts")
```

---

### ⏭️ break / continue / pass
```python
# break — stop the loop entirely
for i in range(10):
    if i == 5:
        break
    print(i)   # prints 0-4

# continue — skip this iteration, keep going
for i in range(5):
    if i == 2:
        continue
    print(i)   # prints 0,1,3,4

# pass — do nothing (placeholder)
for i in range(3):
    pass   # valid empty loop
```

---

### 🧠 List Comprehensions (compact loops)
```python
squares   = [x**2 for x in range(6)]      # [0,1,4,9,16,25]
evens     = [x for x in range(10) if x%2==0]  # [0,2,4,6,8]
upper_items = [s.upper() for s in ["a","b","c"]]
```

---

> 💡 **Pro Tip:** Use `for` when you know the number of iterations; use `while` when waiting for a condition.
        """,
        "code_example": '''# 🔀 Logic & Loops — Full Demo

# Conditional logic
score = 85
if score >= 90:
    grade = "S-Rank ⭐"
elif score >= 70:
    grade = "A-Rank 🔥"
elif score >= 50:
    grade = "B-Rank 👍"
else:
    grade = "Keep Trying 💪"
print(f"Score {score} → {grade}")

# Ternary
label = "PASS" if score >= 60 else "FAIL"
print(f"Result: {label}")

# for loop with range
print("\\nCounting up:")
for i in range(1, 6):
    print(f"  {i}", end=" ")

# enumerate
print("\\n\\nInventory:")
items = ["🗡️ Sword","🛡️ Shield","🧪 Potion"]
for idx, item in enumerate(items, start=1):
    print(f"  Slot {idx}: {item}")

# zip
print("\\nParty stats:")
names  = ["Alex","Sam","Jordan"]
hp_vals = [120, 95, 80]
for hero, hp in zip(names, hp_vals):
    bar = "█" * (hp // 20)
    print(f"  {hero:8s} {bar} {hp}")

# while with break
print("\\nBoss fight:")
boss_hp = 100
turn = 0
while boss_hp > 0:
    damage = 35
    boss_hp -= damage
    turn += 1
    print(f"  Turn {turn}: dealt {damage} dmg, boss HP={max(boss_hp,0)}")
    if turn >= 5:
        break

# continue
print("\\nEven items only:")
for i in range(10):
    if i % 2 != 0:
        continue
    print(f"  {i}", end=" ")

# List comprehension
print("\\n\\nSquares: ", [x**2 for x in range(6)])
print("Evens:   ", [x for x in range(10) if x % 2 == 0])
''',
        "questions": [
            {"q": "What does `range(0, 5)` produce?",
             "options": ["0,1,2,3,4,5", "0,1,2,3,4", "1,2,3,4,5", "1,2,3,4"], "answer": "0,1,2,3,4"},
            {"q": "Which keyword exits a loop immediately?",
             "options": ["exit", "stop", "break", "return"], "answer": "break"},
            {"q": "What is the result of `not True`?",
             "options": ["True", "False", "None", "Error"], "answer": "False"},
            {"q": "What does `range(2, 10, 2)` produce?",
             "options": ["2,4,6,8,10", "2,4,6,8", "2,6,10", "0,2,4,6,8"], "answer": "2,4,6,8"},
            {"q": "What does `continue` do inside a loop?",
             "options": ["Stops the loop", "Skips the current iteration", "Restarts the loop", "Does nothing"],
             "answer": "Skips the current iteration"},
            {"q": "What is printed by: `for i in range(3): print(i)`?",
             "options": ["1 2 3", "0 1 2", "0 1 2 3", "1 2"], "answer": "0 1 2"},
            {"q": "What is `5 == 5.0` in Python?",
             "options": ["False", "True", "Error", "None"], "answer": "True"},
            {"q": "What does `pass` do in Python?",
             "options": ["Exits the function", "Skips to next iteration", "Does nothing (placeholder)", "Returns None"],
             "answer": "Does nothing (placeholder)"},
            {"q": "What does `elif` stand for?",
             "options": ["else if", "else in loop", "end if", "evaluated if"], "answer": "else if"},
            {"q": "`True and False` evaluates to?",
             "options": ["True", "False", "None", "Error"], "answer": "False"},
            {"q": "`False or True` evaluates to?",
             "options": ["True", "False", "None", "Error"], "answer": "True"},
            {"q": "What is the output of `[x for x in range(5) if x % 2 == 0]`?",
             "options": ["[1,3]", "[0,2,4]", "[0,1,2,3,4]", "[2,4]"], "answer": "[0,2,4]"},
            {"q": "How many times does `for i in range(5)` execute?",
             "options": ["4", "5", "6", "0"], "answer": "5"},
            {"q": "What operator checks if two variables point to the same object?",
             "options": ["==", "is", "===", "equals"], "answer": "is"},
            {"q": "What does `!=` mean?",
             "options": ["equal", "not equal", "less than", "greater than"], "answer": "not equal"},
            {"q": "What is `'a' < 'b'` in Python?",
             "options": ["False", "True", "Error", "None"], "answer": "True"},
            {"q": "What is the ternary expression for: if x>5 return 'big' else 'small'?",
             "options": ["'big' if x>5 else 'small'", "if x>5: 'big' else 'small'", "x>5 ? 'big' : 'small'", "'small' if x>5 else 'big'"],
             "answer": "'big' if x>5 else 'small'"},
            {"q": "`while True:` without a `break` creates?",
             "options": ["A syntax error", "An infinite loop", "A loop that runs once", "A loop that never runs"],
             "answer": "An infinite loop"},
            {"q": "What does `enumerate(['a','b','c'])` yield on first iteration?",
             "options": ["'a'", "(0, 'a')", "(1, 'a')", "0"], "answer": "(0, 'a')"},
            {"q": "What does `zip([1,2],[3,4])` produce?",
             "options": ["[1,2,3,4]", "[(1,3),(2,4)]", "[(1,2),(3,4)]", "[[1,3],[2,4]]"],
             "answer": "[(1,3),(2,4)]"},
        ],
    },
    3: {
        "title": "Lists & Dictionaries", "subtitle": "The Inventory",
        "icon": "🎒", "pixel_art": "📦", "color": "#00CFFF", "xp_reward": 140,
        "description": """
## 🎒 Chapter 3 — Lists & Dictionaries

Python's most powerful built-in collections. Lists are your **ordered item bags**; dictionaries are your **character sheets**.

---

### 📋 Lists — Ordered, Mutable Sequences

```python
# Creating lists
empty    = []
numbers  = [1, 2, 3, 4, 5]
mixed    = [42, "hello", True, 3.14]
nested   = [[1,2], [3,4], [5,6]]
```

**Indexing & Slicing:**
```python
items = ["sword", "shield", "potion", "map", "key"]
items[0]     # "sword"   (first)
items[-1]    # "key"     (last)
items[1:3]   # ["shield","potion"] (index 1 up to but not including 3)
items[:2]    # ["sword","shield"]  (from start)
items[2:]    # ["potion","map","key"] (to end)
items[::2]   # every 2nd: ["sword","potion","key"]
items[::-1]  # reversed: ["key","map","potion","shield","sword"]
```

**Modifying Lists:**
```python
items.append("torch")      # add to end
items.insert(0, "helmet")  # add at index 0
items.remove("shield")     # remove first occurrence
items.pop()                # remove & return last item
items.pop(1)               # remove & return item at index 1
items.sort()               # sort in-place (alphabetical)
items.sort(reverse=True)   # sort descending
items.reverse()            # reverse in-place
items.clear()              # remove all elements
```

**List Info:**
```python
len(items)          # number of items
items.count("x")    # how many times x appears
items.index("x")    # first index of x
"sword" in items    # True/False — membership test
```

---

### 📖 Dictionaries — Key-Value Stores

```python
# Creating dicts
hero = {}                               # empty
hero = {"name": "Alex", "hp": 100, "class": "Wizard"}
hero = dict(name="Alex", hp=100)        # keyword style
```

**Accessing & Modifying:**
```python
hero["name"]             # "Alex"
hero.get("name")         # "Alex" (safe — no KeyError)
hero.get("mp", 0)        # 0 if "mp" key doesn't exist

hero["level"] = 5        # add new key
hero["hp"] = 120         # update existing key
del hero["class"]        # delete a key
hero.pop("level", None)  # remove & return (safe)
```

**Iterating:**
```python
for key in hero:                    # iterate keys
    print(key)

for key, value in hero.items():     # iterate key-value pairs
    print(f"{key}: {value}")

hero.keys()    # dict_keys(["name","hp",...])
hero.values()  # dict_values(["Alex",100,...])
hero.items()   # dict_items([("name","Alex"),...])
```

**Merging:**
```python
defaults = {"hp": 100, "mp": 50, "level": 1}
custom   = {"name": "Alex", "hp": 150}
merged   = {**defaults, **custom}  # custom overrides defaults
defaults.update(custom)            # in-place merge
```

---

### 🔵 Tuples — Immutable Sequences
```python
coords   = (10, 20)          # can't be changed
rgb      = (255, 128, 0)
name, age = ("Alex", 25)     # tuple unpacking
singleton = (42,)            # comma makes it a tuple!
```

---

### 🟣 Sets — Unique, Unordered
```python
unique_items = {1, 2, 3, 2, 1}   # {1, 2, 3}
s = set([1, 2, 2, 3, 3])         # {1, 2, 3}
s.add(4)
s.remove(1)
{1,2,3} & {2,3,4}   # {2,3} intersection
{1,2,3} | {2,3,4}   # {1,2,3,4} union
```

---

### ⚡ Comprehensions
```python
squares_list = [x**2 for x in range(5)]       # list
squares_set  = {x**2 for x in range(5)}        # set
squares_dict = {x: x**2 for x in range(5)}     # dict
```

---

> 💡 **Pro Tip:** Use `dict.get(key, default)` instead of `dict[key]` when the key might not exist — it avoids a `KeyError`.
        """,
        "code_example": '''# 🎒 Lists & Dictionaries — Full Demo

# === LISTS ===
inventory = ["sword", "shield", "potion"]

inventory.append("map")
inventory.insert(0, "helmet")
inventory.remove("shield")
popped = inventory.pop()   # removes last

print("Inventory:", inventory)
print("Popped:   ", popped)
print("Length:   ", len(inventory))
print("Index 0:  ", inventory[0])
print("Slice 1:3:", inventory[1:3])
print("Reversed: ", inventory[::-1])

# Sorting
scores = [42, 15, 88, 7, 63]
scores.sort()
print("\\nSorted:   ", scores)
print("Max:      ", max(scores))
print("Min:      ", min(scores))
print("Sum:      ", sum(scores))

# List comprehension
powered = [item.upper() for item in inventory]
print("\\nPowered:  ", powered)
even_scores = [s for s in scores if s % 2 == 0]
print("Even scores:", even_scores)

# === DICTIONARIES ===
print("\\n--- Hero Sheet ---")
hero = {
    "name":  "Alex",
    "hp":    100,
    "mp":    50,
    "class": "Wizard",
    "level": 3,
}

hero["xp"] = 250           # add key
hero["hp"] = 120           # update key
missing = hero.get("gold", 0)  # safe get

for stat, val in hero.items():
    print(f"  {stat:8s}: {val}")
print(f"  gold    : {missing} (default)")

# Nested dict
party = {
    "Alex":   {"hp": 120, "role": "Wizard"},
    "Sam":    {"hp":  95, "role": "Rogue"},
    "Jordan": {"hp":  80, "role": "Archer"},
}
print("\\n--- Party ---")
for name, stats in party.items():
    print(f"  {name}: HP={stats['hp']}, {stats['role']}")

# === SET ===
visited = {"dungeon", "forest", "cave", "dungeon"}
print("\\nVisited zones:", visited)  # no duplicates
''',
        "questions": [
            {"q": "How do you add an element to the END of a list `my_list`?",
             "options": ["my_list.add(x)", "my_list.append(x)", "my_list.insert(x)", "my_list.push(x)"],
             "answer": "my_list.append(x)"},
            {"q": "What does `my_dict.get('key', 'default')` return if 'key' doesn't exist?",
             "options": ["Raises a KeyError", "Returns None", "Returns 'default'", "Returns empty string"],
             "answer": "Returns 'default'"},
            {"q": "What is the output of `[x*2 for x in [1,2,3]]`?",
             "options": ["[1,2,3]", "[2,4,6]", "(2,4,6)", "[1,4,9]"], "answer": "[2,4,6]"},
            {"q": "What does `my_list[-1]` return?",
             "options": ["First element", "Last element", "Second-to-last element", "Error"], "answer": "Last element"},
            {"q": "What is `len([1, 2, 3, 4, 5])`?",
             "options": ["4", "5", "6", "Error"], "answer": "5"},
            {"q": "What does `[1,2,3].pop()` return?",
             "options": ["1", "2", "3", "None"], "answer": "3"},
            {"q": "What does `sorted([3,1,2])` return?",
             "options": ["[3,1,2]", "[1,2,3]", "[3,2,1]", "None"], "answer": "[1,2,3]"},
            {"q": "What does `dict.keys()` return?",
             "options": ["All values", "All keys", "All items as tuples", "Length of dict"],
             "answer": "All keys"},
            {"q": "What is `{'a':1, 'b':2}['a']`?",
             "options": ["2", "1", "'a'", "Error"], "answer": "1"},
            {"q": "What does `list.insert(0, x)` do?",
             "options": ["Appends x to end", "Inserts x at the beginning", "Replaces index 0 with x", "Adds x at position x"],
             "answer": "Inserts x at the beginning"},
            {"q": "Is `'a' in {'a': 1}` True or False?",
             "options": ["True", "False", "Error", "None"], "answer": "True"},
            {"q": "What is `[1,2] + [3,4]`?",
             "options": ["[1,2,3,4]", "[3,4,1,2]", "Error", "[2,4]"], "answer": "[1,2,3,4]"},
            {"q": "What does a Python set automatically remove?",
             "options": ["Sorted elements", "Negative numbers", "Duplicate values", "String elements"],
             "answer": "Duplicate values"},
            {"q": "A tuple is different from a list because it is?",
             "options": ["Unordered", "Immutable", "Mutable", "Slower"], "answer": "Immutable"},
            {"q": "What does `dict.items()` return?",
             "options": ["Only keys", "Only values", "Key-value pairs", "Length"], "answer": "Key-value pairs"},
            {"q": "What does `list.count(x)` do?",
             "options": ["Returns length", "Returns how many times x appears", "Returns index of x", "Removes x"],
             "answer": "Returns how many times x appears"},
            {"q": "What is `[0,1,2,3][1:3]`?",
             "options": ["[0,1]", "[1,2]", "[2,3]", "[1,2,3]"], "answer": "[1,2]"},
            {"q": "What is `{1,2,2,3}` in Python?",
             "options": ["[1,2,2,3]", "{1,2,3}", "(1,2,3)", "Error"], "answer": "{1,2,3}"},
            {"q": "What does `list.reverse()` return?",
             "options": ["A new reversed list", "None (reverses in place)", "The first element", "Error"],
             "answer": "None (reverses in place)"},
            {"q": "What does `dict.update(other)` do?",
             "options": ["Creates a new dict", "Merges other into dict", "Returns the length", "Clears the dict"],
             "answer": "Merges other into dict"},
        ],
    },
    4: {
        "title": "Functions", "subtitle": "The Spells",
        "icon": "✨", "pixel_art": "🪄", "color": "#FF6B6B", "xp_reward": 160,
        "description": """
## ✨ Chapter 4 — Functions

Functions are **reusable blocks of code** — your hero's spellbook. Define once, cast anywhere. They make code organised, testable and maintainable.

---

### 📝 Defining & Calling Functions
```python
# Basic function
def greet(name):
    return f"Welcome, {name}!"

result = greet("Alex")   # call it
print(result)            # Welcome, Alex!

# Function with multiple parameters
def add(a, b):
    return a + b

print(add(3, 4))   # 7
```

---

### 🎯 Parameters & Arguments

**Default parameters** (optional when calling):
```python
def cast_spell(name, power=10, critical=False):
    damage = power * (2 if critical else 1)
    return f"{name} deals {damage} damage!"

cast_spell("Fireball")               # power=10, critical=False
cast_spell("Lightning", power=30)    # critical=False
cast_spell("Thunder", 20, True)      # all args provided
cast_spell("Bolt", critical=True)    # keyword argument
```

**`*args` — variable positional arguments** (collected as a tuple):
```python
def total(*numbers):
    return sum(numbers)

total(1, 2, 3)         # 6
total(10, 20, 30, 40)  # 100
```

**`**kwargs` — variable keyword arguments** (collected as a dict):
```python
def show_stats(**stats):
    for key, val in stats.items():
        print(f"  {key}: {val}")

show_stats(hp=100, mp=50, level=3)
```

---

### 🔄 Return Values

```python
def divide(a, b):
    if b == 0:
        return None          # early return
    return a / b

# Return multiple values (tuple)
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 4, 1, 5, 9])
# low=1, high=9
```

---

### 🌍 Scope — Local vs Global
```python
score = 100         # global variable

def update_score():
    global score    # declare intent to modify global
    score += 50

update_score()
print(score)   # 150

def local_example():
    x = 99      # local — only exists inside this function
    return x
# print(x)  would raise NameError!
```

---

### ⚡ Lambda Functions (Anonymous)
```python
double  = lambda x: x * 2
add     = lambda a, b: a + b
is_even = lambda n: n % 2 == 0

double(5)     # 10
add(3, 4)     # 7

# Common use: as key functions
nums = [5, 2, 8, 1, 9]
nums.sort(key=lambda x: -x)   # sort descending
```

---

### 🗺️ Higher-Order Functions
```python
# map — apply function to each element
list(map(lambda x: x*2, [1,2,3]))    # [2,4,6]
list(map(str, [1,2,3]))              # ['1','2','3']

# filter — keep elements where function is True
list(filter(lambda x: x>2, [1,2,3,4]))   # [3,4]

# sorted with key
heroes = [{"name":"Alex","hp":120},{"name":"Sam","hp":95}]
sorted(heroes, key=lambda h: h["hp"])    # sorted by hp
```

---

### 🔁 Recursion
```python
def factorial(n):
    if n <= 1:            # base case — MUST have one!
        return 1
    return n * factorial(n - 1)   # recursive call

factorial(5)   # 120  (5*4*3*2*1)

def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)
```

---

### 📄 Docstrings
```python
def calculate_damage(base, multiplier=1.0, critical=False):
    \"\"\"
    Calculate damage dealt to an enemy.

    Args:
        base (int): Base damage value.
        multiplier (float): Damage multiplier (default 1.0).
        critical (bool): Whether it is a critical hit.

    Returns:
        int: Final damage dealt.
    \"\"\"
    dmg = int(base * multiplier * (2 if critical else 1))
    return dmg

help(calculate_damage)   # shows the docstring
```

---

> 💡 **Pro Tip:** Every function should do ONE thing well. If your function is doing three different things, split it into three functions!
        """,
        "code_example": '''# ✨ Functions — Full Demo

# Basic function
def greet(name):
    return f"Welcome, {name}! Your quest begins."

# Default params + critical hit
def cast_spell(spell_name, power=10, critical=False):
    damage = power * (2 if critical else 1)
    return f"⚡ {spell_name} deals {damage} damage!"

# *args
def total_xp(*xp_gains):
    return sum(xp_gains)

# **kwargs
def create_hero(**attributes):
    return {k: v for k, v in attributes.items()}

# Multiple return values
def analyze_scores(scores):
    return min(scores), max(scores), sum(scores)/len(scores)

# Recursive factorial
def factorial(n):
    if n <= 1: return 1
    return n * factorial(n - 1)

# Lambda
double = lambda x: x * 2

# higher-order functions
heroes = [{"name":"Alex","hp":120},{"name":"Sam","hp":95},{"name":"Jordan","hp":80}]

# --- Run it all ---
print(greet("Alex"))
print(cast_spell("Fireball", power=25))
print(cast_spell("Lightning", power=30, critical=True))
print(f"Total XP: {total_xp(50, 30, 20, 15)}")

hero = create_hero(name="Zara", hp=100, class_="Mage", level=5)
print(f"\\nHero: {hero}")

scores = [72, 88, 95, 61, 78]
lo, hi, avg = analyze_scores(scores)
print(f"\\nScores → min:{lo}, max:{hi}, avg:{avg:.1f}")

print(f"\\n5! = {factorial(5)}")
print(f"Double 7 = {double(7)}")

# map + filter
nums = [1, 2, 3, 4, 5, 6]
doubled  = list(map(lambda x: x*2, nums))
evens    = list(filter(lambda x: x%2==0, nums))
print(f"\\nDoubled: {doubled}")
print(f"Evens:   {evens}")

# sort by hp
ranked = sorted(heroes, key=lambda h: h["hp"], reverse=True)
print("\\nHero ranking by HP:")
for i, h in enumerate(ranked, 1):
    print(f"  #{i} {h['name']}: {h['hp']} HP")
''',
        "questions": [
            {"q": "What keyword defines a function in Python?",
             "options": ["function", "func", "def", "define"], "answer": "def"},
            {"q": "What does a function return with no `return` statement?",
             "options": ["0", "False", "None", "An error"], "answer": "None"},
            {"q": "What is `lambda x: x ** 2` equivalent to?",
             "options": ["def f(x): x**2", "def f(x): return x**2", "def f(): return x**2", "lambda: x**2"],
             "answer": "def f(x): return x**2"},
            {"q": "What does `*args` collect in a function?",
             "options": ["A single argument", "Positional arguments as a tuple", "Keyword arguments as a dict", "Default arguments"],
             "answer": "Positional arguments as a tuple"},
            {"q": "What does `**kwargs` collect?",
             "options": ["Positional args as list", "Keyword arguments as a dict", "All arguments as a set", "Nothing"],
             "answer": "Keyword arguments as a dict"},
            {"q": "Given `def f(x=5): return x`, what does `f()` return?",
             "options": ["0", "None", "5", "Error"], "answer": "5"},
            {"q": "What does the `global` keyword do inside a function?",
             "options": ["Creates a new variable", "Makes a variable accessible everywhere", "Modifies a global variable from inside a function", "Deletes a global variable"],
             "answer": "Modifies a global variable from inside a function"},
            {"q": "What does every recursive function need to avoid infinite recursion?",
             "options": ["A global variable", "A base case", "A lambda", "A return value"],
             "answer": "A base case"},
            {"q": "What does `list(map(lambda x: x*2, [1,2,3]))` return?",
             "options": ["[1,2,3]", "[2,4,6]", "[1,4,9]", "Error"], "answer": "[2,4,6]"},
            {"q": "What does `list(filter(lambda x: x>2, [1,2,3,4]))` return?",
             "options": ["[1,2]", "[3,4]", "[1,2,3,4]", "[2,3,4]"], "answer": "[3,4]"},
            {"q": "A docstring is placed?",
             "options": ["At the top of the file", "Right after the `def` line", "At the end of the function", "Before the `def` line"],
             "answer": "Right after the `def` line"},
            {"q": "Can a Python function return multiple values?",
             "options": ["No", "Yes, as a tuple", "Only with *args", "Only with **kwargs"],
             "answer": "Yes, as a tuple"},
            {"q": "What does `return` do in a function?",
             "options": ["Pauses the function", "Exits the function and optionally returns a value", "Restarts the function", "Skips to next line"],
             "answer": "Exits the function and optionally returns a value"},
            {"q": "A higher-order function is one that?",
             "options": ["Has more than 5 parameters", "Takes or returns other functions", "Uses recursion", "Has default parameters"],
             "answer": "Takes or returns other functions"},
            {"q": "What does `list(map(str, [1,2,3]))` produce?",
             "options": ["[1,2,3]", "['1','2','3']", "['str','str','str']", "Error"],
             "answer": "['1','2','3']"},
            {"q": "What is a variable declared inside a function called?",
             "options": ["Global variable", "Local variable", "Static variable", "Instance variable"],
             "answer": "Local variable"},
            {"q": "What is `sorted([5,2,8], key=lambda x: -x)`?",
             "options": ["[2,5,8]", "[8,5,2]", "[5,2,8]", "[-5,-2,-8]"],
             "answer": "[8,5,2]"},
            {"q": "Calling `def f(): pass` returns?",
             "options": ["0", "False", "None", "Error"], "answer": "None"},
            {"q": "What does `enumerate(['a','b'])` produce on first iteration?",
             "options": ["'a'", "(0,'a')", "(1,'a')", "0"], "answer": "(0,'a')"},
            {"q": "What is `factorial(4)` if factorial(n) = n * factorial(n-1) and factorial(1)=1?",
             "options": ["8", "12", "24", "16"], "answer": "24"},
        ],
    },
    5: {
        "title": "The Final Boss", "subtitle": "Comprehensive Python Test",
        "icon": "🐉", "pixel_art": "💀", "color": "#FF4444", "xp_reward": 200,
        "description": """
## 🐉 Chapter 5 — The Final Boss

You've mastered the four disciplines. Now face the **comprehensive gauntlet** that combines everything — plus three powerful new weapons.

---

### 🔁 Quick Review
- **Variables & Types:** `int`, `float`, `str`, `bool`, `None`; type conversion; f-strings
- **Logic & Loops:** `if/elif/else`, `for`, `while`, `break`, `continue`, comprehensions
- **Lists & Dicts:** indexing, slicing, all methods, `set`, `tuple`
- **Functions:** `def`, `return`, `*args`, `**kwargs`, `lambda`, `map`, `filter`, recursion

---

### 🏛️ Object-Oriented Programming (OOP)

```python
class Hero:
    # Class variable (shared by all instances)
    species = "Human"

    def __init__(self, name, hp=100):
        # Instance variables
        self.name = name
        self.hp   = hp
        self.inventory = []

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        return f"{self.name} took {amount} dmg! HP: {self.hp}"

    def pick_up(self, item):
        self.inventory.append(item)

    def __str__(self):       # controls print(hero)
        return f"Hero({self.name}, HP={self.hp})"

    def __repr__(self):      # controls repr(hero)
        return f"Hero(name={self.name!r}, hp={self.hp})"

# Create instances
hero1 = Hero("Alex", hp=120)
hero2 = Hero("Sam")           # hp defaults to 100

print(hero1.take_damage(35))
hero1.pick_up("sword")
print(hero1)                  # Hero(Alex, HP=85)
print(Hero.species)           # "Human"
```

**Inheritance:**
```python
class Wizard(Hero):
    def __init__(self, name, hp=80, mp=100):
        super().__init__(name, hp)   # call parent __init__
        self.mp = mp

    def cast(self, spell, cost=10):
        if self.mp >= cost:
            self.mp -= cost
            return f"✨ {spell} cast! MP: {self.mp}"
        return "Not enough MP!"

wizard = Wizard("Merlin")
print(wizard.cast("Fireball", cost=20))
print(isinstance(wizard, Hero))    # True
```

---

### 🛡️ Error Handling — try / except

```python
# Catch specific exceptions
try:
    result = 10 / 0
except ZeroDivisionError:
    result = 0
    print("Cannot divide by zero!")

# Multiple exceptions
try:
    value = int("abc")
except ValueError as e:
    print(f"ValueError: {e}")
except TypeError as e:
    print(f"TypeError: {e}")
else:
    print("No error occurred!")     # runs if no exception
finally:
    print("This always runs!")      # always executes

# Raise custom errors
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError(f"Insufficient funds: {balance}")
    return balance - amount
```

---

### 📁 File I/O

```python
# Writing to a file
with open("scores.txt", "w") as f:
    f.write("Alex: 95\\n")
    f.write("Sam: 87\\n")

# Reading all at once
with open("scores.txt", "r") as f:
    content = f.read()

# Reading line by line
with open("scores.txt", "r") as f:
    for line in f:
        print(line.strip())

# Writing JSON
import json
data = {"player": "Alex", "score": 95}
with open("save.json", "w") as f:
    json.dump(data, f)

# Reading JSON
with open("save.json", "r") as f:
    loaded = json.load(f)
```

---

### 📦 Modules & Imports

```python
import math
import random
import os
from datetime import datetime
from collections import Counter, defaultdict

math.sqrt(16)        # 4.0
math.pi              # 3.14159...
random.randint(1,6)  # dice roll
random.choice(["a","b","c"])  # random pick
random.shuffle(mylist)

os.path.exists("file.txt")
os.getcwd()          # current directory
datetime.now()       # current timestamp

Counter("aabbcc")    # Counter({'a':2,'b':2,'c':2})
```

---

### 🔮 Advanced Patterns
```python
# Generator — lazy evaluation
def count_up(n):
    for i in range(n):
        yield i           # pauses and returns i

gen = count_up(5)
next(gen)    # 0
next(gen)    # 1

# Context manager
class ManaPool:
    def __enter__(self):
        print("Mana pool opened")
        return self
    def __exit__(self, *args):
        print("Mana pool closed")

with ManaPool() as pool:
    pass

# any / all
any([False, True, False])   # True
all([True, True, True])     # True
all([True, False, True])    # False
```

---

> 🏆 **Final Challenge:** Answer 10 questions across ALL topics. Score 6/10 to claim your **Python Master Certificate**!
        """,
        "code_example": '''# 🐉 Final Boss — All Skills Combined

import random
from collections import Counter

# ── OOP ──
class Hero:
    def __init__(self, name, hp=100, mp=50):
        self.name = name
        self.hp   = hp
        self.mp   = mp
        self.inventory = []
        self.xp   = 0

    def attack(self, enemy, base=20):
        crit = random.random() < 0.25
        dmg  = base * 2 if crit else base
        enemy.hp = max(0, enemy.hp - dmg)
        tag = " 💥CRIT!" if crit else ""
        return f"{self.name} → {enemy.name}: {dmg} dmg{tag} (HP:{enemy.hp})"

    def heal(self, amount=30):
        if self.mp < 10:
            return "Not enough MP!"
        self.hp  = min(200, self.hp + amount)
        self.mp -= 10
        return f"{self.name} healed +{amount} HP (HP:{self.hp})"

    def __str__(self):
        return f"{self.name} [HP:{self.hp} MP:{self.mp} XP:{self.xp}]"

class Boss(Hero):
    def __init__(self, name, hp=300, power=35):
        super().__init__(name, hp)
        self.power = power

    def rage_attack(self, hero):
        dmg = self.power + random.randint(0, 20)
        hero.hp = max(0, hero.hp - dmg)
        return f"🐉 {self.name} RAGE → {hero.name}: {dmg} dmg!"

# ── Error handling ──
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 0

# ── Higher-order / comprehensions ──
def analyze_party(members):
    alive  = [m for m in members if m.hp > 0]
    hps    = [m.hp for m in members]
    return {
        "total":   len(members),
        "alive":   len(alive),
        "avg_hp":  round(sum(hps)/len(hps), 1),
        "strongest": max(members, key=lambda m: m.hp).name,
    }

# ── Simulation ──
hero = Hero("Alex", hp=150, mp=60)
boss = Boss("Shadow Dragon")

print("⚔️  BATTLE START!")
print(hero)
print(boss)

for round_num in range(1, 6):
    print(f"\\n--- Round {round_num} ---")
    print(" ", hero.attack(boss))
    if boss.hp > 0:
        print(" ", boss.rage_attack(hero))
    if hero.hp <= 0 or boss.hp <= 0:
        break

winner = hero.name if hero.hp > 0 else boss.name
print(f"\\n🏆 {winner} wins!")

# Party analysis
party = [Hero("Alex",120), Hero("Sam",95), Hero("Jordan",0)]
stats = analyze_party(party)
print("\\n📊 Party Stats:", stats)

# misc
items = ["sword","shield","sword","potion","sword"]
freq  = Counter(items)
print("\\n🗃️  Item frequency:", dict(freq))
print("Safe 10/0 =", safe_divide(10, 0))
''',
        "questions": [
            {"q": "What does `max([3,1,4,1,5,9], key=lambda x: -x)` return?",
             "options": ["9", "1", "3", "-9"], "answer": "1"},
            {"q": "Which line correctly unpacks a dict into keyword arguments?",
             "options": ["func(*my_dict)", "func(**my_dict)", "func(my_dict...)", "func(#my_dict)"],
             "answer": "func(**my_dict)"},
            {"q": "What is the average-case time complexity of a Python dict lookup?",
             "options": ["O(n)", "O(log n)", "O(1)", "O(n²)"], "answer": "O(1)"},
            {"q": "Which block in try/except ALWAYS executes, even if an exception occurs?",
             "options": ["try", "except", "else", "finally"], "answer": "finally"},
            {"q": "What does `__init__` do in a Python class?",
             "options": ["Destroys the object", "Initializes an instance when it's created", "Returns a string representation", "Defines class variables"],
             "answer": "Initializes an instance when it's created"},
            {"q": "What does `self` refer to inside a class method?",
             "options": ["The class itself", "The current instance", "The parent class", "A global variable"],
             "answer": "The current instance"},
            {"q": "How do you call the parent class `__init__` from a child class?",
             "options": ["parent.__init__()", "super().__init__()", "base.__init__()", "class.__init__()"],
             "answer": "super().__init__()"},
            {"q": "What does `any([False, True, False])` return?",
             "options": ["False", "True", "None", "Error"], "answer": "True"},
            {"q": "What does `all([True, True, False])` return?",
             "options": ["True", "False", "None", "Error"], "answer": "False"},
            {"q": "What keyword creates a generator function?",
             "options": ["return", "yield", "generate", "next"], "answer": "yield"},
            {"q": "What does `isinstance(wizard, Hero)` return if `Wizard` inherits from `Hero`?",
             "options": ["False", "True", "Error", "None"], "answer": "True"},
            {"q": "Which exception is raised by `int('abc')`?",
             "options": ["TypeError", "ValueError", "KeyError", "IndexError"], "answer": "ValueError"},
            {"q": "What does `with open('f.txt') as f:` ensure?",
             "options": ["The file is opened in write mode", "The file is automatically closed after the block", "The file is read entirely", "The file is created if missing"],
             "answer": "The file is automatically closed after the block"},
            {"q": "What does `raise ValueError('msg')` do?",
             "options": ["Catches a ValueError", "Manually throws a ValueError exception", "Prints a warning", "Ignores the error"],
             "answer": "Manually throws a ValueError exception"},
            {"q": "What does `Counter('aabbcc')` from `collections` return?",
             "options": ["['a','b','c']", "Counter({'a':2,'b':2,'c':2})", "{'a','b','c'}", "3"],
             "answer": "Counter({'a':2,'b':2,'c':2})"},
            {"q": "What is `__str__` used for in a class?",
             "options": ["Converts object to bytes", "Defines string representation for print()", "Deletes the object", "Compares two objects"],
             "answer": "Defines string representation for print()"},
            {"q": "What does `json.dump(data, f)` do?",
             "options": ["Reads JSON from a file", "Writes Python object as JSON to a file", "Converts JSON to dict", "Validates JSON"],
             "answer": "Writes Python object as JSON to a file"},
            {"q": "Which is the correct way to handle multiple exception types separately?",
             "options": ["try/catch multiple", "multiple except blocks", "except (E1, E2) only", "multiple try blocks"],
             "answer": "multiple except blocks"},
            {"q": "What does `random.choice(['a','b','c'])` do?",
             "options": ["Returns all elements", "Returns a random element", "Shuffles the list", "Returns the first element"],
             "answer": "Returns a random element"},
            {"q": "What does `sorted()` return compared to `list.sort()`?",
             "options": ["sorted() modifies in place; sort() returns a new list", "Both return None", "sorted() returns a new list; sort() modifies in place", "They are identical"],
             "answer": "sorted() returns a new list; sort() modifies in place"},
        ],
    },
}

# ============================================================
# BOSS BATTLES  — one per level, answered by typing exact text
# ============================================================
BOSS_BATTLES = {
    1: {
        "title": "The Type Titan",
        "icon": "🧨",
        "flavor": "The Type Titan morphs into any data form — name the Python method that converts a string to ALL UPPERCASE letters.",
        "hint": "It's a built-in str method. Call it like: 'hello'.????()",
        "answer": ".upper()",
        "xp_reward": 60,
        "success_msg": "CRITICAL HIT! The Type Titan crumbles — it can't handle your string mastery!",
    },
    2: {
        "title": "The Infinite Looper",
        "icon": "♾️",
        "flavor": "The Infinite Looper spins forever unless you know the exact keyword that exits a `while True:` loop instantly.",
        "hint": "A single Python keyword — the one that exits a loop immediately.",
        "answer": "break",
        "xp_reward": 70,
        "success_msg": "LOOP SHATTERED! The Infinite Looper vanishes — your control flow is flawless!",
    },
    3: {
        "title": "The List Lich",
        "icon": "📜",
        "flavor": "The List Lich guards a forbidden list. Type the list method that adds a single item to the END of a list.",
        "hint": "The most common list mutation method. `my_list.????(item)`",
        "answer": ".append()",
        "xp_reward": 80,
        "success_msg": "APPENDED TO VICTORY! The List Lich's collection is yours now!",
    },
    4: {
        "title": "The Lambda Shadow",
        "icon": "λ",
        "flavor": "The Lambda Shadow hides in anonymous functions. Reveal the Python keyword used to define a named function.",
        "hint": "It comes before the function name: `??? my_func():`",
        "answer": "def",
        "xp_reward": 90,
        "success_msg": "FUNCTION MASTERED! The Lambda Shadow dissolves in the light of your knowledge!",
    },
    5: {
        "title": "The Final Dragon",
        "icon": "🔥",
        "flavor": "The Final Dragon breathes exceptions! Type the keyword that manually raises an exception in Python.",
        "hint": "`??? ValueError('msg')` — how do you throw an exception?",
        "answer": "raise",
        "xp_reward": 150,
        "success_msg": "LEGENDARY! The Final Dragon is vanquished — you are a true Python Master!",
    },
}

# ============================================================
# XP / RANK SYSTEM
# ============================================================
XP_TIERS = [
    (0,   "Apprentice",    "🌱"),
    (100, "Coder",         "💻"),
    (250, "Wizard",        "🧙"),
    (450, "Sorcerer",      "🔮"),
    (700, "Python Master", "🐍"),
]

def get_character_info(xp: int):
    title, icon = XP_TIERS[0][1], XP_TIERS[0][2]
    for threshold, t, i in XP_TIERS:
        if xp >= threshold:
            title, icon = t, i
    return title, icon

def xp_to_progress(xp: int) -> float:
    max_xp = sum(v["xp_reward"] for v in LEVELS.values())
    return min(xp / max_xp, 1.0)

PASS_THRESHOLD = 6   # out of 10
QUESTIONS_PER_EXAM = 10
QUESTIONS_IN_BANK  = 20

# ============================================================
# PASSWORD HELPERS
# ============================================================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password: str, pw_hash: str) -> bool:
    return hash_password(password) == pw_hash


# ============================================================
# PERSISTENT PROGRESS  (JSON-backed)
# ============================================================
def empty_progress():
    return {
        "xp": 0, "completed_levels": [], "quiz_state": {}, "cert_name": "",
        "last_login": None, "streak": 0, "boss_battles_done": [],
    }

def load_user_progress(username: str):
    db   = get_db()
    prog = db["progress"].get(username, empty_progress())
    st.session_state.xp               = prog.get("xp", 0)
    st.session_state.completed_levels = set(prog.get("completed_levels", []))
    raw_qs = prog.get("quiz_state", {})
    st.session_state.quiz_state       = {int(k): v for k, v in raw_qs.items()}
    st.session_state.cert_name        = prog.get("cert_name", "")
    st.session_state.streak           = prog.get("streak", 0)
    st.session_state.last_login       = prog.get("last_login", None)
    st.session_state.boss_battles_done = set(prog.get("boss_battles_done", []))

    # ── Streak logic ──
    today = date.today().isoformat()
    last  = st.session_state.last_login
    if last is None:
        st.session_state.streak = 1
    elif last == today:
        pass  # already counted today
    else:
        try:
            last_date = date.fromisoformat(last)
            delta     = (date.today() - last_date).days
            if delta == 1:
                st.session_state.streak += 1
            elif delta > 1:
                st.session_state.streak = 1
        except Exception:
            st.session_state.streak = 1
    st.session_state.last_login = today

def save_user_progress(username: str):
    db = get_db()
    if "progress" not in db:
        db["progress"] = {}
    db["progress"][username] = {
        "xp":                st.session_state.xp,
        "completed_levels":  list(st.session_state.completed_levels),
        "quiz_state":        {str(k): v for k, v in st.session_state.quiz_state.items()},
        "cert_name":         st.session_state.cert_name,
        "last_login":        st.session_state.get("last_login", None),
        "streak":            st.session_state.get("streak", 0),
        "boss_battles_done": list(st.session_state.get("boss_battles_done", set())),
    }
    flush_db()


# ============================================================
# SESSION STATE INIT
# ============================================================
def init_state():
    defaults = {
        "logged_in": False, "username": "",
        "auth_tab": "login", "auth_error": "", "auth_success": "",
        "xp": 0, "completed_levels": set(), "quiz_state": {}, "cert_name": "",
        "current_level": 1, "show_badge": None, "view": "hub",
        "streak": 0, "last_login": None, "boss_battles_done": set(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ============================================================
# AUTH ACTIONS
# ============================================================
def do_register(username, password, confirm):
    username = username.strip().lower()
    if not username or not password:
        st.session_state.auth_error = "Username and password cannot be empty."
        return
    if len(username) < 3:
        st.session_state.auth_error = "Username must be at least 3 characters."
        return
    if len(password) < 6:
        st.session_state.auth_error = "Password must be at least 6 characters."
        return
    if password != confirm:
        st.session_state.auth_error = "Passwords do not match."
        return
    db = get_db()
    if username in db["users"]:
        st.session_state.auth_error = "Username already taken. Try another."
        return
    db["users"][username] = {"pw_hash": hash_password(password),
                              "registered": datetime.now().isoformat()}
    db["progress"][username] = empty_progress()
    flush_db()
    st.session_state.auth_error   = ""
    st.session_state.auth_success = f"Account created! Welcome, {username} 🎉 Now log in."
    st.session_state.auth_tab     = "login"

def do_login(username, password):
    username = username.strip().lower()
    db = get_db()
    if username not in db["users"]:
        st.session_state.auth_error = "Username not found. Please register first."
        return
    if not check_password(password, db["users"][username]["pw_hash"]):
        st.session_state.auth_error = "Incorrect password. Try again."
        return
    st.session_state.auth_error   = ""
    st.session_state.auth_success = ""
    st.session_state.logged_in    = True
    st.session_state.username     = username
    load_user_progress(username)
    st.session_state.view = "hub"


# ============================================================
# AUTH SCREEN
# ============================================================
def render_auth():
    st.markdown(
        '<div style="text-align:center;padding-top:2rem;">'
        '<div style="font-family:Space Mono,monospace;font-size:0.6rem;color:#00FF41;'
        'letter-spacing:0.35em;margin-bottom:0.5rem;">🐍 PYTHON CODING ADVENTURE</div>'
        '<div style="font-family:Space Mono,monospace;font-size:1.6rem;color:#fff;'
        'text-shadow:0 0 15px rgba(0,255,65,0.4);">Welcome, Adventurer</div>'
        '<div style="color:#888;font-size:0.85rem;margin-top:0.3rem;">'
        'Create an account to save your XP and progress permanently</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        if st.button("🔓 Log In", use_container_width=True, key="tab_login"):
            st.session_state.auth_tab     = "login"
            st.session_state.auth_error   = ""
            st.session_state.auth_success = ""
            st.rerun()
    with col_r:
        if st.button("✨ Register", use_container_width=True, key="tab_reg"):
            st.session_state.auth_tab     = "register"
            st.session_state.auth_error   = ""
            st.session_state.auth_success = ""
            st.rerun()

    active = st.session_state.auth_tab
    st.markdown(
        f'<div style="display:flex;gap:0;margin-bottom:1.5rem;">'
        f'<div style="flex:1;height:3px;background:{"#00FF41" if active=="login" else "#2A2A2A"};'
        f'border-radius:2px 0 0 2px;"></div>'
        f'<div style="flex:1;height:3px;background:{"#00FF41" if active=="register" else "#2A2A2A"};'
        f'border-radius:0 2px 2px 0;"></div></div>',
        unsafe_allow_html=True,
    )

    if st.session_state.auth_error:
        st.markdown(
            f'<div style="background:rgba(255,68,68,0.12);border-left:4px solid #FF4444;'
            f'border-radius:0 8px 8px 0;padding:0.8rem 1rem;color:#FF8888;margin-bottom:0.8rem;">'
            f'⚠️ {st.session_state.auth_error}</div>',
            unsafe_allow_html=True,
        )
    if st.session_state.auth_success:
        st.markdown(f'<div class="success-box">✅ {st.session_state.auth_success}</div>', unsafe_allow_html=True)

    if active == "login":
        username = st.text_input("Username", placeholder="your_username", key="li_user")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="li_pass")
        st.markdown("")
        if st.button("⚡ Log In & Start Adventure", use_container_width=True, key="login_btn"):
            do_login(username, password)
            st.rerun()
        st.markdown(
            '<div style="text-align:center;color:#555;font-size:0.78rem;margin-top:1rem;">'
            "No account yet? Click <strong style='color:#9D46FF'>Register</strong> above.</div>",
            unsafe_allow_html=True,
        )
    else:
        username = st.text_input("Choose a Username", placeholder="coolcoder99 (min 3 chars)", key="reg_user")
        password = st.text_input("Choose a Password", type="password", placeholder="Min. 6 characters", key="reg_pass")
        confirm  = st.text_input("Confirm Password",  type="password", placeholder="Repeat password",   key="reg_conf")
        st.markdown("")
        if st.button("🚀 Create My Account", use_container_width=True, key="reg_btn"):
            do_register(username, password, confirm)
            st.rerun()
        st.markdown(
            '<div style="text-align:center;color:#555;font-size:0.78rem;margin-top:1rem;">'
            "Already have an account? Click <strong style='color:#00FF41'>Log In</strong> above.</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div style="text-align:center;margin-top:2.5rem;padding:0.8rem;'
        'background:#111;border:1px dashed #333;border-radius:8px;">'
        '<span style="font-size:0.75rem;color:#555;">💾 Progress is saved to disk and persists across server restarts. '
        'Log back in anytime to continue your adventure!</span></div>',
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    xp    = st.session_state.xp
    title, icon = get_character_info(xp)
    max_xp    = sum(v["xp_reward"] for v in LEVELS.values())
    completed = len(st.session_state.completed_levels)

    with st.sidebar:
        st.markdown(
            '<p class="pixel-font" style="font-size:0.5rem;color:#00FF41;'
            'text-align:center;letter-spacing:0.2em;">PYTHON ADVENTURE</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="text-align:center;padding:0.8rem 0;">'
            f'<div style="font-size:3rem;">{icon}</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.9rem;color:#fff;font-weight:700;">{title}</div>'
            f'<div style="font-size:0.72rem;color:#00FF41;margin-top:0.2rem;">@{st.session_state.username}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(
            f'<div class="stat-row"><span style="color:#888">XP</span>'
            f'<span class="xp-badge">{xp} / {max_xp}</span></div>',
            unsafe_allow_html=True,
        )
        st.progress(xp_to_progress(xp))
        st.markdown(
            f'<div class="stat-row"><span style="color:#888">Levels Done</span>'
            f'<span style="color:#00FF41;font-family:Space Mono,monospace;">{completed} / 5</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="stat-row"><span style="color:#888">Pass mark</span>'
            f'<span style="color:#9D46FF;font-family:Space Mono,monospace;">6 / 10 (60%)</span></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown('<p style="font-family:Space Mono,monospace;font-size:0.7rem;color:#666;margin-bottom:0.4rem;">LEVEL MAP</p>', unsafe_allow_html=True)
        for lvl_id, lvl in LEVELS.items():
            st_icon = {"done":"✅","unlocked":"🔓","locked":"🔒"}[level_status(lvl_id)]
            color   = {"done":"#00FF41","unlocked":"#E8E8E8","locked":"#555"}[level_status(lvl_id)]
            # show score if attempted
            qs = st.session_state.quiz_state.get(lvl_id, {})
            score_txt = f" ({qs.get('score',0)}/10)" if qs.get("submitted") else ""
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:0.5rem;padding:0.25rem 0;font-size:0.72rem;">'
                f'<span>{st_icon}</span>'
                f'<span style="color:{color};font-family:Space Mono,monospace;">L{lvl_id}: {lvl["subtitle"]}{score_txt}</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        if st.button("🏠 Adventure Hub", use_container_width=True):
            st.session_state.view = "hub"
            st.rerun()
        if st.button("🚪 Log Out", use_container_width=True):
            save_user_progress(st.session_state.username)
            for k in ["logged_in","username","xp","completed_levels","quiz_state",
                      "cert_name","current_level","show_badge","view",
                      "streak","last_login","boss_battles_done"]:
                st.session_state.pop(k, None)
            st.rerun()

        # ── Streak display ──
        streak = st.session_state.get("streak", 0)
        if streak >= 2:
            st.markdown(
                f'<div class="streak-badge" style="display:block;text-align:center;margin-top:0.6rem;">'
                f'🔥 {streak}-Day Streak! &nbsp;·&nbsp; 1.2× XP Bonus</div>',
                unsafe_allow_html=True,
            )




# ============================================================
# HELPERS
# ============================================================
def is_level_unlocked(level_id):
    return level_id == 1 or (level_id - 1) in st.session_state.completed_levels

def level_status(level_id):
    if level_id in st.session_state.completed_levels: return "done"
    if is_level_unlocked(level_id): return "unlocked"
    return "locked"

def quiz_key(level_id, q_idx):
    return f"q_{level_id}_{q_idx}"

def get_exam_questions(level_id: int) -> list[dict]:
    """Return the 10 questions chosen for this user's exam.
    The selection is stored in quiz_state so it never changes mid-attempt."""
    qs_data = st.session_state.quiz_state.get(level_id, {})
    bank    = LEVELS[level_id]["questions"]  # 20 questions

    if "indices" in qs_data:
        # Already selected — restore same set
        indices = qs_data["indices"]
    else:
        # First visit — randomly choose 10
        indices = sorted(random.sample(range(len(bank)), QUESTIONS_PER_EXAM))
        # Store immediately so they persist
        if level_id not in st.session_state.quiz_state:
            st.session_state.quiz_state[level_id] = {}
        st.session_state.quiz_state[level_id]["indices"] = indices
        save_user_progress(st.session_state.username)

    return [bank[i] for i in indices], indices


# ============================================================
# LEADERBOARD
# ============================================================
def render_leaderboard():
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
    st.markdown(
        '<h2 style="font-family:Space Mono,monospace;font-size:1rem;color:#FFA000;margin-bottom:0.2rem;">🏆 Global Rankings</h2>'
        '<p style="font-size:0.75rem;color:#666;font-family:Space Mono,monospace;margin-bottom:0.8rem;">Top 10 adventurers ranked by total XP</p>',
        unsafe_allow_html=True,
    )
    db    = get_db()
    prog  = db.get("progress", {})
    users = db.get("users", {})

    ranked = sorted(
        [
            {
                "username": uname,
                "xp":       data.get("xp", 0),
                "levels":   len(data.get("completed_levels", [])),
                "streak":   data.get("streak", 0),
            }
            for uname, data in prog.items()
            if uname in users
        ],
        key=lambda r: r["xp"],
        reverse=True,
    )[:10]

    medal = {1: "🥇", 2: "🥈", 3: "🥉"}
    rows_html = ""
    for rank, row in enumerate(ranked, 1):
        is_me  = row["username"] == st.session_state.username
        title, icon = get_character_info(row["xp"])
        bg     = "rgba(98,0,238,0.12)" if is_me else "transparent"
        border = "1px solid #6200EE" if is_me else "none"
        streak_html = f'<span style="color:#FFA000;font-size:0.7rem;">🔥{row["streak"]}</span>' if row["streak"] >= 2 else ""
        rows_html += (
            f'<div class="leaderboard-row" style="background:{bg};border:{border};border-radius:4px;">'
            f'<span style="min-width:28px;color:#888;">{medal.get(rank, f"#{rank}")}</span>'
            f'<span style="min-width:20px;">{icon}</span>'
            f'<span style="flex:1;color:{"#00FF41" if is_me else "#E8E8E8"};">'
            f'{"<strong>" if is_me else ""}{row["username"]}{"</strong>" if is_me else ""}'
            f'{"&nbsp;(you)" if is_me else ""}</span>'
            f'{streak_html}'
            f'<span style="color:#9D46FF;min-width:60px;text-align:right;">{row["xp"]} XP</span>'
            f'<span style="color:#555;min-width:50px;text-align:right;">{row["levels"]}/5 lvl</span>'
            f'</div>'
        )

    if not ranked:
        rows_html = '<div style="color:#555;font-family:Space Mono,monospace;font-size:0.78rem;padding:1rem;">No adventurers yet. Be the first!</div>'

    st.markdown(
        f'<div class="card" style="padding:0.5rem;">{rows_html}</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# BOSS BATTLE
# ============================================================
def render_boss_battle(level_id: int):
    boss    = BOSS_BATTLES[level_id]
    beaten  = level_id in st.session_state.get("boss_battles_done", set())
    streak  = st.session_state.get("streak", 0)
    bonus   = streak >= 2

    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
    if beaten:
        st.markdown(
            f'<div class="success-box" style="text-align:center;">'
            f'<div style="font-size:1.5rem;margin-bottom:0.3rem;">{boss["icon"]}</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.85rem;">⚔️ {boss["title"]} DEFEATED</div>'
            f'<div style="font-size:0.75rem;margin-top:0.3rem;color:#888;">You already claimed the boss XP reward.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        return

    xp_reward = int(boss["xp_reward"] * 1.2) if bonus else boss["xp_reward"]
    bonus_html = f'<span style="color:#FFA000;"> (+20% streak bonus!)</span>' if bonus else ""

    st.markdown(
        f'<div class="boss-box">'
        f'<div style="font-family:Space Mono,monospace;font-size:0.6rem;color:#FF6666;letter-spacing:0.3em;">⚔️ BOSS BATTLE</div>'
        f'<div style="font-family:Space Mono,monospace;font-size:1.1rem;color:#fff;font-weight:700;margin:0.4rem 0;">'
        f'{boss["icon"]} {boss["title"]}</div>'
        f'<div style="color:#E8E8E8;font-size:0.85rem;margin-bottom:0.8rem;">{boss["flavor"]}</div>'
        f'<div class="info-box" style="font-size:0.8rem;">💡 Hint: {boss["hint"]}</div>'
        f'<div style="margin-top:0.6rem;font-family:Space Mono,monospace;font-size:0.72rem;color:#9D46FF;">'
        f'Reward: <strong style="color:#00FF41">+{xp_reward} XP</strong>{bonus_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    attempt = st.text_input(
        "Type your answer to defeat the boss:",
        placeholder="e.g.  .append()",
        key=f"boss_input_{level_id}",
    )
    if st.button(f"⚔️ Strike!", key=f"boss_submit_{level_id}"):
        if attempt.strip() == boss["answer"]:
            st.session_state.xp += xp_reward
            if "boss_battles_done" not in st.session_state:
                st.session_state.boss_battles_done = set()
            st.session_state.boss_battles_done.add(level_id)
            save_user_progress(st.session_state.username)
            st.balloons()
            st.markdown(
                f'<div class="milestone">'
                f'<div style="font-size:2.5rem;">{boss["icon"]}</div>'
                f'<div style="font-family:Space Mono,monospace;color:#FF4444;font-size:0.9rem;margin:0.5rem 0;">BOSS DEFEATED!</div>'
                f'<div style="color:#fff;font-size:0.82rem;">{boss["success_msg"]}</div>'
                f'<div style="margin-top:0.8rem;"><span class="xp-badge">+{xp_reward} XP earned 💾</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.rerun()
        else:
            st.markdown(
                '<div style="background:rgba(255,68,68,0.1);border-left:4px solid #FF4444;'
                'border-radius:0 8px 8px 0;padding:0.7rem 1rem;color:#FF8888;font-family:Space Mono,monospace;font-size:0.8rem;">'
                '💥 The boss deflects your attack! Check your spelling and try again.</div>',
                unsafe_allow_html=True,
            )


# ============================================================
# PRACTICE LAB  (right-column panel used in hub & level views)
# ============================================================
def render_practice_lab(default_code: str = ""):
    """Render the full-height Practice Lab sidebar panel."""

    # ── Panel header ──────────────────────────────────────────
    st.markdown(
        '<div class="lab-panel">'
        '<div class="lab-header">'
        '<span class="lab-header-dot" style="background:#FF5F57;"></span>'
        '<span class="lab-header-dot" style="background:#FEBC2E;"></span>'
        '<span class="lab-header-dot" style="background:#28C840;"></span>'
        '<span class="lab-title">⚗️ PRACTICE LAB</span>'
        '<span class="lab-filename">main.py</span>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    # ── Editor ────────────────────────────────────────────────
    st.markdown('<div class="lab-editor-wrap">', unsafe_allow_html=True)
    if "sandbox_code" not in st.session_state:
        st.session_state.sandbox_code = default_code or "# Start coding here!\nprint('Hello, World!')\n"

    code_input = st.text_area(
        "code",
        value=st.session_state.sandbox_code,
        height=320,
        key="sandbox_code",
        label_visibility="hidden",
        placeholder="# Write your Python here…\nprint('Hello, World!')",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Run button ────────────────────────────────────────────
    st.markdown('<div class="lab-run-wrap">', unsafe_allow_html=True)
    run_clicked = st.button("▶  Run Code", use_container_width=True, key="run_sandbox_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Console output ────────────────────────────────────────
    st.markdown(
        '<div class="lab-console-wrap">'
        '<div class="lab-console-header">▸ CONSOLE OUTPUT</div>',
        unsafe_allow_html=True,
    )

    if run_clicked:
        stdout_cap = io.StringIO()
        stderr_cap = io.StringIO()
        try:
            old_out, old_err = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = stdout_cap, stderr_cap
            exec(compile(code_input, "<sandbox>", "exec"), {})
            sys.stdout, sys.stderr = old_out, old_err
            out = stdout_cap.getvalue()
            err = stderr_cap.getvalue()
            if not out and not err:
                st.markdown('<div class="lab-console"><span class="lab-console-idle">(no output)</span></div>', unsafe_allow_html=True)
            else:
                err_part = f'<span class="lab-console-error">{err}</span>' if err else ""
                import html as _html
                safe_out = _html.escape(out)
                st.markdown(f'<div class="lab-console">{safe_out}{err_part}</div>', unsafe_allow_html=True)
        except Exception as exc:
            sys.stdout, sys.stderr = old_out, old_err
            import html as _html
            st.markdown(
                f'<div class="lab-console"><span class="lab-console-error">'
                f'{_html.escape(type(exc).__name__)}: {_html.escape(str(exc))}'
                f'</span></div>',
                unsafe_allow_html=True,
            )
    else:
        output_hist = st.session_state.get("_lab_last_output", "")
        if output_hist:
            st.markdown(f'<div class="lab-console">{output_hist}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="lab-console"><span class="lab-console-idle">'
                '# Output will appear here…\n# Try: print("Hello, World!")'
                '</span></div>',
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)  # close console-wrap


# ============================================================
# HUB
# ============================================================
def render_hub():
    col_main, col_lab = st.columns([3, 2], gap="large")

    with col_main:
        st.markdown(
            f'<h1 class="neon-heading" style="font-size:1.6rem;margin-bottom:0.2rem;">🐍 Python Coding Adventure</h1>'
            f'<p style="color:#888;font-family:Space Mono,monospace;font-size:0.75rem;">'
            f'Welcome back, <span style="color:#00FF41">@{st.session_state.username}</span> — choose your next mission!</p>',
            unsafe_allow_html=True,
        )
        st.markdown("<hr class='divider'/>", unsafe_allow_html=True)

        # ── Mission cards in 2 columns inside the left pane ──
        mission_cols = st.columns(2)
        for i, (lvl_id, lvl) in enumerate(LEVELS.items()):
            status = level_status(lvl_id)
            with mission_cols[i % 2]:
                border  = "#00FF41" if status=="done" else (lvl["color"] if status=="unlocked" else "#2A2A2A")
                shadow  = f"4px 4px 0 {border}" if status!="locked" else "none"
                opacity = "1" if status!="locked" else "0.4"
                lbl_txt = "✅ COMPLETE" if status=="done" else ("▶ PLAY" if status=="unlocked" else "🔒 LOCKED")
                lbl_col = "#00FF41" if status=="done" else ("#fff" if status=="unlocked" else "#555")
                sc_html = ""
                qs = st.session_state.quiz_state.get(lvl_id, {})
                if qs.get("submitted"):
                    sc = qs.get("score", 0)
                    passed_icon = "✅" if sc >= PASS_THRESHOLD else "❌"
                    sc_html = f'<div style="font-size:0.7rem;color:#888;margin-top:0.3rem;">{passed_icon} Score: {sc}/{QUESTIONS_PER_EXAM}</div>'
                # Glowing neon border for unlocked/done
                glow = f"box-shadow:{shadow},0 0 18px rgba(0,255,65,0.12);" if status=="done" else (f"box-shadow:{shadow};" if status!="locked" else "")
                st.markdown(
                    f'<div style="background:linear-gradient(160deg,#131313,#0F1A12);border:2px solid {border};'
                    f'border-radius:10px;padding:1rem;{glow}text-align:center;margin-bottom:0.6rem;opacity:{opacity};">'
                    f'<div style="font-size:2rem;margin-bottom:0.3rem;">{lvl["pixel_art"]}</div>'
                    f'<div style="font-family:Space Mono,monospace;font-size:0.58rem;color:{border};letter-spacing:0.2em;">LEVEL {lvl_id}</div>'
                    f'<div style="font-family:Space Mono,monospace;font-size:0.78rem;color:#fff;font-weight:700;margin:0.25rem 0;">{lvl["icon"]} {lvl["title"]}</div>'
                    f'<div style="font-size:0.68rem;color:#888;margin-bottom:0.5rem;">{lvl["subtitle"]}</div>'
                    f'<div style="font-family:Space Mono,monospace;font-size:0.6rem;color:{lbl_col};">{lbl_txt}</div>'
                    f'{sc_html}</div>',
                    unsafe_allow_html=True,
                )
                if status != "locked":
                    btn = "Review Level" if status=="done" else "Start Level"
                    if st.button(btn, key=f"hub_{lvl_id}", use_container_width=True):
                        st.session_state.view = "level"
                        st.session_state.current_level = lvl_id
                        st.rerun()

        st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
        xp = st.session_state.xp
        title, icon = get_character_info(xp)
        max_xp = sum(v["xp_reward"] for v in LEVELS.values())
        done   = len(st.session_state.completed_levels)
        stars  = sum(
            st.session_state.quiz_state.get(l, {}).get("score", 0)
            for l in st.session_state.completed_levels
        )

        for stat_col, val, label, sub, color in zip(
            st.columns(4),
            [f"{icon} {title}", str(xp), f"{done}/5", f"{stars}⭐"],
            ["Rank", "XP Earned", "Levels Done", "Stars"],
            ["Character class", f"of {max_xp} total", "Keep going!", "quiz correct"],
            ["#00FF41", "#9D46FF", "#00CFFF", "#FF6B6B"],
        ):
            with stat_col:
                st.markdown(
                    f'<div class="card" style="text-align:center;padding:1rem;">'
                    f'<div style="font-family:Space Mono,monospace;font-size:1.2rem;color:#fff;">{val}</div>'
                    f'<div style="font-family:Space Mono,monospace;font-size:0.72rem;color:{color};">{label}</div>'
                    f'<div style="font-size:0.68rem;color:#888;">{sub}</div></div>',
                    unsafe_allow_html=True,
                )

        render_leaderboard()

    with col_lab:
        render_practice_lab()


# ============================================================
# LEVEL VIEW
# ============================================================
def render_level(level_id):
    lvl = LEVELS[level_id]
    col_main, col_lab = st.columns([3, 2], gap="large")

    with col_main:
        if st.button("← Back to Hub"):
            st.session_state.view = "hub"
            st.rerun()
        st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;">'
            f'<div style="font-size:3rem;background:#111;border:2px solid #2A2A2A;border-radius:8px;'
            f'padding:0.3rem 0.8rem;box-shadow:3px 3px 0 #000;">{lvl["pixel_art"]}</div>'
            f'<div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.62rem;color:{lvl["color"]};'
            f'letter-spacing:0.25em;">LEVEL {level_id}</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:1.3rem;color:#fff;font-weight:700;">'
            f'{lvl["icon"]} {lvl["title"]}</div>'
            f'<div style="font-size:0.82rem;color:#888;">{lvl["subtitle"]}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
        if not is_level_unlocked(level_id):
            st.markdown(f'<div class="locked-box">🔒 Complete Level {level_id-1} first.</div>', unsafe_allow_html=True)
            with col_lab:
                render_practice_lab()
            return

        quiz_passed = level_id in st.session_state.completed_levels
        boss        = BOSS_BATTLES.get(level_id)
        boss_beaten = level_id in st.session_state.get("boss_battles_done", set())

        boss_label = "⚔️ Boss Battle ✅" if boss_beaten else ("⚔️ Boss Battle 🔓" if quiz_passed else "⚔️ Boss Battle 🔒")

        tab1, tab2, tab3, tab4 = st.tabs(["📖 Learn", "💻 Code Example", "🎯 Quiz (10 Q)", boss_label])
        with tab1:
            st.markdown(lvl["description"], unsafe_allow_html=False)
            st.markdown(f'<div class="info-box">💡 Complete the quiz to earn <strong style="color:#00FF41">+{lvl["xp_reward"]} XP</strong> — Pass mark: <strong>6/10 (60%)</strong></div>', unsafe_allow_html=True)
        with tab2:
            st.markdown('<p style="color:#888;font-size:0.8rem;font-family:Space Mono,monospace;">// Study this before the quiz</p>', unsafe_allow_html=True)
            st.code(lvl["code_example"], language="python")
        with tab3:
            render_quiz(level_id, lvl)
        with tab4:
            if not quiz_passed:
                st.markdown(
                    '<div class="locked-box">🔒 Pass the quiz first to unlock the Boss Battle and earn bonus XP!</div>',
                    unsafe_allow_html=True,
                )
            else:
                render_boss_battle(level_id)

    with col_lab:
        # Pre-seed the lab with the level's code example on first visit to this level
        lab_key = f"_lab_seeded_{level_id}"
        if lab_key not in st.session_state:
            st.session_state.sandbox_code = lvl["code_example"]
            st.session_state[lab_key] = True
        render_practice_lab(default_code=lvl["code_example"])


# ============================================================
# QUIZ
# ============================================================
def render_quiz(level_id, lvl):
    questions, _indices = get_exam_questions(level_id)
    qs_data   = st.session_state.quiz_state.get(level_id, {})
    passed    = level_id in st.session_state.completed_levels
    submitted = qs_data.get("submitted", False)
    score     = qs_data.get("score", 0)

    # ── Milestone badge ──
    if st.session_state.show_badge == level_id:
        st.balloons()
        xp_earned   = qs_data.get("xp_earned", lvl["xp_reward"])
        streak       = st.session_state.get("streak", 0)
        bonus_html   = ' <span style="color:#FFA000;font-size:0.75rem;">(🔥 streak bonus!)</span>' if streak >= 2 else ""
        st.markdown(
            f'<div class="milestone">'
            f'<div style="font-size:3rem;">🏆</div>'
            f'<div style="font-family:Space Mono,monospace;color:#00FF41;font-size:1rem;margin:0.5rem 0;">MILESTONE UNLOCKED!</div>'
            f'<div style="color:#fff;">{lvl["subtitle"]} Complete — Score: {score}/{QUESTIONS_PER_EXAM}</div>'
            f'<div style="margin-top:0.8rem;"><span class="xp-badge">+{xp_earned} XP saved 💾</span>{bonus_html}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.session_state.show_badge = None

    # ── Result banner ──
    if submitted:
        pct = int(score / QUESTIONS_PER_EXAM * 100)
        if passed:
            st.markdown(
                f'<div class="success-box">✅ Level PASSED! Score: {score}/{QUESTIONS_PER_EXAM} ({pct}%) — '
                f'Progress saved 💾</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="background:rgba(255,68,68,0.10);border-left:4px solid #FF4444;'
                f'border-radius:0 8px 8px 0;padding:0.9rem 1.2rem;margin:0.8rem 0;color:#FF8888;">'
                f'❌ Score: {score}/{QUESTIONS_PER_EXAM} ({pct}%) — Need 6/10 to pass. Try again!</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        f'<p style="font-family:Space Mono,monospace;font-size:0.78rem;color:#888;margin-bottom:1rem;">'
        f'Answer all {QUESTIONS_PER_EXAM} questions, then submit. Pass mark: {PASS_THRESHOLD}/{QUESTIONS_PER_EXAM} (60%)'
        f' — Questions are randomly selected from a bank of {QUESTIONS_IN_BANK}.</p>',
        unsafe_allow_html=True,
    )

    saved_answers = qs_data.get("answers", [None] * QUESTIONS_PER_EXAM)
    user_answers  = []

    for i, q in enumerate(questions):
        st.markdown(
            f'<div class="card" style="margin-bottom:0.6rem;">'
            f'<p style="font-family:Space Mono,monospace;font-size:0.82rem;color:#fff;margin:0 0 0.8rem;">'
            f'Q{i+1}/{QUESTIONS_PER_EXAM}: {q["q"]}</p></div>',
            unsafe_allow_html=True,
        )
        saved_val = saved_answers[i] if i < len(saved_answers) else None
        default_idx = q["options"].index(saved_val) if saved_val in q["options"] else 0
        disabled    = submitted and passed
        choice = st.radio(
            f"Q{i+1}", q["options"], index=default_idx,
            key=quiz_key(level_id, i), label_visibility="collapsed", disabled=disabled,
        )
        user_answers.append(choice)
        if submitted:
            if choice == q["answer"]:
                st.markdown(f'<div class="success-box">✅ Correct! <code>{q["answer"]}</code></div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div style="background:rgba(255,68,68,0.08);border-left:4px solid #FF4444;'
                    f'border-radius:0 8px 8px 0;padding:0.7rem 1rem;margin:0.4rem 0;color:#FF8888;">'
                    f'❌ Yours: <code>{choice}</code> — Correct: <code>{q["answer"]}</code></div>',
                    unsafe_allow_html=True,
                )
        st.markdown("")

    # ── Submit / Retry buttons ──
    if submitted and not passed:
        st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
        st.markdown('<p style="color:#FF8888;font-family:Space Mono,monospace;font-size:0.8rem;">You need 6/10 to pass. New random questions will be generated on retry.</p>', unsafe_allow_html=True)
        if st.button("🔄 Retry Quiz", key=f"retry_{level_id}"):
            # Clear this level's quiz state so new questions are drawn
            st.session_state.quiz_state.pop(level_id, None)
            save_user_progress(st.session_state.username)
            st.rerun()

    if not submitted:
        if st.button("⚡ Submit Answers", key=f"submit_{level_id}"):
            new_score = sum(1 for i, q in enumerate(questions) if user_answers[i] == q["answer"])
            new_passed = new_score >= PASS_THRESHOLD

            current = st.session_state.quiz_state.get(level_id, {})
            current.update({
                "answers":   user_answers,
                "submitted": True,
                "score":     new_score,
                "indices":   current.get("indices", []),
            })
            st.session_state.quiz_state[level_id] = current

            if new_passed and level_id not in st.session_state.completed_levels:
                streak     = st.session_state.get("streak", 0)
                xp_earned  = int(lvl["xp_reward"] * 1.2) if streak >= 2 else lvl["xp_reward"]
                st.session_state.xp += xp_earned
                st.session_state.completed_levels.add(level_id)
                st.session_state.show_badge = level_id
                # Store actual XP awarded so badge can display it
                current["xp_earned"] = xp_earned

            save_user_progress(st.session_state.username)
            st.rerun()

    if level_id == 5 and 5 in st.session_state.completed_levels:
        render_certificate()


# ============================================================
# CERTIFICATE
# ============================================================
def render_certificate():
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:Space Mono,monospace;font-size:1rem;color:#00FF41;margin-bottom:0.4rem;">🏅 Certificate of Completion</div>'
        '<p style="color:#888;font-size:0.85rem;">All 5 levels conquered! Enter your name to generate your certificate.</p>',
        unsafe_allow_html=True,
    )
    name_input = st.text_input("Your Name for the Certificate",
                               value=st.session_state.cert_name, placeholder="Enter your full name…")
    if name_input != st.session_state.cert_name:
        st.session_state.cert_name = name_input
        save_user_progress(st.session_state.username)

    if name_input.strip():
        title, icon = get_character_info(st.session_state.xp)
        done    = len(st.session_state.completed_levels)
        xp      = st.session_state.xp
        max_xp  = sum(v["xp_reward"] for v in LEVELS.values())
        date_str = datetime.now().strftime("%B %d, %Y")
        cert_html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<title>Python Coding Adventure — Certificate</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;700&display=swap');
body{{margin:0;padding:2rem;background:#0D0D0D;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:'DM Sans',sans-serif;color:#E8E8E8;}}
.cert{{width:760px;border:4px solid #00FF41;border-radius:16px;padding:3rem;background:#111;box-shadow:0 0 60px rgba(0,255,65,0.3),10px 10px 0 #000;text-align:center;position:relative;}}
.cert::before{{content:'';position:absolute;inset:12px;border:1px dashed rgba(0,255,65,0.2);border-radius:10px;pointer-events:none;}}
.logo{{font-family:'Space Mono',monospace;font-size:0.75rem;color:#00FF41;letter-spacing:0.3em;margin-bottom:0.5rem;}}
.title{{font-family:'Space Mono',monospace;font-size:2rem;color:#00FF41;text-shadow:0 0 20px rgba(0,255,65,0.5);margin:0.5rem 0;}}
.sub{{color:#888;font-size:0.9rem;margin-bottom:2rem;}}
hr{{border:none;border-top:1px solid #2A2A2A;margin:1.5rem 0;}}
.label{{font-size:0.8rem;color:#666;text-transform:uppercase;letter-spacing:0.15em;}}
.hero{{font-family:'Space Mono',monospace;font-size:2.5rem;color:#fff;margin:0.3rem 0 1.5rem;}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1.5rem 0;}}
.stat{{background:#1A1A1A;border:1px solid #2A2A2A;border-radius:8px;padding:1rem;}}
.stat .v{{font-family:'Space Mono',monospace;font-size:1.4rem;color:#00FF41;}}
.stat .l{{font-size:0.75rem;color:#666;margin-top:0.2rem;}}
.badge{{display:inline-block;background:#6200EE;border:2px solid #000;border-radius:6px;padding:0.4rem 1.2rem;font-family:'Space Mono',monospace;font-size:0.8rem;color:#fff;box-shadow:3px 3px 0 #000;margin-top:1rem;}}
.footer{{margin-top:2rem;font-size:0.72rem;color:#555;font-family:'Space Mono',monospace;}}
</style></head><body>
<div class="cert">
  <div class="logo">🐍 PYTHON CODING ADVENTURE</div>
  <div class="title">Certificate of Completion</div>
  <div class="sub">This certifies that the following adventurer has conquered the Python Realm</div>
  <hr/>
  <div class="label">Presented to</div>
  <div class="hero">{name_input.strip()}</div>
  <div class="grid">
    <div class="stat"><div class="v">{xp}/{max_xp}</div><div class="l">XP Earned</div></div>
    <div class="stat"><div class="v">{done}/5</div><div class="l">Levels Completed</div></div>
    <div class="stat"><div class="v">{icon} {title}</div><div class="l">Final Rank</div></div>
  </div>
  <hr/>
  <div class="badge">✅ Python Basics Mastered — 60% Pass Standard</div>
  <div class="footer">Issued on {date_str} &nbsp;|&nbsp; Python Coding Adventure &nbsp;|&nbsp; Powered by Streamlit</div>
</div></body></html>"""
        b64   = base64.b64encode(cert_html.encode()).decode()
        fname = f"python_cert_{name_input.strip().replace(' ','_')}.html"
        st.markdown(
            f'<a href="data:text/html;base64,{b64}" download="{fname}" style="text-decoration:none;">'
            f'<div style="display:inline-block;background:#00FF41;color:#000;font-family:Space Mono,monospace;'
            f'font-weight:700;border:2px solid #000;border-radius:8px;box-shadow:4px 4px 0 #000;'
            f'padding:0.6rem 1.4rem;cursor:pointer;margin-top:0.5rem;">📥 Download Certificate</div></a>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div style="color:#666;font-size:0.82rem;font-style:italic;">↑ Enter your name to unlock the download.</div>', unsafe_allow_html=True)


# ============================================================
# MAIN
# ============================================================
def main():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    init_state()

    if not st.session_state.logged_in:
        render_auth()
        return

    render_sidebar()

    if st.session_state.view == "hub":
        render_hub()
    elif st.session_state.view == "level":
        render_level(st.session_state.current_level)


if __name__ == "__main__":
    main()
