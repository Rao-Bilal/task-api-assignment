from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

tasks = [
    {"id": 1, "title": "Set up server", "done": True},
    {"id": 2, "title": "Build CRUD endpoints", "done": False},
    {"id": 3, "title": "Review Swagger UI", "done": False}
]

@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )

@app.post("/tasks", status_code=201)
def create_task(task_data: dict):
    title = task_data.get("title")
    if not title or not str(title).strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    next_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    new_task = {
        "id": next_id,
        "title": title,
        "done": False
    }

    tasks.append(new_task)
    return new_task