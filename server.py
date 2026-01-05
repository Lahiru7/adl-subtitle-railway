from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="ADL Subtitle Translator")

# LibreTranslate service URL (Railway internal/public)
LIBRETRANSLATE_URL = os.getenv(
    "LIBRETRANSLATE_URL",
    "https://libretranslate-production-7c5c.up.railway.app/translate"
)

class TranslateRequest(BaseModel):
    text: str
    src: str
    dest: str

class TranslateResponse(BaseModel):
    translated_text: str


@app.get("/")
def root():
    return {"status": "ADL Subtitle Translator is running"}


@app.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    try:
        payload = {
            "q": req.text,
            "source": req.src,
            "target": req.dest,
            "format": "text"
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(
            LIBRETRANSLATE_URL,
            json=payload,
            headers=headers,
            timeout=20
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"LibreTranslate error: {response.text}"
            )

        data = response.json()

        if "translatedText" not in data:
            raise HTTPException(
                status_code=500,
                detail="Invalid response from LibreTranslate"
            )

        return {"translated_text": data["translatedText"]}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
