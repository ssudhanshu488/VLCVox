import os
import json
import google.generativeai as genai
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

class VlcAction(BaseModel):
    action: str
    value: Optional[str] = None

response_schema = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": ["play", "pause", "seek", "volume", "next", "previous", "stop", "subtitle_delay", "subtitle_sync", "unknown"]
        },
        "value": {"type": "string"}
    },
    "required": ["action"]
}

def process_command_with_gemini(command: str):
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Extract the VLC media player action and parameters from the user's spoken command: '{command}'.
    Possible actions: play, pause, seek (+30, -15), volume (+10, -5), next, previous, stop, subtitle_delay (+2.5 or -1.0 in seconds), subtitle_sync (for auto-syncing subtitles with audio).
    For volume, if the user says increase or decrease by some percent, use + or - that number.
    For seek, if fast forward to a specific time like 1 hour 50 minutes, calculate in seconds (e.g., +6600).
    For subtitle_delay, if user specifies an amount like "delay subtitles by 2 seconds," use value "+2".
    For general sync requests like "sync subtitles" or "sync the subtitle with the movie," use "subtitle_sync" with no value.
    Respond in JSON only, e.g. {{"action": "seek", "value": "+30"}} or {{"action": "subtitle_sync"}} or {{"action": "unknown"}}.
    """

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            response_schema=response_schema 
        )
    )

    try:
        return response.parsed  # already dict
    except Exception:
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {"action": "unknown"}