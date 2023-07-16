from flask import Flask, render_template
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('movies.json')  # Use the appropriate path to your JSON file


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"

@app.route('/users')
def list_users():
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)


def find_user_by_id(users, id):
  for user in users:
    if user['id'] == id:
      return user
  return None

if __name__ == '__main__':
    app.run(debug=True)