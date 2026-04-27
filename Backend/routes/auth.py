from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from services.firebase import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

# 🟢 REGISTER
@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.json

        user = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "password": generate_password_hash(data.get("password")),
            "farm_name": data.get("farm_name"),
            "state": data.get("state"),
            "farm_size": data.get("farm_size"),
            "crop_type": data.get("crop_type"),
            "irrigation": data.get("irrigation"),
            "alerts_enabled": data.get("alerts_enabled")
        }

        # Save to Firebase
        db.collection("users").add(user)

        return jsonify({
            "message": "User registered successfully"
        }), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# 🟢 LOGIN
@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        users = db.collection("users").where("email", "==", email).stream()

        user_data = None
        for user in users:
            user_data = user.to_dict()
            user_data["id"] = user.id

        if not user_data:
            return jsonify({"message": "User not found"}), 404

        if not check_password_hash(user_data["password"], password):
            return jsonify({"message": "Invalid password"}), 401

        # 🔥 ADD THIS LINE (TOKEN CREATE)
        token = create_access_token(identity=user_data["id"])

        # 🔥 MODIFY RETURN (token add kar)
        return jsonify({
            "message": "Login successful",
            "token": token,   # 👈 IMPORTANT
            "user": {
                "id": user_data["id"],
                "email": user_data["email"],
                "name": user_data["first_name"]
            }
        })

    except Exception as e:
        return jsonify({"message": str(e)}), 500