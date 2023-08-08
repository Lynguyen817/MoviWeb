from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager
from flask_bootstrap import Bootstrap
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)
data_manager = JSONDataManager('movies.json')


@app.route('/')
def home():
    """Returns homepage, alerts error when it's not open."""
    try:
        return render_template("users.html")
    except Exception as e:
        return str(e)


@app.route('/search_movie')
def search_movie():
    """Return a movie that the user searches."""
    title = request.args.get('title')
    movie_data = data_manager.load_movies_data(title)

    if movie_data.get('Response') == 'False':
        return "Movie not found", 404

    return render_template('search_movie.html', movie_data=movie_data)


@app.route('/users')
def list_users():
    """Returns a list of users."""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>/movies')
def user_movies(user_id):
    """Return a list of movies for a given user_id."""
    list_of_users_movies = data_manager.get_user_movies(user_id)
    # Check if the list_of_users_movies is None, and if so, set it to an empty list
    if list_of_users_movies is None:
        list_of_users_movies = []

    # Retrieve the new_movie_list from the query parameters if it exists
    new_movies_list = request.args.get('new_movie_list', None)
    if new_movies_list:
        # Convert the new_movies_list from JSON string to a Python list
       # new_movies_list = json.loads(new_movies_list)
        list_of_users_movies.append(new_movies_list)
        # Redirect to the user_movies route with the new_movie_data as a query parameter
        #return redirect(url_for('user_movies', user_id=user_id, new_movie_list=json.dumps(new_movie_data)))

    return render_template('user_movies.html', user_id=user_id, list_of_users_movies=list_of_users_movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Get a new user."""
    users = data_manager.get_all_users()
    if request.method == 'POST':

        # Get user input from the form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Generate a unique identifier for a new user
        new_user_id = len(users) + 1

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

        if not movie_title:
            return "Please provide a movie title.", 400

        # Call the add_movie method of the data_manager to add the movie to the user's list
        new_movie_list = data_manager.add_movie(user_id, movie_title)
        print(new_movie_list)

        if new_movie_list is not None:
            return redirect(url_for('user_movies', user_id=user_id, new_movie_list=new_movie_list))
        else:
            return "User not found"

    # It's GET method
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    """ Delete a movie from the user's favorite movie list"""
    if request.method == 'POST':
        deleted = data_manager.delete_movie(user_id, movie_id)
        if deleted:
            return redirect(url_for('user_movies', user_id=user_id))
        else:
            return "Movie not found"

    # Get the movie data
    list_of_users_movies = data_manager.get_user_movies(user_id)
    movie = next((m for m in list_of_users_movies if m["id"] == int(movie_id)), None)

    if not movie:
        return "Movie not found"

    # It's a GET request, render the delete page
    return render_template('delete_movie.html', user_id=user_id, movie_id=movie_id, movie=movie)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Update a movie in the user's movie list"""
    movie_to_update = None
    if request.method == 'POST':
        # Update movie details
        movie_to_update["name"] = request.form.get('name')
        movie_to_update["director"] = request.form.get('director')
        movie_to_update["year"] = request.form.get('year')
        movie_to_update["rating"] = request.form.get('rating')
        movie_to_update["image"] = request.form.get('image')

        # Redirect to the user's movie list
        return redirect(url_for('user_movies', user_id=user_id))

    # Render the movie update form
    return render_template('update_movie.html',user_id=user_id, movie=movie_to_update)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)