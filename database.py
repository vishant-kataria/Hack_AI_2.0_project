"""
database.py — Dual-Mode Database for CareerForge
=================================================
Uses PostgreSQL (Neon) when DATABASE_URL is available (Streamlit Cloud).
Falls back to local SQLite for offline/local development.
"""

import json
import datetime
import hashlib
import os

# -----------------------------------------------------------------
# DETECT DATABASE MODE
# -----------------------------------------------------------------
USE_POSTGRES = False
try:
    import streamlit as st
    if "DATABASE_URL" in st.secrets:
        import psycopg2
        import psycopg2.extras
        # Quick connectivity test
        try:
            _test_conn = psycopg2.connect(st.secrets["DATABASE_URL"], connect_timeout=5)
            _test_conn.close()
            USE_POSTGRES = True
        except Exception:
            USE_POSTGRES = False
except Exception:
    pass

if not USE_POSTGRES:
    import sqlite3


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "careerforge.db")


# -----------------------------------------------------------------
# CONNECTION
# -----------------------------------------------------------------
def get_connection():
    if USE_POSTGRES:
        conn = psycopg2.connect(st.secrets["DATABASE_URL"])
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn


def _run(query, params=None, fetch=False, fetch_one=False):
    # Convert placeholder style for SQLite
    if not USE_POSTGRES:
        query = query.replace("%s", "?")

    conn = get_connection()
    try:
        if USE_POSTGRES:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            cur = conn.cursor()
        cur.execute(query, params or ())
        if fetch_one:
            result = cur.fetchone()
            result = dict(result) if result else None
        elif fetch:
            rows = cur.fetchall()
            result = [dict(r) for r in rows] if rows else []
        else:
            result = None
        conn.commit()
        return result
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# -----------------------------------------------------------------
# INIT — creates tables if they don't exist
# -----------------------------------------------------------------
def init_db():
    conn = get_connection()
    try:
        if USE_POSTGRES:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL DEFAULT '',
                    full_name TEXT,
                    email TEXT UNIQUE,
                    skills TEXT DEFAULT '[]',
                    goal TEXT DEFAULT 'SDE',
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    role TEXT NOT NULL CHECK(role IN ('user', 'ai')),
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS resume_results (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    filename TEXT,
                    skills_found TEXT DEFAULT '[]',
                    strengths TEXT DEFAULT '[]',
                    weaknesses TEXT DEFAULT '[]',
                    score INTEGER DEFAULT 0,
                    suggestions TEXT DEFAULT '',
                    analyzed_at TIMESTAMP DEFAULT NOW()
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS interview_scores (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    question TEXT,
                    answer TEXT,
                    correctness INTEGER DEFAULT 0,
                    clarity INTEGER DEFAULT 0,
                    depth INTEGER DEFAULT 0,
                    feedback TEXT DEFAULT '',
                    interviewed_at TIMESTAMP DEFAULT NOW()
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS learning_progress (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    day INTEGER NOT NULL,
                    task_name TEXT NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    completed_at TIMESTAMP,
                    UNIQUE(user_id, day, task_name)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS placement_scores (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    score INTEGER DEFAULT 0,
                    dsa_score INTEGER DEFAULT 0,
                    aptitude_score INTEGER DEFAULT 0,
                    interview_score INTEGER DEFAULT 0,
                    recorded_at TIMESTAMP DEFAULT NOW()
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS daily_activity (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    activity_date DATE NOT NULL,
                    tasks_completed INTEGER DEFAULT 0,
                    tasks_total INTEGER DEFAULT 0,
                    UNIQUE(user_id, activity_date)
                );
            """)
        else:
            # SQLite mode
            cur = conn.cursor()
            cur.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL DEFAULT '',
                    full_name TEXT,
                    email TEXT UNIQUE,
                    skills TEXT DEFAULT '[]',
                    goal TEXT DEFAULT 'SDE',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    role TEXT NOT NULL CHECK(role IN ('user', 'ai')),
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS resume_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    filename TEXT,
                    skills_found TEXT DEFAULT '[]',
                    strengths TEXT DEFAULT '[]',
                    weaknesses TEXT DEFAULT '[]',
                    score INTEGER DEFAULT 0,
                    suggestions TEXT DEFAULT '',
                    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS interview_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    question TEXT,
                    answer TEXT,
                    correctness INTEGER DEFAULT 0,
                    clarity INTEGER DEFAULT 0,
                    depth INTEGER DEFAULT 0,
                    feedback TEXT DEFAULT '',
                    interviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS learning_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    day INTEGER NOT NULL,
                    task_name TEXT NOT NULL,
                    completed BOOLEAN DEFAULT 0,
                    completed_at TIMESTAMP,
                    UNIQUE(user_id, day, task_name)
                );
                CREATE TABLE IF NOT EXISTS placement_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    score INTEGER DEFAULT 0,
                    dsa_score INTEGER DEFAULT 0,
                    aptitude_score INTEGER DEFAULT 0,
                    interview_score INTEGER DEFAULT 0,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS daily_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    activity_date DATE NOT NULL,
                    tasks_completed INTEGER DEFAULT 0,
                    tasks_total INTEGER DEFAULT 0,
                    UNIQUE(user_id, activity_date)
                );
            """)
        conn.commit()
    finally:
        conn.close()


# =================================================================
# USER OPERATIONS
# =================================================================

def _hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def create_user(username, full_name="", email="", skills=None, goal="SDE", password=""):
    password_hash = _hash_password(password) if password else ""
    conn = get_connection()
    try:
        if USE_POSTGRES:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(
                "INSERT INTO users (username, password_hash, full_name, email, skills, goal) "
                "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                (username, password_hash, full_name, email or None, json.dumps(skills or []), goal)
            )
            row = cur.fetchone()
            conn.commit()
            return row["id"] if row else None
        else:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password_hash, full_name, email, skills, goal) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (username, password_hash, full_name, email or None, json.dumps(skills or []), goal)
            )
            conn.commit()
            return cur.lastrowid
    except Exception:
        conn.rollback()
        return None
    finally:
        conn.close()


def authenticate_user(username, password):
    row = _run("SELECT * FROM users WHERE username = %s", (username,), fetch_one=True)
    if row:
        user = dict(row)
        if user["password_hash"] == _hash_password(password):
            user["skills"] = json.loads(user["skills"])
            return user
    return None


def check_username_exists(username):
    row = _run("SELECT id FROM users WHERE username = %s", (username,), fetch_one=True)
    return row is not None


def check_email_exists(email):
    row = _run("SELECT id FROM users WHERE email = %s", (email,), fetch_one=True)
    return row is not None


def get_user(user_id):
    row = _run("SELECT * FROM users WHERE id = %s", (user_id,), fetch_one=True)
    if row:
        user = dict(row)
        user["skills"] = json.loads(user["skills"])
        return user
    return None


def get_user_by_username(username):
    row = _run("SELECT * FROM users WHERE username = %s", (username,), fetch_one=True)
    if row:
        user = dict(row)
        user["skills"] = json.loads(user["skills"])
        return user
    return None


def update_user_skills(user_id, skills):
    _run("UPDATE users SET skills = %s, updated_at = NOW() WHERE id = %s" if USE_POSTGRES
         else "UPDATE users SET skills = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
         (json.dumps(skills), user_id))


# =================================================================
# CHAT HISTORY
# =================================================================

def save_chat_message(user_id, role, content):
    _run("INSERT INTO chat_history (user_id, role, content) VALUES (%s, %s, %s)",
         (user_id, role, content))


def get_chat_history(user_id, limit=50):
    return _run(
        "SELECT role, content, created_at FROM chat_history "
        "WHERE user_id = %s ORDER BY created_at ASC LIMIT %s",
        (user_id, limit), fetch=True
    )


def clear_chat_history(user_id):
    _run("DELETE FROM chat_history WHERE user_id = %s", (user_id,))


# =================================================================
# RESUME RESULTS
# =================================================================

def save_resume_result(user_id, filename, skills_found, strengths, weaknesses, score, suggestions=""):
    conn = get_connection()
    try:
        if USE_POSTGRES:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(
                "INSERT INTO resume_results "
                "(user_id, filename, skills_found, strengths, weaknesses, score, suggestions) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (user_id, filename, json.dumps(skills_found), json.dumps(strengths),
                 json.dumps(weaknesses), score, suggestions)
            )
            row = cur.fetchone()
            conn.commit()
            return row["id"] if row else None
        else:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO resume_results "
                "(user_id, filename, skills_found, strengths, weaknesses, score, suggestions) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_id, filename, json.dumps(skills_found), json.dumps(strengths),
                 json.dumps(weaknesses), score, suggestions)
            )
            conn.commit()
            return cur.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_latest_resume_result(user_id):
    row = _run(
        "SELECT * FROM resume_results WHERE user_id = %s ORDER BY analyzed_at DESC LIMIT 1",
        (user_id,), fetch_one=True
    )
    if row:
        r = dict(row)
        r["skills_found"] = json.loads(r["skills_found"])
        r["strengths"] = json.loads(r["strengths"])
        r["weaknesses"] = json.loads(r["weaknesses"])
        return r
    return None


def get_all_resume_results(user_id):
    rows = _run(
        "SELECT * FROM resume_results WHERE user_id = %s ORDER BY analyzed_at DESC",
        (user_id,), fetch=True
    )
    results = []
    for row in rows:
        r = dict(row)
        r["skills_found"] = json.loads(r["skills_found"])
        r["strengths"] = json.loads(r["strengths"])
        r["weaknesses"] = json.loads(r["weaknesses"])
        results.append(r)
    return results


# =================================================================
# INTERVIEW SCORES
# =================================================================

def save_interview_score(user_id, question, answer, correctness, clarity, depth, feedback=""):
    conn = get_connection()
    try:
        if USE_POSTGRES:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(
                "INSERT INTO interview_scores "
                "(user_id, question, answer, correctness, clarity, depth, feedback) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (user_id, question, answer, correctness, clarity, depth, feedback)
            )
            row = cur.fetchone()
            conn.commit()
            return row["id"] if row else None
        else:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO interview_scores "
                "(user_id, question, answer, correctness, clarity, depth, feedback) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_id, question, answer, correctness, clarity, depth, feedback)
            )
            conn.commit()
            return cur.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_interview_history(user_id, limit=20):
    return _run(
        "SELECT * FROM interview_scores WHERE user_id = %s ORDER BY interviewed_at DESC LIMIT %s",
        (user_id, limit), fetch=True
    )


def get_avg_interview_scores(user_id):
    return _run(
        "SELECT AVG(correctness) as avg_correctness, AVG(clarity) as avg_clarity, "
        "AVG(depth) as avg_depth, COUNT(*) as total_interviews "
        "FROM interview_scores WHERE user_id = %s",
        (user_id,), fetch_one=True
    )


# =================================================================
# LEARNING PROGRESS
# =================================================================

def save_learning_progress(user_id, day, task_name, completed=False):
    completed_at = datetime.datetime.now().isoformat() if completed else None
    _run(
        "INSERT INTO learning_progress (user_id, day, task_name, completed, completed_at) "
        "VALUES (%s, %s, %s, %s, %s) "
        "ON CONFLICT(user_id, day, task_name) "
        "DO UPDATE SET completed = EXCLUDED.completed, completed_at = EXCLUDED.completed_at",
        (user_id, day, task_name, completed, completed_at)
    )


def get_learning_progress(user_id):
    return _run(
        "SELECT * FROM learning_progress WHERE user_id = %s ORDER BY day, task_name",
        (user_id,), fetch=True
    )


def get_learning_completion_rate(user_id):
    row = _run(
        "SELECT COUNT(*) as total, "
        "SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as done "
        "FROM learning_progress WHERE user_id = %s",
        (user_id,), fetch_one=True
    )
    if row and row["total"] > 0:
        return round((row["done"] / row["total"]) * 100, 1)
    return 0.0


# =================================================================
# PLACEMENT SCORES
# =================================================================

def save_placement_score(user_id, score, dsa_score=0, aptitude_score=0, interview_score=0):
    _run(
        "INSERT INTO placement_scores (user_id, score, dsa_score, aptitude_score, interview_score) "
        "VALUES (%s, %s, %s, %s, %s)",
        (user_id, score, dsa_score, aptitude_score, interview_score)
    )


def get_placement_history(user_id, days=30):
    if USE_POSTGRES:
        query = (
            "SELECT * FROM placement_scores "
            "WHERE user_id = %s AND recorded_at >= NOW() - INTERVAL '%s days' "
            "ORDER BY recorded_at ASC"
        )
    else:
        query = (
            "SELECT * FROM placement_scores "
            "WHERE user_id = %s AND recorded_at >= datetime('now', %s || ' days') "
            "ORDER BY recorded_at ASC"
        )
    return _run(query, (user_id, -days if not USE_POSTGRES else days), fetch=True)


def get_latest_placement_score(user_id):
    return _run(
        "SELECT * FROM placement_scores WHERE user_id = %s ORDER BY recorded_at DESC LIMIT 1",
        (user_id,), fetch_one=True
    )


# =================================================================
# DAILY ACTIVITY / STREAKS
# =================================================================

def log_daily_activity(user_id, tasks_completed, tasks_total):
    today = datetime.date.today().isoformat()
    _run(
        "INSERT INTO daily_activity (user_id, activity_date, tasks_completed, tasks_total) "
        "VALUES (%s, %s, %s, %s) "
        "ON CONFLICT(user_id, activity_date) "
        "DO UPDATE SET tasks_completed = EXCLUDED.tasks_completed, tasks_total = EXCLUDED.tasks_total",
        (user_id, today, tasks_completed, tasks_total)
    )


def get_streak(user_id):
    rows = _run(
        "SELECT activity_date FROM daily_activity "
        "WHERE user_id = %s AND tasks_completed > 0 ORDER BY activity_date DESC",
        (user_id,), fetch=True
    )
    if not rows:
        return 0
    streak = 0
    expected = datetime.date.today()
    for row in rows:
        activity_date = row["activity_date"]
        if isinstance(activity_date, str):
            activity_date = datetime.date.fromisoformat(activity_date)
        if activity_date == expected:
            streak += 1
            expected -= datetime.timedelta(days=1)
        elif activity_date < expected:
            break
    return streak


def get_weekly_stats(user_id, weeks=4):
    if USE_POSTGRES:
        query = (
            "SELECT EXTRACT(WEEK FROM activity_date)::int as week_num, "
            "SUM(tasks_completed) as completed, "
            "SUM(tasks_total - tasks_completed) as missed "
            "FROM daily_activity WHERE user_id = %s "
            "GROUP BY week_num ORDER BY week_num DESC LIMIT %s"
        )
    else:
        query = (
            "SELECT strftime('%%W', activity_date) as week_num, "
            "SUM(tasks_completed) as completed, "
            "SUM(tasks_total - tasks_completed) as missed "
            "FROM daily_activity WHERE user_id = %s "
            "GROUP BY week_num ORDER BY week_num DESC LIMIT %s"
        )
    rows = _run(query, (user_id, weeks), fetch=True)
    return list(reversed(rows)) if rows else []


# =================================================================
# DASHBOARD STATS
# =================================================================

def get_dashboard_stats(user_id):
    latest_placement = get_latest_placement_score(user_id)
    streak = get_streak(user_id)
    avg_interview = get_avg_interview_scores(user_id)
    learning_rate = get_learning_completion_rate(user_id)
    return {
        "placement_score": latest_placement["score"] if latest_placement else 0,
        "dsa_score": latest_placement["dsa_score"] if latest_placement else 0,
        "aptitude_score": latest_placement["aptitude_score"] if latest_placement else 0,
        "streak": streak,
        "total_interviews": avg_interview["total_interviews"] if avg_interview else 0,
        "avg_correctness": round(avg_interview["avg_correctness"] or 0) if avg_interview else 0,
        "learning_completion": learning_rate,
    }


# -----------------------------------------------------------------
# AUTO-INIT on import
# -----------------------------------------------------------------
init_db()
