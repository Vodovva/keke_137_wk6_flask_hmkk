from flask import request
from app import app, db
from datetime import datetime
from data.tasks import tasks_list
from app.models import Task, User
from app.auth import basic_auth, token_auth



# USER ENDPOINTS 
@app.route("/token")
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return {"token":token,
            "tokenExpiration":user.token_expiration}


@app.route('/tasks')
def get_task():
    task = db.session.execute(db.select(Task)).scalars().all()
    return [t.to_dict() for t in task]


@app.route('/tasks/<int:task_id>')
def get_task_by_id(task_id):
    task = db.session.get(Task, task_id)
    if task:
        return task.to_dict()
    else:
        return {'error': f'Task with an ID of {task_id} does not exist'}, 404



@app.route('/tasks', methods=['POST'])
@token_auth.login_required
def create_task():
    if not request.is_json:
        return {'error': 'Your content type must be application/json'}, 400 
    
    data = request.json
    
    required_fields = ['title', 'description']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    

    title = data.get('title')
    description = data.get('description')
    due_date = data.get('dueDate')

    #get logged in user
    user = token_auth.current_user()

    new_task = Task(title=title,description=description)
    return new_task.to_dict(), 201


@app.route('/tasks/<int:task_id>', methods=["PUT"]) 
@token_auth.login_required
def edit_post(task_id):
    if not request.is_json:
        return {"error":"Your content-type is not application/json"}, 400
    task = db.session.get(Task, task_id)
    if task is None:
        return {"error":f"post with the id of {task_id} does not exist!"}, 404
    current_user = token_auth.current_user()
    if task.author is not current_user:
        return {"error":"This is not your post, you cant edit this"}, 403
    data = request.json
    task.update(**data)
    return task.to_dict()


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@token_auth.login_required
def delete_post(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return {"error":f"We cannot locate posts with the id of {task_id}"}, 404
    current_user = token_auth.current_user()
    if task.author is not current_user:
        return {"error":"You can do that, this sint your post! Get outta here!"}, 403
    task.delete()
    return {"success":f"{task.title} has been deleted!"}


# Create New User
@app.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    
    data = request.json

    required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    # Get the values from the data
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    check_users = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalars().all()
    if check_users:
        return {'error': 'A user with that username and/or email already exists'}, 400

    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
    return new_user.to_dict(), 201

#update
@app.route('/users/<int:user_id>', methods=['PUT'])
@token_auth.login_required
def edit_user(user_id):
    if not request.is_json:
        return {"error": "your content type must be application/json !"}, 400
    user = db.session.get(User, user_id)
    if user is None:
        return {"error": f"User with {user_id} does not exist"},404
    current_user = token_auth.current_user()
    if user is not current_user:
        return {"error":"You cannot change this user as you are not them!"} ,403
    data = request.json
    user.update(**data)
    return user.to_dict()


#delete
@app.route("/users/<int:user_id>", methods=["DELETE"])
@token_auth.login_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    current_user = token_auth.current_user()
    if user is None:
        return {"error":f"User with {user_id} not found!"},404
    if user is not current_user:
        return {"error":"You cant do that, delete yourself only"}, 403
    user.delete()
    return{"success":f"{user.username} has been deleted!"}

#retrieve? 
@app.get("/users/<int:user_id>")
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        return user.to_dict()
    else:
        return {"error":f" user with id:{user_id} not found"}, 404