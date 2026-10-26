from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# Add title, description, and version for Swagger UI
app = FastAPI(
    title="FlyRank Task API",
    description="A robust backend CRUD API built with FastAPI for task management.",
    version="1.0.0"
)

tasks = [
    {"id": 1, "title": "Learn FastAPI basics", "done": True},
    {"id": 2, "title": "Build a CRUD API", "done": False},
    {"id": 3, "title": "Test with Swagger UI", "done": False}
]


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.get("/", summary="Root Endpoint")
def read_root():
    """Returns basic API metadata and available endpoints."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", summary="Health Check")
def health_check():
    """Verifies that the server is up and running."""
    return {"status": "ok"}


@app.get("/tasks", summary="List All Tasks")
def get_tasks():
    """Retrieve the full list of tasks."""
    return tasks


@app.get("/tasks/{id}", summary="Get a Single Task")
def get_task(id: int):
    """Retrieve a specific task by its unique ID. Returns 404 if not found."""
    task = next((t for t in tasks if t["id"] == id), None)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Task {id} not found"}
        )
    return task


@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a Task")
def create_task(task_data: TaskCreate):
    """Create a new task with a given title. Validates that the title is not empty."""
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Title is missing or empty"}
        )

    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {
        "id": new_id,
        "title": task_data.title.strip(),
        "done": False
    }
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{id}", summary="Update a Task")
def update_task(id: int, task_data: TaskUpdate):
    """Update an existing task's title or completion status by ID."""
    task = next((t for t in tasks if t["id"] == id), None)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Task {id} not found"}
        )

    if task_data.title is not None:
        if not task_data.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Title cannot be empty"}
            )
        task["title"] = task_data.title.strip()

    if task_data.done is not None:
        task["done"] = task_data.done

    return task


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Task")
def delete_task(id: int):
    """Delete a task by its ID."""
    global tasks
    task = next((t for t in tasks if t["id"] == id), None)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Task {id} not found"}
        )

    tasks = [t for t in tasks if t["id"] != id]
    return None