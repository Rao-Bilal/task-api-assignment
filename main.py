import sqlite3
from pathlib import Path

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()

DB_PATH = Path(__file__).parent / "tasks.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )
    cur.execute("SELECT COUNT(*) FROM tasks")
    count = cur.fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Set up server", True),
                ("Build CRUD endpoints", False),
                ("Review Swagger UI", False),
            ],
        )
    conn.commit()
    conn.close()


init_db()


def row_to_task(row):
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


tasks = [
    {"id": 1, "title": "Set up server", "done": True},
    {"id": 2, "title": "Build CRUD endpoints", "done": False},
    {"id": 3, "title": "Review Swagger UI", "done": False}
]


@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [row_to_task(row) for row in rows]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    return row_to_task(row)


@app.post("/tasks", status_code=201)
def create_task(task_data: dict):
    title = task_data.get("title")
    if not title or not str(title).strip():
        return JSONResponse(status_code=400, content={"error": "Title is required and cannot be empty"})

    conn = get_connection()
    cur = conn.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, False))
    new_id = cur.lastrowid
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return row_to_task(row)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: dict):
    if not task_data:
        return JSONResponse(status_code=400, content={"error": "Request body cannot be empty"})
    for task in tasks:
        if task["id"] == task_id:
            if "title" in task_data:
                new_title = task_data["title"]
                if not new_title or not str(new_title).strip():
                    return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
                task["title"] = new_title
            if "done" in task_data:
                task["done"] = bool(task_data["done"])
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return Response(status_code=204)
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
