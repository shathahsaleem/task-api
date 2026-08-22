# Task Management CRUD API

A lightweight, high-performance API for managing a to-do list, built with **FastAPI** and **Pydantic**. 

---

## What This Is

This project is a database-backed task management backend service created as part of the FlyRank Backend Internship (Week 2). It simulates a complete backend service for managing to-do items—allowing clients to create new tasks, view existing tasks, update task details, and delete tasks. 

The primary goals of this project are to:
- Practice handling standard HTTP methods (`GET`, `POST`, `PUT`, `DELETE`).
- Implement proper input validation to ensure empty or malformed data is rejected.
- Enforce standard HTTP status codes (`200`, `201`, `204`, `400`, `404`) to give clear feedback to clients[cite: 2].
- Provide self-documenting interactive API testing via Swagger UI.

---

## Database Architecture & Storage

### Why PostgreSQL & Docker?
* **Production-Grade Persistence:** Moves away from local file storage to a fully relational, scalable database system.
* **Isolated Environment:** PostgreSQL runs inside a dedicated Docker container, ensuring identical database environments across development and production.
* **Security First:** Database credentials (`DATABASE_URL`) are managed via environment variables and loaded through a `.env` file, keeping secrets completely isolated from source control.

### Version Control & Secrets
* **Git Ignored File:** `.env` is explicitly included in `.gitignore` to prevent sensitive database passwords and host parameters from leaking into Git history.
* **Container Volume:** Persistent database storage is handled via Docker volumes (`taskdata`), keeping data intact across container restarts.

---

## How to Install & Run

### 1. Installation
Clone the repository, set up a virtual environment, and install dependencies:

```bash
# Clone the repository
git clone [https://github.com/shathahsaleem/task-api.git](https://github.com/shathahsaleem/task-api.git)
cd task-api

# Create and activate a virtual environment
python -m venv venv

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install required dependencies
pip install fastapi uvicorn pydantic
```
### 2. Activation

1. Start the PostgreSQL container:
```bash
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres:16
```

Run the server by starting the Uvicorn development server:
```bash
uvicorn main:app --reload
```
The API will be running live at http://localhost:8000. You can access the interactive Swagger UI documentation directly at http://localhost:8000/docs.

## API Endpoints Overview

| Method | Endpoint | Description | Request Body | Success Status | Error Statuses |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | API metadata and available endpoints | None | `200 OK` | N/A |
| `GET` | `/health` | Health check endpoint | None | `200 OK` | N/A |
| `GET` | `/tasks` | Retrieve all tasks from SQLite database | None | `200 OK` | N/A |
| `GET` | `/tasks/{task_id}` | Retrieve a single task by ID from SQLite database | None | `200 OK` | `404 Not Found` |
| `POST` | `/tasks` | Create a new task in SQLite database | `{"title": "Buy milk"}` | `201 Created` | `400 Bad Request`, `422 Unprocessable` |
| `PUT` | `/tasks/{task_id}` | Update task title and/or completed status in SQLite database| `{"title": "Updated", "done": true}` | `200 OK` | `400 Bad Request`, `404 Not Found` |
| `DELETE` | `/tasks/{task_id}` | Delete a task by ID from SQLite database | None | `204 No Content` | `404 Not Found` |


## Example SQL Query ##

Below is the documented sequence of a task deletion operation executed on the SQLite database:

### 1. Database State Before Deletion
*Initial state showing task ID 5 in the table:*

![Database before DELETE Query](db_before_delete.png)

---

### 2. Execution of Delete Operation
*Running the SQL query to delete task ID 5:*

![DELETE Query Result](delete_query.png)

Executing the delete query and receiving confirmation:
```text
Execution finished without errors.
Result: query executed successfully. Took 2ms, 1 rows affected
At line 1:
DELETE FROM tasks WHERE id = 5
```

---

### 3. Database State After Deletion
*Confirmation that task ID 5 was removed from the database:*

![Database Post-Deletion of a row](db_after_delete.png)


## Sample `curl -i` Execution Output

Below is the raw HTTP response output from creating a new task using `curl -i`:
```text
HTTP/1.1 201 Created
date: Sun, 09 Aug 2026 14:31:23 GMT
server: uvicorn
content-length: 57
content-type: application/json

{"id":4,"title":"Prepare team presentation","done":false}
```

## Interactive Documentation (Swagger UI)

FastAPI automatically generates interactive documentation accessible directly in your browser at:
**`http://localhost:8000/docs`**

---

### Case 1: Read All Tasks (`GET /tasks`)
Retrieves the initial list of pre-filled tasks from memory with a `200 OK` status.

![Swagger UI - GET Tasks](swagger-get-tasks.png)

---

### Case 2: Create Task (`POST /tasks`)
Sends a JSON request body `{"title": "Buy mango juice"}` to create a new task, returning a `201 Created` status and assigning a unique ID.

![Swagger UI - POST Task](swagger-post-task.png)

---

### Case 3: Delete Task (`DELETE /tasks/{task_id}`)
Deletes task #4 by ID, returning a `204 No Content` status confirming successful removal.

![Swagger UI - DELETE Task](swagger-delete-task.png)