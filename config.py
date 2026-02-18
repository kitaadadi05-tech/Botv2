import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
BASE_URL = os.getenv("BASE_URL")
PORT = int(os.getenv("PORT", 8080))

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/yt-analytics.readonly"
]

TOKEN_FILE = "token.json"
QUEUE_FILE = "queue.json"
STATS_FILE = "stats.json"
ANALYTICS_FILE = "analytics.json"
PERFORMANCE_FILE = "performance.json"

BANNED_WORDS = ["kill", "blood", "sex", "nude", "weapon", "drug"]
