from fastapi import FastAPI
from fastapi.responses import JSONResponse
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/download")
def download(url: str):
    try:
        ydl_opts = {
            "format": "best",
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return JSONResponse({
            "title": info.get("title"),
            "url": info.get("webpage_url")
        })

    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=400
        )
