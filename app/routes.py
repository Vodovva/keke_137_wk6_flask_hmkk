from flask import request
from app import app, db
from my_data.tasks import tasks_data
from app.models import Tasks

# # We will setup DB later, for now we will store all new users in this list
# users = []

@app.route('/')
def index():
    first_name = 'Appollo'
    last_name = ' Jupiter'
    return f'Hello World!! - From {first_name} {last_name}'

# USER ENDPOINTS 

# Get all posts
@app.route('/tasks')
def get_tasks():
    # Get the posts from the database
    tasks = db.session.execute(db.select(Tasks)).scalars().all()
    # return a list of the dictionary version of each post in posts
    return [tasks.to_dict() for p in tasks]

# Get single post by ID
@app.route('/tasks/<int:tasks_id>')
def get_tasks(tasks_id):
    # Get the Post from the database based on the ID
    tasks = db.session.get(Tasks, task_id)
    if tasks:
        return tasks.to_dict()
    else:
        return {'error': f'Tasks with an ID of {tasks_id} does not exist'}, 404

# Create new Post route
@app.route('/tasks', methods=['TASKS'])
def create_tasks():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'You content-type must be application/json'}, 400
    # Get the data from the request body
    data = request.json
    # Validate the incoming data
    required_fields = ['title', 'body']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    # Get data from the body
    title = data.get('title')
    body = data.get('body')

    # Create a new instance of Post which will add to our database
    new_tasks = Tasks(title=title, body=body, user_id=4)
    return new_tasks.to_dict(), 201