import json
from .data_manager_interface import DataManagerInterface
import requests

API_KEY = "cfb1ce63"

class JSONDataManager(DataManagerInterface):
    """ Inherits from Storage and implements its functions."""
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return all the users
        with open("movies.json", "r") as fileobj:
            users_data = fileobj.read()
            list_all_users = json.loads(users_data)
        return list_all_users

    def get_user_movies(self, user_id):
        # Return all the movies for a given user
        with open("movies.json", "r") as fileobj:
            movies_data = fileobj.read()
            movies_saved = json.loads(movies_data)
        return movies_saved