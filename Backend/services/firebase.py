import firebase_admin
from firebase_admin import credentials, firestore
import os

if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()


def save_report(report_data: dict) -> str:
    report_data["createdAt"] = firestore.SERVER_TIMESTAMP
    ref = db.collection("reports").add(report_data)
    return ref[1].id


def get_user_reports(user_id: str) -> list:
    docs = (
        db.collection("reports")
        .where("userId", "==", user_id)
        .order_by("createdAt", direction=firestore.Query.DESCENDING)
        .limit(50)
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def get_report_by_id(report_id: str) -> dict:
    """Get a specific report by ID."""
    doc = db.collection("reports").document(report_id).get()
    if doc.exists:
        return {"id": doc.id, **doc.to_dict()}
    return None


def update_alert(disease: str, location: str, severity: str, lat: float = 0.0, lng: float = 0.0):
    """
    Upsert an alert. Uses lat/lng for heatmap.
    Each unique disease+location combo = one doc (atomic increment on count).
    """
    alert_id = f"{disease.replace(' ', '_')}_{location.replace(' ', '_')}".lower()
    alert_ref = db.collection("alerts").document(alert_id)

    alert_ref.set({
        "disease":     disease,
        "location":    location,
        "severity":    severity,
        "lat":         lat,           # ← real GPS lat stored here
        "lng":         lng,           # ← real GPS lng stored here
        "count":       firestore.Increment(1),
        "lastUpdated": firestore.SERVER_TIMESTAMP
    }, merge=True)


def get_location_alerts(location: str) -> list:
    docs = (
        db.collection("alerts")
        .where("location", "==", location)
        .order_by("lastUpdated", direction=firestore.Query.DESCENDING)
        .limit(20)
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def get_all_geo_alerts() -> list:
    """
    Returns ALL alerts that have lat/lng — used for heatmap.
    Filters out docs with lat=0,lng=0 (fallback/unknown locations).
    """
    docs = (
        db.collection("alerts")
        .order_by("lastUpdated", direction=firestore.Query.DESCENDING)
        .limit(100)
        .stream()
    )
    results = []
    for doc in docs:
        data = doc.to_dict()
        lat  = data.get("lat", 0)
        lng  = data.get("lng", 0)
        # Only include docs with real coordinates
        if lat != 0 or lng != 0:
            results.append({"id": doc.id, **data})
    return results


def save_feedback(report_id: str, user_id: str, is_correct: bool):
    db.collection("feedback").add({
        "reportId":  report_id,
        "userId":    user_id,
        "isCorrect": is_correct,
        "createdAt": firestore.SERVER_TIMESTAMP
    })