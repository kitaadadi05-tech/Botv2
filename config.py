import os

# Telegram & AI
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
BASE_URL = os.getenv("BASE_URL")
PORT = int(os.getenv("PORT", 8080))

# YouTube OAuth & Scopes
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/yt-analytics.readonly"
]

# Persistent paths
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

TOKEN_FILE = os.path.join(DATA_DIR, "token.json")
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")
STATS_FILE = os.path.join(DATA_DIR, "stats.json")
ANALYTICS_FILE = os.path.join(DATA_DIR, "analytics.json")

# Monetization filter
BANNED_WORDS = ["kill", "blood", "sex", "nude", "weapon", "drug"]
