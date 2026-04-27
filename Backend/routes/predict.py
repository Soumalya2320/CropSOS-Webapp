from flask import Blueprint, request, jsonify
from services.model import analyze_plant_image
from services.gemini import get_ai_advice
from services.firebase import save_report, update_alert, get_all_geo_alerts, get_location_alerts
import logging
import re

logger = logging.getLogger(__name__)
predict_bp = Blueprint('predict', __name__)


def clean_disease_name(raw: str) -> dict:
    parts = raw.split('___')
    if len(parts) == 2:
        crop    = parts[0].replace('_', ' ').strip()
        disease = parts[1].replace('_', ' ').strip()
    else:
        crop    = 'Unknown Crop'
        disease = raw.replace('_', ' ').strip()

    scientific_map = {
        'Early Blight':     'Alternaria solani',
        'Late Blight':      'Phytophthora infestans',
        'Leaf Mold':        'Passalora fulva',
        'Bacterial Spot':   'Xanthomonas campestris',
        'Powdery Mildew':   'Erysiphe cichoracearum',
        'Leaf Rust':        'Puccinia triticina',
        'Brown Spot':       'Cochliobolus miyabeanus',
        'Healthy':          '',
    }
    return {
        'display_disease': disease,
        'crop_type':       crop,
        'scientific_name': scientific_map.get(disease, ''),
    }


@predict_bp.route('/predict', methods=['POST'])
def predict_disease():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        result = analyze_plant_image(file)

        if 'error' in result:
            return jsonify({"error": result['error']}), 400

        raw_disease = result['disease']
        confidence  = result['confidence']
        conf_pct    = round(confidence * 100, 1)

        cleaned         = clean_disease_name(raw_disease)
        disease_display = cleaned['display_disease']
        crop_type       = cleaned['crop_type']
        scientific      = cleaned['scientific_name']

        user_id   = request.form.get('userId',   'anonymous')
        image_url = request.form.get('imageUrl', '')
        location  = request.form.get('location', 'Unknown')
        crop_type_form = request.form.get('cropType', crop_type)

        # ── GPS coordinates from frontend
        try:
            lat = float(request.form.get('lat', 22.57))
            lng = float(request.form.get('lng', 88.36))
        except (ValueError, TypeError):
            lat, lng = 22.57, 88.36

        advice = get_ai_advice(disease_display)

        spread_risk  = advice.get('spread_risk', 'Unknown') if isinstance(advice, dict) else 'Unknown'
        severity_map = {'Low': 'low', 'Medium': 'medium', 'High': 'high', 'Critical': 'critical'}
        severity     = severity_map.get(spread_risk, 'medium')

        report_data = {
            "userId":         user_id,
            "imageUrl":       image_url,
            "disease":        disease_display,
            "rawDisease":     raw_disease,
            "scientificName": scientific,
            "confidence":     conf_pct,
            "advice":         advice,
            "cropType":       crop_type_form,
            "severity":       severity,
            "location":       location,
            "lat":            lat,      # ← stored in Firestore
            "lng":            lng,      # ← stored in Firestore
        }
        report_id = save_report(report_data)
        update_alert(disease_display, location, severity, lat, lng)

        return jsonify({
            "reportId":        report_id,
            "disease":         disease_display,
            "scientific_name": scientific,
            "confidence":      conf_pct,
            "advice":          advice,
            "severity":        severity,
            "location":        location,
            "cropType":        crop_type_form,
        }), 200

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# ── NEW: Get ALL geo-tagged alerts (for heatmap)
@predict_bp.route('/alerts/geo', methods=['GET'])
def get_geo_alerts():
    try:
        alerts = get_all_geo_alerts()
        return jsonify({"alerts": alerts}), 200
    except Exception as e:
        logger.error(f"Geo alerts error: {str(e)}")
        return jsonify({"error": "Could not fetch geo alerts"}), 500


@predict_bp.route('/alerts/<location>', methods=['GET'])
def get_alerts(location):
    try:
        alerts = get_location_alerts(location)
        return jsonify({"alerts": alerts}), 200
    except Exception as e:
        logger.error(f"Alerts fetch error: {str(e)}")
        return jsonify({"error": "Could not fetch alerts"}), 500


@predict_bp.route('/reports/<report_or_user_id>', methods=['GET'])
def get_reports(report_or_user_id):
    """
    Get either:
    - A single report by ID (if called as /reports/{reportId})
    - All reports for a user (if called as /reports/{userId})
    """
    try:
        from services.firebase import get_report_by_id, get_user_reports
        
        # First try to get as a single report
        report = get_report_by_id(report_or_user_id)
        if report:
            return jsonify(report), 200
        
        # If not found, try as user_id (returns multiple reports)
        reports = get_user_reports(report_or_user_id)
        if reports:
            return jsonify({"reports": reports}), 200
        
        # Not found as either
        return jsonify({"error": "Not found", "reports": []}), 200
    except Exception as e:
        logger.error(f"Get reports error: {str(e)}")
        return jsonify({"error": "Could not fetch reports", "reports": []}), 200


@predict_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    try:
        data       = request.get_json()
        report_id  = data.get('reportId')
        user_id    = data.get('userId')
        is_correct = data.get('isCorrect')
        if report_id is None or is_correct is None:
            return jsonify({"error": "reportId and isCorrect required"}), 400
        from services.firebase import save_feedback
        save_feedback(report_id, user_id, is_correct)
        return jsonify({"message": "Feedback saved. Thank you!"}), 200
    except Exception as e:
        return jsonify({"error": "Could not save feedback"}), 500