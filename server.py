from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from libretranslatepy import LibreTranslateAPI

app = FastAPI(title="ADL Subtitle Translator")

translator = LibreTranslateAPI("https://libretranslate.de")

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
        translated_text = translator.translate(
            req.text,
            req.src,
            req.dest
        )

        return {
            "source": req.src,
            "target": req.dest,
            "original": req.text,
            "translated": translated_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
