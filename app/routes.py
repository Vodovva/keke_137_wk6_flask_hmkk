from flask import request
from . import app
from data.tasks import tasks_list

tasks = []

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

    # Check to see if any current task titles already exists
    for task in tasks:
        if task['title'] == title:
            return {'error': 'A task with that title already exists'}, 400


    new_task = {
        "id": len(tasks) +1,
        "title": title,
        "description": description,
        "completed": "",
        "createdAt": "2024-01-09T11:25:45",
    }
    tasks.append(new_task)
    return new_task, 201




@app.route('/')
def index():
    return f"Hello, please search for a task"

@app.route('/tasks')
def get_tasks():
    tasks = tasks_list
    return tasks


@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    task = tasks_list
    for task in task:
        if task['id'] == task_id:
            return task
    return