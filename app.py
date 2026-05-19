from flask import Flask, render_template, request, redirect, session, jsonify, url_for
import sqlite3
import random
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'quiz-secret-2024-change-in-prod')

DB_PATH = os.environ.get('DB_PATH', 'quiz.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ── Home ──────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    db = get_db()
    categories = db.execute(
        "SELECT DISTINCT category FROM questions ORDER BY category"
    ).fetchall()
    db.close()
    return render_template('index.html', categories=[r['category'] for r in categories])

# ── Start quiz ─────────────────────────────────────────────────────────────────
@app.route('/start', methods=['POST'])
def start():
    player_name = request.form.get('player_name', '').strip()
    category    = request.form.get('category', 'All')
    difficulty  = request.form.get('difficulty', 'All')

    if not player_name:
        return redirect(url_for('home'))

    db = get_db()
    query  = "SELECT * FROM questions WHERE 1=1"
    params = []
    if category != 'All':
        query += " AND category = ?";  params.append(category)
    if difficulty != 'All':
        query += " AND difficulty = ?"; params.append(difficulty)
    questions = db.execute(query, params).fetchall()
    db.close()

    if not questions:
        return redirect(url_for('home'))

    # sample up to 10, randomise
    sample = random.sample(questions, min(10, len(questions)))
    session['player_name'] = player_name
    session['category']    = category
    session['difficulty']  = difficulty
    session['question_ids']= [q['id'] for q in sample]
    session['current_idx'] = 0
    session['score']       = 0
    session['start_time']  = datetime.utcnow().isoformat()
    session['answers']     = {}
    return redirect(url_for('quiz'))

# ── Quiz page ──────────────────────────────────────────────────────────────────
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'question_ids' not in session:
        return redirect(url_for('home'))

    ids = session['question_ids']
    idx = session['current_idx']

    if request.method == 'POST':
        qid    = request.form.get('qid')
        chosen = request.form.get('answer', '')

        db = get_db()
        q  = db.execute("SELECT * FROM questions WHERE id = ?", (qid,)).fetchone()
        db.close()

        answers = session.get('answers', {})
        answers[str(qid)] = {
            'chosen':  chosen,
            'correct': q['answer'],
            'question': q['question'],
            'is_correct': chosen == q['answer']
        }
        session['answers'] = answers

        if chosen == q['answer']:
            session['score'] = session.get('score', 0) + 1

        session['current_idx'] = idx + 1
        if session['current_idx'] >= len(ids):
            return redirect(url_for('result'))
        return redirect(url_for('quiz'))

    # GET – serve next question
    if idx >= len(ids):
        return redirect(url_for('result'))

    db = get_db()
    q  = db.execute("SELECT * FROM questions WHERE id = ?", (ids[idx],)).fetchone()
    db.close()

    opts = [q['opt1'], q['opt2'], q['opt3'], q['opt4']]
    random.shuffle(opts)

    return render_template('quiz.html',
        question   = q,
        options    = opts,
        current    = idx + 1,
        total      = len(ids),
        player     = session.get('player_name', 'Player'),
        time_limit = 20,          # seconds per question
    )

# ── Result page ────────────────────────────────────────────────────────────────
@app.route('/result')
def result():
    if 'score' not in session:
        return redirect(url_for('home'))

    score     = session.get('score', 0)
    total     = len(session.get('question_ids', []))
    player    = session.get('player_name', 'Player')
    category  = session.get('category', 'All')
    difficulty= session.get('difficulty', 'All')
    answers   = session.get('answers', {})

    # calc time taken
    try:
        start = datetime.fromisoformat(session['start_time'])
        secs  = int((datetime.utcnow() - start).total_seconds())
    except Exception:
        secs  = 0

    pct = round((score / total) * 100) if total else 0

    # save to leaderboard
    db = get_db()
    db.execute(
        "INSERT INTO scores (player_name, score, total, percentage, category, difficulty, time_secs, played_at) "
        "VALUES (?,?,?,?,?,?,?,?)",
        (player, score, total, pct, category, difficulty, secs, datetime.utcnow().isoformat())
    )
    db.commit()
    db.close()

    session.clear()
    return render_template('result.html',
        player    = player,
        score     = score,
        total     = total,
        pct       = pct,
        time_secs = secs,
        answers   = answers,
        category  = category,
    )

# ── Leaderboard ────────────────────────────────────────────────────────────────
@app.route('/leaderboard')
def leaderboard():
    category = request.args.get('category', 'All')
    db       = get_db()
    cats     = db.execute("SELECT DISTINCT category FROM questions ORDER BY category").fetchall()

    if category == 'All':
        rows = db.execute(
            "SELECT * FROM scores ORDER BY percentage DESC, time_secs ASC LIMIT 20"
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM scores WHERE category=? ORDER BY percentage DESC, time_secs ASC LIMIT 20",
            (category,)
        ).fetchall()
    db.close()

    return render_template('leaderboard.html',
        rows       = rows,
        categories = ['All'] + [r['category'] for r in cats],
        selected   = category,
    )

# ── API: timer expired → auto-submit blank ─────────────────────────────────────
@app.route('/timeout', methods=['POST'])
def timeout():
    if 'question_ids' not in session:
        return jsonify({'redirect': url_for('home')})
    ids = session['question_ids']
    idx = session.get('current_idx', 0)
    if idx < len(ids):
        qid = ids[idx]
        answers = session.get('answers', {})
        db = get_db()
        q  = db.execute("SELECT * FROM questions WHERE id = ?", (qid,)).fetchone()
        db.close()
        answers[str(qid)] = {
            'chosen': '',
            'correct': q['answer'],
            'question': q['question'],
            'is_correct': False
        }
        session['answers'] = answers
        session['current_idx'] = idx + 1
    if session['current_idx'] >= len(ids):
        return jsonify({'redirect': url_for('result')})
    return jsonify({'redirect': url_for('quiz')})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
