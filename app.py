from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a strong secret key for production

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute("SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC", (user_id,))
    expenses = c.fetchall()

    c.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
    total = c.fetchone()[0]

    conn.close()

    if total is None:
        total = 0

    return render_template("home.html", expenses=expenses, total=total)

@app.route("/add", methods=["POST"])
def add_expense():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    amount = request.form["amount"]
    category = request.form["category"]
    description = request.form["description"]
    date = request.form["date"]

    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
              (user_id, amount, category, description, date))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete_expense(id):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (id, user_id))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        conn = sqlite3.connect("expenses.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if user:
            error = "Username already exists. Try another."
        else:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect("/login")

        conn.close()
    return render_template("register.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("expenses.db")
        c = conn.cursor()
        c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return redirect("/")
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
