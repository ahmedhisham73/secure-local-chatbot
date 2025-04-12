from flask import Flask, request, jsonify
from ldap_sim import authenticate_user
from shared.jwt_utils import generate_token
from flask_cors import CORS
from shared.rbac import requires_auth, requires_role  # ✅ Import decorators
import sys
sys.path.append('/app')


app = Flask(__name__)
#CORS(app)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    user = authenticate_user(username, password)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    token = generate_token(user)
    return jsonify({
        "token": token,
        "user": user
    })

# ✅ Endpoint to test authentication + RBAC
@app.route("/secure-data", methods=["GET"])
@requires_auth
@requires_role("analyst")
def secure_data():
    return jsonify({
        "message": f"Hello {request.user['username']}, you have access to secure data!"
    })

#if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5000)



