import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime, timezone

# Initialize Firebase only once
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()


def save_report(report_data: dict) -> str:
    """Save a scan report to Firestore. Returns the new report ID."""
    report_data["createdAt"] = firestore.SERVER_TIMESTAMP
    ref = db.collection("reports").add(report_data)
    return ref[1].id


def get_user_reports(user_id: str) -> list:
    """Get all reports for a user, ordered by newest first."""
    docs = (
        db.collection("reports")
        .where("userId", "==", user_id)
        .order_by("createdAt", direction=firestore.Query.DESCENDING)
        .limit(50)
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def update_alert(disease: str, location: str, severity: str):
    """
    Increment or create an alert entry for a disease in a location.
    Uses Firestore atomic increment — safe for concurrent requests.
    """
    # Use disease+location as document ID for easy lookup
    alert_id = f"{disease.replace(' ', '_')}_{location.replace(' ', '_')}".lower()
    alert_ref = db.collection("alerts").document(alert_id)

    alert_ref.set({
        "disease": disease,
        "location": location,
        "severity": severity,
        "count": firestore.Increment(1),
        "lastUpdated": firestore.SERVER_TIMESTAMP
    }, merge=True)  # merge=True = create if not exists, update if exists


def get_location_alerts(location: str) -> list:
    """Get all active disease alerts for a region."""
    docs = (
        db.collection("alerts")
        .where("location", "==", location)
        .order_by("lastUpdated", direction=firestore.Query.DESCENDING)
        .limit(20)
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def save_feedback(report_id: str, user_id: str, is_correct: bool):
    """Save farmer feedback on AI diagnosis accuracy."""
    db.collection("feedback").add({
        "reportId": report_id,
        "userId": user_id,
        "isCorrect": is_correct,
        "createdAt": firestore.SERVER_TIMESTAMP
    })