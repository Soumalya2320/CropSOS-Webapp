from flask import Blueprint, request, jsonify
from services.model import analyze_plant_image
from services.gemini import get_ai_advice
from services.firebase import save_report, update_alert
import logging
import re

logger = logging.getLogger(__name__)
predict_bp = Blueprint('predict', __name__)


def clean_disease_name(raw: str) -> dict:
    """
    Convert 'Potato___Early_Blight' → 
      display: 'Early Blight'
      crop:    'Potato'
      scientific: mapped from known diseases
    """
    # Split on ___ (3 underscores = separator between crop and disease)
    parts = raw.split('___')
    if len(parts) == 2:
        crop    = parts[0].replace('_', ' ').strip()
        disease = parts[1].replace('_', ' ').strip()
    else:
        crop    = 'Unknown Crop'
        disease = raw.replace('_', ' ').strip()

    # Scientific name map — add more as needed
    scientific_map = {
        'Early Blight':       'Alternaria solani',
        'Late Blight':        'Phytophthora infestans',
        'Leaf Mold':          'Passalora fulva',
        'Bacterial Spot':     'Xanthomonas campestris',
        'Yellow Leaf Curl':   'Tomato yellow leaf curl virus',
        'Mosaic Virus':       'Tobacco mosaic virus',
        'Powdery Mildew':     'Erysiphe cichoracearum',
        'Leaf Rust':          'Puccinia triticina',
        'Brown Spot':         'Cochliobolus miyabeanus',
        'Healthy':            '',
    }
    scientific = scientific_map.get(disease, '')

    return {
        'display_disease': disease,        # "Early Blight"
        'crop_type':       crop,           # "Potato"
        'scientific_name': scientific,     # "Alternaria solani"
        'full_label':      f"{crop} — {disease}"
    }


@predict_bp.route('/predict', methods=['POST'])
def predict_disease():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        print("STEP 1: file received:", file.filename)

        # ML model
        result = analyze_plant_image(file)
        print("STEP 2: model output:", result)

        if 'error' in result:
            return jsonify({"error": result['error']}), 400

        raw_disease = result['disease']          # "Potato___Early_Blight"
        confidence  = result['confidence']       # 0.9851
        conf_pct    = round(confidence * 100, 1) # 98.5

        # Clean disease name
        cleaned = clean_disease_name(raw_disease)
        disease_display = cleaned['display_disease']  # "Early Blight"
        crop_type       = cleaned['crop_type']         # "Potato"
        scientific      = cleaned['scientific_name']

        # Get extra fields from request
        user_id  = request.form.get('userId',   'anonymous')
        image_url= request.form.get('imageUrl', '')
        location = request.form.get('location', 'Unknown')
        # If frontend didn't send cropType, use what model detected
        crop_type_form = request.form.get('cropType', crop_type)

        print("STEP 3: location from form:", location)

        # Gemini advice — pass cleaned name so prompt is readable
        advice = get_ai_advice(disease_display)
        print("STEP 4: gemini output:", advice)

        # Severity
        spread_risk  = advice.get('spread_risk', 'Unknown') if isinstance(advice, dict) else 'Unknown'
        severity_map = {'Low': 'low', 'Medium': 'medium', 'High': 'high', 'Critical': 'critical'}
        severity     = severity_map.get(spread_risk, 'medium')

        # Save report
        report_data = {
            "userId":         user_id,
            "imageUrl":       image_url,
            "disease":        disease_display,
            "rawDisease":     raw_disease,
            "scientificName": scientific,
            "confidence":     conf_pct,         # store as percentage
            "advice":         advice,
            "cropType":       crop_type_form,
            "severity":       severity,
            "location":       location,
        }
        report_id = save_report(report_data)

        # Update alert for this location
        update_alert(disease_display, location, severity)

        return jsonify({
            "reportId":        report_id,
            "disease":         disease_display,   # "Early Blight"
            "scientific_name": scientific,         # "Alternaria solani"
            "confidence":      conf_pct,           # 98.5 (not 0.9851)
            "advice":          advice,
            "severity":        severity,
            "location":        location,
            "cropType":        crop_type_form,
        }), 200

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@predict_bp.route('/history/<user_id>', methods=['GET'])
def get_user_history(user_id):
    try:
        from services.firebase import get_user_reports
        reports = get_user_reports(user_id)
        return jsonify({"reports": reports}), 200
    except Exception as e:
        logger.error(f"History fetch error: {str(e)}")
        return jsonify({"error": "Could not fetch history"}), 500


@predict_bp.route('/alerts/<location>', methods=['GET'])
def get_alerts(location):
    try:
        from services.firebase import get_location_alerts
        alerts = get_location_alerts(location)
        return jsonify({"alerts": alerts}), 200
    except Exception as e:
        logger.error(f"Alerts fetch error: {str(e)}")
        return jsonify({"error": "Could not fetch alerts"}), 500


@predict_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    try:
        data      = request.get_json()
        report_id = data.get('reportId')
        user_id   = data.get('userId')
        is_correct= data.get('isCorrect')

        if report_id is None or is_correct is None:
            return jsonify({"error": "reportId and isCorrect required"}), 400

        from services.firebase import save_feedback
        save_feedback(report_id, user_id, is_correct)
        return jsonify({"message": "Feedback saved. Thank you!"}), 200
    except Exception as e:
        logger.error(f"Feedback error: {str(e)}")
        return jsonify({"error": "Could not save feedback"}), 500