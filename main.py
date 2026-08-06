from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

tasks_db=[
    {'id': 1, 'title': 'Setup development environment', 'done': True},
    {'id': 2, 'title': 'Build FastAPI CRUD endpoints', 'done': False},
    {'id': 3, 'title': 'Write API documentation', 'done': False}
]

# Stage 1 endpoints
@app.get('/')
def root():
    return {'name': 'Task API', 'version' : '1.0' , 'endpoints' : ['/tasks'] }

@app.get('/health')
def healthcheck():
    return {'status' : 'ok'}

# Stage 2 endpoints
@app.get('/tasks')
def get_tasks():
    return tasks_db

@app.get('/tasks/{task_id}')
def get_task(task_id:int):
    for task in tasks_db:
        if task['id'] == task_id:
            return task
    return JSONResponse(status_code=404, content={'error': f'Task {task_id} not found'})