from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

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

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return JSONResponse({
            "success": True,
            "platform": info.get("extractor"),
            "title": info.get("title"),
            "url": info.get("webpage_url")
        })

    except Exception as e:
        error_message = str(e)

        # YouTube bot判定などのとき
        if "Sign in to confirm you’re not a bot" in error_message:
            return JSONResponse({
                "success": False,
                "platform": "youtube",
                "error": "YouTube側の制限により、この動画は現在取得できません。時間を置いて再度お試しください。"
            })

        return JSONResponse({
            "success": False,
            "error": error_message
        }, status_code=400)
