from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()

# Your in-memory "database"
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


# --- STAGE 4 ENDPOINTS ---

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: dict):
    if not task_data:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    # Find the task
    for task in tasks:
        if task["id"] == task_id:
            # Update title if provided
            if "title" in task_data:
                title = task_data["title"]
                if not title or not str(title).strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title cannot be empty"}
                    )
                task["title"] = title

            # Update done status if provided
            if "done" in task_data:
                task["done"] = bool(task_data["done"])

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)  # Remove the task from the list
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )
