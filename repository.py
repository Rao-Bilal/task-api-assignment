import os
from pathlib import Path
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def row_to_task(row):
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


def get_all_tasks():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM tasks ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [row_to_task(row) for row in rows]


def get_task_by_id(task_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row_to_task(row) if row else None


def create_task(title):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *",
        (title, False),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row_to_task(row)


def update_task(task_id, title=None, done=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    existing = cur.fetchone()
    if existing is None:
        cur.close()
        conn.close()
        return None

    new_title = title if title is not None else existing["title"]
    new_done = done if done is not None else existing["done"]

    cur.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *",
        (new_title, new_done, task_id),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row_to_task(row)


def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM tasks WHERE id = %s", (task_id,))
    existing = cur.fetchone()
    if existing is None:
        cur.close()
        conn.close()
        return False

    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True
