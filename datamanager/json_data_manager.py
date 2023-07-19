import json
from .data_manager_interface import DataManagerInterface
import requests


class JSONDataManager(DataManagerInterface):
    """ Inherits from Storage and implements its functions."""
    def __init__(self, filename):
        self.filename = filename

    def load_movies_data(self, title):
        API_KEY = "cfb1ce63"
        API_MOVIE_URL = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
        res = requests.get(API_MOVIE_URL)
        movies_data = json.loads(res.text)
        return movies_data
        #print(f'Movie {movies_data["Title"]} successfully added')

    def get_all_users(self):
        """ Return all the users."""
        with open("movies.json", "r") as fileobj:
            users_data = fileobj.read()
            list_all_users = json.loads(users_data)
        print(list_all_users)
        return list_all_users

    def get_user_movies(self, user_id):
        """ Return all the movies for a given user."""
        self.load_movies_data()
        self.get_all_users()
        for user in self.get_all_users():
            if user['id'] == user_id:
                user_movie_list = user['movie']
                print(user_movie_list)
                return user_movie_list

    def add_user(self, user_id, name):
        """ Add a new user."""
        all_users = self.get_all_users()
        new_user = {"id": user_id,
                    "name": name,
                    "movies": []}
        if user_id not in all_users["id"]:
            all_users.append(new_user)
            return all_users


    def add_movie(self, user_id, title):
        """ Adds a movie to the user movie list and saves it."""
        list_of_users = self.get_all_users()
        exist_movie_list = self.get_user_movies()
        for user in list_of_users:
            if user["id"] == user_id:
                for movie in exist_movie_list:
                    if movie["name"] != title:
                        # Generate a unique identifier for the new movie
                        new_movie_id = len(exist_movie_list) + 1
                        new_movie_data = {
                                "id": new_movie_id,
                                "name": exist_movie_list["Title"],
                                "director": exist_movie_list["Director"],
                                "year": exist_movie_list["Year"],
                                "rating": exist_movie_list["imdbRating"],
                                "image": exist_movie_list["Poster"]
                            }
                        new_dict = {**exist_movie_list, **new_movie_data}

                        with open("movies.json", "w") as save_file:
                            json_file = json.dumps(new_dict)
                            saved_movies = save_file.write(json_file)
                        return saved_movies

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