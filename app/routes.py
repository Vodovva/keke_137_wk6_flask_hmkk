from flask import request
from app import app, db
from my_data.tasks import tasks_data
from app.models import Tasks, User

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

@app.route('/')
def index():
    first_name = 'Brian'
    last_name = 'Stanton'
    return f'Hello World!! - From {first_name} {last_name}'

# USER ENDPOINTS 
@app.route("/token")
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return {"token":token,
            "tokenExpiration":user.token_expiration}


# Create New User
@app.route('/users', methods=['POST'])
def create_user():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    
    # Get the data from the request body
    data = request.json

    # Validate that the data has all of the required fields
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

    # Check to see if any current users already have that username and/or email
    check_users = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalars().all()
    # If the list is not empty then someone already has that username or email
    if check_users:
        return {'error': 'A user with that username and/or email already exists'}, 400

    # Create a new user instance with the request data which will add it to the database
    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
    return new_user.to_dict(), 201

#update
@app.route('/users/<int:user_id>', methods=['PUT'])
@token_auth.login_required
def edit_user(user_id):
    # check if they sent the data correctly
    if not request.is_json:
        return {"error": "your content type must be application/json !"}, 400
    # get user based off id
    user = db.session.get(User, user_id)
    # make sure it exists
    if user is None:
        return {"error": f"User with {user_id} does not exist"},404
    # get their token
    current_user = token_auth.current_user()
    # make sure they are the person logged in
    if user is not current_user:
        return {"error":"You cannot change this user as you are not them!"} ,403
    # then we update!
    data = request.json
    user.update(**data)
    return user.to_dict()


#delete
@app.route("/users/<int:user_id>", methods=["DELETE"])
@token_auth.login_required
def delete_user(user_id):
    # get the user based on the id
    user = db.session.get(User, user_id)
    #get token
    current_user = token_auth.current_user()
    # make sure its a real user
    if user is None:
        return {"error":f"User with {user_id} not found!"},404
    # make sure user to del is current user
    if user is not current_user:
        return {"error":"You cant do that, delete yourself only"}, 403
    # delete the user 
    user.delete()
    return{"success":f"{user.username} has been deleted!"}


#retrieve? 
@app.get("/users/<int:user_id>")
def get_user(user_id):
    #get the user
    user = db.session.get(User, user_id)
    #if no user let them know
    if user:
        return user.to_dict()
    else:
        return {"error":f" user with id:{user_id} not found"}, 404
    


# POST ENDPOINTS
