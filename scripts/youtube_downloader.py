import sys

import yt_dlp

if len(sys.argv) > 1:
    ydl_opts = {
        "outtmpl": "videos/%(title)s.%(ext)s",
        "format": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best[height<=480]",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([sys.argv[1]])
