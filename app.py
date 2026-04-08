import streamlit as st
import hashlib, base64, random, json, os, sys, io, traceback
from datetime import datetime, date

# ============================================================
# PAGE CONFIG  — sidebar starts expanded, we pin it via CSS
# ============================================================
st.set_page_config(
    page_title="Python Coding Adventure",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PERSISTENT STORAGE
# ============================================================
USERS_FILE = "python_adventure_users.json"

def _load_raw():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE) as f: return json.load(f)
        except Exception: pass
    return {"users": {}, "progress": {}}

def _save_raw(data):
    with open(USERS_FILE, "w") as f: json.dump(data, f, indent=2)

if "_DB_CACHE" not in st.__dict__:
    st._DB_CACHE = _load_raw()

def get_db():  return st._DB_CACHE
def flush_db(): _save_raw(st._DB_CACHE)

# ============================================================
# SPELLBOOK  — unlocks as levels complete
# ============================================================
SPELLBOOK = {
    1: {"title": "📦 Variables & Types", "spells": [
        ("Declare variable",    'name = "Alex"\nxp = 100\nactive = True'),
        ("Type conversion",     'int("42")  # → 42\nstr(100)   # → "100"\nbool(0)    # → False'),
        ("f-string",            'f"HP: {hp}, XP: {xp*2}"'),
        ("String slicing",      '"Python"[0:3]  # → "Pyt"\n"Python"[-1]   # → "n"'),
        ("Floor div / Modulo",  '10 // 3  # → 3\n10 % 3   # → 1\n2 ** 8   # → 256'),
    ]},
    2: {"title": "🔀 Logic & Loops", "spells": [
        ("if / elif / else",    'if x > 0:\n    ...\nelif x == 0:\n    ...\nelse:\n    ...'),
        ("Ternary",             '"Pass" if score >= 60 else "Fail"'),
        ("for range",           'for i in range(5):   # 0-4\nfor i in range(1,6): # 1-5'),
        ("enumerate / zip",     'for i, v in enumerate(lst):\nfor a, b in zip(l1, l2):'),
        ("List comprehension",  '[x**2 for x in range(6) if x%2==0]'),
    ]},
    3: {"title": "🎒 Lists & Dicts", "spells": [
        ("List methods",        'lst.append(x)\nlst.insert(0,x)\nlst.pop()\nlst.sort()'),
        ("Slicing",             'lst[1:3]   # index 1 and 2\nlst[::-1]  # reversed'),
        ("Dict access",         'd["key"]\nd.get("key", default)\ndel d["key"]'),
        ("Dict iteration",      'for k, v in d.items():\nfor k in d.keys():'),
        ("Set",                 '{1,2,2,3}  # → {1,2,3}\ns.add(x); s.discard(x)'),
    ]},
    4: {"title": "✨ Functions", "spells": [
        ("Define function",     'def greet(name, title="Hero"):\n    return f"Welcome, {title} {name}!"'),
        ("*args / **kwargs",    'def f(*args):    # tuple\ndef f(**kwargs): # dict'),
        ("Lambda",              'double = lambda x: x * 2\nsorted(lst, key=lambda x: x["hp"])'),
        ("map / filter",        'list(map(lambda x: x*2, lst))\nlist(filter(lambda x: x>0, lst))'),
        ("Scope / global",      'global score\nscore += 50  # modify global inside fn'),
    ]},
    5: {"title": "🐉 Advanced", "spells": [
        ("Class",               'class Hero:\n    def __init__(self, name):\n        self.name = name'),
        ("Inheritance",         'class Wizard(Hero):\n    def __init__(self, name):\n        super().__init__(name)'),
        ("try / except",        'try:\n    risky()\nexcept ValueError as e:\n    handle(e)\nfinally:\n    cleanup()'),
        ("with open",           'with open("f.txt","w") as f:\n    f.write("data")'),
        ("json",                'import json\njson.dump(obj, f)\njson.load(f)'),
    ]},
}

# ============================================================
# CURRICULUM DATA
# ============================================================
LEVELS = {
    1: {
        "title": "Variables & Data Types", "mission": "Mission 1: Repair the Data Core",
        "subtitle": "The Foundation", "icon": "🧱", "pixel_art": "🔢",
        "color": "#00FF41", "xp_reward": 100,
        "lore": "The Data Core is corrupted. Restore it by mastering variables and types.",
        "description": """
## 🧱 Chapter 1 — Variables & Data Types

Variables are **named containers** that hold data. Python uses **dynamic typing** — you never need to declare the type explicitly.

---

### 📦 Declaring Variables
```python
name = "Alex"       # str
level = 1           # int
xp = 0.0            # float
is_hero = True      # bool
lives = None        # NoneType

x = y = z = 0       # multiple assignment
a, b, c = 1, 2, 3   # tuple unpacking
```

### 🔢 Core Data Types

| Type | Example | Description |
|------|---------|-------------|
| `int` | `42`, `-7` | Whole numbers |
| `float` | `3.14`, `-0.5` | Decimal numbers |
| `str` | `"Hello"` | Text (immutable) |
| `bool` | `True`, `False` | Truth values |
| `NoneType` | `None` | Absence of value |

### 🔄 Type Conversion
```python
int("42")      # → 42
float("3.14")  # → 3.14
str(100)       # → "100"
bool(0)        # → False
bool("hi")     # → True
```

### ✏️ String Operations
```python
name = "python"
name.upper()          # "PYTHON"
name.replace("p","P") # "Python"
len(name)             # 6
name[0]               # "p"
name[-1]              # "n"
name[0:3]             # "pyt"
f"Score: {95 * 2}"    # f-strings
```

### ➗ Arithmetic
```python
10 + 3   # 13    10 - 3  # 7
10 * 3   # 30    10 / 3  # 3.333
10 // 3  # 3     10 % 3  # 1
2 ** 10  # 1024
```
> 💡 Use `SCREAMING_SNAKE_CASE` for constants: `MAX_HEALTH = 100`
        """,
        "code_example": '''name = "Alex"\nlevel = 1\nxp_multiplier = 1.5\nis_hero = True\n\nprint(f"Player: {name}")\nprint(f"Level:  {level}")\nprint(f"XP Mult:{xp_multiplier}")\n\nscore_str = "250"\nscore_int = int(score_str)\nprint(f"\\nConverted: {score_int}")\nprint(f"Doubled:   {score_int * 2}")\n\ntag = "python_master"\nprint(f"\\nUpper:   {tag.upper()}")\nprint(f"Length:  {len(tag)}")\nprint(f"Slice:   {tag[0:6]}")\n\nprint(f"\\n7 // 2 = {7 // 2}")\nprint(f"7 %  2 = {7 %  2}")\nprint(f"2**8   = {2**8}")''',
        "questions": [
            {"q": "What data type is `3.14`?", "options": ["int","float","str","bool"], "answer": "float"},
            {"q": "Which is a valid Python variable name?", "options": ["2nd_player","player-name","player_name","class"], "answer": "player_name"},
            {"q": "What does `type('Hello')` return?", "options": ["<class 'str'>","<class 'int'>","str","String"], "answer": "<class 'str'>"},
            {"q": "What is `int('42')`?", "options": ["'42'","42.0","42","Error"], "answer": "42"},
            {"q": "What does `bool(0)` return?", "options": ["True","False","None","0"], "answer": "False"},
            {"q": "Which is NOT a valid variable name?", "options": ["_score","score1","my_score","2score"], "answer": "2score"},
            {"q": "What does `len('Python')` return?", "options": ["5","6","7","Error"], "answer": "6"},
            {"q": "What is `'Hello' + ' ' + 'World'`?", "options": ["Hello World","'Hello World'","HelloWorld","Error"], "answer": "Hello World"},
            {"q": "What is `7 // 2`?", "options": ["3.5","4","3","2"], "answer": "3"},
            {"q": "What is `10 % 3`?", "options": ["3","1","0","2"], "answer": "1"},
            {"q": "What does `str(100)` return?", "options": ["100","'100'","int","Error"], "answer": "'100'"},
            {"q": "What is `type(None)`?", "options": ["<class 'NoneType'>","<class 'null'>","<class 'none'>","None"], "answer": "<class 'NoneType'>"},
            {"q": "What is `2 ** 10`?", "options": ["20","512","1024","100"], "answer": "1024"},
            {"q": "What does `bool('hello')` return?", "options": ["False","True","None","Error"], "answer": "True"},
            {"q": "What is `'Python'[0]`?", "options": ["'P'","'y'","'Python'","Error"], "answer": "'P'"},
            {"q": "After `x = 5; x += 3`, what is `x`?", "options": ["5","3","8","15"], "answer": "8"},
            {"q": "What is `f'{3 + 4}'`?", "options": ["7","'7'","3 + 4","Error"], "answer": "'7'"},
            {"q": "Which converts a string to uppercase?", "options": [".upper()",".toUpper()",".capitalize()",".UPPER()"], "answer": ".upper()"},
            {"q": "What is `'Python'[-1]`?", "options": ["'P'","'n'","'o'","Error"], "answer": "'n'"},
            {"q": "What is `isinstance(42, int)`?", "options": ["True","False","42","Error"], "answer": "True"},
        ],
        "boss": {
            "name": "The Type Phantom 👻", "xp_reward": 50,
            "lore": "A shapeless entity that shifts between data types, crashing programs and corrupting memory.",
            "challenge": "The Type Phantom is shapeshifting! 🧱 Type the Python built-in function (with a placeholder like `x`) used to check any variable's data type.",
            "hint": "Used like: `___(my_variable)` — returns `<class 'int'>` for integers.",
            "accepted": ["type(x)","type(n)","type(v)","type(val)","type(variable)","type(a)","type()"],
            "display_answer": "type(x)",
        },
    },
    2: {
        "title": "Logic & Loops", "mission": "Mission 2: Navigate the Loop Maze",
        "subtitle": "The Path", "icon": "🔀", "pixel_art": "♾️",
        "color": "#9D46FF", "xp_reward": 120,
        "lore": "The Loop Maze traps adventurers in infinite cycles. Master conditionals to find the exit.",
        "description": """
## 🔀 Chapter 2 — Logic & Loops

Control flow lets your program **make decisions** and **repeat actions**.

### ⚖️ Comparison & Logical Operators
```python
5 == 5    # True    5 != 3   # True
5 > 3     # True    5 < 3    # False
5 >= 5    # True    5 <= 4   # False

True and False  # False
True or False   # True
not True        # False
```

### 🌿 if / elif / else
```python
score = 85
if score >= 90:
    grade = "S-Rank"
elif score >= 70:
    grade = "A-Rank"
else:
    grade = "Try Again"

# Ternary
label = "Pass" if score >= 60 else "Fail"
```

### 🔁 for Loops
```python
for i in range(5):           # 0,1,2,3,4
for i in range(1, 6):        # 1,2,3,4,5
for i in range(0, 10, 2):    # 0,2,4,6,8

for idx, item in enumerate(items):
for name, score in zip(names, scores):
```

### 🔄 while / break / continue
```python
while health > 0:
    health -= 25

for i in range(10):
    if i == 5: break      # stop entirely
    if i == 2: continue   # skip this one
```

### 🧠 List Comprehensions
```python
squares = [x**2 for x in range(6)]
evens   = [x for x in range(10) if x%2==0]
```
> 💡 Use `for` when you know iterations; `while` when waiting for a condition.
        """,
        "code_example": '''score = 85\nif score >= 90:\n    grade = "S-Rank ⭐"\nelif score >= 70:\n    grade = "A-Rank 🔥"\nelif score >= 50:\n    grade = "B-Rank 👍"\nelse:\n    grade = "Keep Trying 💪"\nprint(f"Score {score} → {grade}")\n\nfor i in range(1, 6):\n    print(f"  {i}", end=" ")\nprint()\n\nitems = ["Sword","Shield","Potion"]\nfor idx, item in enumerate(items, start=1):\n    print(f"  Slot {idx}: {item}")\n\nboss_hp = 100\nturn = 0\nwhile boss_hp > 0:\n    boss_hp -= 35\n    turn += 1\n    print(f"  Turn {turn}: boss HP={max(boss_hp,0)}")\n    if turn >= 5: break\n\nprint("Squares:", [x**2 for x in range(6)])''',
        "questions": [
            {"q": "What does `range(0, 5)` produce?", "options": ["0,1,2,3,4,5","0,1,2,3,4","1,2,3,4,5","1,2,3,4"], "answer": "0,1,2,3,4"},
            {"q": "Which keyword exits a loop immediately?", "options": ["exit","stop","break","return"], "answer": "break"},
            {"q": "What is `not True`?", "options": ["True","False","None","Error"], "answer": "False"},
            {"q": "What does `range(2, 10, 2)` produce?", "options": ["2,4,6,8,10","2,4,6,8","2,6,10","0,2,4,6,8"], "answer": "2,4,6,8"},
            {"q": "What does `continue` do?", "options": ["Stops the loop","Skips the current iteration","Restarts the loop","Does nothing"], "answer": "Skips the current iteration"},
            {"q": "`for i in range(3): print(i)` prints?", "options": ["1 2 3","0 1 2","0 1 2 3","1 2"], "answer": "0 1 2"},
            {"q": "What is `5 == 5.0`?", "options": ["False","True","Error","None"], "answer": "True"},
            {"q": "What does `pass` do?", "options": ["Exits the function","Skips to next iteration","Does nothing (placeholder)","Returns None"], "answer": "Does nothing (placeholder)"},
            {"q": "What does `elif` stand for?", "options": ["else if","else in loop","end if","evaluated if"], "answer": "else if"},
            {"q": "`True and False` evaluates to?", "options": ["True","False","None","Error"], "answer": "False"},
            {"q": "`False or True` evaluates to?", "options": ["True","False","None","Error"], "answer": "True"},
            {"q": "Output of `[x for x in range(5) if x % 2 == 0]`?", "options": ["[1,3]","[0,2,4]","[0,1,2,3,4]","[2,4]"], "answer": "[0,2,4]"},
            {"q": "How many times does `for i in range(5)` execute?", "options": ["4","5","6","0"], "answer": "5"},
            {"q": "Which operator checks same object identity?", "options": ["==","is","===","equals"], "answer": "is"},
            {"q": "What does `!=` mean?", "options": ["equal","not equal","less than","greater than"], "answer": "not equal"},
            {"q": "Is `'a' < 'b'` True or False?", "options": ["False","True","Error","None"], "answer": "True"},
            {"q": "Ternary for 'big' if x>5 else 'small'?", "options": ["'big' if x>5 else 'small'","if x>5: 'big' else 'small'","x>5 ? 'big' : 'small'","'small' if x>5 else 'big'"], "answer": "'big' if x>5 else 'small'"},
            {"q": "`while True:` without `break` creates?", "options": ["A syntax error","An infinite loop","A loop that runs once","A loop that never runs"], "answer": "An infinite loop"},
            {"q": "`enumerate(['a','b','c'])` first iteration?", "options": ["'a'","(0, 'a')","(1, 'a')","0"], "answer": "(0, 'a')"},
            {"q": "What does `zip([1,2],[3,4])` produce?", "options": ["[1,2,3,4]","[(1,3),(2,4)]","[(1,2),(3,4)]","[[1,3],[2,4]]"], "answer": "[(1,3),(2,4)]"},
        ],
        "boss": {
            "name": "The Loop Lord ♾️", "xp_reward": 60,
            "lore": "An ancient construct spinning in infinite cycles, trapping adventurers forever.",
            "challenge": "The Loop Lord has you in an infinite spin! 🔀 Type the keyword that immediately terminates a loop.",
            "hint": "One word. Used inside `for` and `while` to escape early.",
            "accepted": ["break"], "display_answer": "break",
        },
    },
    3: {
        "title": "Lists & Dictionaries", "mission": "Mission 3: Reclaim the Inventory Vault",
        "subtitle": "The Inventory", "icon": "🎒", "pixel_art": "📦",
        "color": "#00CFFF", "xp_reward": 140,
        "lore": "The Inventory Vault was ransacked. Rebuild it using Python's most powerful collections.",
        "description": """
## 🎒 Chapter 3 — Lists & Dictionaries

### 📋 Lists
```python
items = ["sword", "shield", "potion", "map"]
items[0]      # "sword"   (first)
items[-1]     # "map"     (last)
items[1:3]    # ["shield","potion"]
items[::-1]   # reversed

items.append("torch")
items.insert(0, "helmet")
items.remove("shield")
items.pop()
items.sort()
len(items)
"sword" in items   # membership test
```

### 📖 Dictionaries
```python
hero = {"name": "Alex", "hp": 100, "class": "Wizard"}
hero["name"]           # "Alex"
hero.get("mp", 0)      # 0 (safe default)
hero["level"] = 5      # add key
del hero["class"]      # delete key

for key, value in hero.items():
    print(f"{key}: {value}")
```

### 🔵 Tuples & Sets
```python
coords = (10, 20)         # immutable
unique = {1, 2, 2, 3}     # → {1,2,3}
```

### ⚡ Comprehensions
```python
squares = [x**2 for x in range(5)]
sq_dict = {x: x**2 for x in range(5)}
```
> 💡 Use `dict.get(key, default)` to avoid `KeyError`.
        """,
        "code_example": '''inventory = ["sword", "shield", "potion"]\ninventory.append("map")\ninventory.insert(0, "helmet")\ninventory.remove("shield")\npopped = inventory.pop()\n\nprint("Inventory:", inventory)\nprint("Popped:   ", popped)\nprint("Length:   ", len(inventory))\nprint("Slice 1:3:", inventory[1:3])\nprint("Reversed: ", inventory[::-1])\n\nhero = {"name": "Alex", "hp": 100, "mp": 50, "level": 3}\nhero["xp"] = 250\nmissing = hero.get("gold", 0)\n\nfor stat, val in hero.items():\n    print(f"  {stat:8s}: {val}")\nprint(f"  gold    : {missing} (default)")\n\nvisited = {"dungeon", "forest", "cave", "dungeon"}\nprint("\\nVisited zones:", visited)''',
        "questions": [
            {"q": "Add element to END of `my_list`?", "options": ["my_list.add(x)","my_list.append(x)","my_list.insert(x)","my_list.push(x)"], "answer": "my_list.append(x)"},
            {"q": "`my_dict.get('key', 'default')` if key missing?", "options": ["Raises KeyError","Returns None","Returns 'default'","Returns empty string"], "answer": "Returns 'default'"},
            {"q": "Output of `[x*2 for x in [1,2,3]]`?", "options": ["[1,2,3]","[2,4,6]","(2,4,6)","[1,4,9]"], "answer": "[2,4,6]"},
            {"q": "What does `my_list[-1]` return?", "options": ["First element","Last element","Second-to-last","Error"], "answer": "Last element"},
            {"q": "What is `len([1,2,3,4,5])`?", "options": ["4","5","6","Error"], "answer": "5"},
            {"q": "What does `[1,2,3].pop()` return?", "options": ["1","2","3","None"], "answer": "3"},
            {"q": "What does `sorted([3,1,2])` return?", "options": ["[3,1,2]","[1,2,3]","[3,2,1]","None"], "answer": "[1,2,3]"},
            {"q": "What does `dict.keys()` return?", "options": ["All values","All keys","All items as tuples","Length"], "answer": "All keys"},
            {"q": "What is `{'a':1,'b':2}['a']`?", "options": ["2","1","'a'","Error"], "answer": "1"},
            {"q": "What does `list.insert(0, x)` do?", "options": ["Appends x","Inserts x at beginning","Replaces index 0","Adds at x"], "answer": "Inserts x at beginning"},
            {"q": "Is `'a' in {'a': 1}` True?", "options": ["True","False","Error","None"], "answer": "True"},
            {"q": "What is `[1,2] + [3,4]`?", "options": ["[1,2,3,4]","[3,4,1,2]","Error","[2,4]"], "answer": "[1,2,3,4]"},
            {"q": "What does a Python set remove automatically?", "options": ["Sorted elements","Negatives","Duplicate values","Strings"], "answer": "Duplicate values"},
            {"q": "A tuple differs from a list because it is?", "options": ["Unordered","Immutable","Mutable","Slower"], "answer": "Immutable"},
            {"q": "What does `dict.items()` return?", "options": ["Only keys","Only values","Key-value pairs","Length"], "answer": "Key-value pairs"},
            {"q": "What does `list.count(x)` do?", "options": ["Returns length","Returns occurrences of x","Returns index of x","Removes x"], "answer": "Returns occurrences of x"},
            {"q": "What is `[0,1,2,3][1:3]`?", "options": ["[0,1]","[1,2]","[2,3]","[1,2,3]"], "answer": "[1,2]"},
            {"q": "What is `{1,2,2,3}` in Python?", "options": ["[1,2,2,3]","{1,2,3}","(1,2,3)","Error"], "answer": "{1,2,3}"},
            {"q": "What does `list.reverse()` return?", "options": ["New reversed list","None (in place)","First element","Error"], "answer": "None (in place)"},
            {"q": "What does `dict.update(other)` do?", "options": ["Creates new dict","Merges other into dict","Returns length","Clears dict"], "answer": "Merges other into dict"},
        ],
        "boss": {
            "name": "The Inventory Demon 📦", "xp_reward": 70,
            "lore": "A hoarder lurking at the bottom of your list. Only the correct method can banish it.",
            "challenge": "The Demon stole your last item! 🎒 Type the list method (with dot and parentheses) that adds to the END.",
            "hint": "Called like: `my_list.___(item)` — always adds to end.",
            "accepted": [".append()","append()",".append"], "display_answer": ".append()",
        },
    },
    4: {
        "title": "Functions", "mission": "Mission 4: Forge the Spellbook",
        "subtitle": "The Spells", "icon": "✨", "pixel_art": "🪄",
        "color": "#FF6B6B", "xp_reward": 160,
        "lore": "The ancient Spellbook is blank. Inscribe it with the power of reusable functions.",
        "description": """
## ✨ Chapter 4 — Functions

Functions are **reusable blocks of code** — your hero's spellbook.

### 📝 Defining & Calling
```python
def greet(name):
    return f"Welcome, {name}!"

result = greet("Alex")
```

### 🎯 Parameters
```python
def cast_spell(name, power=10, critical=False):
    damage = power * (2 if critical else 1)
    return f"{name} deals {damage} damage!"

# *args — positional as tuple
def total(*numbers):
    return sum(numbers)

# **kwargs — keyword args as dict
def show_stats(**stats):
    for k, v in stats.items():
        print(f"  {k}: {v}")
```

### ⚡ Lambda & Higher-Order Functions
```python
double  = lambda x: x * 2
list(map(lambda x: x*2, [1,2,3]))       # [2,4,6]
list(filter(lambda x: x>2, [1,2,3,4])) # [3,4]
sorted(heroes, key=lambda h: h["hp"])
```

### 🔁 Recursion
```python
def factorial(n):
    if n <= 1: return 1      # base case!
    return n * factorial(n-1)
```

### 🌍 Scope
```python
score = 100        # global
def update():
    global score   # required to modify
    score += 50
```
> 💡 One function = one job. Split it if it does more.
        """,
        "code_example": '''def greet(name):\n    return f"Welcome, {name}! Your quest begins."\n\ndef cast_spell(spell_name, power=10, critical=False):\n    damage = power * (2 if critical else 1)\n    return f"⚡ {spell_name} deals {damage} damage!"\n\ndef total_xp(*xp_gains):\n    return sum(xp_gains)\n\ndef factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n - 1)\n\ndouble = lambda x: x * 2\n\nprint(greet("Alex"))\nprint(cast_spell("Fireball", power=25))\nprint(cast_spell("Lightning", power=30, critical=True))\nprint(f"Total XP: {total_xp(50, 30, 20, 15)}")\nprint(f"5! = {factorial(5)}")\nprint(f"Double 7 = {double(7)}")\n\nnums = [1, 2, 3, 4, 5, 6]\nprint("Doubled:", list(map(lambda x: x*2, nums)))\nprint("Evens:  ", list(filter(lambda x: x%2==0, nums)))''',
        "questions": [
            {"q": "Which keyword defines a function?", "options": ["function","func","def","define"], "answer": "def"},
            {"q": "What does a function return with no `return`?", "options": ["0","False","None","Error"], "answer": "None"},
            {"q": "`lambda x: x ** 2` is equivalent to?", "options": ["def f(x): x**2","def f(x): return x**2","def f(): return x**2","lambda: x**2"], "answer": "def f(x): return x**2"},
            {"q": "What does `*args` collect?", "options": ["Single argument","Positional args as tuple","Keyword args as dict","Default args"], "answer": "Positional args as tuple"},
            {"q": "What does `**kwargs` collect?", "options": ["Positional as list","Keyword args as dict","All args as set","Nothing"], "answer": "Keyword args as dict"},
            {"q": "`def f(x=5): return x` — `f()` returns?", "options": ["0","None","5","Error"], "answer": "5"},
            {"q": "What does `global` keyword do inside a function?", "options": ["Creates variable","Accessible everywhere","Modifies global var","Deletes global"], "answer": "Modifies global var"},
            {"q": "What does every recursive function need?", "options": ["A global","A base case","A lambda","A return value"], "answer": "A base case"},
            {"q": "`list(map(lambda x: x*2, [1,2,3]))` returns?", "options": ["[1,2,3]","[2,4,6]","[1,4,9]","Error"], "answer": "[2,4,6]"},
            {"q": "`list(filter(lambda x: x>2, [1,2,3,4]))` returns?", "options": ["[1,2]","[3,4]","[1,2,3,4]","[2,3,4]"], "answer": "[3,4]"},
            {"q": "A docstring is placed?", "options": ["Top of file","After def line","End of function","Before def"], "answer": "After def line"},
            {"q": "Can a Python function return multiple values?", "options": ["No","Yes, as a tuple","Only with *args","Only with **kwargs"], "answer": "Yes, as a tuple"},
            {"q": "What does `return` do?", "options": ["Pauses function","Exits and optionally returns value","Restarts","Skips line"], "answer": "Exits and optionally returns value"},
            {"q": "A higher-order function?", "options": [">5 parameters","Takes or returns functions","Uses recursion","Has defaults"], "answer": "Takes or returns functions"},
            {"q": "`list(map(str, [1,2,3]))` produces?", "options": ["[1,2,3]","['1','2','3']","['str','str','str']","Error"], "answer": "['1','2','3']"},
            {"q": "Variable inside a function is?", "options": ["Global","Local","Static","Instance"], "answer": "Local"},
            {"q": "`sorted([5,2,8], key=lambda x: -x)` returns?", "options": ["[2,5,8]","[8,5,2]","[5,2,8]","[-5,-2,-8]"], "answer": "[8,5,2]"},
            {"q": "`def f(): pass` returns?", "options": ["0","False","None","Error"], "answer": "None"},
            {"q": "`enumerate(['a','b'])` first iteration?", "options": ["'a'","(0,'a')","(1,'a')","0"], "answer": "(0,'a')"},
            {"q": "`factorial(4)` where base case is 1?", "options": ["8","12","24","16"], "answer": "24"},
        ],
        "boss": {
            "name": "The Spell Caster 🪄", "xp_reward": 80,
            "lore": "An ancient wizard who guards the secrets of reusable code.",
            "challenge": "Prove you can create a function! ✨ Type the Python keyword used to *define* a new function.",
            "hint": "Every function starts with: `___ function_name():`",
            "accepted": ["def"], "display_answer": "def",
        },
    },
    5: {
        "title": "The Final Boss", "mission": "Mission 5: Slay the Shadow Dragon",
        "subtitle": "Comprehensive Python Test", "icon": "🐉", "pixel_art": "💀",
        "color": "#FF4444", "xp_reward": 200,
        "lore": "The Shadow Dragon has awoken. Prove total mastery of Python to defeat it.",
        "description": """
## 🐉 Chapter 5 — The Final Boss

### 🏛️ Object-Oriented Programming
```python
class Hero:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp   = hp

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        return f"{self.name} took {amount} dmg!"

    def __str__(self):
        return f"Hero({self.name}, HP={self.hp})"

class Wizard(Hero):
    def __init__(self, name, hp=80, mp=100):
        super().__init__(name, hp)
        self.mp = mp
```

### 🛡️ Error Handling
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    result = 0
except ValueError as e:
    print(f"Error: {e}")
else:
    print("No errors!")
finally:
    print("Always runs!")

raise ValueError("Custom error!")
```

### 📁 File I/O & JSON
```python
with open("save.json", "w") as f:
    json.dump({"score": 95}, f)

with open("save.json", "r") as f:
    data = json.load(f)
```

### 📦 Useful Modules
```python
import math, random
from collections import Counter
math.sqrt(16)              # 4.0
random.randint(1, 6)       # dice roll
Counter("aabbcc")          # {'a':2,'b':2,'c':2}
any([False, True])         # True
all([True, False])         # False
```
> 🏆 Score 6/10 to claim your **Python Master Certificate**!
        """,
        "code_example": '''import random\nfrom collections import Counter\n\nclass Hero:\n    def __init__(self, name, hp=100, mp=50):\n        self.name = name\n        self.hp   = hp\n        self.mp   = mp\n\n    def attack(self, enemy, base=20):\n        crit = random.random() < 0.25\n        dmg  = base * 2 if crit else base\n        enemy.hp = max(0, enemy.hp - dmg)\n        return f"{self.name}→{enemy.name}: {dmg} dmg{\" CRIT!\" if crit else \"\"} (HP:{enemy.hp})"\n\nclass Boss(Hero):\n    def rage(self, hero):\n        dmg = 35 + random.randint(0, 20)\n        hero.hp = max(0, hero.hp - dmg)\n        return f"RAGE {self.name}→{hero.name}: {dmg} dmg!"\n\nhero = Hero("Alex", hp=150, mp=60)\nboss = Boss("Shadow Dragon", hp=200)\nprint("BATTLE START!")\nfor r in range(1, 6):\n    print(f"\\n--- Round {r} ---")\n    print(" ", hero.attack(boss))\n    if boss.hp > 0: print(" ", boss.rage(hero))\n    if hero.hp <= 0 or boss.hp <= 0: break\nprint(f"\\nWinner: {hero.name if hero.hp > 0 else boss.name}")''',
        "questions": [
            {"q": "`max([3,1,4,1,5,9], key=lambda x: -x)` returns?", "options": ["9","1","3","-9"], "answer": "1"},
            {"q": "Unpack dict into keyword arguments?", "options": ["func(*my_dict)","func(**my_dict)","func(my_dict...)","func(#my_dict)"], "answer": "func(**my_dict)"},
            {"q": "Average-case dict lookup complexity?", "options": ["O(n)","O(log n)","O(1)","O(n²)"], "answer": "O(1)"},
            {"q": "Which block ALWAYS executes in try/except?", "options": ["try","except","else","finally"], "answer": "finally"},
            {"q": "What does `__init__` do?", "options": ["Destroys object","Initializes instance","Returns string","Defines class vars"], "answer": "Initializes instance"},
            {"q": "What does `self` refer to?", "options": ["The class","Current instance","Parent class","Global variable"], "answer": "Current instance"},
            {"q": "Call parent `__init__` from child?", "options": ["parent.__init__()","super().__init__()","base.__init__()","class.__init__()"], "answer": "super().__init__()"},
            {"q": "`any([False, True, False])` returns?", "options": ["False","True","None","Error"], "answer": "True"},
            {"q": "`all([True, True, False])` returns?", "options": ["True","False","None","Error"], "answer": "False"},
            {"q": "Which keyword creates a generator?", "options": ["return","yield","generate","next"], "answer": "yield"},
            {"q": "`isinstance(wizard, Hero)` if Wizard inherits Hero?", "options": ["False","True","Error","None"], "answer": "True"},
            {"q": "Exception raised by `int('abc')`?", "options": ["TypeError","ValueError","KeyError","IndexError"], "answer": "ValueError"},
            {"q": "`with open('f.txt') as f:` ensures?", "options": ["Write mode","Auto-closed after block","Full read","Created if missing"], "answer": "Auto-closed after block"},
            {"q": "`raise ValueError('msg')` does?", "options": ["Catches ValueError","Throws ValueError","Prints warning","Ignores error"], "answer": "Throws ValueError"},
            {"q": "`Counter('aabbcc')` returns?", "options": ["['a','b','c']","Counter({'a':2,'b':2,'c':2})","{'a','b','c'}","3"], "answer": "Counter({'a':2,'b':2,'c':2})"},
            {"q": "What is `__str__` for?", "options": ["Convert to bytes","String repr for print()","Deletes object","Compares objects"], "answer": "String repr for print()"},
            {"q": "`json.dump(data, f)` does?", "options": ["Reads JSON","Writes Python as JSON","Converts JSON to dict","Validates JSON"], "answer": "Writes Python as JSON"},
            {"q": "Handle multiple exception types?", "options": ["try/catch multiple","Multiple except blocks","except(E1,E2) only","Multiple try blocks"], "answer": "Multiple except blocks"},
            {"q": "`random.choice(['a','b','c'])` does?", "options": ["Returns all","Random element","Shuffles","Returns first"], "answer": "Random element"},
            {"q": "`sorted()` vs `list.sort()`?", "options": ["sorted() in-place; sort() new list","Both return None","sorted() new list; sort() in-place","Identical"], "answer": "sorted() new list; sort() in-place"},
        ],
        "boss": {
            "name": "The Shadow Dragon 🐉", "xp_reward": 100,
            "lore": "The ultimate guardian of the Python Realm — source of all runtime crashes.",
            "challenge": "The Shadow Dragon breathes exceptions! 🐉 Type the keyword used to *catch* exceptions in a try block.",
            "hint": "Structure: `try: ... ___ SomeError: handle it`",
            "accepted": ["except"], "display_answer": "except",
        },
    },
}

# ============================================================
# XP / RANK
# ============================================================
XP_TIERS = [
    (0,   "Apprentice",    "🌱"),
    (100, "Coder",         "💻"),
    (250, "Wizard",        "🧙"),
    (450, "Sorcerer",      "🔮"),
    (700, "Python Master", "🐍"),
]

def get_character_info(xp):
    title, icon = XP_TIERS[0][1], XP_TIERS[0][2]
    for threshold, t, i in XP_TIERS:
        if xp >= threshold: title, icon = t, i
    return title, icon

def xp_to_progress(xp):
    return min(xp / sum(v["xp_reward"] for v in LEVELS.values()), 1.0)

PASS_THRESHOLD     = 6
QUESTIONS_PER_EXAM = 10
QUESTIONS_IN_BANK  = 20

# ============================================================
# AUTH HELPERS
# ============================================================
def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()
def check_password(p, h): return hash_password(p) == h

def empty_progress():
    return {"xp":0,"completed_levels":[],"quiz_state":{},"cert_name":"","last_login":"","streak":0,"boss_beaten":[]}

def load_user_progress(username):
    db   = get_db()
    prog = db["progress"].get(username, empty_progress())
    st.session_state.xp               = prog.get("xp", 0)
    st.session_state.completed_levels = set(prog.get("completed_levels", []))
    raw_qs = prog.get("quiz_state", {})
    st.session_state.quiz_state        = {int(k): v for k, v in raw_qs.items()}
    st.session_state.cert_name         = prog.get("cert_name", "")
    st.session_state.streak            = prog.get("streak", 0)
    st.session_state.last_login        = prog.get("last_login", "")
    st.session_state.boss_beaten       = set(prog.get("boss_beaten", []))

def save_user_progress(username):
    db = get_db()
    db.setdefault("progress", {})[username] = {
        "xp":               st.session_state.xp,
        "completed_levels": list(st.session_state.completed_levels),
        "quiz_state":       {str(k): v for k, v in st.session_state.quiz_state.items()},
        "cert_name":        st.session_state.cert_name,
        "streak":           st.session_state.get("streak", 0),
        "last_login":       st.session_state.get("last_login", ""),
        "boss_beaten":      list(st.session_state.get("boss_beaten", set())),
    }
    flush_db()

def update_streak(username):
    today = date.today().isoformat()
    db    = get_db()
    prog  = db["progress"].get(username, empty_progress())
    last  = prog.get("last_login", "")
    s     = prog.get("streak", 0)
    if last:
        try:
            diff = (date.today() - date.fromisoformat(last)).days
            if diff == 0:   pass
            elif diff == 1: s += 1
            else:           s = 1
        except: s = 1
    else: s = 1
    prog["last_login"] = today
    prog["streak"]     = s
    db["progress"][username] = prog
    flush_db()
    return s

# ============================================================
# SESSION STATE
# ============================================================
def init_state():
    defaults = {
        "logged_in": False, "username": "", "auth_tab": "login",
        "auth_error": "", "auth_success": "",
        "xp": 0, "completed_levels": set(), "quiz_state": {}, "cert_name": "",
        "current_level": 1, "show_badge": None, "view": "hub",
        "streak": 0, "last_login": "", "boss_beaten": set(),
        "lab_open": False, "sandbox_code": "", "sandbox_output": "", "sandbox_error": "",
        "dark_mode": True,
    }
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v

# ============================================================
# GAME HELPERS
# ============================================================
def is_level_unlocked(lid): return lid == 1 or (lid-1) in st.session_state.completed_levels
def level_status(lid):
    if lid in st.session_state.completed_levels: return "done"
    if is_level_unlocked(lid): return "unlocked"
    return "locked"
def quiz_key(lid, idx): return f"q_{lid}_{idx}"
def streak_multiplier(): return 1.2 if st.session_state.get("streak",0) >= 2 else 1.0

def get_exam_questions(level_id):
    qs_data = st.session_state.quiz_state.get(level_id, {})
    bank    = LEVELS[level_id]["questions"]
    if "indices" in qs_data:
        indices = qs_data["indices"]
    else:
        indices = sorted(random.sample(range(len(bank)), QUESTIONS_PER_EXAM))
        st.session_state.quiz_state.setdefault(level_id, {})["indices"] = indices
        save_user_progress(st.session_state.username)
    return [bank[i] for i in indices], indices

def do_register(username, password, confirm):
    username = username.strip().lower()
    if not username or not password:          st.session_state.auth_error = "Fields cannot be empty."; return
    if len(username) < 3:                     st.session_state.auth_error = "Username: min 3 chars."; return
    if len(password) < 6:                     st.session_state.auth_error = "Password: min 6 chars."; return
    if password != confirm:                   st.session_state.auth_error = "Passwords do not match."; return
    db = get_db()
    if username in db["users"]:               st.session_state.auth_error = "Username taken."; return
    db["users"][username]    = {"pw_hash": hash_password(password), "registered": datetime.now().isoformat()}
    db["progress"][username] = empty_progress()
    flush_db()
    st.session_state.auth_error   = ""
    st.session_state.auth_success = f"Account created! Welcome, {username} 🎉 Now log in."
    st.session_state.auth_tab     = "login"

def do_login(username, password):
    username = username.strip().lower()
    db = get_db()
    if username not in db["users"]:            st.session_state.auth_error = "Username not found."; return
    if not check_password(password, db["users"][username]["pw_hash"]):
        st.session_state.auth_error = "Incorrect password."; return
    st.session_state.auth_error   = ""
    st.session_state.auth_success = ""
    st.session_state.logged_in    = True
    st.session_state.username     = username
    new_streak = update_streak(username)
    load_user_progress(username)
    st.session_state.streak = new_streak
    st.session_state.view   = "hub"

# ============================================================
# apply_styles()  — FULL CSS with permanent sidebar hack
# ============================================================
def apply_styles():
    dark = st.session_state.get("dark_mode", True)

    if dark:
        bg          = "#0A0A0A"
        bg2         = "#111111"
        card        = "#161616"
        card2       = "#1C1C1C"
        border      = "#2A2A2A"
        text        = "#F0F0F0"
        text2       = "#DDDDDD"
        muted       = "#888888"
        neon        = "#00FF41"
        purple      = "#6200EE"
        purple2     = "#9D46FF"
        sidebar_bg  = "#090909"
        code_bg     = "#060606"
        code_color  = "#00FF41"
        input_bg    = "#111111"
        btn_glow    = "0 0 18px rgba(0,255,65,0.55), 4px 4px 0 #000"
        btn_hover   = "0 0 30px rgba(0,255,65,0.85), 6px 6px 0 #000"
        shadow      = "4px 4px 0 #000"
        xp_grad     = "linear-gradient(90deg, #00FF41 0%, #00CC33 50%, #FFD700 100%)"
        xp_glow     = "0 0 14px rgba(0,255,65,0.6), inset 0 1px 3px rgba(255,255,255,0.1)"
    else:
        bg          = "#F5F0E8"
        bg2         = "#EDE8DC"
        card        = "#FFFFFF"
        card2       = "#F8F4EC"
        border      = "#C8C0B0"
        text        = "#0D1B2A"
        text2       = "#1E3050"
        muted       = "#4A5568"
        neon        = "#006600"
        purple      = "#4A00CC"
        purple2     = "#6622EE"
        sidebar_bg  = "#EDE8DC"
        code_bg     = "#1A1A2E"
        code_color  = "#00FF41"
        input_bg    = "#FFFFFF"
        btn_glow    = "0 0 10px rgba(0,100,0,0.3), 3px 3px 0 #555"
        btn_hover   = "0 0 18px rgba(0,100,0,0.5), 5px 5px 0 #444"
        shadow      = "3px 3px 0 #888"
        xp_grad     = "linear-gradient(90deg, #006600 0%, #009900 60%, #CC7700 100%)"
        xp_glow     = "0 0 8px rgba(0,100,0,0.4), inset 0 1px 3px rgba(255,255,255,0.15)"

    st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

  /* ════════════════════════════════════════════
     PERMANENT SIDEBAR — hides collapse button,
     locks sidebar open at all times
  ════════════════════════════════════════════ */
  [data-testid="collapsedControl"]          {{ display: none !important; }}
  [data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
  button[data-testid="baseButton-header"]   {{ display: none !important; }}
  [data-testid="stSidebar"] {{
    min-width: 290px !important;
    max-width: 290px !important;
    width:     290px !important;
    background: {sidebar_bg} !important;
    border-right: 2px solid {border};
    transform: none !important;
    visibility: visible !important;
    display: block !important;
  }}
  [data-testid="stSidebar"] > div:first-child {{
    transform: none !important;
    width: 290px !important;
  }}
  [data-testid="stSidebar"] .block-container {{
    padding: 0.8rem 1rem !important;
    width: 100% !important;
  }}
  /* force main content not to cover sidebar */
  .main .block-container {{
    padding-left: 1.5rem !important;
    max-width: 1000px !important;
  }}

  /* ── Base ── */
  :root {{
    --bg:      {bg};
    --bg2:     {bg2};
    --card:    {card};
    --card2:   {card2};
    --border:  {border};
    --text:    {text};
    --text2:   {text2};
    --muted:   {muted};
    --neon:    {neon};
    --purple:  {purple};
    --purple2: {purple2};
    --radius:  8px;
  }}
  .stApp {{
    background: {bg} !important;
    font-family: 'Outfit', sans-serif;
    color: {text};
  }}
  #MainMenu, footer, header {{ visibility: hidden; }}
  .stDeployButton {{ display: none; }}

  /* ── Typography ── */
  h1, h2, h3 {{ font-family: 'Syne', sans-serif !important; color: {text} !important; }}
  p, li, span {{ color: {text2} !important; }}
  code {{ color: {code_color} !important; }}

  /* ── Sidebar text overrides — all must be visible ── */
  [data-testid="stSidebar"] * {{
    color: {text} !important;
    font-family: 'Outfit', sans-serif;
  }}
  [data-testid="stSidebar"] code {{
    color: {code_color} !important;
    background: {code_bg} !important;
  }}

  /* ── Buttons ── */
  .stButton > button {{
    background: {neon} !important;
    color: #000 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    border: 2px solid #000 !important;
    border-radius: var(--radius) !important;
    box-shadow: {btn_glow} !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.12s ease !important;
    letter-spacing: 0.02em;
    width: 100%;
  }}
  .stButton > button:hover  {{ transform: translate(-2px,-2px) !important; box-shadow: {btn_hover} !important; }}
  .stButton > button:active {{ transform: translate(1px,1px) !important; }}
  .stButton > button:disabled {{ background: {border} !important; color: {muted} !important; box-shadow: none !important; }}

  /* ── RPG XP Bar ── */
  .xp-bar-wrap {{
    background: {card2};
    border: 2px solid {border};
    border-radius: 50px;
    height: 28px;
    width: 100%;
    margin: 0.4rem 0 0.8rem;
    position: relative;
    overflow: hidden;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.5);
  }}
  .xp-bar-fill {{
    height: 100%;
    border-radius: 50px;
    background: {xp_grad};
    box-shadow: {xp_glow};
    transition: width 0.6s ease;
    position: relative;
  }}
  .xp-bar-fill::after {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 40%;
    background: rgba(255,255,255,0.15);
    border-radius: 50px 50px 0 0;
  }}
  .xp-bar-label {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    color: #fff !important;
    text-shadow: 0 1px 3px rgba(0,0,0,0.9);
    white-space: nowrap;
    z-index: 2;
  }}

  /* ── Player Card (sidebar top) ── */
  .player-card {{
    background: linear-gradient(135deg, {card} 0%, {card2} 100%);
    border: 2px solid {border};
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    text-align: center;
  }}
  .avatar-ring {{
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: linear-gradient(135deg, {purple}, {neon});
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.5rem;
    border: 3px solid {neon};
    box-shadow: 0 0 16px rgba(0,255,65,0.35);
  }}

  /* ── Stat rows ── */
  .stat-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid {border};
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.73rem;
  }}
  .stat-row .label {{ color: {muted} !important; }}
  .stat-row .val   {{ color: {text}  !important; font-weight: 700; }}

  /* ── Cards ── */
  .card {{
    background: {card};
    border: 2px solid {border};
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    box-shadow: {shadow};
    margin-bottom: 0.8rem;
  }}
  .card * {{ color: {text2} !important; }}
  .card-neon {{
    background: {card};
    border: 2px solid {neon};
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    box-shadow: 0 0 12px rgba(0,255,65,0.2), {shadow};
    margin-bottom: 0.8rem;
  }}

  /* ── Boxes ── */
  .info-box {{
    background: rgba(98,0,238,0.1);
    border-left: 4px solid {purple2};
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 0.8rem 1.1rem;
    margin: 0.8rem 0;
    color: {text2} !important;
  }}
  .info-box * {{ color: {text2} !important; }}
  .success-box {{
    background: rgba(0,255,65,0.07);
    border-left: 4px solid {neon};
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 0.8rem 1.1rem;
    margin: 0.8rem 0;
    color: {neon} !important;
  }}
  .locked-box {{
    background: rgba(255,100,0,0.07);
    border: 2px dashed #FF6400;
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    text-align: center;
    color: #FF8844 !important;
  }}
  .locked-box * {{ color: #FF8844 !important; }}
  .divider {{ border: none; border-top: 2px solid {border}; margin: 1rem 0; }}
  .neon-heading {{
    color: {neon} !important;
    text-shadow: 0 0 12px rgba(0,255,65,0.35);
    font-family: 'Syne', sans-serif;
  }}

  /* ── Quest path ── */
  .mission-card {{
    background: {card};
    border: 2px solid {border};
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0;
    transition: border-color 0.2s, box-shadow 0.2s;
  }}
  .mission-card.active {{
    border-color: {neon};
    box-shadow: 0 0 14px rgba(0,255,65,0.2), {shadow};
  }}
  .mission-card.locked {{ opacity: 0.45; }}
  .path-line {{
    width: 3px;
    height: 2rem;
    background: linear-gradient(180deg, {neon} 0%, transparent 100%);
    margin: 0 auto;
    border-radius: 2px;
    opacity: 0.35;
  }}
  .path-line-locked {{
    width: 3px;
    height: 2rem;
    background: {border};
    margin: 0 auto;
    border-radius: 2px;
    opacity: 0.25;
  }}

  /* ── Milestone ── */
  .milestone {{
    background: linear-gradient(135deg, #6200EE, #9D46FF);
    border: 3px solid {neon};
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 0 30px rgba(0,255,65,0.3), 6px 6px 0 #000;
    margin: 1rem 0;
  }}
  .milestone * {{ color: #fff !important; }}

  /* ── Boss ── */
  .boss-card {{
    background: linear-gradient(135deg, #1a0505, #300000);
    border: 3px solid #FF4444;
    border-radius: 12px;
    padding: 1.6rem;
    box-shadow: 0 0 30px rgba(255,68,68,0.3), 6px 6px 0 #000;
    margin: 1rem 0;
  }}
  .boss-card p, .boss-card span {{ color: #ddd !important; }}
  .boss-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    color: #FF4444 !important;
    text-shadow: 0 0 12px rgba(255,68,68,0.6);
    margin-bottom: 0.6rem;
    font-weight: 700;
  }}
  .boss-beaten {{
    background: rgba(0,255,65,0.07);
    border: 2px solid {neon};
    border-radius: 8px;
    padding: 1.2rem;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    color: {neon} !important;
    font-size: 0.9rem;
    margin-top: 1rem;
  }}

  /* ── Leaderboard ── */
  .lb-row {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.7rem 1rem;
    background: {card2};
    border: 1px solid {border};
    border-radius: 8px;
    margin-bottom: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    transition: border-color 0.2s;
  }}
  .lb-row:hover {{ border-color: {neon}; }}
  .lb-rank {{ font-size: 1.3rem; min-width: 2.5rem; text-align: center; }}
  .lb-name {{ color: {text}  !important; font-size: 0.78rem; flex: 1; }}
  .lb-xp   {{ color: {neon} !important; font-size: 0.78rem; font-weight: 700; min-width: 5rem; text-align: right; }}
  .lb-you  {{ color: #FFD700 !important; }}

  /* ── Practice Lab ── */
  .lab-panel {{
    background: {card};
    border: 2px solid {neon};
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 0 24px rgba(0,255,65,0.15), {shadow};
  }}
  .stTextArea > div > div > textarea {{
    background: {code_bg} !important;
    border: 2px solid {border} !important;
    color: {code_color} !important;
    border-radius: var(--radius) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    line-height: 1.55 !important;
  }}
  .stTextArea > div > div > textarea:focus {{ border-color: {neon} !important; }}
  .sandbox-output {{
    background: {code_bg};
    border: 2px solid {border};
    border-radius: 8px;
    padding: 0.75rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: {code_color} !important;
    white-space: pre-wrap;
    min-height: 2.5rem;
    max-height: 12rem;
    overflow-y: auto;
    margin-top: 0.3rem;
  }}
  .sandbox-error {{
    background: rgba(255,68,68,0.06);
    border: 2px solid #FF4444;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    color: #FF8888 !important;
    white-space: pre-wrap;
    margin-top: 0.3rem;
  }}
  .sandbox-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem;
    color: {muted} !important;
    margin: 0.2rem 0;
  }}

  /* ── Inputs ── */
  .stTextInput > div > div > input {{
    background: {input_bg} !important;
    border: 2px solid {border} !important;
    color: {text} !important;
    border-radius: var(--radius) !important;
    font-family: 'JetBrains Mono', monospace !important;
  }}
  .stTextInput > div > div > input:focus {{
    border-color: {neon} !important;
    box-shadow: 0 0 0 1px {neon} !important;
  }}
  .stTextInput > label {{ color: {muted} !important; font-size: 0.76rem !important; }}

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {{ background: transparent; gap: 0.4rem; }}
  .stTabs [data-baseweb="tab"] {{
    background: {card2} !important;
    border: 2px solid {border} !important;
    border-radius: var(--radius) !important;
    color: {text2} !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.74rem !important;
  }}
  .stTabs [aria-selected="true"] {{
    background: {purple} !important;
    border-color: {purple} !important;
    color: #fff !important;
  }}
  .stTabs [data-baseweb="tab-panel"] {{ background: transparent !important; padding: 1rem 0 !important; }}

  /* ── Radio ── */
  .stRadio > label {{ color: {text} !important; }}
  .stRadio [data-testid="stMarkdownContainer"] p {{ color: {text} !important; }}
  .stRadio label span {{ color: {text} !important; }}

  /* ── Code ── */
  .stCodeBlock, pre, code {{
    font-family: 'JetBrains Mono', monospace !important;
    background: {code_bg} !important;
    border: 1px solid {border} !important;
    border-radius: var(--radius) !important;
  }}

  /* ── Expander ── */
  .streamlit-expanderHeader {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.76rem !important;
    color: {neon} !important;
    background: {card2} !important;
    border: 1px solid {border} !important;
    border-radius: 6px !important;
  }}
  [data-testid="stSidebar"] .streamlit-expanderHeader {{
    background: {sidebar_bg} !important;
  }}

  /* ── XP badge ── */
  .xp-badge {{
    display: inline-block;
    background: {purple};
    color: #fff !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border: 2px solid #000;
    border-radius: 4px;
    box-shadow: 2px 2px 0 #000;
  }}
  .streak-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: linear-gradient(135deg, #FF6400, #FF9000);
    color: #000 !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.3rem 0.8rem;
    border: 2px solid #000;
    border-radius: 4px;
    box-shadow: 2px 2px 0 #000;
    width: 100%;
    justify-content: center;
    margin: 0.3rem 0;
  }}
  .pass-badge {{ color: {neon}   !important; font-family: 'JetBrains Mono',monospace; font-size:0.78rem; }}
  .fail-badge {{ color: #FF4444 !important; font-family: 'JetBrains Mono',monospace; font-size:0.78rem; }}

  /* ── Markdown tables ── */
  table {{ width:100%; border-collapse: collapse; margin: 0.8rem 0; }}
  th {{ background: {card2}; color: {text} !important; padding: 0.5rem; border: 1px solid {border}; font-family:'JetBrains Mono',monospace; font-size:0.78rem; }}
  td {{ color: {text2} !important; padding: 0.45rem; border: 1px solid {border}; font-size:0.82rem; }}
</style>
""", unsafe_allow_html=True)


# ============================================================
# render_lab()  — FLOATING PRACTICE LAB
# ============================================================
def render_lab():
    lab_open = st.session_state.get("lab_open", False)

    with st.sidebar:
        btn_label = "✕ Close Lab" if lab_open else "🧪 Practice Lab"
        if st.button(btn_label, key="lab_fab"):
            st.session_state.lab_open = not lab_open
            st.rerun()

    if not st.session_state.get("lab_open", False):
        return

    # Render inline below sidebar — in main area
    dark      = st.session_state.get("dark_mode", True)
    neon      = "#00FF41"
    code_bg   = "#060606" if dark else "#1A1A2E"

    st.markdown('<div class="lab-panel">', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:{neon};margin-bottom:0.5rem;">'
        '// 🧪 PRACTICE LAB — Write Python, hit ▶ Run</div>',
        unsafe_allow_html=True)

    code = st.text_area(
        "lab_editor",
        value=st.session_state.get("sandbox_code", ""),
        height=170,
        key="sandbox_code_widget",
        placeholder='print("Hello, Realm!")\nfor i in range(5):\n    print(i)',
        label_visibility="collapsed",
    )
    st.session_state.sandbox_code = code

    col_run, col_clr, col_x = st.columns([3, 1, 1])
    with col_run:
        run_clicked = st.button("▶ Run", key="lab_run", use_container_width=True)
    with col_clr:
        if st.button("🗑", key="lab_clear", use_container_width=True):
            st.session_state.sandbox_output = ""
            st.session_state.sandbox_error  = ""
            st.rerun()
    with col_x:
        if st.button("✕", key="lab_close", use_container_width=True):
            st.session_state.lab_open = False
            st.rerun()

    if run_clicked and code.strip():
        buf = io.StringIO()
        sys.stdout = buf
        try:
            exec(compile(code, "<lab>", "exec"), {})
            st.session_state.sandbox_output = buf.getvalue() or "(no output)"
            st.session_state.sandbox_error  = ""
        except Exception:
            tb = traceback.format_exc()
            st.session_state.sandbox_error  = tb
            st.session_state.sandbox_output = ""
            # Dungeon Guide — smart feedback
            if "NameError"          in tb: st.toast("🧙 Guide: A variable is used before it's defined!", icon="💡")
            elif "SyntaxError"      in tb: st.toast("🧙 Guide: Check your colons, brackets & quotes!", icon="💡")
            elif "IndentationError" in tb: st.toast("🧙 Guide: Python needs exactly 4 spaces per indent.", icon="💡")
            elif "TypeError"        in tb: st.toast("🧙 Guide: Mixing incompatible types — e.g. str + int!", icon="💡")
            elif "IndexError"       in tb: st.toast("🧙 Guide: List index out of range!", icon="💡")
            elif "KeyError"         in tb: st.toast("🧙 Guide: Dict key doesn't exist — use .get()!", icon="💡")
            elif "ZeroDivisionError"in tb: st.toast("🧙 Guide: Can't divide by zero!", icon="💡")
            else:                          st.toast("🧙 Guide: Read the error message carefully!", icon="⚠️")
        finally:
            sys.stdout = sys.__stdout__

    out = st.session_state.get("sandbox_output", "")
    err = st.session_state.get("sandbox_error",  "")
    if out:
        st.markdown(f'<div class="sandbox-label">// OUTPUT</div><div class="sandbox-output">{out}</div>', unsafe_allow_html=True)
    if err:
        st.markdown(f'<div class="sandbox-label" style="color:#FF4444;">// ERROR</div><div class="sandbox-error">{err}</div>', unsafe_allow_html=True)
    if not out and not err:
        st.markdown('<div class="sandbox-label">// output appears here after Run ▶</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# render_sidebar()
# ============================================================
def render_sidebar():
    xp          = st.session_state.xp
    title, icon = get_character_info(xp)
    max_xp      = sum(v["xp_reward"] for v in LEVELS.values())
    completed   = len(st.session_state.completed_levels)
    boss_count  = len(st.session_state.get("boss_beaten", set()))
    streak      = st.session_state.get("streak", 0)
    stars       = sum(st.session_state.quiz_state.get(l,{}).get("score",0) for l in st.session_state.completed_levels)
    pct         = int(xp_to_progress(xp) * 100)
    bar_w       = xp_to_progress(xp) * 100
    dark        = st.session_state.get("dark_mode", True)
    neon        = "#00FF41" if dark else "#006600"
    muted       = "#888" if dark else "#4A5568"
    text        = "#F0F0F0" if dark else "#0D1B2A"
    avatar      = st.session_state.username[:2].upper() if st.session_state.username else "??"

    with st.sidebar:
        # ── Brand ──
        st.markdown(
            f'<div style="text-align:center;padding:0.3rem 0 0.6rem;">'
            f'<span style="font-family:JetBrains Mono,monospace;font-size:0.48rem;'
            f'color:{neon};letter-spacing:0.35em;">🐍 PYTHON ADVENTURE</span>'
            f'</div>',
            unsafe_allow_html=True)

        # ── PLAYER CARD ──
        streak_fires = "🔥" * min(streak, 5) if streak >= 1 else ""
        streak_label = f"🔥 {streak}-Day Streak! +20% XP" if streak >= 2 else ("🔥 Login tomorrow for a streak!" if streak == 1 else "No streak yet")
        streak_color = "#FF9000" if streak >= 1 else muted

        st.markdown(
            f'<div class="player-card">'
            f'  <div class="avatar-ring">'
            f'    <span style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;color:#fff;">{avatar}</span>'
            f'  </div>'
            f'  <div style="font-family:Syne,sans-serif;font-size:1rem;font-weight:700;color:{text};">{icon} {title}</div>'
            f'  <div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:{neon};margin:0.1rem 0;">@{st.session_state.username}</div>'
            f'  <div style="font-size:0.68rem;color:{streak_color};margin-top:0.25rem;">{streak_label}</div>'
            f'</div>',
            unsafe_allow_html=True)

        # ── RPG XP BAR ──
        st.markdown(
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:{muted};'
            f'letter-spacing:0.1em;margin-bottom:0.2rem;">EXPERIENCE POINTS</div>'
            f'<div class="xp-bar-wrap">'
            f'  <div class="xp-bar-fill" style="width:{bar_w:.1f}%;"></div>'
            f'  <div class="xp-bar-label">{xp} / {max_xp} XP</div>'
            f'</div>',
            unsafe_allow_html=True)

        # ── STATS ──
        for label, val, color in [
            ("Levels Done",   f"{completed} / 5",      neon),
            ("Bosses Slain",  f"💀 {boss_count} / 5",  "#FF4444"),
            ("Quiz Stars",    f"⭐ {stars} pts",        "#FFD700"),
            ("Pass Mark",     "6 / 10 (60%)",           "#9D46FF"),
        ]:
            st.markdown(
                f'<div class="stat-row">'
                f'<span class="label">{label}</span>'
                f'<span class="val" style="color:{color}!important;">{val}</span>'
                f'</div>',
                unsafe_allow_html=True)

        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        # ── NAVIGATION ──
        st.markdown(
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.58rem;color:{muted};'
            f'letter-spacing:0.12em;margin-bottom:0.4rem;">NAVIGATION</div>',
            unsafe_allow_html=True)

        if st.button("🏠  Adventure Hub",   key="nav_hub"):
            st.session_state.view = "hub";         st.rerun()
        if st.button("🏆  Leaderboard",     key="nav_lb"):
            st.session_state.view = "leaderboard"; st.rerun()

        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        # ── PRACTICE LAB TOGGLE (FAB inside sidebar) ──
        render_lab()   # draws the toggle button here

        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        # ── QUEST MAP ──
        st.markdown(
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.58rem;color:{muted};'
            f'letter-spacing:0.12em;margin-bottom:0.4rem;">QUEST MAP</div>',
            unsafe_allow_html=True)

        for idx, (lid, lvl) in enumerate(LEVELS.items()):
            status  = level_status(lid)
            st_icon = {"done":"✅","unlocked":"🔓","locked":"🔒"}[status]
            clr     = {"done":neon,"unlocked":text,"locked":muted}[status]
            qs      = st.session_state.quiz_state.get(lid,{})
            sc_txt  = f" ({qs.get('score',0)}/10)" if qs.get("submitted") else ""
            boss_ic = " 💀" if lid in st.session_state.get("boss_beaten",set()) else ""
            mission_n = lvl["mission"].split(":")[0]

            st.markdown(
                f'<div style="display:flex;align-items:center;gap:0.5rem;padding:0.3rem 0.4rem;'
                f'border-radius:6px;{"background:rgba(0,255,65,0.05);" if status=="unlocked" else ""}">'
                f'<span style="font-size:0.9rem;">{st_icon}</span>'
                f'<div>'
                f'<div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:{clr};font-weight:700;">'
                f'{mission_n}{sc_txt}{boss_ic}</div>'
                f'<div style="font-size:0.6rem;color:{muted};">{lvl["title"]}</div>'
                f'</div></div>',
                unsafe_allow_html=True)

            if idx < len(LEVELS)-1:
                cls = "path-line" if status != "locked" else "path-line-locked"
                st.markdown(f'<div class="{cls}"></div>', unsafe_allow_html=True)

        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        # ── SPELLBOOK ──
        available = [1] + sorted(i for i in st.session_state.completed_levels if i != 1)
        with st.expander("📖 My Spellbook", expanded=False):
            if len(available) == 1 and 1 not in st.session_state.completed_levels:
                st.markdown(f'<span style="color:{muted};font-size:0.72rem;">Complete missions to unlock spells!</span>', unsafe_allow_html=True)
            else:
                for lid in available:
                    sb = SPELLBOOK.get(lid)
                    if not sb: continue
                    st.markdown(f'<div style="color:{neon};font-family:JetBrains Mono,monospace;font-size:0.65rem;margin:0.5rem 0 0.2rem;">{sb["title"]}</div>', unsafe_allow_html=True)
                    for spell_name, snippet in sb["spells"]:
                        st.markdown(f'<div style="color:{muted};font-size:0.6rem;">{spell_name}</div>', unsafe_allow_html=True)
                        st.code(snippet, language="python")

        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        # ── THEME + LOGOUT ──
        dark_label = "☀️  Scholar Mode (Light)" if dark else "🌑  Matrix Mode (Dark)"
        if st.button(dark_label, key="theme_toggle"):
            st.session_state.dark_mode = not dark; st.rerun()

        if st.button("🚪  Log Out", key="logout"):
            save_user_progress(st.session_state.username)
            for k in ["logged_in","username","xp","completed_levels","quiz_state","cert_name",
                      "current_level","show_badge","view","streak","last_login","boss_beaten",
                      "sandbox_output","sandbox_error","sandbox_code","lab_open"]:
                st.session_state.pop(k, None)
            st.rerun()


# ============================================================
# render_auth()
# ============================================================
def render_auth():
    dark = st.session_state.get("dark_mode", True)
    neon = "#00FF41" if dark else "#006600"
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown(
            f'<div style="text-align:center;padding-top:2.5rem;">'
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.52rem;color:{neon};'
            f'letter-spacing:0.4em;margin-bottom:0.5rem;">🐍 PYTHON CODING ADVENTURE</div>'
            f'<div style="font-family:Syne,sans-serif;font-size:2rem;font-weight:800;color:var(--text);">'
            f'Welcome, Adventurer</div>'
            f'<div style="font-size:0.85rem;color:var(--muted);margin-top:0.3rem;">'
            f'XP, streaks and progress saved permanently</div>'
            f'</div>',
            unsafe_allow_html=True)
        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔓 Log In",   use_container_width=True, key="tab_login"):
                st.session_state.auth_tab = "login";    st.session_state.auth_error = ""; st.rerun()
        with c2:
            if st.button("✨ Register", use_container_width=True, key="tab_reg"):
                st.session_state.auth_tab = "register"; st.session_state.auth_error = ""; st.rerun()

        active = st.session_state.auth_tab
        a_col  = neon if active=="login" else "var(--border)"
        b_col  = neon if active=="register" else "var(--border)"
        st.markdown(
            f'<div style="display:flex;margin-bottom:1.2rem;">'
            f'<div style="flex:1;height:3px;background:{a_col};border-radius:2px 0 0 2px;"></div>'
            f'<div style="flex:1;height:3px;background:{b_col};border-radius:0 2px 2px 0;"></div>'
            f'</div>',
            unsafe_allow_html=True)

        if st.session_state.auth_error:
            st.markdown(f'<div style="background:rgba(255,68,68,0.12);border-left:4px solid #FF4444;border-radius:0 8px 8px 0;padding:0.75rem 1rem;color:#FF8888;margin-bottom:0.8rem;">⚠️ {st.session_state.auth_error}</div>', unsafe_allow_html=True)
        if st.session_state.auth_success:
            st.markdown(f'<div class="success-box">✅ {st.session_state.auth_success}</div>', unsafe_allow_html=True)

        if active == "login":
            u = st.text_input("Username", placeholder="your_username", key="li_u")
            p = st.text_input("Password", type="password", placeholder="••••••••", key="li_p")
            st.markdown("")
            if st.button("⚡ Log In & Start Adventure", use_container_width=True, key="login_btn"):
                do_login(u, p); st.rerun()
        else:
            u  = st.text_input("Choose a Username", placeholder="coolcoder99 (min 3 chars)", key="reg_u")
            p  = st.text_input("Choose a Password", type="password", placeholder="Min. 6 characters", key="reg_p")
            c  = st.text_input("Confirm Password",  type="password", placeholder="Repeat password", key="reg_c")
            st.markdown("")
            if st.button("🚀 Create My Account", use_container_width=True, key="reg_btn"):
                do_register(u, p, c); st.rerun()

        st.markdown(
            '<div style="text-align:center;margin-top:2rem;padding:0.75rem;background:var(--card);'
            'border:1px dashed var(--border);border-radius:8px;">'
            '<span style="font-size:0.72rem;color:var(--muted);">💾 Progress saved to disk — '
            '🔥 Login daily to build your streak and earn +20% bonus XP!</span></div>',
            unsafe_allow_html=True)


# ============================================================
# render_hub()  — VERTICAL QUEST PATH
# ============================================================
def render_hub():
    dark   = st.session_state.get("dark_mode", True)
    neon   = "#00FF41" if dark else "#006600"
    muted  = "#888" if dark else "#4A5568"
    text   = "#F0F0F0" if dark else "#0D1B2A"
    text2  = "#DDDDDD" if dark else "#1E3050"
    streak = st.session_state.get("streak", 0)

    if streak >= 2:
        st.markdown(
            f'<div style="background:linear-gradient(90deg,rgba(255,100,0,0.12),transparent);'
            f'border-left:4px solid #FF6400;border-radius:0 8px 8px 0;padding:0.6rem 1.1rem;margin-bottom:0.8rem;">'
            f'🔥 <strong style="color:#FF9000;">{streak}-Day Streak Active!</strong> '
            f'<span style="color:{muted};font-size:0.8rem;"> All XP gains ×1.2 today.</span></div>',
            unsafe_allow_html=True)

    st.markdown(
        f'<h1 class="neon-heading" style="font-size:1.7rem;margin-bottom:0.15rem;">🐍 Python Coding Adventure</h1>'
        f'<p style="color:{muted};font-family:JetBrains Mono,monospace;font-size:0.72rem;">'
        f'Welcome back, <span style="color:{neon};">@{st.session_state.username}</span>'
        f' — choose your next mission!</p>',
        unsafe_allow_html=True)
    st.markdown("<div class='divider'/>", unsafe_allow_html=True)

    level_items = list(LEVELS.items())
    for idx, (lid, lvl) in enumerate(level_items):
        status  = level_status(lid)
        border  = neon if status=="done" else (lvl["color"] if status=="unlocked" else "var(--border)")
        opacity = "1" if status != "locked" else "0.45"
        lbl_txt = "✅ COMPLETE" if status=="done" else ("▶ LAUNCH MISSION" if status=="unlocked" else "🔒 LOCKED")
        lbl_col = neon if status=="done" else (text if status=="unlocked" else muted)
        glow    = f"0 0 14px rgba(0,255,65,0.2), 3px 3px 0 #000" if status=="unlocked" else "3px 3px 0 #000"
        qs      = st.session_state.quiz_state.get(lid,{})
        sc_html = ""
        if qs.get("submitted"):
            sc      = qs.get("score",0)
            sc_html = f'<span style="font-size:0.65rem;color:{muted};margin-left:0.5rem;">{"✅" if sc>=PASS_THRESHOLD else "❌"} {sc}/{QUESTIONS_PER_EXAM}</span>'
        boss_html = ""
        if lid in st.session_state.get("boss_beaten",set()):
            boss_html = '<span style="font-size:0.65rem;color:#FF4444;margin-left:0.4rem;">💀 Boss Slain</span>'

        left_col, right_col = st.columns([4, 1])
        with left_col:
            st.markdown(
                f'<div style="background:var(--card);border:2px solid {border};border-radius:10px;'
                f'padding:1rem 1.2rem;opacity:{opacity};box-shadow:{glow};">'
                f'<div style="display:flex;align-items:center;gap:0.9rem;">'
                f'<div style="font-size:2.2rem;background:var(--card2);border:1px solid var(--border);'
                f'border-radius:6px;padding:0.25rem 0.6rem;">{lvl["pixel_art"]}</div>'
                f'<div style="flex:1;">'
                f'<div style="font-family:JetBrains Mono,monospace;font-size:0.55rem;color:{border};letter-spacing:0.2em;">'
                f'{lvl["mission"].split(":")[0].upper()}</div>'
                f'<div style="font-family:Syne,sans-serif;font-size:0.95rem;color:{text};font-weight:700;margin:0.1rem 0;">'
                f'{lvl["icon"]} {lvl["title"]}</div>'
                f'<div style="font-size:0.72rem;color:{text2};">{lvl["lore"]}</div>'
                f'</div></div>'
                f'<div style="margin-top:0.55rem;display:flex;align-items:center;gap:0.2rem;">'
                f'<span style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:{lbl_col};">{lbl_txt}</span>'
                f'{sc_html}{boss_html}</div>'
                f'</div>',
                unsafe_allow_html=True)

        with right_col:
            mult    = streak_multiplier()
            xp_show = int(lvl["xp_reward"] * mult)
            st.markdown(
                f'<div style="text-align:center;padding:0.7rem 0.5rem;background:var(--card2);'
                f'border:1px solid var(--border);border-radius:8px;height:100%;">'
                f'<div style="font-family:JetBrains Mono,monospace;font-size:0.95rem;color:#9D46FF;font-weight:700;">+{xp_show}</div>'
                f'<div style="font-size:0.58rem;color:{muted};">XP reward</div>'
                f'</div>',
                unsafe_allow_html=True)
            if status != "locked":
                btn_l = "🔍 Review" if status=="done" else "⚡ Start"
                if st.button(btn_l, key=f"hub_{lid}", use_container_width=True):
                    st.session_state.view = "level"
                    st.session_state.current_level = lid
                    st.rerun()

        if idx < len(level_items)-1:
            cls = "path-line" if status=="done" else "path-line-locked"
            st.markdown(f'<div class="{cls}"></div>', unsafe_allow_html=True)

    # ── Bottom stats strip ──
    st.markdown("<div class='divider'/>", unsafe_allow_html=True)
    xp          = st.session_state.xp
    title, icon = get_character_info(xp)
    max_xp      = sum(v["xp_reward"] for v in LEVELS.values())
    done        = len(st.session_state.completed_levels)
    stars       = sum(st.session_state.quiz_state.get(l,{}).get("score",0) for l in st.session_state.completed_levels)
    bosses      = len(st.session_state.get("boss_beaten",set()))

    for col, val, label, sub, color in zip(
        st.columns(5),
        [f"{icon} {title}", str(xp), f"{done}/5", f"⭐{stars}", f"💀{bosses}/5"],
        ["Rank","XP Earned","Levels Done","Stars","Bosses"],
        ["Character class",f"of {max_xp} total","Keep going!","quiz correct","defeated"],
        [neon,"#9D46FF",neon,"#FFD700","#FF4444"],
    ):
        with col:
            st.markdown(
                f'<div class="card" style="text-align:center;padding:0.8rem;">'
                f'<div style="font-family:Syne,sans-serif;font-size:0.95rem;color:{text};font-weight:700;">{val}</div>'
                f'<div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:{color};">{label}</div>'
                f'<div style="font-size:0.58rem;color:{muted};">{sub}</div></div>',
                unsafe_allow_html=True)


# ============================================================
# render_leaderboard()
# ============================================================
def render_leaderboard():
    dark  = st.session_state.get("dark_mode", True)
    neon  = "#00FF41" if dark else "#006600"
    muted = "#888" if dark else "#4A5568"
    text  = "#F0F0F0" if dark else "#0D1B2A"

    st.markdown(
        f'<h1 class="neon-heading" style="font-size:1.6rem;margin-bottom:0.15rem;">🏆 Global Rankings</h1>'
        f'<p style="color:{muted};font-family:JetBrains Mono,monospace;font-size:0.72rem;">Top adventurers ranked by total XP</p>',
        unsafe_allow_html=True)
    st.markdown("<div class='divider'/>", unsafe_allow_html=True)

    db      = get_db()
    entries = [(u, p.get("xp",0), len(p.get("completed_levels",[])), len(p.get("boss_beaten",[])), p.get("streak",0))
               for u, p in db.get("progress",{}).items()]
    entries.sort(key=lambda x: x[1], reverse=True)
    medals = ["🥇","🥈","🥉"] + ["🏅"]*7
    me     = st.session_state.username

    if not entries:
        st.markdown('<div class="info-box">No adventurers yet — be the first! 🚀</div>', unsafe_allow_html=True)
    else:
        for rank, (uname, xp, lvls, bosses, streak) in enumerate(entries[:10], 1):
            medal    = medals[rank-1] if rank <= len(medals) else f"#{rank}"
            is_you   = uname == me
            you_lbl  = ' <span style="color:#FFD700;font-size:0.65rem;">(YOU)</span>' if is_you else ""
            flame    = f' <span style="color:#FF9000;">🔥{streak}</span>' if streak >= 2 else ""
            boss_tag = f' <span style="color:#FF4444;font-size:0.68rem;">💀×{bosses}</span>' if bosses else ""
            bd       = "border-color:#FFD700;" if is_you else ""
            nc       = "lb-you" if is_you else ""
            st.markdown(
                f'<div class="lb-row" style="{bd}">'
                f'<div class="lb-rank">{medal}</div>'
                f'<div class="lb-name {nc}">@{uname}{you_lbl}{flame}{boss_tag}</div>'
                f'<div style="color:{muted};font-size:0.68rem;font-family:JetBrains Mono,monospace;min-width:5rem;">{lvls}/5 levels</div>'
                f'<div class="lb-xp">{xp} XP</div>'
                f'</div>',
                unsafe_allow_html=True)

    st.markdown("<div class='divider'/>", unsafe_allow_html=True)
    if st.button("← Back to Hub", key="lb_back"):
        st.session_state.view = "hub"; st.rerun()


# ============================================================
# render_boss_battle()
# ============================================================
def render_boss_battle(level_id, lvl):
    boss   = lvl.get("boss")
    if not boss:
        st.markdown('<div class="info-box">No boss for this level yet.</div>', unsafe_allow_html=True); return

    beaten = level_id in st.session_state.get("boss_beaten", set())
    mult   = streak_multiplier()
    bonus  = int(boss["xp_reward"] * mult)
    streak = st.session_state.get("streak", 0)

    if beaten:
        st.markdown(
            f'<div class="boss-beaten">💀 {boss["name"]} HAS BEEN DEFEATED!<br/>'
            f'<span style="font-size:0.76rem;">+{bonus} XP claimed</span></div>',
            unsafe_allow_html=True); return

    streak_note = f' <span style="color:#FF9000;font-size:0.73rem;">(🔥 ×{mult:.1f} streak bonus!)</span>' if streak>=2 else ""
    st.markdown(
        f'<div class="boss-card">'
        f'<div class="boss-title">⚔️ BOSS BATTLE: {boss["name"]}</div>'
        f'<p style="font-size:0.85rem;margin:0 0 0.8rem;">{boss["lore"]}</p>'
        f'<p style="color:#FF9090;font-family:JetBrains Mono,monospace;font-size:0.8rem;line-height:1.6;">{boss["challenge"]}</p>'
        f'<p style="color:#666;font-size:0.76rem;font-style:italic;margin-top:0.4rem;">💡 Hint: {boss["hint"]}</p>'
        f'<p style="color:#9D46FF;font-family:JetBrains Mono,monospace;font-size:0.76rem;margin-top:0.4rem;">'
        f'Reward: <strong>+{bonus} XP</strong>{streak_note}</p>'
        f'</div>', unsafe_allow_html=True)

    ans = st.text_input("Your answer:", key=f"boss_input_{level_id}", placeholder="Type your answer exactly…")
    if st.button("⚔️ Deliver the Final Blow!", key=f"boss_submit_{level_id}"):
        cleaned = ans.strip().lower().replace('"',"'")
        if any(cleaned == a.strip().lower() for a in boss["accepted"]):
            st.session_state.xp += bonus
            if not isinstance(st.session_state.get("boss_beaten"), set):
                st.session_state.boss_beaten = set()
            st.session_state.boss_beaten.add(level_id)
            save_user_progress(st.session_state.username)
            st.toast(f"🏆 BOSS DEFEATED! +{bonus} XP earned!", icon="⚔️")
            st.balloons()
            st.rerun()
        else:
            st.markdown(
                '<div style="background:rgba(255,68,68,0.08);border-left:4px solid #FF4444;'
                'border-radius:0 8px 8px 0;padding:0.6rem 1rem;margin:0.3rem 0;color:#FF8888;">'
                '❌ Not quite — read the hint and try again!</div>',
                unsafe_allow_html=True)


# ============================================================
# render_level()
# ============================================================
def render_level(level_id):
    dark  = st.session_state.get("dark_mode", True)
    text  = "#F0F0F0" if dark else "#0D1B2A"
    text2 = "#DDDDDD" if dark else "#1E3050"
    muted = "#888" if dark else "#4A5568"
    neon  = "#00FF41" if dark else "#006600"

    lvl = LEVELS[level_id]
    if st.button("← Back to Hub", key="back_hub"):
        st.session_state.view = "hub"; st.rerun()
    st.markdown("<div class='divider'/>", unsafe_allow_html=True)

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.6rem;">'
        f'<div style="font-size:2.6rem;background:var(--card2);border:2px solid var(--border);'
        f'border-radius:8px;padding:0.25rem 0.65rem;box-shadow:3px 3px 0 #000;">{lvl["pixel_art"]}</div>'
        f'<div>'
        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.56rem;color:{lvl["color"]};letter-spacing:0.25em;">'
        f'{lvl["mission"].split(":")[0].upper()}</div>'
        f'<div style="font-family:Syne,sans-serif;font-size:1.25rem;color:{text};font-weight:800;">{lvl["icon"]} {lvl["title"]}</div>'
        f'<div style="font-size:0.78rem;color:{text2};">{lvl["lore"]}</div>'
        f'</div></div>',
        unsafe_allow_html=True)

    if not is_level_unlocked(level_id):
        st.markdown(f'<div class="locked-box">🔒 Complete Mission {level_id-1} first to unlock this.</div>', unsafe_allow_html=True)
        return

    tab1, tab2, tab3, tab4 = st.tabs(["📖 Learn","💻 Code Example","🎯 Quiz (10 Q)","💀 Boss Battle"])
    with tab1:
        st.markdown(lvl["description"], unsafe_allow_html=False)
        mult = streak_multiplier()
        bonus_note = f" <em style='color:#FF9000;'>🔥 Streak — XP ×{mult:.1f}!</em>" if mult > 1 else ""
        st.markdown(
            f'<div class="info-box">💡 Complete the quiz to earn '
            f'<strong style="color:{neon}">+{int(lvl["xp_reward"]*mult)} XP</strong>'
            f' — Pass mark: <strong>6/10 (60%)</strong>{bonus_note}</div>',
            unsafe_allow_html=True)
    with tab2:
        st.markdown(f'<p style="color:{muted};font-size:0.78rem;font-family:JetBrains Mono,monospace;">// Study this before the quiz</p>', unsafe_allow_html=True)
        st.code(lvl["code_example"], language="python")
    with tab3:
        render_quiz(level_id, lvl)
    with tab4:
        render_boss_battle(level_id, lvl)


# ============================================================
# render_quiz()
# ============================================================
def render_quiz(level_id, lvl):
    dark  = st.session_state.get("dark_mode", True)
    neon  = "#00FF41" if dark else "#006600"
    muted = "#888" if dark else "#4A5568"
    text  = "#F0F0F0" if dark else "#0D1B2A"

    questions, _ = get_exam_questions(level_id)
    qs_data   = st.session_state.quiz_state.get(level_id, {})
    passed    = level_id in st.session_state.completed_levels
    submitted = qs_data.get("submitted", False)
    score     = qs_data.get("score", 0)
    mult      = streak_multiplier()

    if st.session_state.show_badge == level_id:
        st.balloons()
        xp_gained = int(lvl["xp_reward"] * mult)
        st.toast(f"🏆 {lvl['mission']} COMPLETE! +{xp_gained} XP!", icon="🌟")
        st.markdown(
            f'<div class="milestone">'
            f'<div style="font-size:2.8rem;">🏆</div>'
            f'<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;margin:0.4rem 0;">MISSION COMPLETE!</div>'
            f'<div>{lvl["mission"]} — Score: {score}/{QUESTIONS_PER_EXAM}</div>'
            f'<div style="margin-top:0.7rem;"><span class="xp-badge">+{xp_gained} XP saved 💾</span></div>'
            f'</div>', unsafe_allow_html=True)
        st.session_state.show_badge = None

    if submitted:
        pct = int(score / QUESTIONS_PER_EXAM * 100)
        if passed:
            st.markdown(f'<div class="success-box">✅ Mission PASSED! Score: {score}/{QUESTIONS_PER_EXAM} ({pct}%) — Progress saved 💾</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div style="background:rgba(255,68,68,0.09);border-left:4px solid #FF4444;'
                f'border-radius:0 8px 8px 0;padding:0.85rem 1.1rem;margin:0.7rem 0;color:#FF8888;">'
                f'❌ Score: {score}/{QUESTIONS_PER_EXAM} ({pct}%) — Need 6/10. Retry!</div>',
                unsafe_allow_html=True)

    streak_note = f" 🔥 Streak ×{mult:.1f}!" if mult > 1 else ""
    st.markdown(
        f'<p style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:{muted};margin-bottom:0.8rem;">'
        f'Answer all {QUESTIONS_PER_EXAM} questions then submit. '
        f'Pass mark: {PASS_THRESHOLD}/{QUESTIONS_PER_EXAM} — '
        f'Random from bank of {QUESTIONS_IN_BANK}.{streak_note}</p>',
        unsafe_allow_html=True)

    saved_answers = qs_data.get("answers", [None]*QUESTIONS_PER_EXAM)
    user_answers  = []
    for i, q in enumerate(questions):
        st.markdown(
            f'<div class="card" style="margin-bottom:0.5rem;">'
            f'<p style="font-family:JetBrains Mono,monospace;font-size:0.8rem;color:{text};margin:0 0 0.6rem;">'
            f'Q{i+1}/{QUESTIONS_PER_EXAM}: {q["q"]}</p></div>',
            unsafe_allow_html=True)
        saved_val   = saved_answers[i] if i < len(saved_answers) else None
        default_idx = q["options"].index(saved_val) if saved_val in q["options"] else 0
        choice = st.radio(f"Q{i+1}", q["options"], index=default_idx,
                          key=quiz_key(level_id, i), label_visibility="collapsed",
                          disabled=submitted and passed)
        user_answers.append(choice)
        if submitted:
            if choice == q["answer"]:
                st.markdown(f'<div class="success-box">✅ Correct! <code>{q["answer"]}</code></div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div style="background:rgba(255,68,68,0.07);border-left:4px solid #FF4444;'
                    f'border-radius:0 8px 8px 0;padding:0.6rem 0.9rem;margin:0.3rem 0;color:#FF8888;">'
                    f'❌ Yours: <code>{choice}</code> — Correct: <code>{q["answer"]}</code></div>',
                    unsafe_allow_html=True)
        st.markdown("")

    if submitted and not passed:
        st.markdown("<div class='divider'/>", unsafe_allow_html=True)
        st.markdown(f'<p style="color:#FF8888;font-family:JetBrains Mono,monospace;font-size:0.76rem;">Need 6/10 to pass. New random questions on retry.</p>', unsafe_allow_html=True)
        if st.button("🔄 Retry Mission", key=f"retry_{level_id}"):
            st.session_state.quiz_state.pop(level_id, None)
            save_user_progress(st.session_state.username)
            st.rerun()

    if not submitted:
        if st.button("⚡ Submit Answers", key=f"submit_{level_id}"):
            new_score  = sum(1 for i, q in enumerate(questions) if user_answers[i] == q["answer"])
            new_passed = new_score >= PASS_THRESHOLD
            current    = st.session_state.quiz_state.get(level_id, {})
            current.update({"answers": user_answers, "submitted": True, "score": new_score, "indices": current.get("indices",[])})
            st.session_state.quiz_state[level_id] = current
            if new_passed and level_id not in st.session_state.completed_levels:
                xp_gain = int(lvl["xp_reward"] * mult)
                st.session_state.xp += xp_gain
                st.session_state.completed_levels.add(level_id)
                st.session_state.show_badge = level_id
            save_user_progress(st.session_state.username)
            st.rerun()

    if level_id == 5 and 5 in st.session_state.completed_levels:
        render_certificate()


# ============================================================
# render_certificate()
# ============================================================
def render_certificate():
    dark = st.session_state.get("dark_mode", True)
    neon = "#00FF41" if dark else "#006600"
    st.markdown("<div class='divider'/>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.95rem;color:{neon};margin-bottom:0.3rem;">🏅 Certificate of Completion</div>'
        '<p style="color:var(--muted);font-size:0.82rem;">All 5 missions complete! Enter your name to download your certificate.</p>',
        unsafe_allow_html=True)

    name_input = st.text_input("Your Name", value=st.session_state.cert_name, placeholder="Enter your full name…", key="cert_name_input")
    if name_input != st.session_state.cert_name:
        st.session_state.cert_name = name_input
        save_user_progress(st.session_state.username)

    if name_input.strip():
        title, icon = get_character_info(st.session_state.xp)
        done   = len(st.session_state.completed_levels)
        xp     = st.session_state.xp
        max_xp = sum(v["xp_reward"] for v in LEVELS.values())
        bosses = len(st.session_state.get("boss_beaten", set()))
        streak = st.session_state.get("streak", 0)
        ds     = datetime.now().strftime("%B %d, %Y")

        cert = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<title>Python Coding Adventure — Certificate</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@700;800&display=swap');
body{{margin:0;padding:2rem;background:#0A0A0A;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:'Syne',sans-serif;color:#E8E8E8;}}
.cert{{width:760px;border:4px solid #00FF41;border-radius:16px;padding:3rem;background:#111;box-shadow:0 0 60px rgba(0,255,65,0.3),10px 10px 0 #000;text-align:center;position:relative;}}
.cert::before{{content:'';position:absolute;inset:12px;border:1px dashed rgba(0,255,65,0.2);border-radius:10px;pointer-events:none;}}
.logo{{font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#00FF41;letter-spacing:0.3em;margin-bottom:0.5rem;}}
.title{{font-size:2rem;font-weight:800;color:#00FF41;text-shadow:0 0 20px rgba(0,255,65,0.5);margin:0.5rem 0;}}
.sub{{color:#888;font-size:0.9rem;margin-bottom:2rem;}}
hr{{border:none;border-top:1px solid #2A2A2A;margin:1.5rem 0;}}
.label{{font-size:0.72rem;color:#666;text-transform:uppercase;letter-spacing:0.15em;font-family:'JetBrains Mono',monospace;}}
.hero{{font-size:2.4rem;font-weight:800;color:#fff;margin:0.3rem 0 1.5rem;}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:1.5rem 0;}}
.stat{{background:#1A1A1A;border:1px solid #2A2A2A;border-radius:8px;padding:1rem;}}
.stat .v{{font-family:'JetBrains Mono',monospace;font-size:1.1rem;color:#00FF41;}}
.stat .l{{font-size:0.68rem;color:#666;margin-top:0.2rem;font-family:'JetBrains Mono',monospace;}}
.badge{{display:inline-block;background:#6200EE;border:2px solid #000;border-radius:6px;padding:0.35rem 1rem;font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#fff;box-shadow:3px 3px 0 #000;margin:0.3rem;}}
.footer{{margin-top:2rem;font-size:0.65rem;color:#555;font-family:'JetBrains Mono',monospace;}}
</style></head><body><div class="cert">
<div class="logo">🐍 PYTHON CODING ADVENTURE</div>
<div class="title">Certificate of Completion</div>
<div class="sub">This certifies that the following adventurer has conquered the Python Realm</div>
<hr/>
<div class="label">Presented to</div>
<div class="hero">{name_input.strip()}</div>
<div class="grid">
  <div class="stat"><div class="v">{xp}/{max_xp}</div><div class="l">XP Earned</div></div>
  <div class="stat"><div class="v">{done}/5</div><div class="l">Missions Done</div></div>
  <div class="stat"><div class="v">💀 {bosses}/5</div><div class="l">Bosses Slain</div></div>
  <div class="stat"><div class="v">🔥 {streak}</div><div class="l">Day Streak</div></div>
</div>
<hr/>
<span class="badge">✅ Python Basics Mastered</span>
<span class="badge">🎯 60% Pass Standard</span>
<div class="footer">Issued on {ds} &nbsp;|&nbsp; Python Coding Adventure &nbsp;|&nbsp; Powered by Streamlit</div>
</div></body></html>"""

        b64   = base64.b64encode(cert.encode()).decode()
        fname = f"python_cert_{name_input.strip().replace(' ','_')}.html"
        st.markdown(
            f'<a href="data:text/html;base64,{b64}" download="{fname}" style="text-decoration:none;">'
            f'<div style="display:inline-block;background:{neon};color:#000;'
            f'font-family:JetBrains Mono,monospace;font-weight:700;border:2px solid #000;'
            f'border-radius:8px;padding:0.6rem 1.3rem;cursor:pointer;margin-top:0.5rem;">'
            f'📥 Download Certificate</div></a>',
            unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:var(--muted);font-size:0.8rem;font-style:italic;">↑ Enter your name to unlock the download.</div>', unsafe_allow_html=True)


# ============================================================
# MAIN
# ============================================================
def main():
    init_state()
    apply_styles()

    if not st.session_state.logged_in:
        render_auth()
        return

    render_sidebar()

    if st.session_state.view == "hub":
        render_hub()
    elif st.session_state.view == "level":
        render_level(st.session_state.current_level)
    elif st.session_state.view == "leaderboard":
        render_leaderboard()


if __name__ == "__main__":
    main()

