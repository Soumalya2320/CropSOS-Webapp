from transformers import pipeline
from PIL import Image
import os
import uuid


# Load model ONCE at startup — not on every request (performance critical)
print("Loading plant disease model...")
classifier = pipeline(
    "image-classification",
    model="HurudzaAI/plantdiseasedetection1"
)
print("Model loaded successfully.")

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MAX_FILE_SIZE_MB = 10


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS


def analyze_plant_image(image_file) -> dict:
    """Analyze a plant image and return detected disease and confidence."""
    
    # Input validation
    if not image_file or image_file.filename == '':
        return {"error": "No file selected"}

    if not allowed_file(image_file.filename):
        return {"error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}

    # FIX #5: Unique temp file per request — prevents race conditions
    temp_path = f"/tmp/cropsos_{uuid.uuid4().hex}.jpg"

    try:
        # Save temp file
        image_file.save(temp_path)

        # Validate it's actually an image
        try:
            image = Image.open(temp_path).convert("RGB")
        except Exception:
            return {"error": "Invalid image file — could not open"}

        # Run classifier
        results = classifier(image)

        if not results:
            return {"error": "Model returned no results"}

        top_result = results[0]
        disease = top_result['label']
        confidence = round(float(top_result['score']), 4)

        return {
            "disease": disease,
            "confidence": confidence
        }

    except Exception as e:
        return {"error": f"Image analysis failed: {str(e)}"}

    finally:
        # Always clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)