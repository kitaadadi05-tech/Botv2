import asyncio, logging
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from bot_handlers import handle_video, stats_cmd, upload_queue
from config import TELEGRAM_TOKEN, PORT, BASE_URL, ADMIN_CHAT_ID, QUEUE_FILE
from utils import load_json, save_json

logging.basicConfig(level=logging.INFO)
BOT_APP=None

async def auto_retry_engine():
    global BOT_APP
    while True:
        await asyncio.sleep(600)
        if not upload_queue: continue
        item=upload_queue.pop(0)
        try:
            # Retry upload
            save_json(QUEUE_FILE, upload_queue)
        except:
            upload_queue.append(item)
            save_json(QUEUE_FILE, upload_queue)

async def on_startup(app):
    global BOT_APP, upload_queue
    BOT_APP=app
    upload_queue.extend(load_json(QUEUE_FILE,[]))
    asyncio.create_task(auto_retry_engine())
    print("✅ Background engine started")

def main():
    app=ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.post_init=on_startup
    print("🚀 WEBHOOK MODE ACTIVE")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"{BASE_URL}/{TELEGRAM_TOKEN}",
        drop_pending_updates=True
    )

if __name__=="__main__":
    main()
