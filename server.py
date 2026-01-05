from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from libretranslatepy import LibreTranslate

app = FastAPI(title="ADL Subtitle Translator")

lt = LibreTranslate("https://libretranslate.de")

class TranslateRequest(BaseModel):
    text: str
    src: str = "en"
    dest: str = "si"

@app.get("/")
def root():
    return {"status": "ADL Subtitle Translator is running"}

@app.post("/translate")
def translate(req: TranslateRequest):
    try:
        translated = lt.translate(
            req.text,
            source=req.src,
            target=req.dest
        )
        return {
            "source": req.src,
            "target": req.dest,
            "original": req.text,
            "translated": translated
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
