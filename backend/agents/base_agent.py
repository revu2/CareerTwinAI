import json
import re
import logging
from typing import Optional, Dict, Any, TypeVar, Type
from pydantic import BaseModel
from ..services.gemini_client import call_llm

logger = logging.getLogger("CareerTwinAI.Agents")

T = TypeVar("T", bound=BaseModel)

class BaseAgent:
    def __init__(self, name: str, role_description: str):
        self.name = name
        self.role_description = role_description

    def _invoke_llm(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        json_mode: bool = True
    ) -> Optional[str]:
        return call_llm(
            prompt=prompt,
            system_instruction=system_instruction or f"You are the {self.name}, {self.role_description}.",
            json_mode=json_mode
        )

    def _parse_json_response(self, text: Optional[str]) -> Optional[Dict[str, Any]]:
        if not text:
            return None
        try:
            # Clean markdown codeblocks if present
            cleaned = text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            return json.loads(cleaned)
        except Exception as e:
            logger.warning(f"Failed to parse LLM JSON output in {self.name}: {e}\nRaw output: {text}")
            # Try regex extraction of first {...}
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except Exception:
                    pass
            return None
