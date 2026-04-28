from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}


_classifier = None

def _get_classifier():
    global _classifier
    if _classifier is None:
        logger.info("Loading plant disease model (first request)...")
        
        from transformers import pipeline
        import torch

        _classifier = pipeline(
            "image-classification",
            model="HurudzaAI/plantdiseasedetection1",
            device=-1,                    
            dtype=torch.float32
        )
        logger.info("Model loaded successfully.")
    return _classifier


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS


def analyze_plant_image(image_file) -> dict:
    if not image_file or image_file.filename == '':
        return {"error": "No file selected"}

    if not allowed_file(image_file.filename):
        return {"error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}

    try:
        image = Image.open(image_file.stream).convert("RGB")
    except Exception:
        return {"error": "Invalid image file — could not open"}

    try:
        classifier = _get_classifier()
        results    = classifier(image)

        if not results:
            return {"error": "Model returned no results"}

        top        = results[0]
        disease    = top['label']
        confidence = round(float(top['score']), 4)

        return {"disease": disease, "confidence": confidence}

    except Exception as e:
        logger.error(f"Model inference error: {str(e)}", exc_info=True)
        return {"error": f"Image analysis failed: {str(e)}"}