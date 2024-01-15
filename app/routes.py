from flask import request
from app import app, db
from my_data.posts import tasks_data
from app.models import Post

# # We will setup DB later, for now we will store all new users in this list
# users = []

@app.route('/')
def index():
    first_name = 'Appollo'
    last_name = ' Jupiter'
    return f'Hello World!! - From {first_name} {last_name}'

# USER ENDPOINTS 

# Get all posts
@app.route('/posts')
def get_posts():
    # Get the posts from the database
    posts = db.session.execute(db.select(Post)).scalars().all()
    # return a list of the dictionary version of each post in posts
    return [p.to_dict() for p in posts]

# Get single post by ID
@app.route('/posts/<int:post_id>')
def get_post(post_id):
    # Get the Post from the database based on the ID
    post = db.session.get(Post, post_id)
    if post:
        return post.to_dict()
    else:
        return {'error': f'Post with an ID of {post_id} does not exist'}, 404

# Create new Post route
@app.route('/posts', methods=['POST'])
def create_post():
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
    new_post = Post(title=title, body=body, user_id=4)
    return new_post.to_dict(), 201