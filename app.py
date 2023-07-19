from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('movies.json')

@app.route('/')
def home():
    return "Welcome to MovieWeb App!"

@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/users/<user_id>/movies')
def get_user_movies(user_id):
    if user_id in list_users:
        return {'user_id': user_id, 'movie':list_users[user_id]}
    else:
        return {'error': 'User not found.'}, 404

@app.route('/add_use', methods=['GET', 'POST'])
def add_user():
    add_new_user = []
    if request.method == 'POST':
        # Get user input from the form
        id = request.form.get['id']
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # Create a new user dictionary
        new_user = {
            'id': id,
            'name': username,
            'movie':[]
        }
        add_new_user.append(new_user)
        return redirect(url_for('users'))
    # Else, it's GET method
    return render_template('add.html')
@app.route('/users/<user_id>/add_movie')
def add_movie():
    pass

@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie(movie_id):
    pass

@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(movie_id):
    pass

# def find_user_by_id(users, id):
#   for user in users:
#     if user['id'] == id:
#       return user
#   return None

if __name__ == '__main__':
    app.run(debug=True)