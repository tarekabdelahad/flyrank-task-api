# FlyRank Task API — Dockerized SQLite

A RESTful Task Management API built with FastAPI and SQLite, containerized using Docker and Docker Compose.

## Technologies
- Python 3.11
- FastAPI
- SQLite
- Docker
- Docker Compose
- Uvicorn

## Features
- Create, retrieve, update, and delete tasks.
- Automatic API documentation using Swagger UI.
- SQLite database persistence.
- Dockerized application environment.
- Docker Compose for simplified startup.

## Project Structure

```text
PythonProject3/
├── main.py
├── tasks.db
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

## Run the Application

Make sure Docker Desktop is running.

Build and start the application:

```bash
docker compose up --build
```

Open Swagger UI:

http://localhost:8000/docs

Stop the application using:

```bash
docker compose down
```

## Database Persistence

The application uses SQLite with a Docker bind mount:

```yaml
volumes:
  - ./tasks.db:/app/tasks.db
```

This mounts the local database file into the container, allowing database changes to persist when the container is stopped and restarted.

### Persistence Verification

1. Created a new task using the POST endpoint.
2. Stopped the Docker container.
3. Started the application again using `docker compose up -d`.
4. Retrieved all tasks using GET `/tasks`.
5. Confirmed that the previously created task was still present.

## Important Note

This implementation uses SQLite with Docker. It demonstrates application containerization and persistent database storage, but does not implement the PostgreSQL requirement of the original BE-04 assignment.