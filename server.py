from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import random
import time

app = FastAPI(title="ADL Subtitle Translator")

# 🔥 YOUR RAILWAY LIBRETRANSLATE SERVICE
LIBRE_ENDPOINTS = [
    "https://libretranslate-production-7c5c.up.railway.app/translate"
]

class TranslateRequest(BaseModel):
    text: str
    src: str
    dest: str

class TranslateResponse(BaseModel):
    translated_text: str

@app.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    endpoint = random.choice(LIBRE_ENDPOINTS)

    payload = {
        "q": req.text,
        "source": req.src,
        "target": req.dest,
        "format": "text"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=60
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"LibreTranslate error {response.status_code}: {response.text}"
        )

    try:
        data = response.json()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Invalid JSON response from LibreTranslate"
        )

    if "translatedText" not in data:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected response: {data}"
        )

    return TranslateResponse(translated_text=data["translatedText"])


@app.get("/")
def root():
    return {"status": "ADL Subtitle Translator is running"}
