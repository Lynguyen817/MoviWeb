import json
from .data_manager_interface import DataManagerInterface
import requests


class JSONDataManager(DataManagerInterface):
    """ Inherits from Storage and implements its functions."""
    def __init__(self, filename):
        self.filename = filename

    def load_movies_data(self, title):
        """Load movies from the api link when a title is input."""
        API_KEY = "cfb1ce63"
        API_MOVIE_URL = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
        res = requests.get(API_MOVIE_URL)
        movies_data = json.loads(res.text)
        return movies_data

    def get_all_users(self):
        """ Return all the users."""
        with open("MoviWeb/movies.json", "r") as fileobj:
            users_data = fileobj.read()
            list_all_users = json.loads(users_data)
        return list_all_users

    def get_user_movies(self, user_id):
        """ Return all the movies for a given user."""
        user_favorite_movies = []
        for user in self.get_all_users():
            if user['id'] == int(user_id.strip("<>")):
                user_favorite_movies.append(user['movies'])
                return user_favorite_movies
        return "User not found", 404

    def add_user(self, user_id, name):
        """ Add a new user and save it to the database.."""
        all_users = self.get_all_users()
        user_exists = False

        for user in all_users:
            if user_id == user["id"]:
                user_exists = True
                break

        new_user = {"id": user_id,
                    "name": name,
                    "movies": []}
        if user_exists:
            return "User already exists."
        else:
            all_users.append(new_user)
            with open("MoviWeb/movies.json", "w") as save_file:
                json_file = json.dumps(all_users)
                save_file.write(json_file)
            return "User added successfully."

    def add_movie(self, user_id, title):
        """ Adds a movie to the user movie list and saves it."""
        list_of_users = self.get_all_users()
        for user in list_of_users:
            if user["id"] == user_id:
                # Get a new movie from API
                new_movie_api = self.load_movies_data(title)
                # Generate a unique identifier for the new movie
                new_movie_id = len(user["movies"]) + 1

                new_movie_data = {
                        "id": new_movie_id,
                        "name": new_movie_api["Title"],
                        "director": new_movie_api["Director"],
                        "year": new_movie_api["Year"],
                        "rating": new_movie_api["imdbRating"],
                        "image": new_movie_api["Poster"]
                }

                user["movies"].append(new_movie_data)
                break

        with open("movies.json", "w") as save_file:
            json_file = json.dumps(list_of_users)
            save_file.write(json_file)
        return list_of_users

    def delete_movie(self, user_id,  title):
        """Deletes a movie from the movies database"""
        list_of_users = self.get_all_users()
        exist_movie_list = self.get_user_movies()
        #exist_movies_data = self.list_movies()
        for user in list_of_users:
            if user["id"] == user_id:
                for movie in exist_movie_list:
                    if movie["name"] == title:
                        del (exist_movie_list[title])
        with open("data.json", "w") as save_file:
            json.dump(exist_movie_list, save_file)
        return

    def update_movie(self, user_id, title, new_rating):
        """Updates a movie from the movies database with a new rating"""
        list_of_users = self.get_all_users()
        exist_movie_list = self.get_user_movies()
        for user in list_of_users:
            if user["id"] == user_id:
                for movie in exist_movie_list:
                    if movie["name"] == title:
        #movies_data = self.list_movies()
                        for key, val in movie.items():
                            if title == key:
                                val["rating"] = new_rating
        with open("movies.json", "w") as save_file:
            json.dump(exist_movie_list, save_file)
            return exist_movie_list
