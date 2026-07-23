from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

import repository

app = FastAPI()


@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return repository.get_all_tasks()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = repository.get_task_by_id(task_id)
    if task is None:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    return task


@app.post("/tasks", status_code=201)
def create_task(task_data: dict):
    title = task_data.get("title")
    if not title or not str(title).strip():
        return JSONResponse(status_code=400, content={"error": "Title is required and cannot be empty"})
    return repository.create_task(title)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: dict):
    if not task_data:
        return JSONResponse(status_code=400, content={"error": "Request body cannot be empty"})

    title = task_data.get("title")
    if "title" in task_data and (not title or not str(title).strip()):
        return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})

    done = task_data.get("done") if "done" in task_data else None

    updated = repository.update_task(task_id, title=title, done=done)
    if updated is None:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    return updated


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    deleted = repository.delete_task(task_id)
    if not deleted:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    return Response(status_code=204)
