from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.predict import predict_bp
import logging
import os
from dotenv import load_dotenv
from routes.auth import auth_bp
from services.firebase import get_user_reports, db
from services.firebase import save_feedback
from flask_jwt_extended import JWTManager



load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# CORS — allow only your frontend domain in production
CORS(app, origins=[
    "http://localhost:8080",
    "http://localhost:5173",      # Vue dev server
    "http://localhost:3000",
    os.getenv("FRONTEND_URL", "*")  # Set in .env for production
])

# Register blueprints
app.register_blueprint(predict_bp)
app.register_blueprint(auth_bp)

# Health check endpoint
@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "service": "CropSOS Backend",
        "version": "1.0.0"
    })

# Global error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

@app.route("/reports/<user_id>", methods=["GET"])
def get_reports(user_id):
    try:
        reports = get_user_reports(user_id)
        return {"reports": reports}, 200
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json

    save_feedback(
        data.get("reportId"),
        data.get("userId"),
        data.get("isCorrect")
    )

    return {"message": "Feedback saved"}, 200

@app.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user_doc = db.collection("users").document(user_id).get()

        if not user_doc.exists:
            return {"error": "User not found"}, 404

        user_data = user_doc.to_dict()
        user_data["id"] = user_doc.id

        return {"user": user_data}, 200

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    port = int(os.getenv("PORT", 5000))
    logger.info(f"Starting CropSOS backend on port {port}")
    app.run(debug=debug_mode, host="0.0.0.0", port=port)