from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager
import uuid
import json

app = Flask(__name__)
data_manager = JSONDataManager('movies.json')


@app.route('/')
def home():
    try:
        return render_template("users.html")
    except Exception as e:
        return str(e)


@app.route('/users')
def list_users():
    """Returns a list of users."""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>/movies')
def user_movies(user_id):
    """Return a list of movies for a given user_id."""
    list_of_users_movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user_id=user_id, list_of_users_movies=list_of_users_movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Get a new user."""
    if request.method == 'POST':
        # Get user input from the form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # Generate a unique identifier for a new user
        new_user_id = str(uuid.uuid4())
        # Add the new user to the data manager
        data_manager.add_user(new_user_id, username)
        return redirect(url_for('list_users'))
    # Else, it's GET method
    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Adds a new movie to a user's favorite movies list."""
    if request.method == 'POST':
        movie_title = request.form.get('title')
        favorite_movies = data_manager.add_movie(user_id, movie_title)
        # Update the favorite_movies list and save the changes
        if user_id in favorite_movies:
            favorite_movies[user_id].append(movie_title)
        else:
            favorite_movies[user_id] = [movie_title]

        with open("movies.json", "w") as save_file:
            json_file = json.dumps(favorite_movies)
            save_file.write(json_file)

        return f"Movie '{movie_title}' added to user {user_id}'s favorite movies."
    # It's GET method
    return render_template('add_movie.html', user_id=user_id)


# @app.route('/users/<user_id>/delete_movie/<movie_id>', method=['DELETE'])
# def delete_movie(user_id, movie_id):
#     """ Delete a movie with given user_id."""
#     users = list_users()
#     if user_id in users:
#         movies = users[user_id]['movies']
#         if movie_id in movies:
#             movies.remove(movie_id)
#             return jsonify({'message':f'Movie {movie_id} deleted from user {user_id} favorite list.'})
#         else:
#             return jsonify({'error': f'Movie {movie_id} not found in user {user_id} favorite list.'}), 404
#     else:
#         return jsonify({'error': f'User {user_id} not found.'}), 404


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movies = user_movies()
    if request.method == 'POST':
        # Get the updated movie details from the form
        updated_title = request.form['title']
        updated_genre = request.form['genre']
        updated_rating = request.form['rating']

        # Redirect to the user's movie list
        return redirect(f'/users/{user_id}/movies')

    # Render the movie update form
    return render_template('update_movie.html', movie=movies)

# def find_user_by_id(users, id):
#   for user in users:
#     if user['id'] == id:
#       return user
#   return None

if __name__ == '__main__':
    app.run(debug=True)