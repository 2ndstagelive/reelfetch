import tkinter as tk
from tkinter import messagebox, ttk
import yt_dlp
import instaloader
import threading


def start_download():
    url_or_code = entry.get().strip()
    mode = var.get()
    fmt = format_var.get()

    if not url_or_code or url_or_code == "ここにURLを入力":
        messagebox.showwarning("入力エラー", "URLを入力してください")
        return

    entry.delete(0, tk.END)

    def run():
        try:
            status_label.config(text="ダウンロード中...", fg="blue")
            btn_download.config(state="disabled")

            if mode == 1:
                ydl_opts = {
                    "outtmpl": "%(title)s.%(ext)s"
                }

                if fmt == "最高画質 (Video)":
                    ydl_opts["format"] = "bestvideo+bestaudio/best"

                elif fmt == "低画質 (Video)":
                    ydl_opts["format"] = "worst"

                elif fmt == "音声のみ (MP3)":
                    ydl_opts.update({
                        "format": "bestaudio/best",
                        "postprocessors": [{
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }]
                    })

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_or_code])

            else:
                if "instagram.com" in url_or_code:
                    parts = url_or_code.rstrip("/").split("/")
                    shortcode = parts[-1]
                else:
                    shortcode = url_or_code

                L = instaloader.Instaloader(
                    download_pictures=False,
                    download_comments=False,
                    download_geotags=False,
                    download_metadata_json=False,
                    save_metadata=False
                )

                post = instaloader.Post.from_shortcode(
                    L.context,
                    shortcode
                )

                L.download_post(
                    post,
                    target=f"IG_{post.owner_username}"
                )

            status_label.config(
                text="完了しました！",
                fg="green"
            )

            messagebox.showinfo(
                "成功",
                "保存が完了しました"
            )

        except Exception as e:
            status_label.config(
                text="エラー発生",
                fg="red"
            )

            if "ffmpeg" in str(e).lower():
                messagebox.showerror(
                    "エラー",
                    "MP3変換にはFFmpegが必要です。\nwinget install Gyan.FFmpeg"
                )
            else:
                messagebox.showerror(
                    "エラー",
                    f"失敗しました:\n{e}"
                )

        finally:
            btn_download.config(state="normal")

    threading.Thread(target=run).start()


root = tk.Tk()
root.title("動画・音声ダウンローダー")
root.geometry("420x340")


tk.Label(
    root,
    text="動画・音声ダウンローダー",
    font=("MS Gothic", 16, "bold")
).pack(pady=10)


var = tk.IntVar(value=1)

tk.Radiobutton(
    root,
    text="YouTube",
    variable=var,
    value=1
).pack()

tk.Radiobutton(
    root,
    text="Instagram",
    variable=var,
    value=2
).pack()


tk.Label(
    root,
    text="画質・形式（YouTube用）"
).pack(pady=(10, 0))


formats = [
    "最高画質 (Video)",
    "低画質 (Video)",
    "音声のみ (MP3)"
]

format_var = tk.StringVar()

format_dropdown = ttk.Combobox(
    root,
    textvariable=format_var,
    values=formats,
    state="readonly",
    width=22
)

format_dropdown.pack(pady=5)
format_dropdown.current(0)


entry = tk.Entry(root, width=45)
entry.pack(pady=10)

entry.insert(0, "ここにURLを入力")


def clear_placeholder(event):
    if entry.get() == "ここにURLを入力":
        entry.delete(0, tk.END)


entry.bind("<FocusIn>", clear_placeholder)


btn_download = tk.Button(
    root,
    text="ダウンロード開始",
    command=start_download,
    bg="lightgray",
    font=("MS Gothic", 10, "bold")
)

btn_download.pack(pady=10)


status_label = tk.Label(
    root,
    text="待機中"
)

status_label.pack()


root.mainloop()