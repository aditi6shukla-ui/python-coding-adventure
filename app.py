import streamlit as st
import hashlib
import base64
from datetime import datetime

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
# MODULE-LEVEL USER DATABASE
# Persists across reruns while the Streamlit server is running.
# ============================================================
if "_USER_DB" not in st.__dict__:
    st._USER_DB = {}        # {username: {"pw_hash": str}}

if "_USER_PROGRESS" not in st.__dict__:
    st._USER_PROGRESS = {}  # {username: {xp, completed_levels, quiz_state, cert_name}}


# ============================================================
# CUSTOM CSS — CodeDex / Neubrutalism Dark Theme
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

  /* Neubrutalism buttons */
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
</style>
"""

# ============================================================
# CURRICULUM DATA
# ============================================================
LEVELS = {
    1: {
        "title": "Variables & Data Types", "subtitle": "The Foundation",
        "icon": "🧱", "pixel_art": "🔢", "color": "#00FF41", "xp_reward": 50,
        "description": """
Variables are like **labeled boxes** that store information. Python automatically detects the type — no need to declare types explicitly!

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

print(f"Player: {name}")
print(f"Level:  {level}")
print(f"Type of xp_multiplier: {type(xp_multiplier)}")

# Type conversion
score_str = "250"
score_int = int(score_str)
print(f"Score doubled: {score_int * 2}")
''',
        "questions": [
            {"q": "What data type is the value `3.14` in Python?",
             "options": ["int", "float", "str", "bool"], "answer": "float"},
            {"q": "Which of the following is a valid Python variable name?",
             "options": ["2nd_player", "player-name", "player_name", "class"], "answer": "player_name"},
            {"q": "What does `type('Hello')` return?",
             "options": ["<class 'str'>", "<class 'int'>", "str", "String"], "answer": "<class 'str'>"},
        ],
    },
    2: {
        "title": "Logic & Loops", "subtitle": "The Path",
        "icon": "🔀", "pixel_art": "♾️", "color": "#9D46FF", "xp_reward": 60,
        "description": """
Control flow lets your program **make decisions** and **repeat actions**.

**Conditionals (`if / elif / else`):** Execute code only when a condition is `True`.

**Loops:**
- `for` loop → Iterate over a sequence a fixed number of times
- `while` loop → Repeat as long as a condition is `True`

**Operators:** `==`, `!=`, `<`, `>`, `<=`, `>=`, `and`, `or`, `not`
        """,
        "code_example": '''# 🔀 Logic & Loops

score = 85
if score >= 90:
    grade = "S-Rank"
elif score >= 70:
    grade = "A-Rank"
else:
    grade = "Try Again"
print(f"Your grade: {grade}")

# For loop
for i in range(1, 6):
    print(f"  Item #{i} collected!")

# While loop
health = 100
hits = 0
while health > 0:
    health -= 30
    hits += 1
print(f"KO after {hits} hits!")
''',
        "questions": [
            {"q": "What does `range(0, 5)` produce?",
             "options": ["0,1,2,3,4,5", "0,1,2,3,4", "1,2,3,4,5", "1,2,3,4"], "answer": "0,1,2,3,4"},
            {"q": "Which keyword exits a loop early?",
             "options": ["exit", "stop", "break", "return"], "answer": "break"},
            {"q": "What is the result of `not True`?",
             "options": ["True", "False", "None", "Error"], "answer": "False"},
        ],
    },
    3: {
        "title": "Lists & Dictionaries", "subtitle": "The Inventory",
        "icon": "🎒", "pixel_art": "📦", "color": "#00CFFF", "xp_reward": 70,
        "description": """
**Lists** are ordered, mutable sequences — your adventurer's **item bag**.

**Dictionaries** are key-value stores — like a **character sheet**.

**Key list ops:** `append()`, `remove()`, `pop()`, `len()`, slicing `[start:end]`

**Key dict ops:** `dict[key]`, `dict.get(key)`, `.keys()`, `.values()`, `.items()`
        """,
        "code_example": '''# 🎒 Lists & Dictionaries

inventory = ["sword", "shield", "potion"]
inventory.append("map")
inventory.remove("shield")
print(f"Inventory: {inventory}")

# List comprehension
powered = [item.upper() for item in inventory]
print(f"Powered: {powered}")

# Dictionary
hero = {"name": "Alex", "hp": 100, "class": "Wizard"}
hero["level"] = 5
for stat, value in hero.items():
    print(f"  {stat}: {value}")
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
        ],
    },
    4: {
        "title": "Functions", "subtitle": "The Spells",
        "icon": "✨", "pixel_art": "🪄", "color": "#FF6B6B", "xp_reward": 80,
        "description": """
**Functions** are reusable blocks of code — your hero's **spellbook**. Define once, cast anywhere.

**Key concepts:**
- `def` keyword to define a function
- **Parameters** receive input values
- `return` sends a value back to the caller
- **Default parameters** provide fallback values
- `lambda` for one-liner functions
        """,
        "code_example": '''# ✨ Functions

def greet(name):
    return f"Welcome, {name}! Your quest begins."

def cast_spell(spell_name, power=10, critical=False):
    damage = power * (2 if critical else 1)
    return f"⚡ {spell_name} deals {damage} damage!"

def total_xp(*xp_gains):
    return sum(xp_gains)

print(greet("Alex"))
print(cast_spell("Fireball", power=25))
print(cast_spell("Lightning", power=30, critical=True))
print(f"Total XP: {total_xp(50, 30, 20, 15)}")

double = lambda x: x * 2
print(f"Double 7 = {double(7)}")
''',
        "questions": [
            {"q": "What keyword defines a function in Python?",
             "options": ["function", "func", "def", "define"], "answer": "def"},
            {"q": "What does a function return with no `return` statement?",
             "options": ["0", "False", "None", "An error"], "answer": "None"},
            {"q": "What is `lambda x: x ** 2` equivalent to?",
             "options": ["def f(x): x**2", "def f(x): return x**2", "def f(): return x**2", "lambda: x**2"],
             "answer": "def f(x): return x**2"},
        ],
    },
    5: {
        "title": "The Final Boss", "subtitle": "Comprehensive Python Test",
        "icon": "🐉", "pixel_art": "💀", "color": "#FF4444", "xp_reward": 100,
        "description": """
You've studied the ancient texts. You've mastered the four disciplines.

Now face **The Final Boss** — a comprehensive gauntlet mixing Variables, Logic, Lists, Dictionaries, and Functions.

Answer correctly to claim your **Python Master Certificate**. 🏆
        """,
        "code_example": '''# 🐉 Final Boss — All Skills Combined

def analyze_party(members: list) -> dict:
    """Analyze a party of heroes and return stats."""
    if not members:
        return {"error": "Empty party!"}

    total_hp  = sum(m["hp"] for m in members)
    avg_hp    = total_hp / len(members)
    max_hero  = max(members, key=lambda m: m["hp"])
    alive     = [m["name"] for m in members if m["hp"] > 0]
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
    {"name": "Alex",   "hp": 120, "class": "Wizard"},
    {"name": "Sam",    "hp": 95,  "class": "Rogue"},
    {"name": "Jordan", "hp": 0,   "class": "Wizard"},
]
for key, val in analyze_party(party).items():
    print(f"{key:12s}: {val}")
''',
        "questions": [
            {"q": "What does `max([3,1,4,1,5,9], key=lambda x: -x)` return?",
             "options": ["9", "1", "3", "-9"], "answer": "1"},
            {"q": "Which line correctly unpacks a dict into keyword arguments?",
             "options": ["func(*my_dict)", "func(**my_dict)", "func(my_dict...)", "func(#my_dict)"],
             "answer": "func(**my_dict)"},
            {"q": "What is the time complexity of looking up a key in a Python dict?",
             "options": ["O(n)", "O(log n)", "O(1)", "O(n²)"], "answer": "O(1)"},
        ],
    },
}

# ============================================================
# XP / RANK SYSTEM
# ============================================================
XP_TIERS = [
    (0,   "Apprentice",    "🌱"),
    (50,  "Coder",         "💻"),
    (120, "Wizard",        "🧙"),
    (200, "Sorcerer",      "🔮"),
    (300, "Python Master", "🐍"),
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
# PASSWORD HELPERS
# ============================================================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password: str, pw_hash: str) -> bool:
    return hash_password(password) == pw_hash


# ============================================================
# PROGRESS HELPERS
# ============================================================
def empty_progress():
    return {"xp": 0, "completed_levels": set(), "quiz_state": {}, "cert_name": ""}

def load_user_progress(username: str):
    prog = st._USER_PROGRESS.get(username, empty_progress())
    st.session_state.xp               = prog["xp"]
    st.session_state.completed_levels  = set(prog["completed_levels"])
    st.session_state.quiz_state        = dict(prog["quiz_state"])
    st.session_state.cert_name         = prog["cert_name"]

def save_user_progress(username: str):
    st._USER_PROGRESS[username] = {
        "xp":               st.session_state.xp,
        "completed_levels": set(st.session_state.completed_levels),
        "quiz_state":       dict(st.session_state.quiz_state),
        "cert_name":        st.session_state.cert_name,
    }


# ============================================================
# SESSION STATE INIT
# ============================================================
def init_state():
    defaults = {
        "logged_in": False, "username": "",
        "auth_tab": "login", "auth_error": "", "auth_success": "",
        "xp": 0, "completed_levels": set(), "quiz_state": {}, "cert_name": "",
        "current_level": 1, "show_badge": None, "view": "hub",
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
    if username in st._USER_DB:
        st.session_state.auth_error = "Username already taken. Try another."
        return
    st._USER_DB[username] = {"pw_hash": hash_password(password)}
    st._USER_PROGRESS[username] = empty_progress()
    st.session_state.auth_error   = ""
    st.session_state.auth_success = f"Account created! Welcome, {username} 🎉 Now log in."
    st.session_state.auth_tab     = "login"

def do_login(username, password):
    username = username.strip().lower()
    if username not in st._USER_DB:
        st.session_state.auth_error = "Username not found. Please register first."
        return
    if not check_password(password, st._USER_DB[username]["pw_hash"]):
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
        'Create an account to save your XP and progress across sessions</div>'
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

    # Which tab is active indicator
    active = st.session_state.auth_tab
    st.markdown(
        f'<div style="display:flex;gap:0;margin-bottom:1.5rem;">'
        f'<div style="flex:1;height:3px;background:{"#00FF41" if active=="login" else "#2A2A2A"};'
        f'border-radius:2px 0 0 2px;"></div>'
        f'<div style="flex:1;height:3px;background:{"#00FF41" if active=="register" else "#2A2A2A"};'
        f'border-radius:0 2px 2px 0;"></div></div>',
        unsafe_allow_html=True,
    )

    # Error / success banners
    if st.session_state.auth_error:
        st.markdown(
            f'<div style="background:rgba(255,68,68,0.12);border-left:4px solid #FF4444;'
            f'border-radius:0 8px 8px 0;padding:0.8rem 1rem;color:#FF8888;margin-bottom:0.8rem;">'
            f'⚠️ {st.session_state.auth_error}</div>',
            unsafe_allow_html=True,
        )
    if st.session_state.auth_success:
        st.markdown(f'<div class="success-box">✅ {st.session_state.auth_success}</div>', unsafe_allow_html=True)

    # ── LOGIN FORM ──
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

    # ── REGISTER FORM ──
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
        '<span style="font-size:0.75rem;color:#555;">💾 Your XP and completed levels are automatically '
        'saved every time you answer a quiz. Log back in anytime to continue!</span></div>',
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    xp = st.session_state.xp
    title, icon = get_character_info(xp)
    max_xp = sum(v["xp_reward"] for v in LEVELS.values())
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

        st.markdown("---")
        st.markdown('<p style="font-family:Space Mono,monospace;font-size:0.7rem;color:#666;margin-bottom:0.4rem;">LEVEL MAP</p>', unsafe_allow_html=True)
        for lvl_id, lvl in LEVELS.items():
            st_icon = {"done":"✅","unlocked":"🔓","locked":"🔒"}[level_status(lvl_id)]
            color   = {"done":"#00FF41","unlocked":"#E8E8E8","locked":"#555"}[level_status(lvl_id)]
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:0.5rem;padding:0.25rem 0;font-size:0.72rem;">'
                f'<span>{st_icon}</span>'
                f'<span style="color:{color};font-family:Space Mono,monospace;">L{lvl_id}: {lvl["subtitle"]}</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        if st.button("🏠 Adventure Hub", use_container_width=True):
            st.session_state.view = "hub"
            st.rerun()
        if st.button("🚪 Log Out", use_container_width=True):
            save_user_progress(st.session_state.username)
            for k in ["logged_in","username","xp","completed_levels","quiz_state",
                      "cert_name","current_level","show_badge","view"]:
                st.session_state.pop(k, None)
            st.rerun()


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


# ============================================================
# HUB
# ============================================================
def render_hub():
    st.markdown(
        f'<h1 class="neon-heading" style="font-size:1.6rem;margin-bottom:0.2rem;">🐍 Python Coding Adventure</h1>'
        f'<p style="color:#888;font-family:Space Mono,monospace;font-size:0.75rem;">'
        f'Welcome back, <span style="color:#00FF41">@{st.session_state.username}</span> — choose your next mission!</p>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (lvl_id, lvl) in enumerate(LEVELS.items()):
        status = level_status(lvl_id)
        with cols[i % 3]:
            border  = "#00FF41" if status=="done" else (lvl["color"] if status=="unlocked" else "#2A2A2A")
            shadow  = f"4px 4px 0 {border}" if status!="locked" else "none"
            opacity = "1" if status!="locked" else "0.4"
            lbl_txt = "✅ COMPLETE" if status=="done" else ("▶ PLAY" if status=="unlocked" else "🔒 LOCKED")
            lbl_col = "#00FF41" if status=="done" else ("#fff" if status=="unlocked" else "#555")
            sc_html = ""
            if lvl_id in st.session_state.quiz_state and st.session_state.quiz_state[lvl_id].get("submitted"):
                sc = st.session_state.quiz_state[lvl_id].get("score",0)
                sc_html = f'<div style="font-size:0.7rem;color:#888;margin-top:0.3rem;">Score: {sc}/3 ⭐</div>'
            st.markdown(
                f'<div style="background:#181818;border:2px solid {border};border-radius:8px;padding:1.2rem;'
                f'box-shadow:{shadow};text-align:center;margin-bottom:0.6rem;opacity:{opacity};">'
                f'<div style="font-size:2.2rem;margin-bottom:0.4rem;">{lvl["pixel_art"]}</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:0.62rem;color:{border};letter-spacing:0.2em;">LEVEL {lvl_id}</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:0.82rem;color:#fff;font-weight:700;margin:0.3rem 0;">{lvl["icon"]} {lvl["title"]}</div>'
                f'<div style="font-size:0.72rem;color:#888;margin-bottom:0.6rem;">{lvl["subtitle"]}</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:0.62rem;color:{lbl_col};">{lbl_txt}</div>'
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
    done = len(st.session_state.completed_levels)
    stars = sum(st.session_state.quiz_state.get(l,{}).get("score",0) for l in st.session_state.completed_levels)

    for col, val, label, sub, color in zip(
        st.columns(4),
        [f"{icon} {title}", str(xp), f"{done}/5", f"{stars}⭐"],
        ["Rank", "XP Earned", "Levels Done", "Stars"],
        ["Character class", f"of {max_xp} total", "Keep going!", "quiz correct"],
        ["#00FF41", "#9D46FF", "#00CFFF", "#FF6B6B"],
    ):
        with col:
            st.markdown(
                f'<div class="card" style="text-align:center;padding:1rem;">'
                f'<div style="font-family:Space Mono,monospace;font-size:1.2rem;color:#fff;">{val}</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:0.72rem;color:{color};">{label}</div>'
                f'<div style="font-size:0.68rem;color:#888;">{sub}</div></div>',
                unsafe_allow_html=True,
            )


# ============================================================
# LEVEL VIEW
# ============================================================
def render_level(level_id):
    lvl = LEVELS[level_id]
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
        return

    tab1, tab2, tab3 = st.tabs(["📖 Learn", "💻 Code Example", "🎯 Quiz"])
    with tab1:
        st.markdown(f'<div class="card-purple">{lvl["description"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-box">💡 Complete the quiz to earn <strong style="color:#00FF41">+{lvl["xp_reward"]} XP</strong></div>', unsafe_allow_html=True)
    with tab2:
        st.markdown('<p style="color:#888;font-size:0.8rem;font-family:Space Mono,monospace;">// Study this before the quiz</p>', unsafe_allow_html=True)
        st.code(lvl["code_example"], language="python")
    with tab3:
        render_quiz(level_id, lvl)


# ============================================================
# QUIZ
# ============================================================
def render_quiz(level_id, lvl):
    questions = lvl["questions"]
    qs_data   = st.session_state.quiz_state.get(level_id, {})
    passed    = level_id in st.session_state.completed_levels
    submitted = qs_data.get("submitted", False)

    if st.session_state.show_badge == level_id:
        st.balloons()
        st.markdown(
            f'<div class="milestone">'
            f'<div style="font-size:3rem;">🏆</div>'
            f'<div style="font-family:Space Mono,monospace;color:#00FF41;font-size:1rem;margin:0.5rem 0;">MILESTONE UNLOCKED!</div>'
            f'<div style="color:#fff;">{lvl["subtitle"]} Complete — Score: {qs_data.get("score",0)}/3</div>'
            f'<div style="margin-top:0.8rem;"><span class="xp-badge">+{lvl["xp_reward"]} XP saved 💾</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.session_state.show_badge = None

    if passed and submitted:
        st.markdown(
            f'<div class="success-box">✅ Level complete! Score: {qs_data.get("score",0)}/3 — '
            f'Progress saved to your account 💾</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<p style="font-family:Space Mono,monospace;font-size:0.78rem;color:#888;margin-bottom:1rem;">Answer all 3 questions, then submit.</p>', unsafe_allow_html=True)

    user_answers = []
    for i, q in enumerate(questions):
        st.markdown(
            f'<div class="card" style="margin-bottom:0.6rem;">'
            f'<p style="font-family:Space Mono,monospace;font-size:0.82rem;color:#fff;margin:0 0 0.8rem;">'
            f'Q{i+1}: {q["q"]}</p></div>',
            unsafe_allow_html=True,
        )
        saved = qs_data.get("answers", [None, None, None])
        default_idx = q["options"].index(saved[i]) if saved[i] in q["options"] else 0
        disabled = submitted and passed
        choice = st.radio(f"Q{i+1}", q["options"], index=default_idx,
                          key=quiz_key(level_id, i), label_visibility="collapsed", disabled=disabled)
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

    if not (submitted and passed):
        if st.button("⚡ Submit Answers", key=f"submit_{level_id}"):
            score = sum(1 for i, q in enumerate(questions) if user_answers[i] == q["answer"])
            st.session_state.quiz_state[level_id] = {"answers": user_answers, "submitted": True, "score": score}
            if level_id not in st.session_state.completed_levels:
                st.session_state.xp += score * 10 + (lvl["xp_reward"] - 30)
                st.session_state.completed_levels.add(level_id)
                st.session_state.show_badge = level_id
            save_user_progress(st.session_state.username)   # ← auto-save!
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
        done = len(st.session_state.completed_levels)
        xp   = st.session_state.xp
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
    <div class="stat"><div class="v">{xp}</div><div class="l">XP Earned</div></div>
    <div class="stat"><div class="v">{done}/5</div><div class="l">Levels Completed</div></div>
    <div class="stat"><div class="v">{icon} {title}</div><div class="l">Final Rank</div></div>
  </div>
  <hr/>
  <div class="badge">✅ Python Basics Mastered</div>
  <div class="footer">Issued on {date_str} &nbsp;|&nbsp; Python Coding Adventure &nbsp;|&nbsp; Powered by Streamlit</div>
</div></body></html>"""
        b64 = base64.b64encode(cert_html.encode()).decode()
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
 
   


    
  
