import sqlite3
import os

DB_PATH = os.environ.get('DB_PATH', 'quiz.db')
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Questions table – 4 options + category + difficulty
c.execute('''CREATE TABLE IF NOT EXISTS questions (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    question   TEXT NOT NULL,
    opt1       TEXT NOT NULL,
    opt2       TEXT NOT NULL,
    opt3       TEXT NOT NULL,
    opt4       TEXT NOT NULL,
    answer     TEXT NOT NULL,
    category   TEXT NOT NULL DEFAULT 'General',
    difficulty TEXT NOT NULL DEFAULT 'Medium'
)''')

# Scores / Leaderboard table
c.execute('''CREATE TABLE IF NOT EXISTS scores (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    score       INTEGER NOT NULL,
    total       INTEGER NOT NULL,
    percentage  INTEGER NOT NULL,
    category    TEXT NOT NULL,
    difficulty  TEXT NOT NULL,
    time_secs   INTEGER NOT NULL,
    played_at   TEXT NOT NULL
)''')

questions = [
    # ── Geography ──────────────────────────────────────────────
    ("What is the capital of India?",       "Mumbai","Delhi","Chennai","Kolkata",  "Delhi",         "Geography","Easy"),
    ("What is the capital of France?",      "Berlin","Rome","Madrid","Paris",      "Paris",         "Geography","Easy"),
    ("Which is the longest river in the world?","Amazon","Nile","Yangtze","Mississippi","Nile",     "Geography","Medium"),
    ("Which country has the most natural lakes?","Russia","Canada","USA","Brazil", "Canada",        "Geography","Medium"),
    ("What is the smallest country in the world?","Monaco","San Marino","Vatican City","Liechtenstein","Vatican City","Geography","Hard"),
    ("Which continent has the most countries?","Asia","Africa","Europe","Americas","Africa",        "Geography","Medium"),
    ("What is the highest mountain on Earth?","K2","Kangchenjunga","Mount Everest","Lhotse","Mount Everest","Geography","Easy"),
    ("The Amazon rainforest is primarily in which country?","Colombia","Peru","Ecuador","Brazil","Brazil","Geography","Easy"),

    # ── Science ───────────────────────────────────────────────
    ("What is the chemical symbol for Gold?","Au","Ag","Gd","Go",              "Au",              "Science","Easy"),
    ("What planet is known as the Red Planet?","Jupiter","Mars","Saturn","Venus","Mars",           "Science","Easy"),
    ("What is the speed of light in vacuum (approx)?","300,000 km/s","150,000 km/s","3,000 km/s","30,000 km/s","300,000 km/s","Science","Medium"),
    ("What gas do plants absorb from the atmosphere?","Oxygen","Nitrogen","Carbon Dioxide","Hydrogen","Carbon Dioxide","Science","Easy"),
    ("How many bones are in the adult human body?","196","206","216","226",     "206",             "Science","Medium"),
    ("What is the powerhouse of the cell?","Nucleus","Ribosome","Mitochondria","Chloroplast","Mitochondria","Science","Easy"),
    ("What is the atomic number of Carbon?","4","6","8","12",                  "6",               "Science","Medium"),
    ("Which planet has the most moons?","Jupiter","Saturn","Uranus","Neptune",  "Saturn",          "Science","Hard"),

    # ── Mathematics ───────────────────────────────────────────
    ("What is 2 + 2?",                      "3","4","5","6",                    "4",               "Mathematics","Easy"),
    ("What is 15% of 200?",                 "25","30","35","40",                "30",              "Mathematics","Easy"),
    ("What is the square root of 144?",     "11","12","13","14",                "12",              "Mathematics","Medium"),
    ("What is 7 × 8?",                      "54","56","58","64",                "56",              "Mathematics","Easy"),
    ("What is the value of Pi (approx.)?",  "3.14","3.16","3.12","3.18",       "3.14",            "Mathematics","Easy"),
    ("How many sides does a dodecagon have?","10","11","12","13",               "12",              "Mathematics","Medium"),
    ("What is 2^10?",                       "512","1024","256","2048",          "1024",            "Mathematics","Medium"),
    ("What is the sum of angles in a triangle?","90°","180°","270°","360°",    "180°",            "Mathematics","Easy"),

    # ── History ───────────────────────────────────────────────
    ("In which year did World War II end?", "1943","1944","1945","1946",        "1945",            "History","Easy"),
    ("Who was the first President of the United States?","John Adams","Thomas Jefferson","George Washington","Benjamin Franklin","George Washington","History","Easy"),
    ("The Renaissance began in which country?","France","England","Germany","Italy","Italy",       "History","Medium"),
    ("In which year did the Berlin Wall fall?","1987","1988","1989","1990",     "1989",            "History","Medium"),
    ("Who wrote the Magna Carta?","King John","King Henry II","King Richard I","King Edward I","King John","History","Hard"),
    ("Which empire was ruled by Genghis Khan?","Ottoman","Mongol","Roman","Persian","Mongol",      "History","Medium"),

    # ── Technology ────────────────────────────────────────────
    ("Who co-founded Apple Inc.?",          "Bill Gates","Elon Musk","Steve Jobs","Mark Zuckerberg","Steve Jobs","Technology","Easy"),
    ("What does 'HTTP' stand for?",         "HyperText Transfer Protocol","High Transfer Text Protocol","Hyper Transfer Technology Protocol","HyperText Technology Protocol","HyperText Transfer Protocol","Technology","Medium"),
    ("Which programming language is known as the language of the web?","Python","Java","JavaScript","C++","JavaScript","Technology","Easy"),
    ("What does 'CPU' stand for?",          "Central Processing Unit","Computer Processing Unit","Core Processing Unit","Central Program Unit","Central Processing Unit","Technology","Easy"),
    ("Which company developed the Android OS?","Apple","Microsoft","Google","Samsung","Google",    "Technology","Easy"),
    ("What is the binary representation of the decimal number 10?","1010","1001","1100","1110",    "1010",            "Technology","Medium"),
]

# Only insert if table is empty
existing = c.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
if existing == 0:
    c.executemany(
        "INSERT INTO questions (question,opt1,opt2,opt3,opt4,answer,category,difficulty) VALUES (?,?,?,?,?,?,?,?)",
        questions
    )
    print(f"Inserted {len(questions)} questions.")
else:
    print(f"Database already has {existing} questions – skipping seed.")

conn.commit()
conn.close()
print("Database initialised successfully.")
