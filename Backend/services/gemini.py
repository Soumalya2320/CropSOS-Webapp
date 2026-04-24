from google import genai
from google.genai import types
import json
import re
import os
import time
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)
MODEL  = "gemini-2.0-flash"


def get_ai_advice(disease_name: str) -> dict:
    """Get structured AI advice — retries on 429 rate limit."""

    prompt = f"""
A plant disease has been detected: {disease_name}.

Generate a structured JSON response with the following fields:
1. immediate_actions: List 3 short actionable steps farmers should take immediately.
2. diagnostic_context: Explain the disease in simple terms (2-3 lines).
3. spread_risk: One word only (Low / Medium / High / Critical).
4. estimated_yield_impact: Percentage range (e.g., "10-20%").

Return ONLY valid JSON. No extra text, no markdown, no backticks.

{{
  "immediate_actions": ["...", "...", "..."],
  "diagnostic_context": "...",
  "spread_risk": "...",
  "estimated_yield_impact": "..."
}}
"""

    # Retry up to 3 times on 429
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=512,
                )
            )

            raw = response.text.strip()
            raw = re.sub(r'^```(?:json)?\s*', '', raw)
            raw = re.sub(r'\s*```$', '', raw)

            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if not match:
                raise ValueError("No JSON in response")

            return json.loads(match.group())

        except Exception as e:
            err_str = str(e)
            logger.warning(f"Gemini attempt {attempt+1} failed: {err_str}")

            # 429 = rate limit — wait and retry
            if '429' in err_str and attempt < 2:
                wait = (attempt + 1) * 5   # 5s, then 10s
                logger.info(f"Rate limited. Waiting {wait}s before retry...")
                time.sleep(wait)
                continue

            # Any other error — return fallback immediately
            break

    # All attempts failed — return useful fallback (app doesn't crash)
    logger.error(f"Gemini failed for '{disease_name}' — using fallback")
    return _fallback(disease_name)


def _fallback(disease_name: str) -> dict:
    """
    Hardcoded fallback for common diseases when Gemini is unavailable.
    Better than generic 'consult agronomist' for demo purposes.
    """
    disease_lower = disease_name.lower()

    if 'early blight' in disease_lower:
        return {
            "immediate_actions": [
                "Remove and destroy all infected lower leaves immediately",
                "Apply copper-based fungicide (e.g. Mancozeb) to healthy foliage",
                "Switch to drip irrigation to keep leaves dry"
            ],
            "diagnostic_context": "Early Blight (Alternaria solani) creates dark concentric ring spots on older leaves. It thrives in warm humid conditions and spreads rapidly through water splash.",
            "spread_risk": "High",
            "estimated_yield_impact": "15-30%"
        }
    elif 'late blight' in disease_lower:
        return {
            "immediate_actions": [
                "Isolate affected plants and remove infected material in sealed bags",
                "Apply systemic fungicide (Metalaxyl + Mancozeb) immediately",
                "Improve field drainage and air circulation"
            ],
            "diagnostic_context": "Late Blight (Phytophthora infestans) causes water-soaked lesions that rapidly turn brown-black. Extremely fast spreading in cool, wet weather.",
            "spread_risk": "Critical",
            "estimated_yield_impact": "30-80%"
        }
    elif 'leaf rust' in disease_lower:
        return {
            "immediate_actions": [
                "Apply triazole fungicide (Tebuconazole) at first sign",
                "Remove heavily infected leaves and burn them",
                "Avoid overhead irrigation"
            ],
            "diagnostic_context": "Leaf Rust causes orange-brown pustules on leaf surfaces. Wind-spread disease that can devastate crops if not treated early.",
            "spread_risk": "High",
            "estimated_yield_impact": "10-25%"
        }
    elif 'healthy' in disease_lower:
        return {
            "immediate_actions": [
                "Continue current irrigation and fertilization schedule",
                "Monitor weekly for early signs of disease",
                "Maintain field hygiene — remove dead plant material"
            ],
            "diagnostic_context": "No disease detected. Your crop appears healthy. Regular monitoring will help catch any issues early.",
            "spread_risk": "Low",
            "estimated_yield_impact": "0%"
        }
    else:
        return {
            "immediate_actions": [
                "Isolate visibly affected plants from healthy ones",
                "Consult a local agronomist with this diagnosis",
                "Monitor surrounding crops closely for the next 48 hours"
            ],
            "diagnostic_context": f"{disease_name} detected. Avoid overhead watering and ensure good air circulation around plants.",
            "spread_risk": "Medium",
            "estimated_yield_impact": "10-20%"
        }