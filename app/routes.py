from app import app
from fake_data.tasks import tasks_list

@app.route('/')
def SacredGoddess():
    first_name = 'Valerie'
    last_name = 'McCray Vodovnik'
    return f'Hello Goddess!! - From {first_name} {last_name}'

# POST ENDPOINTS

# Get all posts
@app.route('/tasks')
def get_tasks():
    # Get the posts from storage (fake data, will setup db tomorrow)
    tasks = tasks_list 
    return tasks

# Get single post by ID
@app.route('/tasks/<int:task_id>')
def get_taskss(task_id):
    # print(f"The post ID is {post_id} and the type is {type(post_id)}")
    # return str(post_id)
    # Get the posts from storage
    tasks = tasks_list
    # For each dictionary in the list of post dictionaries
    for task in tasks:
        # if the key of 'id' on the post dictionary matched the post_id from the URL
        if task['id'] == task_id:
            # Return that post dictionary
            return task 
    # If we loop through all of the posts without returning, the post with that ID does not exist
        return {'error' : f'task with n ID of {task_id} does not exist'}, 404