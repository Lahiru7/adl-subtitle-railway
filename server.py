from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiohttp

app = FastAPI()

LIBRE_ENDPOINTS = [
    "https://translate.terraprint.co/translate",
    "https://libretranslate.com/translate",
    "https://libretranslate.de/translate"
]

class Req(BaseModel):
    text: str
    src: str = "en"
    dest: str = "si"

@app.post("/translate")
async def translate(req: Req):
    last_error = None

    for url in LIBRE_ENDPOINTS:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json={
                        "q": req.text,
                        "source": req.src,
                        "target": req.dest,
                        "format": "text"
                    },
                    headers={"Accept": "application/json"},
                    timeout=60
                ) as r:

                    # Ensure JSON response
                    if "application/json" not in r.headers.get("Content-Type", ""):
                        raise Exception(f"Non-JSON response from {url}")

                    data = await r.json()
                    if "translatedText" in data:
                        return {"translated": data["translatedText"]}

        except Exception as e:
            last_error = str(e)
            continue

    raise HTTPException(status_code=500, detail=f"All translators failed: {last_error}")
