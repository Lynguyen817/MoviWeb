import json
from .data_manager_interface import DataManagerInterface
import requests

API_KEY = "cfb1ce63"
API_MOVIE_URL = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"


class JSONDataManager(DataManagerInterface):
    """ Inherits from Storage and implements its functions."""
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        """ Return all the users."""
        with open("movies.json", "r") as fileobj:
            users_data = fileobj.read()
            list_all_users = json.loads(users_data)
        print(list_all_users)
        return list_all_users

    def get_user_movies(self, user_id):
        """ Return all the movies for a given user."""
        self.get_all_users()
        for user in self.get_all_users():
            if user['id'] == user_id:
                user_movie_list = user['movie']
                print(user_movie_list)
                return user_movie_list

    def add_user_movie(self, title):
        """ Adds a movie to the movie database and saves it."""
        res = requests.get(API_MOVIE_URL)
        movies_data = json.loads(res.text)
        print(f'Movie {movies_data["Title"]} successfully added')

        with open("data.json", "r") as handle:
            exist_data = json.loads(handle.read())

        new_movie_data = {
            movies_data["Title"]: {
                "year": movies_data["Year"],
                "rating": movies_data["imdbRating"],
                "image": movies_data["Poster"]
            }
        }
        new_dict = {**exist_data, **new_movie_data}

        with open("data.json", "w") as save_file:
            json_file = json.dumps(new_dict)
            saved_movies = save_file.write(json_file)
        return saved_movies

    def delete_user_movie(self, title):
        """Deletes a movie from the movies database"""
        exist_movies_data = self.list_movies()
        del (exist_movies_data[title])
        with open("data.json", "w") as save_file:
            json.dump(exist_movies_data, save_file)
        return

    def update_user_movie(self, title, new_rating):
        """Updates a movie from the movies database with a new rating"""
        movies_data = self.list_movies()
        for key, val in movies_data.items():
            if title == key:
                val["rating"] = new_rating
                with open("data.json", "w") as save_file:
                    json.dump(movies_data, save_file)
                    return movies_data