import os
import uuid
from pathlib import Path

def cleanup_file(path: str) -> None:
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

def generate_temp_filename(prefix: str = "temp", suffix: str = "") -> str:
    unique_id = uuid.uuid4().hex
    if suffix and not suffix.startswith('.'):
        suffix = f".{suffix}"
    return f"{prefix}_{unique_id}{suffix}"

def safe_get_gemini_text(response) -> str:
    try:
        if hasattr(response, "text"):  # some SDKs expose .text
            return response.text.strip()
        elif isinstance(response, dict):  # JSON response
            return response.get("output", "No output from Gemini").strip()
        elif hasattr(response, "candidates"):  # candidate-based response
            return response.candidates[0].content.parts[0].text.strip()
    except Exception as e:
        print(f"[Gemini Parsing Error] {e}")
    
    # Fallback if all parsing attempts fail
    return "Unable to parse Gemini response"
