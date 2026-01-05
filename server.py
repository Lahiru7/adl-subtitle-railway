from fastapi import FastAPI
from pydantic import BaseModel
import aiohttp

app = FastAPI()
LIBRE_URL = "https://libretranslate.de/translate"

class Req(BaseModel):
    text: str
    src: str = "en"
    dest: str = "si"

@app.post("/translate")
async def translate(req: Req):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            LIBRE_URL,
            json={
                "q": req.text,
                "source": req.src,
                "target": req.dest,
                "format": "text"
            }
        ) as r:
            data = await r.json()
            return {"translated": data.get("translatedText", req.text)}
