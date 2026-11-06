# FlyRank Task API — BE-02: Connecting to the Database

## Overview
A RESTful task management API built with FastAPI and SQLite. This project extends the previous CRUD API by replacing in-memory storage with persistent database storage.

## Technologies
- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn

## Database Implementation
SQLite was selected because it is lightweight, serverless, and does not require a separate database server.

The database file (`tasks.db`) is automatically created in the project root directory when the application starts.

The `tasks` table contains:
- `id`: Integer primary key
- `title`: Text, required
- `done`: Boolean, required

The database is initialized automatically, and three sample tasks are inserted when the table is empty.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task |

## Installation and Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install fastapi uvicorn
```

4. Start the application:

```bash
uvicorn main:app --reload
```

5. Open Swagger UI:

`http://127.0.0.1:8000/docs`

## Database Verification

To inspect the database using Python:

```python
import sqlite3

connection = sqlite3.connect("tasks.db")
results = connection.execute("SELECT * FROM tasks").fetchall()
print(results)
connection.close()
```

## Testing
The following operations were tested successfully:
- Creating a task and verifying its database insertion.
- Retrieving all tasks.
- Restarting the server and confirming data persistence.
- Updating an existing task.
- Deleting a task and confirming its removal from SQLite.

## Project Structure

```text
PythonProject3/
├── main.py
├── tasks.db
├── README.md
└── requirements.txt
```