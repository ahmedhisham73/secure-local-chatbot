from functools import wraps
from flask import request, jsonify
from shared.jwt_utils import decode_token


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ")[1]
        decoded = decode_token(token)
        if "error" in decoded:
            return jsonify(decoded), 401

        request.user = decoded  # attach user info to request
        return f(*args, **kwargs)
    return decorated

def requires_role(required_role):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = getattr(request, "user", None)
            if not user or user.get("role") != required_role:
                return jsonify({"error": "Forbidden – insufficient role"}), 403
            return f(*args, **kwargs)
        return decorated
    return wrapper

