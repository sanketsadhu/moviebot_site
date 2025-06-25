from flask import Flask, render_template, request
from pyrogram import Client
import os

app = Flask(__name__)

# Telegram bot credentials (replace with your own)
API_ID = int(os.environ.get("API_ID", "123456"))  # from https://my.telegram.org
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

# Initialize Pyrogram bot client
bot = Client("movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.route("/")
def home():
    return "Movie Bot Website is Live!"

@app.route("/movie/<slug>")
def movie_page(slug):
    cid = request.args.get("cid")
    mid = request.args.get("mid")

    if not cid or not mid:
        return "Missing parameters", 400

    try:
        mid = int(mid)
        with bot:
            message = bot.get_messages(cid, mid)

        title = message.caption or "Untitled Movie"
        media = message.video or message.document or None
        size = round(media.file_size / (1024 * 1024), 2) if media else "Unknown"
        poster_url = message.photo.thumbs[-1].file_id if message.photo else None

        download_link = f"https://t.me/{cid.strip('@')}/{mid}"

        return render_template("movie.html",
                               title=title,
                               size=size,
                               slug=slug,
                               download_link=download_link,
                               poster_url=poster_url)
    except Exception as e:
        return f"Error: {str(e)}", 500
