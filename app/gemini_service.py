import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()
KEY=os.getenv("GEMINI_API_KEY","").strip()
MODEL=os.getenv("GEMINI_MODEL","gemini-3.6-flash")
_client=None

def client():
    global _client
    if _client is None:
        if not KEY or KEY=="PASTE_YOUR_GEMINI_API_KEY_HERE":
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env.")
        _client=genai.Client(api_key=KEY)
    return _client

def text(prompt):
    r=client().models.generate_content(model=MODEL,contents=prompt)
    if not getattr(r,"text",None): raise RuntimeError("Gemini returned no text.")
    return r.text.strip()

def image_text(prompt,path:Path):
    b=path.read_bytes()
    mime={".jpg":"image/jpeg",".jpeg":"image/jpeg",".png":"image/png",".webp":"image/webp"}.get(path.suffix.lower(),"image/jpeg")
    r=client().models.generate_content(model=MODEL,contents=[types.Part.from_text(text=prompt),types.Part.from_bytes(data=b,mime_type=mime)])
    if not getattr(r,"text",None): raise RuntimeError("Gemini returned no text.")
    return r.text.strip()
