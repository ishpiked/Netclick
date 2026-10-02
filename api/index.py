import os

import httpx
from fastapi import FastAPI, Request

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

IMAGE_URL = "https://imagehost-pearl.vercel.app/i/d7d6a4dee472.png"
KITSU_URL = "https://t.me/AniKitsuBot"

MESSAGE = """<b>This Bot Is Closed</b>

This bot is no longer available for streaming movies and series. We’ve moved the viewing experience to <b>Kitsu</b>, where you can find and stream movies and series through a more reliable and streamlined system.

For better playback quality, improved server handling, subtitle support, and a smoother overall experience, we recommend switching to <b>Kitsu</b> for all future streaming.

Your existing searches and sessions on this bot will no longer be supported. Please use <b>Kitsu</b> for new searches, stream preparation, and playback.

Thank you for using this bot. We hope to see you on Kitsu."""

KEYBOARD = {
    "inline_keyboard": [
        [
            {
                "text": "Open Kitsu",
                "url": KITSU_URL
            }
        ]
    ]
}


async def send_closed_message(chat_id: int):
    async with httpx.AsyncClient(timeout=15) as client:
        await client.post(
            f"{TELEGRAM_API}/sendPhoto",
            json={
                "chat_id": chat_id,
                "photo": IMAGE_URL,
                "caption": MESSAGE,
                "parse_mode": "HTML",
                "reply_markup": KEYBOARD
            }
        )


@app.get("/")
async def home():
    return {
        "status": "online",
        "message": "This bot is closed. Use Kitsu."
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()

    message = update.get("message")

    if message:
        chat = message.get("chat")

        if chat and chat.get("id"):
            await send_closed_message(chat["id"])

    return {
        "ok": True
    }
