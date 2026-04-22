import google.generativeai as genai
import re
import json
import os
from dotenv import load_dotenv

load_dotenv()

# FIX #1: Use env variable NAME, not the actual key value
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

# FIX #4: gemini-pro is deprecated — use gemini-1.5-flash
model = genai.GenerativeModel("gemini-1.5-flash")


def get_ai_advice(disease_name: str) -> dict:
    """Get structured AI advice for a detected plant disease."""
    try:
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

Keep language simple and practical for farmers.
"""

        response = model.generate_content(prompt)

        # Extract JSON from response
        clean_text = re.search(r'\{.*\}', response.text, re.DOTALL)
        if not clean_text:
            raise ValueError("No valid JSON found in Gemini response")

        data = json.loads(clean_text.group())
        return data

    except json.JSONDecodeError:
        return {
            "immediate_actions": ["Isolate affected plants", "Consult local agronomist", "Monitor surrounding crops"],
            "diagnostic_context": f"Disease detected: {disease_name}. Please consult an expert for detailed advice.",
            "spread_risk": "Unknown",
            "estimated_yield_impact": "Unknown"
        }
    except Exception as e:
        return {
            "immediate_actions": ["Isolate affected plants", "Consult local agronomist", "Monitor surrounding crops"],
            "diagnostic_context": f"AI advice unavailable: {str(e)}",
            "spread_risk": "Unknown",
            "estimated_yield_impact": "Unknown"
        }