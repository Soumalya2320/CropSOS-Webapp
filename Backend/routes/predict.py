from flask import Blueprint, request, jsonify
from services.model import analyze_plant_image
from services.gemini import get_ai_advice
from services.firebase import save_report, update_alert
import logging

logger = logging.getLogger(__name__)
predict_bp = Blueprint('predict', __name__)


# FIX #2: Only ONE function on this route (removed duplicate)
@predict_bp.route('/predict', methods=['POST'])
def predict_disease():
    try:
        # File validation
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']

        # Analyze image with ML model
        result = analyze_plant_image(file)

        if 'error' in result:
            return jsonify({"error": result['error']}), 400

        disease = result['disease']
        confidence = result['confidence']

        # FIX #3: Pass only disease_name (matching gemini.py signature)
        advice = get_ai_advice(disease)

        # Get extra fields from request
        user_id = request.form.get('userId', 'anonymous')
        image_url = request.form.get('imageUrl', '')
        crop_type = request.form.get('cropType', 'Unknown')
        location = request.form.get('location', 'Unknown')

        # Determine severity from spread_risk
        spread_risk = advice.get('spread_risk', 'Unknown') if isinstance(advice, dict) else 'Unknown'
        severity_map = {'Low': 'low', 'Medium': 'medium', 'High': 'high', 'Critical': 'critical'}
        severity = severity_map.get(spread_risk, 'medium')

        # Save report to Firestore
        report_data = {
            "userId": user_id,
            "imageUrl": image_url,
            "disease": disease,
            "confidence": confidence,
            "advice": advice,
            "cropType": crop_type,
            "severity": severity,
            "location": location,
        }
        report_id = save_report(report_data)

        # Update regional alert count
        update_alert(disease, location, severity)

        return jsonify({
            "reportId": report_id,
            "disease": disease,
            "confidence": confidence,
            "advice": advice,
            "severity": severity,
            "location": location
        }), 200

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@predict_bp.route('/history/<user_id>', methods=['GET'])
def get_user_history(user_id):
    """Get all reports for a specific user."""
    try:
        from services.firebase import get_user_reports
        reports = get_user_reports(user_id)
        return jsonify({"reports": reports}), 200
    except Exception as e:
        logger.error(f"History fetch error: {str(e)}")
        return jsonify({"error": "Could not fetch history"}), 500


@predict_bp.route('/alerts/<location>', methods=['GET'])
def get_alerts(location):
    """Get disease alerts for a specific location/region."""
    try:
        from services.firebase import get_location_alerts
        alerts = get_location_alerts(location)
        return jsonify({"alerts": alerts}), 200
    except Exception as e:
        logger.error(f"Alerts fetch error: {str(e)}")
        return jsonify({"error": "Could not fetch alerts"}), 500


@predict_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """Farmer submits Yes/No — was diagnosis correct?"""
    try:
        data = request.get_json()
        report_id = data.get('reportId')
        user_id = data.get('userId')
        is_correct = data.get('isCorrect')

        if report_id is None or is_correct is None:
            return jsonify({"error": "reportId and isCorrect required"}), 400

        from services.firebase import save_feedback
        save_feedback(report_id, user_id, is_correct)

        return jsonify({"message": "Feedback saved. Thank you!"}), 200
    except Exception as e:
        logger.error(f"Feedback error: {str(e)}")
        return jsonify({"error": "Could not save feedback"}), 500