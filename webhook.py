import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
VERCEL_URL = os.getenv("VERCEL_URL")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing")

if not VERCEL_URL:
    raise ValueError("VERCEL_URL environment variable is missing")

VERCEL_URL = VERCEL_URL.rstrip("/")
WEBHOOK_URL = f"{VERCEL_URL}/webhook"

response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    json={
        "url": WEBHOOK_URL
    },
    timeout=15
)

print(response.json())
