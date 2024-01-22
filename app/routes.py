from flask import request
from . import app, db
from data.tasks import tasks_list
from app.models import Task


# Creating a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content type must be application/json'}, 400 
    
    data = request.json
    
    #validate that the data has all of the required feilds
    required_fields = ['title', 'description']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    

    # Get the value from the data
    title = data.get('title')
    description = data.get('description')

    new_task = Task(title=title,description=description)
    return new_task.to_dict(), 201



@app.route('/')
def index():
    return f"Hello, please search for a task"

@app.route('/tasks')
def get_tasks():
    tasks = db.session.execute(db.select(Task)).scalars.all()
    return [t.to_dict() for t in tasks]

@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    task = db.session.get(Task, id)
    if task:
        return task.to_dict()
    else:
        return {'error': f'Post with an ID of {id} does not exist'}, 404