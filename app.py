import streamlit as st
import base64
from datetime import datetime

# ============================================================
# PAGE CONFIG — must be first Streamlit call
# ============================================================
st.set_page_config(
    page_title="Python Coding Adventure",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS  ─ CodeDex / Neubrutalism Dark Theme
# ============================================================
CUSTOM_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Press+Start+2P&family=DM+Sans:wght@400;500;700&display=swap');

  /* ── Root variables ── */
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
    --shadow:  4px 4px 0px #000;
    --shadow-neon: 4px 4px 0px #00FF41;
    --shadow-purple: 4px 4px 0px #6200EE;
    --radius:  8px;
  }

  /* ── Global reset ── */
  .stApp { background: var(--bg) !important; font-family: 'DM Sans', sans-serif; color: var(--text); }
  .block-container { padding: 1.5rem 2rem !important; max-width: 1100px; }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .stDeployButton { display: none; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: #0A0A0A !important;
    border-right: 2px solid var(--border);
  }
  [data-testid="stSidebar"] .block-container { padding: 1rem !important; }

  /* ── Typography ── */
  h1, h2, h3 { font-family: 'Space Mono', monospace !important; }
  .pixel-font  { font-family: 'Press Start 2P', monospace !important; }

  /* ── Buttons — Neubrutalism style ── */
  .stButton > button {
    background: var(--neon) !important;
    color: #000 !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    border: 2px solid #000 !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow) !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.1s ease !important;
    letter-spacing: 0.04em;
  }
  .stButton > button:hover {
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0px #000 !important;
  }
  .stButton > button:active {
    transform: translate(2px, 2px) !important;
    box-shadow: 2px 2px 0px #000 !important;
  }
  .stButton > button:disabled {
    background: #333 !important;
    color: #666 !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
  }

  /* ── Radio buttons ── */
  .stRadio > label { color: var(--text) !important; font-family: 'DM Sans', sans-serif; }
  .stRadio [data-testid="stMarkdownContainer"] p { color: var(--text) !important; }

  /* ── Cards ── */
  .card {
    background: var(--card);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
  }
  .card-purple {
    background: var(--card);
    border: 2px solid var(--purple);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-purple);
    margin-bottom: 1rem;
  }
  .card-neon {
    background: var(--card);
    border: 2px solid var(--neon);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-neon);
    margin-bottom: 1rem;
  }

  /* ── Level cards in grid ── */
  .level-card {
    background: var(--card2);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem;
    box-shadow: var(--shadow);
    text-align: center;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .level-card:hover { transform: translate(-2px,-2px); box-shadow: 6px 6px 0px #000; }
  .level-card.locked { opacity: 0.45; cursor: not-allowed; }
  .level-card.done   { border-color: var(--neon); box-shadow: var(--shadow-neon); }

  /* ── Code blocks ── */
  .stCodeBlock, pre, code {
    font-family: 'Space Mono', monospace !important;
    background: #111 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: var(--radius) !important;
  }

  /* ── Progress bar ── */
  .stProgress > div > div { background: var(--neon) !important; }
  .stProgress { filter: drop-shadow(0 0 6px var(--neon)); }

  /* ── XP Badge ── */
  .xp-badge {
    display: inline-block;
    background: var(--purple);
    color: #fff;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.3rem 0.8rem;
    border: 2px solid #000;
    border-radius: 4px;
    box-shadow: 2px 2px 0px #000;
  }

  /* ── Milestone badge ── */
  .milestone {
    background: linear-gradient(135deg, #6200EE, #9D46FF);
    border: 3px solid var(--neon);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 0 30px rgba(0,255,65,0.3), 6px 6px 0px #000;
    margin: 1rem 0;
  }

  /* ── Pixel icon box ── */
  .pixel-icon {
    font-size: 2.5rem;
    background: #111;
    border: 2px solid var(--border);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    display: inline-block;
    box-shadow: var(--shadow);
    margin-bottom: 0.5rem;
  }

  /* ── Neon heading ── */
  .neon-heading {
    color: var(--neon);
    text-shadow: 0 0 12px rgba(0,255,65,0.5);
    font-family: 'Space Mono', monospace;
  }

  /* ── Section divider ── */
  .divider {
    border: none;
    border-top: 2px solid var(--border);
    margin: 1.5rem 0;
  }

  /* ── Info box ── */
  .info-box {
    background: rgba(98,0,238,0.12);
    border-left: 4px solid var(--purple2);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 0.9rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.92rem;
  }

  /* ── Success box ── */
  .success-box {
    background: rgba(0,255,65,0.08);
    border-left: 4px solid var(--neon);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 0.9rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.92rem;
    color: var(--neon);
  }

  /* ── Warning/locked box ── */
  .locked-box {
    background: rgba(255,100,0,0.08);
    border: 2px dashed #FF6400;
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    text-align: center;
    color: #FF6400;
  }

  /* ── Sidebar stat row ── */
  .stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border);
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
  }

  /* ── Certificate box ── */
  .cert-wrapper {
    border: 3px solid var(--neon);
    border-radius: 12px;
    padding: 2rem;
    background: #0A0A0A;
    box-shadow: 0 0 40px rgba(0,255,65,0.2), 8px 8px 0 #000;
    text-align: center;
  }

  /* ── Selectbox ── */
  .stSelectbox > div > div {
    background: var(--card) !important;
    border: 2px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
  }

  /* ── Text input ── */
  .stTextInput > div > div > input {
    background: var(--card) !important;
    border: 2px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
    font-family: 'Space Mono', monospace !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: var(--neon) !important;
    box-shadow: 0 0 0 1px var(--neon) !important;
  }

  /* ── Tab styling ── */
  .stTabs [data-baseweb="tab-list"] {
    background: transparent;
    gap: 0.5rem;
  }
  .stTabs [data-baseweb="tab"] {
    background: var(--card2) !important;
    border: 2px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--muted) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
  }
  .stTabs [aria-selected="true"] {
    background: var(--purple) !important;
    border-color: var(--purple) !important;
    color: #fff !important;
  }
  .stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding: 1rem 0 !important;
  }
</style>
"""

# ============================================================
# CURRICULUM DATA
# ============================================================
LEVELS = {
    1: {
        "title": "Variables & Data Types",
        "subtitle": "The Foundation",
        "icon": "🧱",
        "pixel_art": "🔢",
        "color": "#00FF41",
        "xp_reward": 50,
        "description": """
Variables are like **labeled boxes** that store information. Python automatically detects the type of data you put in them — no need to declare types explicitly!

**Core Data Types:**
- `int` → Whole numbers: `42`, `-7`, `0`
- `float` → Decimals: `3.14`, `-0.5`
- `str` → Text in quotes: `"Hello"`, `'World'`
- `bool` → Truth values: `True`, `False`

Use `type()` to inspect any variable's type, and `print()` to display output.
        """,
        "code_example": '''# 🐍 Variables & Data Types

name = "Alex"          # str
level = 1              # int
xp_multiplier = 1.5    # float
is_hero = True         # bool

# Print with f-strings (modern Python!)
print(f"Player: {name}")
print(f"Level:  {level}")
print(f"Type of xp_multiplier: {type(xp_multiplier)}")

# Type conversion
score_str = "250"
score_int = int(score_str)
print(f"Score doubled: {score_int * 2}")
''',
        "questions": [
            {
                "q": "What data type is the value `3.14` in Python?",
                "options": ["int", "float", "str", "bool"],
                "answer": "float",
            },
            {
                "q": "Which of the following is a valid Python variable name?",
                "options": ["2nd_player", "player-name", "player_name", "class"],
                "answer": "player_name",
            },
            {
                "q": "What does `type('Hello')` return?",
                "options": ["<class 'str'>", "<class 'int'>", "str", "String"],
                "answer": "<class 'str'>",
            },
        ],
    },
    2: {
        "title": "Logic & Loops",
        "subtitle": "The Path",
        "icon": "🔀",
        "pixel_art": "♾️",
        "color": "#9D46FF",
        "xp_reward": 60,
        "description": """
Control flow lets your program **make decisions** and **repeat actions**. These are the building blocks of all real programs.

**Conditionals (`if / elif / else`):**
Execute code only when a condition is `True`.

**Loops:**
- `for` loop → Iterate over a sequence a known number of times
- `while` loop → Repeat *as long as* a condition remains `True`

**Comparison operators:** `==`, `!=`, `<`, `>`, `<=`, `>=`
**Logical operators:** `and`, `or`, `not`
        """,
        "code_example": '''# 🔀 Logic & Loops

# --- If / elif / else ---
score = 85

if score >= 90:
    grade = "S-Rank"
elif score >= 70:
    grade = "A-Rank"
elif score >= 50:
    grade = "B-Rank"
else:
    grade = "Try Again"

print(f"Your grade: {grade}")

# --- For loop ---
print("\\nCounting loot:")
for i in range(1, 6):
    print(f"  Item #{i} collected!")

# --- While loop ---
health = 100
damage_per_hit = 30
hits = 0
while health > 0:
    health -= damage_per_hit
    hits += 1
print(f"\\nKO after {hits} hits!")
''',
        "questions": [
            {
                "q": "What does `range(0, 5)` produce?",
                "options": [
                    "0, 1, 2, 3, 4, 5",
                    "0, 1, 2, 3, 4",
                    "1, 2, 3, 4, 5",
                    "1, 2, 3, 4",
                ],
                "answer": "0, 1, 2, 3, 4",
            },
            {
                "q": "Which keyword is used to exit a loop early?",
                "options": ["exit", "stop", "break", "return"],
                "answer": "break",
            },
            {
                "q": "What is the result of `not True`?",
                "options": ["True", "False", "None", "Error"],
                "answer": "False",
            },
        ],
    },
    3: {
        "title": "Lists & Dictionaries",
        "subtitle": "The Inventory",
        "icon": "🎒",
        "pixel_art": "📦",
        "color": "#00CFFF",
        "xp_reward": 70,
        "description": """
**Lists** are ordered, mutable sequences. Think of them as your adventurer's **item bag** — you can add, remove, and rearrange items.

**Dictionaries** are key-value stores. Think of them as a **character sheet** — each stat has a named label.

**Key list operations:** `append()`, `remove()`, `pop()`, `len()`, slicing `[start:end]`
**Key dict operations:** `dict[key]`, `dict.get(key)`, `dict.keys()`, `dict.values()`, `dict.items()`
        """,
        "code_example": '''# 🎒 Lists & Dictionaries

# ── Lists ──
inventory = ["sword", "shield", "potion"]
inventory.append("map")          # Add item
inventory.remove("shield")       # Remove item
print(f"Inventory: {inventory}")
print(f"First item: {inventory[0]}")
print(f"Last item:  {inventory[-1]}")
print(f"Bag size:   {len(inventory)}")

# List comprehension (Pythonic!)
powered_up = [item.upper() for item in inventory]
print(f"Powered: {powered_up}")

# ── Dictionaries ──
hero = {
    "name": "Alex",
    "hp": 100,
    "mp": 50,
    "class": "Wizard",
}
print(f"\\nHero: {hero['name']} ({hero['class']})")
hero["level"] = 5           # Add new key
hero["hp"] = 120            # Update value

for stat, value in hero.items():
    print(f"  {stat}: {value}")
''',
        "questions": [
            {
                "q": "How do you add an element to the END of a list called `my_list`?",
                "options": [
                    "my_list.add(x)",
                    "my_list.append(x)",
                    "my_list.insert(x)",
                    "my_list.push(x)",
                ],
                "answer": "my_list.append(x)",
            },
            {
                "q": "What does `my_dict.get('key', 'default')` do if 'key' doesn't exist?",
                "options": [
                    "Raises a KeyError",
                    "Returns None",
                    "Returns 'default'",
                    "Returns an empty string",
                ],
                "answer": "Returns 'default'",
            },
            {
                "q": "What is the output of `[x*2 for x in [1,2,3]]`?",
                "options": [
                    "[1, 2, 3]",
                    "[2, 4, 6]",
                    "(2, 4, 6)",
                    "[1, 4, 9]",
                ],
                "answer": "[2, 4, 6]",
            },
        ],
    },
    4: {
        "title": "Functions",
        "subtitle": "The Spells",
        "icon": "✨",
        "pixel_art": "🪄",
        "color": "#FF6B6B",
        "xp_reward": 80,
        "description": """
**Functions** are reusable blocks of code — your hero's **spellbook**. Define once, cast anywhere.

**Anatomy of a function:**
- `def` keyword to define it
- **Parameters** receive input values
- `return` sends a value back to the caller
- **Default parameters** provide fallback values
- **`*args` / `**kwargs`** for flexible argument counts

Good functions are **small**, **focused**, and have **descriptive names**.
        """,
        "code_example": '''# ✨ Functions — The Spells

# ── Basic function ──
def greet(name):
    return f"Welcome, {name}! Your quest begins."

# ── Default parameters ──
def cast_spell(spell_name, power=10, critical=False):
    damage = power * (2 if critical else 1)
    return f"⚡ {spell_name} deals {damage} damage!"

# ── *args for variable inputs ──
def total_xp(*xp_gains):
    return sum(xp_gains)

# ── Calling functions ──
print(greet("Alex"))
print(cast_spell("Fireball", power=25))
print(cast_spell("Lightning", power=30, critical=True))
print(f"Total XP gained: {total_xp(50, 30, 20, 15)}")

# ── Lambda (one-liner function) ──
double = lambda x: x * 2
print(f"Double 7 = {double(7)}")

# ── Docstring ──
def calculate_level(xp):
    """Return player level based on XP points."""
    return max(1, xp // 100)

help(calculate_level)
''',
        "questions": [
            {
                "q": "What keyword is used to define a function in Python?",
                "options": ["function", "func", "def", "define"],
                "answer": "def",
            },
            {
                "q": "What does a function return if it has no `return` statement?",
                "options": ["0", "False", "None", "An error"],
                "answer": "None",
            },
            {
                "q": "What is `lambda x: x ** 2` equivalent to?",
                "options": [
                    "def f(x): x ** 2",
                    "def f(x): return x ** 2",
                    "def f(): return x ** 2",
                    "lambda: x ** 2",
                ],
                "answer": "def f(x): return x ** 2",
            },
        ],
    },
    5: {
        "title": "The Final Boss",
        "subtitle": "Comprehensive Python Basics Test",
        "icon": "🐉",
        "pixel_art": "💀",
        "color": "#FF4444",
        "xp_reward": 100,
        "description": """
You've studied the ancient texts. You've mastered the four disciplines.
Now face **The Final Boss** — a comprehensive gauntlet that tests every skill you've acquired.

This challenge mixes **Variables**, **Logic & Loops**, **Lists & Dictionaries**, and **Functions** into 3 synthesis questions. Answer correctly to claim your **Python Master Certificate**.

*There is no shame in reviewing previous levels before proceeding. The wise hero prepares.*
        """,
        "code_example": '''# 🐉 Final Boss — All Skills Combined

def analyze_party(members: list[dict]) -> dict:
    """
    Analyzes a list of hero dicts and returns
    party statistics. Combines all Python basics!
    """
    if not members:
        return {"error": "Empty party!"}

    total_hp   = sum(m["hp"] for m in members)
    avg_hp     = total_hp / len(members)
    max_hero   = max(members, key=lambda m: m["hp"])
    alive      = [m["name"] for m in members if m["hp"] > 0]
    class_count = {}
    for m in members:
        cls = m.get("class", "Unknown")
        class_count[cls] = class_count.get(cls, 0) + 1

    return {
        "total_hp":   total_hp,
        "average_hp": round(avg_hp, 2),
        "strongest":  max_hero["name"],
        "alive":      alive,
        "classes":    class_count,
    }

party = [
    {"name": "Alex",  "hp": 120, "class": "Wizard"},
    {"name": "Sam",   "hp": 95,  "class": "Rogue"},
    {"name": "Jordan","hp": 0,   "class": "Wizard"},
]
stats = analyze_party(party)
for key, val in stats.items():
    print(f"{key:12s}: {val}")
''',
        "questions": [
            {
                "q": "What does `max([3,1,4,1,5,9], key=lambda x: -x)` return?",
                "options": ["9", "1", "3", "-9"],
                "answer": "1",
            },
            {
                "q": "Which line correctly unpacks a dictionary into keyword arguments?",
                "options": [
                    "func(*my_dict)",
                    "func(**my_dict)",
                    "func(my_dict...)",
                    "func(#my_dict)",
                ],
                "answer": "func(**my_dict)",
            },
            {
                "q": "What is the time complexity of looking up a key in a Python dict?",
                "options": ["O(n)", "O(log n)", "O(1)", "O(n²)"],
                "answer": "O(1)",
            },
        ],
    },
}

# ============================================================
# XP / CHARACTER LEVEL SYSTEM
# ============================================================
XP_TIERS = [
    (0,   "Apprentice",  "🌱"),
    (50,  "Coder",       "💻"),
    (120, "Wizard",      "🧙"),
    (200, "Sorcerer",    "🔮"),
    (300, "Python Master","🐍"),
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


# ============================================================
# SESSION STATE INITIALISATION
# ============================================================
def init_state():
    defaults = {
        "xp": 0,
        "completed_levels": set(),
        "current_level": 1,
        "quiz_state": {},       # {level_id: {"answers": [], "submitted": bool, "score": int}}
        "show_badge": None,     # level_id to animate badge for
        "cert_name": "",
        "view": "hub",          # "hub" | "level"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ============================================================
# HELPERS
# ============================================================
def is_level_unlocked(level_id: int) -> bool:
    if level_id == 1:
        return True
    return (level_id - 1) in st.session_state.completed_levels


def level_status(level_id: int) -> str:
    if level_id in st.session_state.completed_levels:
        return "done"
    if is_level_unlocked(level_id):
        return "unlocked"
    return "locked"


def quiz_key(level_id: int, q_idx: int) -> str:
    return f"q_{level_id}_{q_idx}"


# ============================================================
# CERTIFICATE GENERATOR
# ============================================================
def build_certificate_html(name: str, xp: int, date_str: str) -> str:
    levels_done = len(st.session_state.completed_levels)
    title, icon = get_character_info(xp)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>Python Coding Adventure — Certificate</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;700&display=swap');
  body {{
    margin:0; padding:0;
    background: #0D0D0D;
    display: flex; justify-content: center; align-items: center;
    min-height: 100vh;
    font-family: 'DM Sans', sans-serif;
    color: #E8E8E8;
  }}
  .cert {{
    width: 780px;
    border: 4px solid #00FF41;
    border-radius: 16px;
    padding: 3rem;
    background: #111;
    box-shadow: 0 0 60px rgba(0,255,65,0.3), 10px 10px 0 #000;
    text-align: center;
    position: relative;
  }}
  .cert::before {{
    content: '';
    position: absolute;
    inset: 12px;
    border: 1px dashed rgba(0,255,65,0.25);
    border-radius: 10px;
    pointer-events: none;
  }}
  .logo {{ font-family: 'Space Mono', monospace; font-size: 0.75rem; color: #00FF41; letter-spacing: 0.3em; text-transform: uppercase; margin-bottom: 0.5rem; }}
  .cert-title {{ font-family: 'Space Mono', monospace; font-size: 2rem; color: #00FF41; text-shadow: 0 0 20px rgba(0,255,65,0.5); margin: 0.5rem 0; }}
  .subtitle {{ color: #888; font-size: 0.9rem; margin-bottom: 2rem; }}
  .divider {{ border: none; border-top: 1px solid #2A2A2A; margin: 1.5rem 0; }}
  .label {{ font-size: 0.8rem; color: #666; text-transform: uppercase; letter-spacing: 0.15em; }}
  .hero-name {{ font-family: 'Space Mono', monospace; font-size: 2.5rem; color: #fff; margin: 0.3rem 0 1.5rem; }}
  .achievement-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1.5rem 0; }}
  .achievement {{ background: #1A1A1A; border: 1px solid #2A2A2A; border-radius: 8px; padding: 1rem; }}
  .achievement .val {{ font-family: 'Space Mono', monospace; font-size: 1.4rem; color: #00FF41; }}
  .achievement .lbl {{ font-size: 0.75rem; color: #666; margin-top: 0.2rem; }}
  .badge {{ display: inline-block; background: #6200EE; border: 2px solid #000; border-radius: 6px; padding: 0.4rem 1.2rem; font-family: 'Space Mono', monospace; font-size: 0.8rem; color: #fff; box-shadow: 3px 3px 0 #000; margin-top: 1rem; }}
  .footer {{ margin-top: 2rem; font-size: 0.75rem; color: #555; font-family: 'Space Mono', monospace; }}
</style>
</head>
<body>
<div class="cert">
  <div class="logo">🐍 Python Coding Adventure</div>
  <div class="cert-title">Certificate of Completion</div>
  <div class="subtitle">This certifies that the following adventurer has conquered the Python Realm</div>
  <hr class="divider"/>
  <div class="label">Presented to</div>
  <div class="hero-name">{name or "Brave Adventurer"}</div>
  <div class="achievement-grid">
    <div class="achievement">
      <div class="val">{xp}</div>
      <div class="lbl">Total XP Earned</div>
    </div>
    <div class="achievement">
      <div class="val">{levels_done}/5</div>
      <div class="lbl">Levels Completed</div>
    </div>
    <div class="achievement">
      <div class="val">{icon} {title}</div>
      <div class="lbl">Final Rank</div>
    </div>
  </div>
  <hr class="divider"/>
  <div class="badge">✅ Python Basics Mastered</div>
  <div class="footer">
    Issued on {date_str} &nbsp;|&nbsp; Python Coding Adventure &nbsp;|&nbsp; Powered by Streamlit
  </div>
</div>
</body>
</html>"""


def get_download_link(html: str, filename: str, label: str) -> str:
    b64 = base64.b64encode(html.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}" style="text-decoration:none;">'
    button_html = (
        f'{href}<div class="stButton"><button style="'
        f'background:#00FF41;color:#000;font-family:Space Mono,monospace;'
        f'font-weight:700;border:2px solid #000;border-radius:8px;'
        f'box-shadow:4px 4px 0 #000;padding:0.6rem 1.4rem;cursor:pointer;'
        f'font-size:0.85rem;">{label}</button></div></a>'
    )
    return button_html


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    xp = st.session_state.xp
    title, icon = get_character_info(xp)
    progress = xp_to_progress(xp)
    completed = len(st.session_state.completed_levels)
    max_xp = sum(v["xp_reward"] for v in LEVELS.values())

    with st.sidebar:
        st.markdown(
            '<p class="pixel-font" style="font-size:0.55rem;color:#00FF41;'
            'text-align:center;letter-spacing:0.2em;">PYTHON ADVENTURE</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="text-align:center;padding:0.8rem 0;">'
            f'<div style="font-size:3rem;">{icon}</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.9rem;color:#fff;'
            f'font-weight:700;">{title}</div>'
            f'<div style="font-size:0.75rem;color:#888;margin-top:0.2rem;">Your Character</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # XP Bar
        st.markdown(
            f'<div class="stat-row"><span style="color:#888">XP</span>'
            f'<span class="xp-badge">{xp} / {max_xp}</span></div>',
            unsafe_allow_html=True,
        )
        st.progress(progress)

        st.markdown(
            f'<div class="stat-row"><span style="color:#888">Levels Done</span>'
            f'<span style="color:#00FF41;font-family:Space Mono,monospace;">'
            f'{completed} / 5</span></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(
            '<p style="font-family:Space Mono,monospace;font-size:0.7rem;'
            'color:#666;margin-bottom:0.5rem;">LEVEL MAP</p>',
            unsafe_allow_html=True,
        )

        for lvl_id, lvl in LEVELS.items():
            status = level_status(lvl_id)
            status_icon = "✅" if status == "done" else ("🔓" if status == "unlocked" else "🔒")
            color = "#00FF41" if status == "done" else ("#E8E8E8" if status == "unlocked" else "#555")
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:0.5rem;'
                f'padding:0.3rem 0;font-size:0.75rem;">'
                f'<span>{status_icon}</span>'
                f'<span style="color:{color};font-family:Space Mono,monospace;">'
                f'L{lvl_id}: {lvl["subtitle"]}</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        if st.button("🏠 Adventure Hub", use_container_width=True):
            st.session_state.view = "hub"
            st.rerun()


# ============================================================
# HUB VIEW
# ============================================================
def render_hub():
    st.markdown(
        '<h1 class="neon-heading" style="font-size:1.6rem;margin-bottom:0.2rem;">'
        '🐍 Python Coding Adventure</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#888;font-family:Space Mono,monospace;font-size:0.78rem;">'
        'Choose your next mission. Complete levels in order to unlock new challenges.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)

    cols = st.columns(3)
    level_ids = list(LEVELS.keys())

    for i, lvl_id in enumerate(level_ids):
        lvl = LEVELS[lvl_id]
        status = level_status(lvl_id)
        col = cols[i % 3]

        with col:
            border_color = (
                "#00FF41" if status == "done"
                else (lvl["color"] if status == "unlocked" else "#2A2A2A")
            )
            shadow = (
                "4px 4px 0 #00FF41" if status == "done"
                else ("4px 4px 0 #000" if status == "unlocked" else "none")
            )
            opacity = "1" if status != "locked" else "0.4"

            status_label = "✅ COMPLETE" if status == "done" else ("▶ PLAY" if status == "unlocked" else "🔒 LOCKED")
            label_color = "#00FF41" if status == "done" else ("#fff" if status == "unlocked" else "#555")

            score_html = ""
            if lvl_id in st.session_state.quiz_state:
                qs = st.session_state.quiz_state[lvl_id]
                if qs.get("submitted"):
                    sc = qs.get("score", 0)
                    score_html = f'<div style="font-size:0.7rem;color:#888;margin-top:0.3rem;">Score: {sc}/3 ⭐</div>'

            st.markdown(
                f'<div style="background:#181818;border:2px solid {border_color};'
                f'border-radius:8px;padding:1.2rem;box-shadow:{shadow};'
                f'text-align:center;margin-bottom:0.8rem;opacity:{opacity};">'
                f'<div style="font-size:2.2rem;margin-bottom:0.4rem;">{lvl["pixel_art"]}</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:0.65rem;'
                f'color:{border_color};letter-spacing:0.2em;">LEVEL {lvl_id}</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:0.82rem;'
                f'color:#fff;font-weight:700;margin:0.3rem 0;">{lvl["title"]}</div>'
                f'<div style="font-size:0.72rem;color:#888;margin-bottom:0.6rem;">{lvl["subtitle"]}</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:0.65rem;'
                f'color:{label_color};">{status_label}</div>'
                f'{score_html}'
                f'</div>',
                unsafe_allow_html=True,
            )

            if status != "locked":
                btn_label = "Review" if status == "done" else "Start Level"
                if st.button(btn_label, key=f"hub_btn_{lvl_id}", use_container_width=True):
                    st.session_state.view = "level"
                    st.session_state.current_level = lvl_id
                    st.rerun()

    # Stats row
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    xp = st.session_state.xp
    title, icon = get_character_info(xp)
    max_xp = sum(v["xp_reward"] for v in LEVELS.values())

    with m1:
        st.markdown(
            f'<div class="card" style="text-align:center;padding:1rem;">'
            f'<div style="font-size:1.8rem;">{icon}</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.75rem;color:#00FF41;">{title}</div>'
            f'<div style="font-size:0.7rem;color:#888;">Rank</div></div>',
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f'<div class="card" style="text-align:center;padding:1rem;">'
            f'<div style="font-family:Space Mono,monospace;font-size:1.6rem;color:#fff;">{xp}</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.75rem;color:#9D46FF;">XP Earned</div>'
            f'<div style="font-size:0.7rem;color:#888;">of {max_xp} total</div></div>',
            unsafe_allow_html=True,
        )
    with m3:
        done = len(st.session_state.completed_levels)
        st.markdown(
            f'<div class="card" style="text-align:center;padding:1rem;">'
            f'<div style="font-family:Space Mono,monospace;font-size:1.6rem;color:#fff;">{done}/5</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.75rem;color:#00CFFF;">Levels Done</div>'
            f'<div style="font-size:0.7rem;color:#888;">Keep going!</div></div>',
            unsafe_allow_html=True,
        )
    with m4:
        stars = sum(
            st.session_state.quiz_state.get(l, {}).get("score", 0)
            for l in st.session_state.completed_levels
        )
        st.markdown(
            f'<div class="card" style="text-align:center;padding:1rem;">'
            f'<div style="font-family:Space Mono,monospace;font-size:1.6rem;color:#fff;">{stars}⭐</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.75rem;color:#FF6B6B;">Stars</div>'
            f'<div style="font-size:0.7rem;color:#888;">quiz correct</div></div>',
            unsafe_allow_html=True,
        )


# ============================================================
# LEVEL VIEW
# ============================================================
def render_level(level_id: int):
    lvl = LEVELS[level_id]
    status = level_status(level_id)

    # Back button
    if st.button("← Back to Hub"):
        st.session_state.view = "hub"
        st.rerun()

    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)

    # Header
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;">'
        f'<div style="font-size:3rem;background:#111;border:2px solid #2A2A2A;'
        f'border-radius:8px;padding:0.3rem 0.8rem;box-shadow:3px 3px 0 #000;">'
        f'{lvl["pixel_art"]}</div>'
        f'<div>'
        f'<div style="font-family:Space Mono,monospace;font-size:0.65rem;'
        f'color:{lvl["color"]};letter-spacing:0.25em;">LEVEL {level_id}</div>'
        f'<div style="font-family:Space Mono,monospace;font-size:1.3rem;'
        f'color:#fff;font-weight:700;">{lvl["icon"]} {lvl["title"]}</div>'
        f'<div style="font-size:0.82rem;color:#888;">{lvl["subtitle"]}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    if not is_level_unlocked(level_id):
        st.markdown(
            f'<div class="locked-box">🔒 Complete Level {level_id-1} first to unlock this level.</div>',
            unsafe_allow_html=True,
        )
        return

    # Tabs
    tab_learn, tab_code, tab_quiz = st.tabs(["📖 Learn", "💻 Code Example", "🎯 Quiz"])

    # ── LEARN TAB ──
    with tab_learn:
        st.markdown(
            f'<div class="card-purple">{lvl["description"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="info-box">💡 <strong>XP Reward:</strong> '
            f'Complete the quiz to earn <strong style="color:#00FF41">'
            f'+{lvl["xp_reward"]} XP</strong> (10 XP per correct answer + '
            f'{lvl["xp_reward"] - 30} bonus for completing the level).</div>',
            unsafe_allow_html=True,
        )

    # ── CODE TAB ──
    with tab_code:
        st.markdown(
            '<p style="color:#888;font-size:0.82rem;font-family:Space Mono,monospace;">'
            '// Study this snippet before taking the quiz</p>',
            unsafe_allow_html=True,
        )
        st.code(lvl["code_example"], language="python")

    # ── QUIZ TAB ──
    with tab_quiz:
        render_quiz(level_id, lvl)


def render_quiz(level_id: int, lvl: dict):
    questions = lvl["questions"]
    qs_data = st.session_state.quiz_state.get(level_id, {})
    already_passed = level_id in st.session_state.completed_levels
    submitted = qs_data.get("submitted", False)

    # Show milestone badge if just completed
    if st.session_state.show_badge == level_id:
        score = qs_data.get("score", 0)
        st.balloons()
        st.markdown(
            f'<div class="milestone">'
            f'<div style="font-size:3rem;">🏆</div>'
            f'<div style="font-family:Space Mono,monospace;color:#00FF41;'
            f'font-size:1rem;margin:0.5rem 0;">MILESTONE UNLOCKED!</div>'
            f'<div style="color:#fff;font-size:0.9rem;">'
            f'"{lvl["subtitle"]}" Complete — Score: {score}/3</div>'
            f'<div style="margin-top:0.8rem;">'
            f'<span class="xp-badge">+{lvl["xp_reward"]} XP</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.session_state.show_badge = None

    if already_passed and submitted:
        score = qs_data.get("score", 0)
        st.markdown(
            f'<div class="success-box">✅ Level complete! You scored {score}/3. '
            f'Review your answers below or head back to the Hub.</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<p style="font-family:Space Mono,monospace;font-size:0.78rem;'
        'color:#888;margin-bottom:1rem;">Answer all 3 questions, then submit.</p>',
        unsafe_allow_html=True,
    )

    user_answers = []
    for i, q in enumerate(questions):
        st.markdown(
            f'<div class="card" style="margin-bottom:0.6rem;">'
            f'<p style="font-family:Space Mono,monospace;font-size:0.82rem;'
            f'color:#fff;margin:0 0 0.8rem 0;">Q{i+1}: {q["q"]}</p></div>',
            unsafe_allow_html=True,
        )

        # Determine default index
        saved = qs_data.get("answers", [None, None, None])
        default_idx = 0
        if saved[i] is not None and saved[i] in q["options"]:
            default_idx = q["options"].index(saved[i])

        disabled = submitted and already_passed
        choice = st.radio(
            f"Q{i+1}",
            q["options"],
            index=default_idx,
            key=quiz_key(level_id, i),
            label_visibility="collapsed",
            disabled=disabled,
        )
        user_answers.append(choice)

        # Show answer feedback if submitted
        if submitted:
            if choice == q["answer"]:
                st.markdown(
                    f'<div class="success-box">✅ Correct! <code>{q["answer"]}</code></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="background:rgba(255,68,68,0.08);border-left:4px solid #FF4444;'
                    f'border-radius:0 8px 8px 0;padding:0.7rem 1rem;margin:0.4rem 0;font-size:0.85rem;color:#FF8888;">'
                    f'❌ Your answer: <code>{choice}</code> — Correct: <code>{q["answer"]}</code></div>',
                    unsafe_allow_html=True,
                )
        st.markdown("")  # spacing

    # Submit button
    if not (submitted and already_passed):
        if st.button("⚡ Submit Answers", key=f"submit_{level_id}"):
            score = sum(1 for i, q in enumerate(questions) if user_answers[i] == q["answer"])

            # Save quiz result
            st.session_state.quiz_state[level_id] = {
                "answers": user_answers,
                "submitted": True,
                "score": score,
            }

            # Award XP and unlock
            if level_id not in st.session_state.completed_levels:
                xp_gain = score * 10 + (lvl["xp_reward"] - 30)  # base 10/q + level bonus
                st.session_state.xp += xp_gain
                st.session_state.completed_levels.add(level_id)
                st.session_state.show_badge = level_id

            st.rerun()

    # If level 5 completed, show certificate section
    if level_id == 5 and 5 in st.session_state.completed_levels:
        render_certificate()


# ============================================================
# CERTIFICATE SECTION
# ============================================================
def render_certificate():
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:Space Mono,monospace;font-size:1rem;'
        'color:#00FF41;margin-bottom:0.5rem;">🏅 Certificate of Completion</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#888;font-size:0.85rem;">You\'ve conquered all 5 levels! '
        'Enter your name to generate your personalized completion certificate.</p>',
        unsafe_allow_html=True,
    )

    name_input = st.text_input(
        "Your Name",
        value=st.session_state.cert_name,
        placeholder="Enter your full name…",
        key="cert_name_field",
    )
    st.session_state.cert_name = name_input

    if name_input.strip():
        cert_html = build_certificate_html(
            name=name_input.strip(),
            xp=st.session_state.xp,
            date_str=datetime.now().strftime("%B %d, %Y"),
        )
        dl_link = get_download_link(
            cert_html,
            f"python_adventure_cert_{name_input.strip().replace(' ','_')}.html",
            "📥 Download Certificate",
        )
        st.markdown(dl_link, unsafe_allow_html=True)

        # Preview
        with st.expander("👁️ Preview Certificate"):
            title, icon = get_character_info(st.session_state.xp)
            st.markdown(
                f'<div class="cert-wrapper">'
                f'<div style="font-family:Space Mono,monospace;font-size:0.65rem;'
                f'color:#00FF41;letter-spacing:0.3em;margin-bottom:0.5rem;">🐍 PYTHON CODING ADVENTURE</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:1.4rem;'
                f'color:#00FF41;text-shadow:0 0 15px rgba(0,255,65,0.5);">Certificate of Completion</div>'
                f'<div style="color:#888;font-size:0.8rem;margin:0.3rem 0 1rem;">This certifies that</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:1.8rem;'
                f'color:#fff;margin-bottom:1rem;">{name_input}</div>'
                f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1rem 0;">'
                f'<div style="background:#1A1A1A;border:1px solid #2A2A2A;border-radius:8px;padding:0.8rem;">'
                f'<div style="color:#00FF41;font-family:Space Mono,monospace;">{st.session_state.xp}</div>'
                f'<div style="font-size:0.7rem;color:#666;">XP Earned</div></div>'
                f'<div style="background:#1A1A1A;border:1px solid #2A2A2A;border-radius:8px;padding:0.8rem;">'
                f'<div style="color:#00FF41;font-family:Space Mono,monospace;">'
                f'{len(st.session_state.completed_levels)}/5</div>'
                f'<div style="font-size:0.7rem;color:#666;">Levels Done</div></div>'
                f'<div style="background:#1A1A1A;border:1px solid #2A2A2A;border-radius:8px;padding:0.8rem;">'
                f'<div style="color:#00FF41;font-family:Space Mono,monospace;">{icon} {title}</div>'
                f'<div style="font-size:0.7rem;color:#666;">Final Rank</div></div>'
                f'</div>'
                f'<div style="display:inline-block;background:#6200EE;border:2px solid #000;'
                f'border-radius:6px;padding:0.3rem 1rem;font-family:Space Mono,monospace;'
                f'font-size:0.75rem;box-shadow:3px 3px 0 #000;margin-top:0.8rem;">'
                f'✅ Python Basics Mastered</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div style="color:#666;font-size:0.82rem;font-style:italic;">'
            '↑ Enter your name above to unlock the download button.</div>',
            unsafe_allow_html=True,
        )


# ============================================================
# MAIN
# ============================================================
def main():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    init_state()
    render_sidebar()

    if st.session_state.view == "hub":
        render_hub()
    elif st.session_state.view == "level":
        render_level(st.session_state.current_level)


if __name__ == "__main__":
    main()
