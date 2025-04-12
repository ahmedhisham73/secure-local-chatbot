import yaml
import os

# بدل الـ USER_DB_PATH ده:
# USER_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'data/users/users.yaml'))

# استخدم المسار المطلق:import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DB_PATH = os.path.join(BASE_DIR, "data", "users", "users.yaml")



def load_users():
    with open(USER_DB_PATH, 'r') as f:
        data = yaml.safe_load(f)
    return data['users']

def authenticate_user(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return {
                "username": user['username'],
                "role": user['role']
            }
    return None

