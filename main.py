import sqlite3
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

app= FastAPI()

conn = sqlite3.connect('tasks.db', check_same_thread=False)
conn.row_factory = sqlite3.Row

def init_db():
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title text NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0
        )
        '''
    )
    conn.commit()

    cursor.execute('SELECT COUNT(*) FROM tasks')
    count = cursor.fetchone()[0]

    if count == 0:
        task = [
            ('Buy groceries', True),
            ('Clean the house', False),
            ('Cook dinner', False)
        ]
        cursor.executemany('INSERT INTO tasks (title, done) VALUES (?, ?)', task)
        conn.commit()

init_db()

# PYDANTIC MODELS
class TaskCreate(BaseModel):
    title: str

@app.get('/')
def root():
    """Returns basic API metadata and the available endpoints. """
    return {
        'name': 'Task API', 
        'version' : '1.0' , 
        'endpoints' : ['/tasks'] 
        }

@app.get('/health')
def healthcheck():
    """Checks API health status."""
    return {'status' : 'ok'}

# # Stage 1 endpoints
@app.get('/tasks')
def get_tasks():
    """Returns all tasks from the SQLite database."""
    cursor= conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
   
    tasks_list = []
    for task in tasks:
       tasks_list.append(
        {
           'id': task['id'],
           'title': task['title'],
           'done': bool(task['done'])
       })
    return tasks_list

@app.get('/tasks/{task_id}')
def get_task(task_id:int):
    """Retrieves a single task by its unique ID from the SQLite database."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    if not task:
        return JSONResponse(status_code=404, content={'error': f'Task {task_id} not found'})
    return {
        'id': task['id'],
        'title': task['title'],
        'done': bool(task['done'])
    }
# # Stage 3 endpoints
# @app.post('/tasks', status_code=201)
# def create_task(task: TaskCreate):
#     """Creates a new task with a title."""
#     if not task.title or not task.title.strip():
#         return JSONResponse(status_code=400, content={'error': 'Task title cannot be empty'})

#     new_id = max(t['id'] for t in tasks_db) + 1 if tasks_db else 1
        
#     new_task = {
#             'id': new_id,
#             'title': task.title.strip(),
#             'done': False
#             }

#     tasks_db.append(new_task)
#     return new_task

# class TaskUpdate(BaseModel):
#     title: Optional[str] = None
#     done: Optional[bool] = None

# # Stage 4 endpoints
# @app.put('/tasks/{task_id}')
# def update_task(task_id:int, task: TaskUpdate):
#     """Updates a task's title and/or completion status."""
#     target_task= None

#     for t in tasks_db:
#         if t['id'] == task_id:
#             target_task = t
#             break
        
#     if not target_task:
#         return JSONResponse(status_code=404, content={'error': f'Task {task_id} not found'})

#     if task.title is None and task.done is None:
#         return JSONResponse(status_code=400, content={'error': 'At least one field (title or done) must be provided for update'})
    
#     if task.title is not None:
#         if not task.title.strip():
#             return JSONResponse(status_code=400, content={'error': 'Task title cannot be empty'})
#         target_task['title'] = task.title.strip()

#     if task.done is not None:
#         target_task['done'] = task.done
    
#     return target_task

# @app.delete('/tasks/{task_id}', status_code=204)
# def delete_task(task_id:int):
#     """Deletes a task by its unique ID."""
#     for i, task in enumerate(tasks_db):
#         if task['id'] == task_id:
#             del tasks_db[i]
#             return Response(status_code=status.HTTP_204_NO_CONTENT)
#     return JSONResponse(status_code=404, content={'error': f'Task {task_id} not found'})
