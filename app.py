import os
import sqlite3
from datetime import datetime, timezone
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash, abort

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "training.db")
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-for-local-testing")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL,
                demo_code TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
init_db()
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        nickname = request.form.get("nickname", "").strip()
        demo_code = request.form.get("demo_code", "").strip()

        # This is deliberately a training code, NOT a password.
        if not nickname or len(nickname) > 40:
            flash("Ləqəb 1–40 simvol olmalıdır.")
            return redirect(url_for("home"))
        if not demo_code or len(demo_code) > 30:
            flash("Təlim kodunu daxil et (maksimum 30 simvol).")
            return redirect(url_for("home"))

        with db() as conn:
            conn.execute(
                "INSERT INTO entries (nickname, demo_code, created_at) VALUES (?, ?, ?)",
                (nickname, demo_code, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
            )
        return render_template("success.html", nickname=nickname)

    return render_template("home.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if not ADMIN_PASSWORD:
        return render_template("setup_admin.html")
    if request.method == "POST":
        supplied = request.form.get("password", "")
        if supplied == ADMIN_PASSWORD:
            session.clear()
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("İdarəçi şifrəsi yanlışdır.")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/admin")
@admin_required
def admin():
    with db() as conn:
        rows = conn.execute("SELECT id, nickname, demo_code, created_at FROM entries ORDER BY id DESC").fetchall()
    return render_template("admin.html", rows=rows)

@app.route("/admin/delete/<int:entry_id>", methods=["POST"])
@admin_required
def delete_entry(entry_id):
    with db() as conn:
        conn.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    return redirect(url_for("admin"))

if __name__ == "__main__":
    init_db()
    # Local-only by default. Do not expose this development server to the internet.
    app.run(host="127.0.0.1", port=8081, debug=False)
