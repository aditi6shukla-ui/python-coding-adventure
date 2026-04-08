import streamlit as st
import hashlib
import base64
import random
import json
import os
import sys
import io
import traceback
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
# PERSISTENT STORAGE
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

if "_DB_CACHE" not in st.__dict__:
    st._DB_CACHE = _load_raw()

def get_db() -> dict:
    return st._DB_CACHE

def flush_db():
    _save_raw(st._DB_CACHE)

# ============================================================
# SPELLBOOK — unlockable syntax cheat sheets per level
# ============================================================
SPELLBOOK = {
    1: {
        "title": "📦 Variables & Types",
        "spells": [
            ("Declare variable",   'name = "Alex"\nxp = 100\nactive = True'),
            ("Type conversion",    'int("42")   # → 42\nstr(100)    # → "100"\nbool(0)     # → False'),
            ("f-string",           'f"HP: {hp}, XP: {xp*2}"'),
            ("String slicing",     '"Python"[0:3]  # → "Pyt"\n"Python"[-1]   # → "n"'),
            ("Floor div / Modulo", '10 // 3  # → 3\n10 % 3   # → 1\n2 ** 8   # → 256'),
        ],
    },
    2: {
        "title": "🔀 Logic & Loops",
        "spells": [
            ("if / elif / else",   'if x > 0:\n    ...\nelif x == 0:\n    ...\nelse:\n    ...'),
            ("Ternary",            '"Pass" if score >= 60 else "Fail"'),
            ("for range",          'for i in range(5):    # 0-4\nfor i in range(1,6):  # 1-5'),
            ("enumerate / zip",    'for i, v in enumerate(lst):\nfor a, b in zip(l1, l2):'),
            ("List comprehension", '[x**2 for x in range(6) if x%2==0]'),
        ],
    },
    3: {
        "title": "🎒 Lists & Dicts",
        "spells": [
            ("List methods",       'lst.append(x)\nlst.insert(0,x)\nlst.pop()\nlst.sort()'),
            ("Slicing",            'lst[1:3]   # index 1 and 2\nlst[::-1]  # reversed'),
            ("Dict access",        'd["key"]\nd.get("key", default)\ndel d["key"]'),
            ("Dict iteration",     'for k, v in d.items():\nfor k in d.keys():\nfor v in d.values():'),
            ("Set",                '{1,2,2,3}  # → {1,2,3}\ns.add(x); s.discard(x)'),
        ],
    },
    4: {
        "title": "✨ Functions",
        "spells": [
            ("Define function",    'def greet(name, title="Hero"):\n    return f"Welcome, {title} {name}!"'),
            ("*args / **kwargs",   'def f(*args):    # tuple\ndef f(**kwargs): # dict'),
            ("Lambda",             'double = lambda x: x * 2\nsorted(lst, key=lambda x: x["hp"])'),
            ("map / filter",       'list(map(lambda x: x*2, lst))\nlist(filter(lambda x: x>0, lst))'),
            ("Scope / global",     'global score\nscore += 50  # modify global inside fn'),
        ],
    },
    5: {
        "title": "🐉 Advanced",
        "spells": [
            ("Class",              'class Hero:\n    def __init__(self, name):\n        self.name = name'),
            ("Inheritance",        'class Wizard(Hero):\n    def __init__(self, name):\n        super().__init__(name)'),
            ("try / except",       'try:\n    risky()\nexcept ValueError as e:\n    handle(e)\nfinally:\n    cleanup()'),
            ("with open",          'with open("f.txt","w") as f:\n    f.write("data")'),
            ("json",               'import json\njson.dump(obj, f)\njson.load(f)'),
        ],
    },
}

# ============================================================
# CURRICULUM DATA
# ============================================================
LEVELS = {
    1: {
        "title": "Variables & Data Types",
        "mission": "Mission 1: Repair the Data Core",
        "subtitle": "The Foundation",
        "icon": "🧱", "pixel_art": "🔢", "color": "#00FF41", "xp_reward": 100,
        "lore": "The Data Core is corrupted. Restore it by mastering variables and types.",
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
name.upper()          # "PYTHON"
name.capitalize()     # "Python"
name.replace("p","P") # "Python"
name.split("t")       # ["py", "hon"]
len(name)             # 6
name[0]               # "p"  (indexing)
name[-1]              # "n"  (negative index)
name[0:3]             # "pyt" (slicing)

# f-strings (best way to embed variables)
score = 95
msg = f"Player scored {score} points!"
msg2 = f"Double: {score * 2}"
```

---

### ➗ Arithmetic Operators
```python
10 + 3   # 13   (addition)
10 - 3   # 7    (subtraction)
10 * 3   # 30   (multiplication)
10 / 3   # 3.333... (float division)
10 // 3  # 3    (floor/integer division)
10 % 3   # 1    (modulo — remainder)
2 ** 10  # 1024 (exponentiation)
```

---

### 🔍 Checking Types
```python
type(42)        # <class 'int'>
type("hello")   # <class 'str'>
isinstance(42, int)    # True
isinstance("hi", str)  # True
```

> 💡 **Pro Tip:** Use `SCREAMING_SNAKE_CASE` for constants: `MAX_HEALTH = 100`
        """,
        "code_example": '''# 🐍 Variables & Data Types — Full Demo

name = "Alex"
level = 1
xp_multiplier = 1.5
is_hero = True
lives = None

print(f"Player: {name}")
print(f"Level:  {level}")
print(f"XP Mult:{xp_multiplier}")
print(f"Hero?   {is_hero}")

print(f"\\nType checks:")
print(f"  type(level):          {type(level)}")
print(f"  type(xp_multiplier):  {type(xp_multiplier)}")
print(f"  isinstance(name,str): {isinstance(name, str)}")

score_str = "250"
score_int = int(score_str)
print(f"\\nConverted score: {score_int}")
print(f"Doubled:         {score_int * 2}")
print(f"As float:        {float(score_str)}")

tag = "python_master"
print(f"\\nString ops:")
print(f"  Upper:   {tag.upper()}")
print(f"  Length:  {len(tag)}")
print(f"  Slice:   {tag[0:6]}")
print(f"  Replace: {tag.replace('_',' ').title()}")

print(f"\\nArithmetic:")
print(f"  7 // 2 = {7 // 2}  (floor div)")
print(f"  7 %  2 = {7 %  2}  (remainder)")
print(f"  2**8   = {2**8} (power)")

x, y, z = 10, 20, 30
x, y = y, x
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
        "boss": {
            "name": "The Type Phantom 👻",
            "xp_reward": 50,
            "lore": "A shapeless entity that constantly shifts between data types. It can only be revealed by someone who knows Python's type-inspection function.",
            "challenge": "The Type Phantom is shapeshifting! 🧱 Type the Python built-in function (with a placeholder argument like `x`) used to check the data type of any variable.",
            "hint": "You use it like this: `___(my_variable)` — it returns `<class 'int'>` for integers.",
            "accepted": ["type(x)", "type(n)", "type(v)", "type(val)", "type(variable)", "type(a)", "type()"],
            "display_answer": "type(x)",
        },
    },
    2: {
        "title": "Logic & Loops",
        "mission": "Mission 2: Navigate the Loop Maze",
        "subtitle": "The Path",
        "icon": "🔀", "pixel_art": "♾️", "color": "#9D46FF", "xp_reward": 120,
        "lore": "The Loop Maze traps adventurers in infinite cycles. Master conditionals to find the exit.",
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
True and True   # True
True and False  # False
True or False   # True
not True        # False

x = 5
x > 0 and x < 10   # True
x < 0 or x > 3     # True
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

# Ternary (one-liner if)
label = "Pass" if score >= 60 else "Fail"
```

---

### 🔁 for Loops
```python
for i in range(5):        # 0,1,2,3,4
    print(i)

for i in range(1, 6):     # 1,2,3,4,5
    print(i)

for i in range(0, 10, 2): # 0,2,4,6,8 (step 2)
    print(i)

items = ["sword", "shield", "potion"]
for item in items:
    print(item)

for idx, item in enumerate(items):
    print(f"{idx}: {item}")

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

while True:
    if condition:
        break   # exit the loop
```

---

### ⏭️ break / continue / pass
```python
for i in range(10):
    if i == 5:
        break      # stop entirely → prints 0-4

for i in range(5):
    if i == 2:
        continue   # skip this one → prints 0,1,3,4

for i in range(3):
    pass           # placeholder — do nothing
```

---

### 🧠 List Comprehensions
```python
squares = [x**2 for x in range(6)]
evens   = [x for x in range(10) if x%2==0]
upper   = [s.upper() for s in ["a","b","c"]]
```

> 💡 **Pro Tip:** Use `for` when you know the number of iterations; `while` when waiting for a condition.
        """,
        "code_example": '''# 🔀 Logic & Loops — Full Demo

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

label = "PASS" if score >= 60 else "FAIL"
print(f"Result: {label}")

print("\\nCounting up:")
for i in range(1, 6):
    print(f"  {i}", end=" ")

print("\\n\\nInventory:")
items = ["Sword","Shield","Potion"]
for idx, item in enumerate(items, start=1):
    print(f"  Slot {idx}: {item}")

print("\\nParty stats:")
names   = ["Alex","Sam","Jordan"]
hp_vals = [120, 95, 80]
for hero, hp in zip(names, hp_vals):
    bar = "█" * (hp // 20)
    print(f"  {hero:8s} {bar} {hp}")

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

print("\\nSquares: ", [x**2 for x in range(6)])
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
        "boss": {
            "name": "The Loop Lord ♾️",
            "xp_reward": 60,
            "lore": "An ancient construct that spins in infinite cycles, trapping adventurers forever. It can only be stopped by those who know the secret escape word.",
            "challenge": "The Loop Lord has you caught in an infinite spin! 🔀 Type the single Python keyword that immediately terminates a loop and jumps to the code after it.",
            "hint": "One word. Used inside `for` and `while` to escape early. Not `return`, not `exit`.",
            "accepted": ["break"],
            "display_answer": "break",
        },
    },
    3: {
        "title": "Lists & Dictionaries",
        "mission": "Mission 3: Reclaim the Inventory Vault",
        "subtitle": "The Inventory",
        "icon": "🎒", "pixel_art": "📦", "color": "#00CFFF", "xp_reward": 140,
        "lore": "The Inventory Vault was ransacked. Rebuild it using Python's most powerful collections.",
        "description": """
## 🎒 Chapter 3 — Lists & Dictionaries

Python's most powerful built-in collections. Lists are your **ordered item bags**; dictionaries are your **character sheets**.

---

### 📋 Lists — Ordered, Mutable Sequences

```python
empty   = []
numbers = [1, 2, 3, 4, 5]
mixed   = [42, "hello", True, 3.14]
nested  = [[1,2], [3,4]]
```

**Indexing & Slicing:**
```python
items = ["sword", "shield", "potion", "map", "key"]
items[0]     # "sword"   first
items[-1]    # "key"     last
items[1:3]   # ["shield","potion"]
items[::-1]  # reversed
```

**Modifying:**
```python
items.append("torch")      # add to end
items.insert(0, "helmet")  # add at index
items.remove("shield")     # remove first occurrence
items.pop()                # remove & return last
items.sort()               # sort in-place
items.reverse()            # reverse in-place
items.clear()              # remove all
```

**Info:**
```python
len(items)          # count
items.count("x")    # occurrences
items.index("x")    # first position
"sword" in items    # membership test
```

---

### 📖 Dictionaries — Key-Value Stores

```python
hero = {"name": "Alex", "hp": 100, "class": "Wizard"}

hero["name"]             # "Alex"
hero.get("mp", 0)        # 0 (safe default)
hero["level"] = 5        # add key
del hero["class"]        # delete key

for key, value in hero.items():
    print(f"{key}: {value}")
```

---

### 🔵 Tuples & Sets
```python
coords  = (10, 20)       # immutable
unique  = {1, 2, 2, 3}   # → {1, 2, 3} no duplicates
```

---

### ⚡ Comprehensions
```python
squares = [x**2 for x in range(5)]
sq_dict = {x: x**2 for x in range(5)}
sq_set  = {x**2 for x in range(5)}
```

> 💡 **Pro Tip:** Use `dict.get(key, default)` instead of `dict[key]` to avoid `KeyError`.
        """,
        "code_example": '''# 🎒 Lists & Dictionaries — Full Demo

inventory = ["sword", "shield", "potion"]
inventory.append("map")
inventory.insert(0, "helmet")
inventory.remove("shield")
popped = inventory.pop()

print("Inventory:", inventory)
print("Popped:   ", popped)
print("Length:   ", len(inventory))
print("Slice 1:3:", inventory[1:3])
print("Reversed: ", inventory[::-1])

scores = [42, 15, 88, 7, 63]
scores.sort()
print("\\nSorted:    ", scores)
print("Max/Min/Sum:", max(scores), min(scores), sum(scores))

powered    = [item.upper() for item in inventory]
even_scores = [s for s in scores if s % 2 == 0]
print("\\nPowered:    ", powered)
print("Even scores:", even_scores)

print("\\n--- Hero Sheet ---")
hero = {"name": "Alex", "hp": 100, "mp": 50, "class": "Wizard", "level": 3}
hero["xp"] = 250
hero["hp"] = 120
missing = hero.get("gold", 0)

for stat, val in hero.items():
    print(f"  {stat:8s}: {val}")
print(f"  gold    : {missing} (default)")

party = {
    "Alex":   {"hp": 120, "role": "Wizard"},
    "Sam":    {"hp":  95, "role": "Rogue"},
    "Jordan": {"hp":  80, "role": "Archer"},
}
print("\\n--- Party ---")
for name, stats in party.items():
    print(f"  {name}: HP={stats[\'hp\']}, {stats[\'role\']}")

visited = {"dungeon", "forest", "cave", "dungeon"}
print("\\nVisited zones:", visited)
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
             "options": ["All values", "All keys", "All items as tuples", "Length of dict"], "answer": "All keys"},
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
        "boss": {
            "name": "The Inventory Demon 📦",
            "xp_reward": 70,
            "lore": "A hoarder of stolen items who lurks at the bottom of your list. It can only be banished by naming the exact method that adds items to a list's end.",
            "challenge": "The Inventory Demon stole your last item! 🎒 Type the list method — with dot and empty parentheses — that adds an element to the END of a list.",
            "hint": "Called like: `my_list.___(item)` — it always adds to the end, never the start.",
            "accepted": [".append()", "append()", ".append"],
            "display_answer": ".append()",
        },
    },
    4: {
        "title": "Functions",
        "mission": "Mission 4: Forge the Spellbook",
        "subtitle": "The Spells",
        "icon": "✨", "pixel_art": "🪄", "color": "#FF6B6B", "xp_reward": 160,
        "lore": "The ancient Spellbook is blank. Inscribe it with the power of reusable functions.",
        "description": """
## ✨ Chapter 4 — Functions

Functions are **reusable blocks of code** — your hero's spellbook. Define once, cast anywhere.

---

### 📝 Defining & Calling
```python
def greet(name):
    return f"Welcome, {name}!"

result = greet("Alex")   # call it
```

---

### 🎯 Parameters
```python
# Default parameters
def cast_spell(name, power=10, critical=False):
    damage = power * (2 if critical else 1)
    return f"{name} deals {damage} damage!"

cast_spell("Fireball")               # power=10
cast_spell("Lightning", power=30)
cast_spell("Thunder", 20, True)

# *args — positional as tuple
def total(*numbers):
    return sum(numbers)

# **kwargs — keyword args as dict
def show_stats(**stats):
    for k, v in stats.items():
        print(f"  {k}: {v}")
show_stats(hp=100, mp=50)
```

---

### 🔄 Return Values
```python
def min_max(numbers):
    return min(numbers), max(numbers)   # tuple

low, high = min_max([3,1,4,1,5,9])
```

---

### 🌍 Scope
```python
score = 100        # global

def update():
    global score   # required to modify global
    score += 50

def example():
    x = 99         # local — invisible outside
```

---

### ⚡ Lambda & Higher-Order Functions
```python
double  = lambda x: x * 2
is_even = lambda n: n % 2 == 0

list(map(lambda x: x*2, [1,2,3]))      # [2,4,6]
list(filter(lambda x: x>2, [1,2,3,4])) # [3,4]
sorted(heroes, key=lambda h: h["hp"])
```

---

### 🔁 Recursion
```python
def factorial(n):
    if n <= 1: return 1        # base case!
    return n * factorial(n-1)

factorial(5)  # 120
```

> 💡 **Pro Tip:** A function should do ONE thing well. If it does three things, split it into three functions!
        """,
        "code_example": '''# ✨ Functions — Full Demo

def greet(name):
    return f"Welcome, {name}! Your quest begins."

def cast_spell(spell_name, power=10, critical=False):
    damage = power * (2 if critical else 1)
    return f"⚡ {spell_name} deals {damage} damage!"

def total_xp(*xp_gains):
    return sum(xp_gains)

def create_hero(**attributes):
    return {k: v for k, v in attributes.items()}

def analyze_scores(scores):
    return min(scores), max(scores), sum(scores)/len(scores)

def factorial(n):
    if n <= 1: return 1
    return n * factorial(n - 1)

double = lambda x: x * 2

heroes = [
    {"name":"Alex","hp":120},
    {"name":"Sam","hp":95},
    {"name":"Jordan","hp":80},
]

print(greet("Alex"))
print(cast_spell("Fireball", power=25))
print(cast_spell("Lightning", power=30, critical=True))
print(f"Total XP: {total_xp(50, 30, 20, 15)}")

hero = create_hero(name="Zara", hp=100, level=5)
print(f"\\nHero: {hero}")

scores = [72, 88, 95, 61, 78]
lo, hi, avg = analyze_scores(scores)
print(f"\\nScores → min:{lo}, max:{hi}, avg:{avg:.1f}")
print(f"5! = {factorial(5)}")
print(f"Double 7 = {double(7)}")

nums    = [1, 2, 3, 4, 5, 6]
doubled = list(map(lambda x: x*2, nums))
evens   = list(filter(lambda x: x%2==0, nums))
print(f"\\nDoubled: {doubled}")
print(f"Evens:   {evens}")

ranked = sorted(heroes, key=lambda h: h["hp"], reverse=True)
print("\\nHero ranking by HP:")
for i, h in enumerate(ranked, 1):
    print(f"  #{i} {h[\'name\']}: {h[\'hp\']} HP")
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
             "options": ["A global variable", "A base case", "A lambda", "A return value"], "answer": "A base case"},
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
             "options": ["[2,5,8]", "[8,5,2]", "[5,2,8]", "[-5,-2,-8]"], "answer": "[8,5,2]"},
            {"q": "Calling `def f(): pass` returns?",
             "options": ["0", "False", "None", "Error"], "answer": "None"},
            {"q": "What does `enumerate(['a','b'])` produce on first iteration?",
             "options": ["'a'", "(0,'a')", "(1,'a')", "0"], "answer": "(0,'a')"},
            {"q": "What is `factorial(4)` if factorial(n) = n * factorial(n-1) and factorial(1)=1?",
             "options": ["8", "12", "24", "16"], "answer": "24"},
        ],
        "boss": {
            "name": "The Spell Caster 🪄",
            "xp_reward": 80,
            "lore": "An ancient wizard who jealously guards the secrets of reusable code. He challenges all who wish to harness the power of functions.",
            "challenge": "The Spell Caster demands proof you can create a function! ✨ Type the Python keyword used to *define* a new function.",
            "hint": "Every function starts with: `___ function_name():`",
            "accepted": ["def"],
            "display_answer": "def",
        },
    },
    5: {
        "title": "The Final Boss",
        "mission": "Mission 5: Slay the Shadow Dragon",
        "subtitle": "Comprehensive Python Test",
        "icon": "🐉", "pixel_art": "💀", "color": "#FF4444", "xp_reward": 200,
        "lore": "The Shadow Dragon has awoken. Prove total mastery of Python to defeat it and claim the Realm.",
        "description": """
## 🐉 Chapter 5 — The Final Boss

You've mastered the four disciplines. Now face the **comprehensive gauntlet** that combines everything — plus powerful new weapons.

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
    species = "Human"          # class variable

    def __init__(self, name, hp=100):
        self.name = name       # instance variable
        self.hp   = hp
        self.inventory = []

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        return f"{self.name} took {amount} dmg! HP: {self.hp}"

    def __str__(self):
        return f"Hero({self.name}, HP={self.hp})"

hero = Hero("Alex", hp=120)
print(hero.take_damage(35))
print(hero)
```

**Inheritance:**
```python
class Wizard(Hero):
    def __init__(self, name, hp=80, mp=100):
        super().__init__(name, hp)
        self.mp = mp

    def cast(self, spell, cost=10):
        if self.mp >= cost:
            self.mp -= cost
            return f"✨ {spell} cast!"
        return "Not enough MP!"

isinstance(Wizard("Merlin"), Hero)   # True
```

---

### 🛡️ Error Handling

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    result = 0
except ValueError as e:
    print(f"Error: {e}")
else:
    print("No errors!")       # only if no exception
finally:
    print("Always runs!")     # always

raise ValueError("Custom error!")
```

---

### 📁 File I/O & JSON

```python
with open("data.txt", "w") as f:
    f.write("Hello\\n")

with open("data.txt", "r") as f:
    content = f.read()

import json
with open("save.json", "w") as f:
    json.dump({"score": 95}, f)

with open("save.json", "r") as f:
    data = json.load(f)
```

---

### 📦 Useful Modules

```python
import math, random, os
from datetime import datetime
from collections import Counter, defaultdict

math.sqrt(16)             # 4.0
random.randint(1, 6)      # dice roll
random.choice(["a","b"])  # random pick
Counter("aabbcc")         # Counter({'a':2,...})
any([False, True])        # True
all([True, True])         # True
```

> 🏆 **Final Challenge:** Score 6/10 to claim your **Python Master Certificate**!
        """,
        "code_example": '''# 🐉 Final Boss — All Skills Combined

import random
from collections import Counter

class Hero:
    def __init__(self, name, hp=100, mp=50):
        self.name = name
        self.hp   = hp
        self.mp   = mp
        self.xp   = 0

    def attack(self, enemy, base=20):
        crit = random.random() < 0.25
        dmg  = base * 2 if crit else base
        enemy.hp = max(0, enemy.hp - dmg)
        tag = " CRIT!" if crit else ""
        return f"{self.name}→{enemy.name}: {dmg} dmg{tag} (HP:{enemy.hp})"

    def heal(self, amount=30):
        if self.mp < 10: return "Not enough MP!"
        self.hp = min(200, self.hp + amount)
        self.mp -= 10
        return f"{self.name} healed +{amount} HP → {self.hp}"

    def __str__(self):
        return f"{self.name} [HP:{self.hp} MP:{self.mp}]"

class Boss(Hero):
    def __init__(self, name, hp=300, power=35):
        super().__init__(name, hp)
        self.power = power

    def rage(self, hero):
        dmg = self.power + random.randint(0, 20)
        hero.hp = max(0, hero.hp - dmg)
        return f"RAGE {self.name}→{hero.name}: {dmg} dmg!"

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 0

hero = Hero("Alex", hp=150, mp=60)
boss = Boss("Shadow Dragon")
print("BATTLE START!")
print(hero); print(boss)

for r in range(1, 6):
    print(f"\\n--- Round {r} ---")
    print(" ", hero.attack(boss))
    if boss.hp > 0: print(" ", boss.rage(hero))
    if hero.hp <= 0 or boss.hp <= 0: break

print(f"\\nWinner: {hero.name if hero.hp > 0 else boss.name}")

party = [Hero("Alex",120), Hero("Sam",95), Hero("Jordan",0)]
alive = [m for m in party if m.hp > 0]
hps   = [m.hp for m in party]
print(f"\\nAlive: {len(alive)}/{len(party)}, avg HP: {sum(hps)/len(hps):.1f}")

items = ["sword","shield","sword","potion","sword"]
print("\\nItem freq:", dict(Counter(items)))
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
        "boss": {
            "name": "The Shadow Dragon 🐉",
            "xp_reward": 100,
            "lore": "The ultimate guardian of the Python Realm — ancient, powerful, and the source of all runtime crashes. Defeat it to prove total mastery.",
            "challenge": "The Shadow Dragon breathes exceptions at you! 🐉 Type the keyword used in a `try` block to *catch* and handle exceptions.",
            "hint": "Structure: `try: ... ___ SomeError: handle it`",
            "accepted": ["except"],
            "display_answer": "except",
        },
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

PASS_THRESHOLD     = 6
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
# PERSISTENT PROGRESS
# ============================================================
def empty_progress():
    return {
        "xp": 0, "completed_levels": [], "quiz_state": {},
        "cert_name": "", "last_login": "", "streak": 0, "boss_beaten": [],
    }

def load_user_progress(username: str):
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

def save_user_progress(username: str):
    db = get_db()
    if "progress" not in db:
        db["progress"] = {}
    db["progress"][username] = {
        "xp":               st.session_state.xp,
        "completed_levels": list(st.session_state.completed_levels),
        "quiz_state":       {str(k): v for k, v in st.session_state.quiz_state.items()},
        "cert_name":        st.session_state.cert_name,
        "streak":           st.session_state.get("streak", 0),
        "last_login":       st.session_state.get("last_login", ""),
        "boss_beaten":      list(st.session_state.get("boss_beaten", set())),
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
        "streak": 0, "last_login": "", "boss_beaten": set(),
        "lab_open": False, "sandbox_code": "", "sandbox_output": "", "sandbox_error": "",
        "dark_mode": True,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ============================================================
# STREAK HELPER
# ============================================================
def update_streak(username: str):
    today_str = date.today().isoformat()
    db        = get_db()
    prog      = db["progress"].get(username, empty_progress())
    last      = prog.get("last_login", "")
    streak    = prog.get("streak", 0)
    if last:
        try:
            diff = (date.today() - date.fromisoformat(last)).days
            if diff == 0:   pass
            elif diff == 1: streak += 1
            else:           streak = 1
        except Exception:
            streak = 1
    else:
        streak = 1
    prog["last_login"] = today_str
    prog["streak"]     = streak
    db["progress"][username] = prog
    flush_db()
    return streak

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

def get_exam_questions(level_id: int):
    qs_data = st.session_state.quiz_state.get(level_id, {})
    bank    = LEVELS[level_id]["questions"]
    if "indices" in qs_data:
        indices = qs_data["indices"]
    else:
        indices = sorted(random.sample(range(len(bank)), QUESTIONS_PER_EXAM))
        if level_id not in st.session_state.quiz_state:
            st.session_state.quiz_state[level_id] = {}
        st.session_state.quiz_state[level_id]["indices"] = indices
        save_user_progress(st.session_state.username)
    return [bank[i] for i in indices], indices

def streak_multiplier():
    return 1.2 if st.session_state.get("streak", 0) >= 2 else 1.0

# ============================================================
# apply_styles() — THEME-AWARE CSS
# ============================================================
def apply_styles():
    dark = st.session_state.get("dark_mode", True)

    if dark:
        theme = """
  --neon:    #00FF41;
  --purple:  #6200EE;
  --purple2: #9D46FF;
  --accent:  #00FF41;
  --bg:      #0A0A0A;
  --bg2:     #111111;
  --card:    #161616;
  --card2:   #1C1C1C;
  --border:  #252525;
  --text:    #F0F0F0;
  --text2:   #BBBBBB;
  --muted:   #777777;
  --sidebar-bg: #080808;
  --shadow:        4px 4px 0px #000;
  --shadow-neon:   4px 4px 0px #00CC33;
  --shadow-purple: 4px 4px 0px #4400AA;
  --radius:  8px;
  --btn-glow: 0 0 16px rgba(0,255,65,0.5), 4px 4px 0 #000;
  --btn-glow-hover: 0 0 28px rgba(0,255,65,0.8), 6px 6px 0 #000;
"""
        sidebar_bg   = "#080808"
        code_bg      = "#060606"
        code_color   = "#00FF41"
        input_bg     = "#111"
        expander_bg  = "#101010"
    else:
        theme = """
  --neon:    #006600;
  --purple:  #4A00CC;
  --purple2: #6622EE;
  --accent:  #005500;
  --bg:      #F5F0E8;
  --bg2:     #EDE8DC;
  --card:    #FFFFFF;
  --card2:   #F8F4EC;
  --border:  #C8C0B0;
  --text:    #1A1A1A;
  --text2:   #333333;
  --muted:   #555555;
  --sidebar-bg: #EDE8DC;
  --shadow:        3px 3px 0px #888;
  --shadow-neon:   3px 3px 0px #005500;
  --shadow-purple: 3px 3px 0px #4400AA;
  --radius:  8px;
  --btn-glow: 0 0 10px rgba(0,100,0,0.3), 3px 3px 0 #555;
  --btn-glow-hover: 0 0 18px rgba(0,100,0,0.5), 5px 5px 0 #444;
"""
        sidebar_bg   = "#EDE8DC"
        code_bg      = "#1A1A1A"
        code_color   = "#00FF41"
        input_bg     = "#FFFFFF"
        expander_bg  = "#EDE8DC"

    st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

  :root {{
    {theme}
  }}

  /* ── Base ── */
  .stApp {{ background: var(--bg) !important; font-family: 'Outfit', sans-serif; color: var(--text); }}
  .block-container {{ padding: 1.5rem 2rem !important; max-width: 1100px; }}
  #MainMenu, footer, header {{ visibility: hidden; }}
  .stDeployButton {{ display: none; }}

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {{
    background: {sidebar_bg} !important;
    border-right: 2px solid var(--border);
    min-width: 300px !important;
  }}
  [data-testid="stSidebar"] .block-container {{ padding: 1rem !important; }}
  [data-testid="stSidebar"] * {{ color: var(--text) !important; }}

  /* ── Headings ── */
  h1, h2, h3 {{ font-family: 'Syne', sans-serif !important; color: var(--text) !important; }}
  .pixel-font {{ font-family: 'JetBrains Mono', monospace !important; }}
  .mono {{ font-family: 'JetBrains Mono', monospace !important; }}

  /* ── Buttons — all default ── */
  .stButton > button {{
    background: var(--neon) !important;
    color: #000 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    border: 2px solid #000 !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--btn-glow) !important;
    padding: 0.65rem 1.4rem !important;
    transition: all 0.12s ease !important;
    letter-spacing: 0.03em;
  }}
  .stButton > button:hover {{
    transform: translate(-2px, -2px) !important;
    box-shadow: var(--btn-glow-hover) !important;
  }}
  .stButton > button:active {{
    transform: translate(1px, 1px) !important;
    box-shadow: 2px 2px 0 #000 !important;
  }}
  .stButton > button:disabled {{
    background: var(--border) !important;
    color: var(--muted) !important;
    box-shadow: none !important;
  }}

  /* ── Radio ── */
  .stRadio > label {{ color: var(--text) !important; }}
  .stRadio [data-testid="stMarkdownContainer"] p {{ color: var(--text) !important; }}
  .stRadio label span {{ color: var(--text) !important; }}

  /* ── Cards ── */
  .card {{
    background: var(--card);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
  }}
  .card-neon {{
    background: var(--card);
    border: 2px solid var(--neon);
    border-radius: var(--radius);
    padding: 1.4rem;
    box-shadow: var(--shadow-neon);
    margin-bottom: 1rem;
  }}
  .card-purple {{
    background: var(--card);
    border: 2px solid var(--purple);
    border-radius: var(--radius);
    padding: 1.4rem;
    box-shadow: var(--shadow-purple);
    margin-bottom: 1rem;
  }}

  /* ── Progress bar ── */
  .stProgress > div > div {{ background: var(--neon) !important; }}
  .stProgress {{ filter: drop-shadow(0 0 5px var(--neon)); }}

  /* ── XP badge ── */
  .xp-badge {{
    display: inline-block;
    background: var(--purple);
    color: #fff !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.25rem 0.7rem;
    border: 2px solid #000;
    border-radius: 4px;
    box-shadow: 2px 2px 0 #000;
  }}

  /* ── Streak badge ── */
  .streak-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: linear-gradient(135deg, #FF6400, #FF9000);
    color: #000 !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.35rem 0.9rem;
    border: 2px solid #000;
    border-radius: 4px;
    box-shadow: 2px 2px 0 #000;
    margin: 0.4rem 0;
    width: 100%;
    justify-content: center;
  }}

  /* ── Boxes ── */
  .info-box {{
    background: rgba(98,0,238,0.12);
    border-left: 4px solid var(--purple2);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 0.9rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.92rem;
    color: var(--text2) !important;
  }}
  .success-box {{
    background: rgba(0,255,65,0.08);
    border-left: 4px solid var(--neon);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 0.9rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.92rem;
    color: var(--neon) !important;
  }}
  .locked-box {{
    background: rgba(255,100,0,0.08);
    border: 2px dashed #FF6400;
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    text-align: center;
    color: #FF8844 !important;
  }}
  .stat-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
  }}
  .stat-row span {{ color: var(--text) !important; }}
  .divider {{ border: none; border-top: 2px solid var(--border); margin: 1.5rem 0; }}
  .neon-heading {{
    color: var(--neon) !important;
    text-shadow: 0 0 12px rgba(0,255,65,0.4);
    font-family: 'Syne', sans-serif;
  }}
  .milestone {{
    background: linear-gradient(135deg, #6200EE, #9D46FF);
    border: 3px solid var(--neon);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 0 30px rgba(0,255,65,0.3), 6px 6px 0 #000;
    margin: 1rem 0;
  }}
  .milestone * {{ color: #fff !important; }}

  /* ── Boss cards ── */
  .boss-card {{
    background: linear-gradient(135deg, #1a0505, #300000);
    border: 3px solid #FF4444;
    border-radius: 12px;
    padding: 1.6rem;
    box-shadow: 0 0 30px rgba(255,68,68,0.3), 6px 6px 0 #000;
    margin: 1rem 0;
  }}
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
    border: 2px solid #00FF41;
    border-radius: 8px;
    padding: 1.2rem;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    color: #00FF41 !important;
    font-size: 0.9rem;
    margin-top: 1rem;
  }}

  /* ── Leaderboard ── */
  .lb-row {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 1rem;
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-bottom: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    transition: border-color 0.2s;
  }}
  .lb-row:hover {{ border-color: var(--neon); }}
  .lb-rank {{ font-size: 1.4rem; min-width: 2.5rem; text-align: center; }}
  .lb-name {{ color: var(--text) !important; font-size: 0.8rem; flex: 1; }}
  .lb-xp   {{ color: var(--neon) !important; font-size: 0.8rem; font-weight: 700; min-width: 5rem; text-align: right; }}
  .lb-you  {{ color: #FFD700 !important; }}

  /* ── Practice Lab overlay ── */
  .lab-overlay {{
    position: fixed;
    bottom: 5rem;
    right: 1.5rem;
    width: min(520px, 90vw);
    background: var(--bg2);
    border: 2px solid var(--neon);
    border-radius: 12px;
    padding: 1.2rem;
    box-shadow: 0 0 40px rgba(0,255,65,0.2), 8px 8px 0 #000;
    z-index: 9999;
  }}
  .lab-fab {{
    position: fixed;
    bottom: 1.5rem;
    right: 1.5rem;
    background: var(--neon);
    color: #000 !important;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 0.85rem;
    border: 3px solid #000;
    border-radius: 50px;
    padding: 0.7rem 1.3rem;
    box-shadow: var(--btn-glow);
    cursor: pointer;
    z-index: 10000;
    text-decoration: none;
    display: inline-block;
    transition: all 0.15s;
  }}
  .lab-fab:hover {{ box-shadow: var(--btn-glow-hover); transform: translate(-2px,-2px); }}

  /* ── Sandbox ── */
  .stTextArea > div > div > textarea {{
    background: {code_bg} !important;
    border: 2px solid var(--border) !important;
    color: {code_color} !important;
    border-radius: var(--radius) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    line-height: 1.55 !important;
  }}
  .stTextArea > div > div > textarea:focus {{ border-color: var(--neon) !important; }}
  .sandbox-output {{
    background: {code_bg};
    border: 2px solid var(--border);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: {code_color} !important;
    white-space: pre-wrap;
    min-height: 3rem;
    max-height: 14rem;
    overflow-y: auto;
    margin-top: 0.4rem;
  }}
  .sandbox-error {{
    background: rgba(255,68,68,0.06);
    border: 2px solid #FF4444;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #FF8888 !important;
    white-space: pre-wrap;
    margin-top: 0.4rem;
  }}
  .sandbox-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted) !important;
    margin-top: 0.3rem;
    margin-bottom: 0.1rem;
  }}

  /* ── Text inputs ── */
  .stTextInput > div > div > input {{
    background: {input_bg} !important;
    border: 2px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
    font-family: 'JetBrains Mono', monospace !important;
  }}
  .stTextInput > div > div > input:focus {{
    border-color: var(--neon) !important;
    box-shadow: 0 0 0 1px var(--neon) !important;
  }}
  .stTextInput > label {{ color: var(--muted) !important; font-size: 0.78rem !important; }}

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {{ background: transparent; gap: 0.4rem; }}
  .stTabs [data-baseweb="tab"] {{
    background: var(--card2) !important;
    border: 2px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text2) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.76rem !important;
  }}
  .stTabs [aria-selected="true"] {{
    background: var(--purple) !important;
    border-color: var(--purple) !important;
    color: #fff !important;
  }}
  .stTabs [data-baseweb="tab-panel"] {{ background: transparent !important; padding: 1rem 0 !important; }}

  /* ── Selectbox ── */
  .stSelectbox > div > div {{
    background: var(--card) !important;
    border: 2px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
  }}

  /* ── Code blocks ── */
  .stCodeBlock, pre, code {{
    font-family: 'JetBrains Mono', monospace !important;
    background: {code_bg} !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
  }}

  /* ── Pass/fail ── */
  .pass-badge {{ color: var(--neon) !important; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; }}
  .fail-badge {{ color: #FF4444 !important; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; }}

  /* ── Expander ── */
  .streamlit-expanderHeader {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    color: var(--neon) !important;
    background: {expander_bg} !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
  }}
  [data-testid="stSidebar"] .streamlit-expanderHeader {{
    color: var(--neon) !important;
    background: var(--sidebar-bg) !important;
  }}

  /* ── Quest path connector lines ── */
  .path-connector {{
    width: 3px;
    height: 2.5rem;
    background: linear-gradient(180deg, var(--neon), transparent);
    margin: 0 auto;
    border-radius: 2px;
    opacity: 0.4;
  }}
  .path-connector-locked {{
    width: 3px;
    height: 2.5rem;
    background: var(--border);
    margin: 0 auto;
    border-radius: 2px;
    opacity: 0.3;
  }}

  /* ── Topbar ── */
  .topbar {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
  }}
</style>
""", unsafe_allow_html=True)


# ============================================================
# AUTH ACTIONS
# ============================================================
def do_register(username, password, confirm):
    username = username.strip().lower()
    if not username or not password:
        st.session_state.auth_error = "Username and password cannot be empty."; return
    if len(username) < 3:
        st.session_state.auth_error = "Username must be at least 3 characters."; return
    if len(password) < 6:
        st.session_state.auth_error = "Password must be at least 6 characters."; return
    if password != confirm:
        st.session_state.auth_error = "Passwords do not match."; return
    db = get_db()
    if username in db["users"]:
        st.session_state.auth_error = "Username already taken. Try another."; return
    db["users"][username]    = {"pw_hash": hash_password(password), "registered": datetime.now().isoformat()}
    db["progress"][username] = empty_progress()
    flush_db()
    st.session_state.auth_error   = ""
    st.session_state.auth_success = f"Account created! Welcome, {username} 🎉 Now log in."
    st.session_state.auth_tab     = "login"

def do_login(username, password):
    username = username.strip().lower()
    db = get_db()
    if username not in db["users"]:
        st.session_state.auth_error = "Username not found. Please register first."; return
    if not check_password(password, db["users"][username]["pw_hash"]):
        st.session_state.auth_error = "Incorrect password. Try again."; return
    st.session_state.auth_error   = ""
    st.session_state.auth_success = ""
    st.session_state.logged_in    = True
    st.session_state.username     = username
    new_streak = update_streak(username)
    load_user_progress(username)
    st.session_state.streak = new_streak
    st.session_state.view   = "hub"


# ============================================================
# AUTH SCREEN
# ============================================================
def render_auth():
    dark = st.session_state.get("dark_mode", True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            '<div style="text-align:center;padding-top:2rem;">'
            '<div style="font-family:JetBrains Mono,monospace;font-size:0.55rem;color:var(--neon);'
            'letter-spacing:0.4em;margin-bottom:0.6rem;">🐍 PYTHON CODING ADVENTURE</div>'
            '<div style="font-family:Syne,sans-serif;font-size:2rem;font-weight:800;color:var(--text);'
            'text-shadow:0 0 20px rgba(0,255,65,0.3);">Welcome, Adventurer</div>'
            '<div style="color:var(--muted);font-size:0.85rem;margin-top:0.4rem;">'
            'XP, streaks and progress saved permanently</div>'
            '</div>',
            unsafe_allow_html=True)
        st.markdown("<hr class='divider'/>", unsafe_allow_html=True)

        col_l, col_r = st.columns(2)
        with col_l:
            if st.button("🔓 Log In", use_container_width=True, key="tab_login"):
                st.session_state.auth_tab = "login"; st.session_state.auth_error = ""; st.rerun()
        with col_r:
            if st.button("✨ Register", use_container_width=True, key="tab_reg"):
                st.session_state.auth_tab = "register"; st.session_state.auth_error = ""; st.rerun()

        active = st.session_state.auth_tab
        st.markdown(
            f'<div style="display:flex;gap:0;margin-bottom:1.5rem;">'
            f'<div style="flex:1;height:3px;background:{"var(--neon)" if active=="login" else "var(--border)"};border-radius:2px 0 0 2px;"></div>'
            f'<div style="flex:1;height:3px;background:{"var(--neon)" if active=="register" else "var(--border)"};border-radius:0 2px 2px 0;"></div></div>',
            unsafe_allow_html=True)

        if st.session_state.auth_error:
            st.markdown(
                f'<div style="background:rgba(255,68,68,0.12);border-left:4px solid #FF4444;'
                f'border-radius:0 8px 8px 0;padding:0.8rem 1rem;color:#FF8888;margin-bottom:0.8rem;">'
                f'⚠️ {st.session_state.auth_error}</div>', unsafe_allow_html=True)
        if st.session_state.auth_success:
            st.markdown(f'<div class="success-box">✅ {st.session_state.auth_success}</div>', unsafe_allow_html=True)

        if active == "login":
            username = st.text_input("Username", placeholder="your_username", key="li_user")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="li_pass")
            st.markdown("")
            if st.button("⚡ Log In & Start Adventure", use_container_width=True, key="login_btn"):
                do_login(username, password); st.rerun()
            st.markdown(
                '<div style="text-align:center;color:var(--muted);font-size:0.78rem;margin-top:1rem;">'
                "No account? Click <strong style='color:var(--purple2)'>Register</strong> above.</div>",
                unsafe_allow_html=True)
        else:
            username = st.text_input("Choose a Username", placeholder="coolcoder99 (min 3 chars)", key="reg_user")
            password = st.text_input("Choose a Password", type="password", placeholder="Min. 6 characters", key="reg_pass")
            confirm  = st.text_input("Confirm Password",  type="password", placeholder="Repeat password", key="reg_conf")
            st.markdown("")
            if st.button("🚀 Create My Account", use_container_width=True, key="reg_btn"):
                do_register(username, password, confirm); st.rerun()
            st.markdown(
                '<div style="text-align:center;color:var(--muted);font-size:0.78rem;margin-top:1rem;">'
                "Already have an account? Click <strong style='color:var(--neon)'>Log In</strong> above.</div>",
                unsafe_allow_html=True)

        st.markdown(
            '<div style="text-align:center;margin-top:2.5rem;padding:0.8rem;background:var(--card);'
            'border:1px dashed var(--border);border-radius:8px;">'
            '<span style="font-size:0.75rem;color:var(--muted);">💾 Progress saved to disk — '
            '🔥 Log in daily to build your streak and earn +20% bonus XP!</span></div>',
            unsafe_allow_html=True)


# ============================================================
# load_practice_lab() — FLOATING LAB WITH FAB BUTTON
# ============================================================
def load_practice_lab():
    """Floating Practice Lab — toggled by a FAB button in the sidebar."""
    lab_open = st.session_state.get("lab_open", False)

    btn_label = "✕ Close Lab" if lab_open else "🧪 Summon Lab"
    if st.button(btn_label, key="lab_toggle", use_container_width=True):
        st.session_state.lab_open = not lab_open
        st.rerun()

    if not st.session_state.get("lab_open", False):
        return

    st.markdown("---")
    st.markdown(
        '<div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:var(--neon);">// PRACTICE LAB</div>'
        '<div class="sandbox-label">Write Python and hit ▶ Run</div>',
        unsafe_allow_html=True)

    # Preserve code across reruns via session_state
    code = st.text_area(
        "lab_code_area",
        value=st.session_state.get("sandbox_code", ""),
        height=160,
        key="sandbox_code_widget",
        placeholder='print("Hello, Realm!")\nfor i in range(5):\n    print(i)',
        label_visibility="collapsed",
    )
    # Sync back so it persists when Lab is closed/reopened
    st.session_state.sandbox_code = code

    col_run, col_clr = st.columns([3, 1])
    with col_run:
        run_clicked = st.button("▶ Run Code", key="sandbox_run", use_container_width=True)
    with col_clr:
        if st.button("✕", key="sandbox_clear", use_container_width=True):
            st.session_state.sandbox_output = ""
            st.session_state.sandbox_error  = ""
            st.rerun()

    if run_clicked:
        if code.strip():
            buf        = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = buf
            try:
                exec(compile(code, "<sandbox>", "exec"), {})
                st.session_state.sandbox_output = buf.getvalue() or "(no output)"
                st.session_state.sandbox_error  = ""
            except Exception:
                tb = traceback.format_exc()
                st.session_state.sandbox_error  = tb
                st.session_state.sandbox_output = ""
                # Dungeon Guide tip
                if "NameError" in tb:
                    st.toast("🧙 Guide: NameError means a variable is used before it's defined!", icon="💡")
                elif "SyntaxError" in tb:
                    st.toast("🧙 Guide: SyntaxError — check your colons, brackets, and indentation!", icon="💡")
                elif "IndentationError" in tb:
                    st.toast("🧙 Guide: IndentationError — Python is strict about spaces. Use 4 spaces per indent.", icon="💡")
                elif "TypeError" in tb:
                    st.toast("🧙 Guide: TypeError — you're mixing incompatible types, like str + int!", icon="💡")
                elif "IndexError" in tb:
                    st.toast("🧙 Guide: IndexError — you're accessing a list position that doesn't exist!", icon="💡")
                else:
                    st.toast("🧙 Dungeon Guide: Check the error below and read it carefully!", icon="⚠️")
            finally:
                sys.stdout = old_stdout

    output = st.session_state.get("sandbox_output", "")
    error  = st.session_state.get("sandbox_error",  "")
    if output:
        st.markdown(
            f'<div class="sandbox-label">// OUTPUT</div>'
            f'<div class="sandbox-output">{output}</div>',
            unsafe_allow_html=True)
    if error:
        st.markdown(
            f'<div class="sandbox-label" style="color:#FF4444;">// ERROR</div>'
            f'<div class="sandbox-error">{error}</div>',
            unsafe_allow_html=True)
    if not output and not error:
        st.markdown('<div class="sandbox-label" style="color:var(--border);">// output will appear here</div>',
                    unsafe_allow_html=True)


# ============================================================
# load_sidebar() — UNIFIED SIDEBAR
# ============================================================
def load_sidebar():
    xp          = st.session_state.xp
    title, icon = get_character_info(xp)
    max_xp      = sum(v["xp_reward"] for v in LEVELS.values())
    completed   = len(st.session_state.completed_levels)
    streak      = st.session_state.get("streak", 0)
    boss_count  = len(st.session_state.get("boss_beaten", set()))
    stars       = sum(
        st.session_state.quiz_state.get(l, {}).get("score", 0)
        for l in st.session_state.completed_levels
    )

    with st.sidebar:
        # ── Brand ──
        st.markdown(
            '<div style="text-align:center;padding:0.4rem 0 0.8rem;">'
            '<div style="font-family:JetBrains Mono,monospace;font-size:0.48rem;'
            'color:var(--neon);letter-spacing:0.3em;">🐍 PYTHON ADVENTURE</div>'
            '</div>',
            unsafe_allow_html=True)

        # ── Theme toggle ──
        dark = st.session_state.get("dark_mode", True)
        toggle_label = "☀️ Scholar Mode" if dark else "🌑 Matrix Mode"
        if st.button(toggle_label, key="theme_toggle", use_container_width=True):
            st.session_state.dark_mode = not dark
            st.rerun()

        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        # ── CHARACTER PROFILE ──
        avatar_letters = (st.session_state.username[:2].upper() if st.session_state.username else "??")
        streak_fire = "🔥" * min(streak, 5) if streak >= 1 else ""
        st.markdown(
            f'<div style="text-align:center;padding:0.8rem 0;">'
            f'<div style="width:64px;height:64px;border-radius:50%;background:linear-gradient(135deg,var(--purple),var(--neon));'
            f'display:flex;align-items:center;justify-content:center;margin:0 auto 0.6rem;'
            f'border:3px solid var(--neon);box-shadow:0 0 16px rgba(0,255,65,0.3);">'
            f'<span style="font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:#fff;">{avatar_letters}</span>'
            f'</div>'
            f'<div style="font-family:Syne,sans-serif;font-size:1rem;color:var(--text);font-weight:700;">{icon} {title}</div>'
            f'<div style="font-size:0.7rem;color:var(--neon);margin-top:0.15rem;font-family:JetBrains Mono,monospace;">@{st.session_state.username}</div>'
            f'<div style="font-size:0.95rem;margin-top:0.4rem;">{streak_fire}</div>'
            f'</div>',
            unsafe_allow_html=True)

        # Streak banner
        if streak >= 2:
            st.markdown(
                f'<div class="streak-badge">🔥 {streak}-Day Streak! +20% XP Bonus</div>',
                unsafe_allow_html=True)
        elif streak == 1:
            st.markdown(
                '<div style="text-align:center;font-size:0.67rem;color:#FF9000;font-family:JetBrains Mono,monospace;'
                'padding:0.3rem 0;">🔥 Login tomorrow to ignite your streak!</div>',
                unsafe_allow_html=True)

        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        # ── UNIFIED STATS ──
        st.markdown(
            '<div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;'
            'color:var(--muted);margin-bottom:0.5rem;letter-spacing:0.12em;">CHARACTER STATS</div>',
            unsafe_allow_html=True)

        st.markdown(
            f'<div class="stat-row"><span style="color:var(--muted)">XP</span>'
            f'<span class="xp-badge">{xp} / {max_xp}</span></div>',
            unsafe_allow_html=True)
        st.progress(xp_to_progress(xp))

        for label, val, color in [
            ("Levels Done",   f"{completed} / 5",   "var(--neon)"),
            ("Bosses Beaten", f"💀 {boss_count} / 5", "#FF4444"),
            ("Quiz Stars",    f"⭐ {stars} pts",     "#FFD700"),
            ("Pass Mark",     "6 / 10 (60%)",        "var(--purple2)"),
        ]:
            st.markdown(
                f'<div class="stat-row">'
                f'<span style="color:var(--muted)">{label}</span>'
                f'<span style="color:{color};font-family:JetBrains Mono,monospace;">{val}</span>'
                f'</div>',
                unsafe_allow_html=True)

        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        # ── QUEST MAP (vertical path) ──
        st.markdown(
            '<div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;'
            'color:var(--muted);margin-bottom:0.5rem;letter-spacing:0.12em;">QUEST MAP</div>',
            unsafe_allow_html=True)

        for idx, (lvl_id, lvl) in enumerate(LEVELS.items()):
            status    = level_status(lvl_id)
            st_icon   = {"done": "✅", "unlocked": "🔓", "locked": "🔒"}[status]
            clr       = {"done": "var(--neon)", "unlocked": "var(--text)", "locked": "var(--muted)"}[status]
            qs        = st.session_state.quiz_state.get(lvl_id, {})
            score_txt = f" ({qs.get('score',0)}/10)" if qs.get("submitted") else ""
            boss_icon = " 💀" if lvl_id in st.session_state.get("boss_beaten", set()) else ""
            bg        = "background:rgba(0,255,65,0.06);" if status == "unlocked" else ""
            mission_short = lvl["mission"].split(":")[0]  # "Mission N"

            st.markdown(
                f'<div style="{bg}display:flex;align-items:center;gap:0.6rem;padding:0.4rem 0.6rem;'
                f'border-radius:6px;font-size:0.7rem;">'
                f'<span style="font-size:1rem;">{st_icon}</span>'
                f'<div>'
                f'<div style="color:{clr};font-family:JetBrains Mono,monospace;font-weight:700;">'
                f'{mission_short}{score_txt}{boss_icon}</div>'
                f'<div style="color:var(--muted);font-size:0.62rem;">{lvl["title"]}</div>'
                f'</div></div>',
                unsafe_allow_html=True)

            # Connector line between levels
            if idx < len(LEVELS) - 1:
                css_cls = "path-connector" if status != "locked" else "path-connector-locked"
                st.markdown(f'<div class="{css_cls}"></div>', unsafe_allow_html=True)

        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        # ── MY SPELLBOOK (unlockable cheat sheet) ──
        unlocked_ids = sorted(st.session_state.completed_levels)
        # Always show Level 1 spells regardless
        available = [1] + [i for i in unlocked_ids if i != 1]
        if available:
            with st.expander("📖 My Spellbook", expanded=False):
                for lvl_id in available:
                    sb = SPELLBOOK.get(lvl_id)
                    if not sb:
                        continue
                    st.markdown(
                        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.68rem;'
                        f'color:var(--neon);margin:0.5rem 0 0.2rem;">{sb["title"]}</div>',
                        unsafe_allow_html=True)
                    for spell_name, snippet in sb["spells"]:
                        st.markdown(
                            f'<div style="font-size:0.62rem;color:var(--muted);margin-bottom:0.1rem;">{spell_name}</div>',
                            unsafe_allow_html=True)
                        st.code(snippet, language="python")
        else:
            st.markdown(
                '<div style="font-size:0.72rem;color:var(--muted);text-align:center;padding:0.5rem 0;">'
                '📖 Complete levels to unlock spells!</div>',
                unsafe_allow_html=True)

        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        # ── NAV BUTTONS ──
        if st.button("🏠 Adventure Hub", use_container_width=True):
            st.session_state.view = "hub"; st.rerun()
        if st.button("🏆 Leaderboard", use_container_width=True):
            st.session_state.view = "leaderboard"; st.rerun()

        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        # ── PRACTICE LAB FAB (inside sidebar) ──
        load_practice_lab()

        st.markdown("<div class='divider'/>", unsafe_allow_html=True)

        if st.button("🚪 Log Out", use_container_width=True):
            save_user_progress(st.session_state.username)
            for k in ["logged_in","username","xp","completed_levels","quiz_state",
                      "cert_name","current_level","show_badge","view",
                      "streak","last_login","boss_beaten","sandbox_output","sandbox_error",
                      "sandbox_code","lab_open"]:
                st.session_state.pop(k, None)
            st.rerun()


# ============================================================
# TOPBAR — always-visible XP strip
# ============================================================
def render_topbar():
    xp          = st.session_state.xp
    title, icon = get_character_info(xp)
    max_xp      = sum(v["xp_reward"] for v in LEVELS.values())
    streak      = st.session_state.get("streak", 0)
    progress    = min(xp / max_xp, 1.0)
    filled      = int(progress * 18)
    bar         = "█" * filled + "░" * (18 - filled)
    streak_html = f'<span style="color:#FF9000;margin-left:1rem;font-size:0.7rem;">🔥 {streak}-Day Streak</span>' if streak >= 2 else ""
    st.markdown(
        f'<div class="topbar">'
        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:var(--muted);">'
        f'{icon} <span style="color:var(--text)">{title}</span>'
        f'&nbsp;&nbsp;<span style="color:var(--neon)">{bar}</span>'
        f'&nbsp;<span style="color:var(--muted)">{xp}/{max_xp} XP</span>'
        f'{streak_html}</div>'
        f'<div style="font-size:0.65rem;color:var(--muted);font-family:JetBrains Mono,monospace;">@{st.session_state.username}</div>'
        f'</div>',
        unsafe_allow_html=True)


# ============================================================
# LEADERBOARD
# ============================================================
def render_leaderboard():
    st.markdown(
        '<h1 class="neon-heading" style="font-size:1.6rem;margin-bottom:0.2rem;">🏆 Global Rankings</h1>'
        '<p style="color:var(--muted);font-family:JetBrains Mono,monospace;font-size:0.75rem;">Top adventurers ranked by total XP</p>',
        unsafe_allow_html=True)
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)

    db       = get_db()
    all_prog = db.get("progress", {})
    entries  = [
        (u, p.get("xp", 0), len(p.get("completed_levels", [])), len(p.get("boss_beaten", [])), p.get("streak", 0))
        for u, p in all_prog.items()
    ]
    entries.sort(key=lambda x: x[1], reverse=True)
    medals = ["🥇","🥈","🥉"] + ["🏅"]*7
    me     = st.session_state.username

    if not entries:
        st.markdown('<div class="info-box">No adventurers yet — be the first! 🚀</div>', unsafe_allow_html=True)
    else:
        for rank, (uname, xp, lvls, bosses, streak) in enumerate(entries[:10], 1):
            medal      = medals[rank-1] if rank <= len(medals) else f"#{rank}"
            is_you     = uname == me
            you_label  = ' <span style="color:#FFD700;font-size:0.68rem;">(YOU)</span>' if is_you else ""
            flame      = f' <span style="color:#FF9000;">🔥{streak}</span>' if streak >= 2 else ""
            boss_tag   = f' <span style="color:#FF4444;font-size:0.7rem;">💀×{bosses}</span>' if bosses else ""
            you_border = "border-color:#FFD700;" if is_you else ""
            name_cls   = "lb-you" if is_you else ""
            st.markdown(
                f'<div class="lb-row" style="{you_border}">'
                f'  <div class="lb-rank">{medal}</div>'
                f'  <div class="lb-name {name_cls}">@{uname}{you_label}{flame}{boss_tag}</div>'
                f'  <div style="color:var(--muted);font-size:0.7rem;font-family:JetBrains Mono,monospace;min-width:5rem;">{lvls}/5 levels</div>'
                f'  <div class="lb-xp">{xp} XP</div>'
                f'</div>',
                unsafe_allow_html=True)

    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
    if st.button("← Back to Hub"):
        st.session_state.view = "hub"; st.rerun()


# ============================================================
# load_main_grid() — QUEST PATH HUB
# ============================================================
def load_main_grid():
    streak = st.session_state.get("streak", 0)
    if streak >= 2:
        st.markdown(
            f'<div style="background:linear-gradient(90deg,rgba(255,100,0,0.12),transparent);'
            f'border-left:4px solid #FF6400;border-radius:0 8px 8px 0;padding:0.7rem 1.2rem;margin-bottom:0.8rem;">'
            f'🔥 <strong style="color:#FF9000;">{streak}-Day Streak Active!</strong> '
            f'<span style="color:var(--muted);font-size:0.82rem;">All XP gains ×1.2 today.</span>'
            f'</div>', unsafe_allow_html=True)

    st.markdown(
        f'<h1 class="neon-heading" style="font-size:1.7rem;margin-bottom:0.1rem;">🐍 Python Coding Adventure</h1>'
        f'<p style="color:var(--muted);font-family:JetBrains Mono,monospace;font-size:0.75rem;">'
        f'Welcome back, <span style="color:var(--neon);">@{st.session_state.username}</span>'
        f' — choose your next mission!</p>',
        unsafe_allow_html=True)
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)

    # ── Vertical Quest Path ──
    st.markdown(
        '<div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;'
        'color:var(--muted);letter-spacing:0.15em;margin-bottom:1rem;">// MISSION SELECT</div>',
        unsafe_allow_html=True)

    level_items = list(LEVELS.items())
    for idx, (lvl_id, lvl) in enumerate(level_items):
        status  = level_status(lvl_id)
        border  = "var(--neon)" if status=="done" else (lvl["color"] if status=="unlocked" else "var(--border)")
        opacity = "1" if status != "locked" else "0.45"
        lbl_txt = "✅ COMPLETE" if status=="done" else ("▶ LAUNCH MISSION" if status=="unlocked" else "🔒 LOCKED")
        lbl_col = "var(--neon)" if status=="done" else ("var(--text)" if status=="unlocked" else "var(--muted)")
        qs      = st.session_state.quiz_state.get(lvl_id, {})

        sc_html = ""
        if qs.get("submitted"):
            sc = qs.get("score", 0)
            pi = "✅" if sc >= PASS_THRESHOLD else "❌"
            sc_html = f'<span style="font-size:0.68rem;color:var(--muted);margin-left:0.5rem;">{pi} {sc}/{QUESTIONS_PER_EXAM}</span>'

        boss_html = ""
        if lvl_id in st.session_state.get("boss_beaten", set()):
            boss_html = '<span style="font-size:0.68rem;color:#FF4444;margin-left:0.5rem;">💀 Boss Slain</span>'

        left_col, right_col = st.columns([3, 1])
        with left_col:
            st.markdown(
                f'<div style="background:var(--card);border:2px solid {border};border-radius:10px;'
                f'padding:1rem 1.2rem;opacity:{opacity};'
                f'box-shadow:{"0 0 12px rgba(0,255,65,0.15), 4px 4px 0 #000" if status=="unlocked" else "3px 3px 0 #000"};">'
                f'<div style="display:flex;align-items:center;gap:0.8rem;">'
                f'<div style="font-size:2rem;background:var(--card2);border:1px solid var(--border);'
                f'border-radius:6px;padding:0.3rem 0.6rem;">{lvl["pixel_art"]}</div>'
                f'<div style="flex:1;">'
                f'<div style="font-family:JetBrains Mono,monospace;font-size:0.58rem;color:{border};letter-spacing:0.2em;">'
                f'{lvl["mission"].split(":")[0].upper()}</div>'
                f'<div style="font-family:Syne,sans-serif;font-size:0.95rem;color:var(--text);font-weight:700;margin:0.1rem 0;">'
                f'{lvl["icon"]} {lvl["title"]}</div>'
                f'<div style="font-size:0.72rem;color:var(--text2);">{lvl["lore"]}</div>'
                f'</div></div>'
                f'<div style="margin-top:0.6rem;display:flex;align-items:center;gap:0.3rem;">'
                f'<span style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:{lbl_col};">{lbl_txt}</span>'
                f'{sc_html}{boss_html}</div>'
                f'</div>',
                unsafe_allow_html=True)

        with right_col:
            xp_mult = streak_multiplier()
            xp_show = int(lvl["xp_reward"] * xp_mult)
            st.markdown(
                f'<div style="text-align:center;padding:0.8rem;background:var(--card2);'
                f'border:1px solid var(--border);border-radius:8px;height:100%;'
                f'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0.3rem;">'
                f'<div style="font-family:JetBrains Mono,monospace;font-size:1rem;color:var(--purple2);font-weight:700;">+{xp_show}</div>'
                f'<div style="font-size:0.6rem;color:var(--muted);">XP reward</div>'
                f'<div style="font-size:0.7rem;color:var(--muted);">{lvl["icon"]}</div>'
                f'</div>',
                unsafe_allow_html=True)

            if status != "locked":
                btn_lbl = "🔍 Review" if status == "done" else "⚡ Start"
                if st.button(btn_lbl, key=f"hub_{lvl_id}", use_container_width=True):
                    st.session_state.view = "level"
                    st.session_state.current_level = lvl_id
                    st.rerun()

        # Path connector
        if idx < len(level_items) - 1:
            nxt_status = level_status(level_items[idx+1][0])
            css_cls = "path-connector" if status == "done" else "path-connector-locked"
            st.markdown(f'<div class="{css_cls}"></div>', unsafe_allow_html=True)

    # ── Stats strip at bottom ──
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
    xp          = st.session_state.xp
    title, icon = get_character_info(xp)
    max_xp      = sum(v["xp_reward"] for v in LEVELS.values())
    done        = len(st.session_state.completed_levels)
    stars       = sum(st.session_state.quiz_state.get(l, {}).get("score", 0) for l in st.session_state.completed_levels)
    bosses      = len(st.session_state.get("boss_beaten", set()))

    for col, val, label, sub, color in zip(
        st.columns(5),
        [f"{icon} {title}", str(xp), f"{done}/5", f"⭐{stars}", f"💀{bosses}/5"],
        ["Rank", "XP Earned", "Levels Done", "Stars", "Bosses"],
        ["Character class", f"of {max_xp} total", "Keep going!", "quiz correct", "defeated"],
        ["var(--neon)", "var(--purple2)", "var(--neon)", "#FFD700", "#FF4444"],
    ):
        with col:
            st.markdown(
                f'<div class="card" style="text-align:center;padding:0.9rem;">'
                f'<div style="font-family:Syne,sans-serif;font-size:1rem;color:var(--text);font-weight:700;">{val}</div>'
                f'<div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:{color};">{label}</div>'
                f'<div style="font-size:0.6rem;color:var(--muted);">{sub}</div></div>',
                unsafe_allow_html=True)


# ============================================================
# BOSS BATTLE
# ============================================================
def render_boss_battle(level_id: int, lvl: dict):
    boss   = lvl.get("boss")
    if not boss:
        st.markdown('<div class="info-box">No boss for this level yet.</div>', unsafe_allow_html=True)
        return

    beaten = level_id in st.session_state.get("boss_beaten", set())
    mult   = streak_multiplier()
    bonus  = int(boss["xp_reward"] * mult)
    streak = st.session_state.get("streak", 0)

    if beaten:
        st.markdown(
            f'<div class="boss-beaten">💀 {boss["name"]} HAS BEEN DEFEATED!<br/>'
            f'<span style="font-size:0.78rem;color:var(--purple2);">+{bonus} XP claimed</span></div>',
            unsafe_allow_html=True)
        return

    streak_note = f' <span style="color:#FF9000;font-size:0.75rem;">(🔥 ×{mult:.1f} streak!)</span>' if streak >= 2 else ""
    st.markdown(
        f'<div class="boss-card">'
        f'<div class="boss-title">⚔️ BOSS BATTLE: {boss["name"]}</div>'
        f'<p style="color:#ccc;font-size:0.85rem;margin:0 0 1rem;">{boss["lore"]}</p>'
        f'<p style="color:#FF9090;font-family:JetBrains Mono,monospace;font-size:0.82rem;line-height:1.6;">{boss["challenge"]}</p>'
        f'<p style="color:var(--muted);font-size:0.78rem;font-style:italic;margin-top:0.5rem;">💡 Hint: {boss["hint"]}</p>'
        f'<p style="color:var(--purple2);font-family:JetBrains Mono,monospace;font-size:0.78rem;margin-top:0.5rem;">'
        f'Reward: <strong>+{bonus} XP</strong>{streak_note}</p>'
        f'</div>', unsafe_allow_html=True)

    answer_input = st.text_input("Your answer:", key=f"boss_input_{level_id}", placeholder="Type your answer exactly…")

    if st.button("⚔️ Deliver the Final Blow!", key=f"boss_submit_{level_id}"):
        cleaned = answer_input.strip().lower().replace('"', "'")
        correct = any(cleaned == a.strip().lower() for a in boss["accepted"])
        if correct:
            st.session_state.xp += bonus
            if "boss_beaten" not in st.session_state or not isinstance(st.session_state.boss_beaten, set):
                st.session_state.boss_beaten = set()
            st.session_state.boss_beaten.add(level_id)
            save_user_progress(st.session_state.username)
            st.balloons()
            st.rerun()
        else:
            st.markdown(
                f'<div style="background:rgba(255,68,68,0.08);border-left:4px solid #FF4444;'
                f'border-radius:0 8px 8px 0;padding:0.7rem 1rem;margin:0.4rem 0;color:#FF8888;">'
                f'❌ Not quite — read the hint and try again!</div>',
                unsafe_allow_html=True)


# ============================================================
# LEVEL VIEW
# ============================================================
def render_level(level_id):
    lvl = LEVELS[level_id]
    if st.button("← Back to Hub"):
        st.session_state.view = "hub"; st.rerun()
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)

    # Mission header
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;">'
        f'<div style="font-size:2.8rem;background:var(--card2);border:2px solid var(--border);'
        f'border-radius:8px;padding:0.3rem 0.8rem;box-shadow:3px 3px 0 #000;">{lvl["pixel_art"]}</div>'
        f'<div>'
        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.58rem;color:{lvl["color"]};letter-spacing:0.25em;">{lvl["mission"].split(":")[0].upper()}</div>'
        f'<div style="font-family:Syne,sans-serif;font-size:1.3rem;color:var(--text);font-weight:800;">{lvl["icon"]} {lvl["title"]}</div>'
        f'<div style="font-size:0.82rem;color:var(--text2);">{lvl["lore"]}</div>'
        f'</div></div>',
        unsafe_allow_html=True)

    if not is_level_unlocked(level_id):
        st.markdown(f'<div class="locked-box">🔒 Complete Mission {level_id-1} first.</div>', unsafe_allow_html=True)
        return

    tab1, tab2, tab3, tab4 = st.tabs(["📖 Learn", "💻 Code Example", "🎯 Quiz (10 Q)", "💀 Boss Battle"])
    with tab1:
        st.markdown(lvl["description"], unsafe_allow_html=False)
        mult = streak_multiplier()
        bonus_note = f" <em style='color:#FF9000;'>🔥 Streak active — XP ×{mult:.1f}!</em>" if mult > 1 else ""
        st.markdown(
            f'<div class="info-box">💡 Complete the quiz to earn '
            f'<strong style="color:var(--neon)">+{int(lvl["xp_reward"]*mult)} XP</strong>'
            f' — Pass mark: <strong>6/10 (60%)</strong>{bonus_note}</div>',
            unsafe_allow_html=True)
    with tab2:
        st.markdown('<p style="color:var(--muted);font-size:0.8rem;font-family:JetBrains Mono,monospace;">// Study this before the quiz</p>',
                    unsafe_allow_html=True)
        st.code(lvl["code_example"], language="python")
    with tab3:
        render_quiz(level_id, lvl)
    with tab4:
        render_boss_battle(level_id, lvl)


# ============================================================
# QUIZ
# ============================================================
def render_quiz(level_id, lvl):
    questions, _ = get_exam_questions(level_id)
    qs_data   = st.session_state.quiz_state.get(level_id, {})
    passed    = level_id in st.session_state.completed_levels
    submitted = qs_data.get("submitted", False)
    score     = qs_data.get("score", 0)
    mult      = streak_multiplier()

    if st.session_state.show_badge == level_id:
        st.balloons()
        xp_gained = int(lvl["xp_reward"] * mult)
        st.markdown(
            f'<div class="milestone">'
            f'<div style="font-size:3rem;">🏆</div>'
            f'<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;margin:0.5rem 0;">MISSION COMPLETE!</div>'
            f'<div>{lvl["mission"]} — Score: {score}/{QUESTIONS_PER_EXAM}</div>'
            f'<div style="margin-top:0.8rem;"><span class="xp-badge">+{xp_gained} XP saved 💾</span></div>'
            f'</div>', unsafe_allow_html=True)
        st.session_state.show_badge = None

    if submitted:
        pct = int(score / QUESTIONS_PER_EXAM * 100)
        if passed:
            st.markdown(
                f'<div class="success-box">✅ Mission PASSED! Score: {score}/{QUESTIONS_PER_EXAM} ({pct}%) — Progress saved 💾</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div style="background:rgba(255,68,68,0.10);border-left:4px solid #FF4444;'
                f'border-radius:0 8px 8px 0;padding:0.9rem 1.2rem;margin:0.8rem 0;color:#FF8888;">'
                f'❌ Score: {score}/{QUESTIONS_PER_EXAM} ({pct}%) — Need 6/10 to pass. Retry!</div>',
                unsafe_allow_html=True)

    streak_note = f" 🔥 Streak ×{mult:.1f} bonus active!" if mult > 1 else ""
    st.markdown(
        f'<p style="font-family:JetBrains Mono,monospace;font-size:0.75rem;color:var(--muted);margin-bottom:1rem;">'
        f'Answer all {QUESTIONS_PER_EXAM} questions, then submit. '
        f'Pass mark: {PASS_THRESHOLD}/{QUESTIONS_PER_EXAM} (60%) — '
        f'Randomly selected from a bank of {QUESTIONS_IN_BANK}.{streak_note}</p>',
        unsafe_allow_html=True)

    saved_answers = qs_data.get("answers", [None] * QUESTIONS_PER_EXAM)
    user_answers  = []

    for i, q in enumerate(questions):
        st.markdown(
            f'<div class="card" style="margin-bottom:0.6rem;">'
            f'<p style="font-family:JetBrains Mono,monospace;font-size:0.82rem;color:var(--text);margin:0 0 0.8rem;">'
            f'Q{i+1}/{QUESTIONS_PER_EXAM}: {q["q"]}</p></div>',
            unsafe_allow_html=True)
        saved_val   = saved_answers[i] if i < len(saved_answers) else None
        default_idx = q["options"].index(saved_val) if saved_val in q["options"] else 0
        disabled    = submitted and passed
        choice = st.radio(
            f"Q{i+1}", q["options"], index=default_idx,
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
                    unsafe_allow_html=True)
        st.markdown("")

    if submitted and not passed:
        st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
        st.markdown('<p style="color:#FF8888;font-family:JetBrains Mono,monospace;font-size:0.8rem;">'
                    'You need 6/10 to pass. New random questions on retry.</p>', unsafe_allow_html=True)
        if st.button("🔄 Retry Mission", key=f"retry_{level_id}"):
            st.session_state.quiz_state.pop(level_id, None)
            save_user_progress(st.session_state.username)
            st.rerun()

    if not submitted:
        if st.button("⚡ Submit Answers", key=f"submit_{level_id}"):
            new_score  = sum(1 for i, q in enumerate(questions) if user_answers[i] == q["answer"])
            new_passed = new_score >= PASS_THRESHOLD
            current = st.session_state.quiz_state.get(level_id, {})
            current.update({"answers": user_answers, "submitted": True, "score": new_score, "indices": current.get("indices", [])})
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
# CERTIFICATE
# ============================================================
def render_certificate():
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:JetBrains Mono,monospace;font-size:1rem;color:var(--neon);margin-bottom:0.4rem;">🏅 Certificate of Completion</div>'
        '<p style="color:var(--muted);font-size:0.85rem;">All 5 missions complete! Enter your name to download your certificate.</p>',
        unsafe_allow_html=True)
    name_input = st.text_input("Your Name for the Certificate", value=st.session_state.cert_name, placeholder="Enter your full name…")
    if name_input != st.session_state.cert_name:
        st.session_state.cert_name = name_input
        save_user_progress(st.session_state.username)

    if name_input.strip():
        title, icon = get_character_info(st.session_state.xp)
        done     = len(st.session_state.completed_levels)
        xp       = st.session_state.xp
        max_xp   = sum(v["xp_reward"] for v in LEVELS.values())
        bosses   = len(st.session_state.get("boss_beaten", set()))
        streak   = st.session_state.get("streak", 0)
        date_str = datetime.now().strftime("%B %d, %Y")
        cert_html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<title>Python Coding Adventure — Certificate</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@700;800&display=swap');
body{{margin:0;padding:2rem;background:#0A0A0A;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:'Syne',sans-serif;color:#E8E8E8;}}
.cert{{width:760px;border:4px solid #00FF41;border-radius:16px;padding:3rem;background:#111;box-shadow:0 0 60px rgba(0,255,65,0.3),10px 10px 0 #000;text-align:center;position:relative;}}
.cert::before{{content:'';position:absolute;inset:12px;border:1px dashed rgba(0,255,65,0.2);border-radius:10px;pointer-events:none;}}
.logo{{font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#00FF41;letter-spacing:0.3em;margin-bottom:0.5rem;}}
.title{{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#00FF41;text-shadow:0 0 20px rgba(0,255,65,0.5);margin:0.5rem 0;}}
.sub{{color:#888;font-size:0.9rem;margin-bottom:2rem;}}
hr{{border:none;border-top:1px solid #2A2A2A;margin:1.5rem 0;}}
.label{{font-size:0.75rem;color:#666;text-transform:uppercase;letter-spacing:0.15em;font-family:'JetBrains Mono',monospace;}}
.hero{{font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;color:#fff;margin:0.3rem 0 1.5rem;}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:1.5rem 0;}}
.stat{{background:#1A1A1A;border:1px solid #2A2A2A;border-radius:8px;padding:1rem;}}
.stat .v{{font-family:'JetBrains Mono',monospace;font-size:1.2rem;color:#00FF41;}}
.stat .l{{font-size:0.7rem;color:#666;margin-top:0.2rem;font-family:'JetBrains Mono',monospace;}}
.badge{{display:inline-block;background:#6200EE;border:2px solid #000;border-radius:6px;padding:0.4rem 1.2rem;font-family:'JetBrains Mono',monospace;font-size:0.8rem;color:#fff;box-shadow:3px 3px 0 #000;margin:0.3rem;}}
.footer{{margin-top:2rem;font-size:0.68rem;color:#555;font-family:'JetBrains Mono',monospace;}}
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
    <div class="stat"><div class="v">{done}/5</div><div class="l">Missions Done</div></div>
    <div class="stat"><div class="v">💀 {bosses}/5</div><div class="l">Bosses Slain</div></div>
    <div class="stat"><div class="v">🔥 {streak}</div><div class="l">Day Streak</div></div>
  </div>
  <hr/>
  <span class="badge">✅ Python Basics Mastered</span>
  <span class="badge">🎯 60% Pass Standard</span>
  <div class="footer">Issued on {date_str} &nbsp;|&nbsp; Python Coding Adventure &nbsp;|&nbsp; Powered by Streamlit</div>
</div></body></html>"""
        b64   = base64.b64encode(cert_html.encode()).decode()
        fname = f"python_cert_{name_input.strip().replace(' ','_')}.html"
        st.markdown(
            f'<a href="data:text/html;base64,{b64}" download="{fname}" style="text-decoration:none;">'
            f'<div style="display:inline-block;background:var(--neon);color:#000;'
            f'font-family:JetBrains Mono,monospace;font-weight:700;border:2px solid #000;'
            f'border-radius:8px;box-shadow:var(--btn-glow);padding:0.65rem 1.4rem;cursor:pointer;margin-top:0.5rem;">'
            f'📥 Download Certificate</div></a>',
            unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:var(--muted);font-size:0.82rem;font-style:italic;">↑ Enter your name to unlock the download.</div>',
                    unsafe_allow_html=True)


# ============================================================
# MAIN
# ============================================================
def main():
    init_state()
    apply_styles()

    if not st.session_state.logged_in:
        render_auth()
        return

    load_sidebar()
    render_topbar()

    if st.session_state.view == "hub":
        load_main_grid()
    elif st.session_state.view == "level":
        render_level(st.session_state.current_level)
    elif st.session_state.view == "leaderboard":
        render_leaderboard()


if __name__ == "__main__":
    main()

