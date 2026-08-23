from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "todo.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db_connection()

    todos = conn.execute(
        "SELECT * FROM todos ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        todos=todos
    )


@app.route("/add", methods=["POST"])
def add_todo():

    title = request.form["title"]

    if title.strip():

        conn = get_db_connection()

        conn.execute(
            "INSERT INTO todos (title) VALUES (?)",
            (title,)
        )

        conn.commit()
        conn.close()

    return redirect("/")


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM todos WHERE id = ?",
        (todo_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)