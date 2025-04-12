import os
import jwt
import datetime
from dotenv import load_dotenv

# Load secret key from .env
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET", "changeme")

def generate_token(user_data, expires_in_minutes=30):
    payload = {
        "username": user_data["username"],
        "role": user_data["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_in_minutes)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256").decode('utf-8')
    return token

def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

