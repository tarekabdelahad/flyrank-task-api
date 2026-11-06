from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import  BaseModel
import sqlite3
from pathlib import Path

# Add title, description, and version for Swagger UI
app = FastAPI(
    title="FlyRank Task API",
    description="A robust backend CRUD API built with FastAPI for task management.",
    version="1.0.0"
)
# SQLite database configuration
DATABASE_PATH = Path(__file__).parent / "tasks.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection
def task_to_dict(row):
    task = dict(row)
    task["done"] = bool(task["done"])
    return task

def initialize_database():
    with get_connection() as connection:

        # Create the tasks table if it doesn't exist
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL
            )
        """)

        # Insert example tasks only if the table is empty
        task_count = connection.execute(
            "SELECT COUNT(*) FROM tasks"
        ).fetchone()[0]

        if task_count == 0:
            connection.executemany(
                "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
                [
                    (1, "Learn FastAPI basics", 1),
                    (2, "Build a CRUD API", 0),
                    (3, "Test with Swagger UI", 0)
                ]
            )

# Initialize database when the application starts
initialize_database()

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


@app.get("/tasks")
def get_tasks():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM tasks"
        ).fetchall()

        return [task_to_dict(row) for row in rows]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail={"error": f"Task {task_id} not found"}
            )

        return task_to_dict(row)


@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a Task")
def create_task(task_data: TaskCreate):
    """Create a new task with a given title."""

    if not task_data.title or not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Title is missing or empty"}
        )

    title = task_data.title.strip()

    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            (title, 0)
        )

        new_id = cursor.lastrowid

        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (new_id,)
        ).fetchone()

        return task_to_dict(row)


@app.put("/tasks/{id}", summary="Update a Task")
def update_task(id: int, task_data: TaskUpdate):
    """Update an existing task's title or completion status by ID."""

    with get_connection() as connection:

        # Check whether the task exists
        task = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (id,)
        ).fetchone()

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Task {id} not found"}
            )

        # Validate the title if provided
        if task_data.title is not None:
            if not task_data.title.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": "Title cannot be empty"}
                )

        # Update only the fields provided by the user
        new_title = (
            task_data.title.strip()
            if task_data.title is not None
            else task["title"]
        )

        new_done = (
            task_data.done
            if task_data.done is not None
            else task["done"]
        )

        connection.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (new_title, new_done, id)
        )

        # Retrieve the updated task
        updated_task = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (id,)
        ).fetchone()

        return dict(updated_task)


@app.delete("/tasks/{id}", summary="Delete a Task")
def delete_task(id: int):
    with get_connection() as connection:

        task = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (id,)
        ).fetchone()

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Task {id} not found"}
            )

        connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (id,)
        )

        return {"message": f"Task {id} deleted successfully"}