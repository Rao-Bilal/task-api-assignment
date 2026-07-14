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
    # Iterate through the list to find a matching ID
    for task in tasks:
        if task["id"] == task_id:
            return task

        # If the loop finishes without returning, the task doesn't exist
        return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )