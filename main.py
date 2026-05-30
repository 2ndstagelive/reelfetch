from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# Vercel から Render API を呼べるようにする
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/download")
def download(url: str):
    try:
        ydl_opts = {
            "format": "best",
            "quiet": True,
            "no_warnings": True
        }

        # Instagram / YouTube 共通で情報取得
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return JSONResponse({
            "success": True,
            "title": info.get("title"),
            "url": info.get("webpage_url")
        })

    except Exception as e:
        return JSONResponse(
            {
                "success": False,
                "error": str(e)
            },
            status_code=400
        )
