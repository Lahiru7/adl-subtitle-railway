from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiohttp

app = FastAPI()

LIBRE_URL = "https://translate.terraprint.co/translate"

class Req(BaseModel):
    text: str
    src: str = "en"
    dest: str = "si"

@app.post("/translate")
async def translate(req: Req):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                LIBRE_URL,
                json={
                    "q": req.text,
                    "source": req.src,
                    "target": req.dest,
                    "format": "text"
                },
                timeout=60
            ) as r:
                data = await r.json()
                return {"translated": data.get("translatedText", req.text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
