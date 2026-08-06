from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

tasks_db=[
    {
        'id': 1, 
    'title': 'Setup development environment', 
    'done': True
    },
    {
        'id': 2, 
        'title': 'Build FastAPI CRUD endpoints', 
        'done': False
    },
    {
        'id': 3, 
        'title': 'Write API documentation', 
        'done': False
    }
]

class TaskCreate(BaseModel):
    title: str

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

# Stage 3 endpoints
@app.post('/tasks', status_code=201)
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        return JSONResponse(status_code=400, content={'error': 'Task title cannot be empty'})

    new_id = max(t['id'] for t in tasks_db) + 1 if tasks_db else 1
        
    new_task = {
            'id': new_id,
            'title': task.title.strip(),
            'done': False
            }

    tasks_db.append(new_task)
    return new_task
