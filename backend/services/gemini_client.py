import os
import json
import logging
from typing import Optional, Dict, Any
from ..config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger("CareerTwinAI.Gemini")

_genai_client = None

def get_genai_client():
    global _genai_client
    if _genai_client is not None:
        return _genai_client
    
    if not GEMINI_API_KEY:
        return None

    try:
        from google import genai
        _genai_client = genai.Client(api_key=GEMINI_API_KEY)
        return _genai_client
    except Exception as e:
        logger.warning(f"Could not initialize Google GenAI client: {e}")
        return None

def call_llm(
    prompt: str,
    system_instruction: Optional[str] = None,
    json_mode: bool = False,
    temperature: float = 0.7
) -> Optional[str]:
    """Call Google Gemini API if key is available; returns None on failure or missing key."""
    client = get_genai_client()
    if not client:
        return None

    try:
        config_args: Dict[str, Any] = {
            "temperature": temperature,
        }
        if system_instruction:
            config_args["system_instruction"] = system_instruction
        if json_mode:
            config_args["response_mime_type"] = "application/json"

        # Model fallback selection
        models_to_try = [GEMINI_MODEL, "gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash"]
        # Remove duplicates while preserving order
        models_to_try = list(dict.fromkeys(models_to_try))

        last_error = None
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config_args
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as ex:
                last_error = ex
                continue

        logger.warning(f"All Gemini models failed. Last error: {last_error}")
        return None
    except Exception as e:
        logger.warning(f"Error calling Gemini LLM: {e}")
        return None
