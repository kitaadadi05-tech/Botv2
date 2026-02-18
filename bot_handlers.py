import tempfile, os, time
from telegram import Update
from telegram.ext import ContextTypes
from ai_metadata import generate_metadata
from youtube_utils import upload_video, detect_category, predict_ctr, title_performance_score
from utils import update_stats, trend_score, monetization_risk_score, detect_shadowban, load_json, save_json
from config import QUEUE_FILE, ADMIN_CHAT_ID

# Dua queue terpisah
retry_queue = []       # Video yang gagal upload
pending_queue = []     # Video siap upload tapi tertunda

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.video:
        return

    video = update.message.video
    caption = update.message.caption or "Viral Short 2026"
    start_time = time.time()
    progress_msg = await update.message.reply_text("🚀 Processing your Short...\n")
    temp_path = ""
    metadata = {}

    try:
        # Step 1: Download
        await progress_msg.edit_text("📥 Step 1/4 - Downloading video...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            temp_path = tmp.name
        file = await context.bot.get_file(video.file_id)
        await file.download_to_drive(temp_path)

        # Step 2: Generate metadata
        await progress_msg.edit_text("🧠 Step 2/4 - Generating AI Metadata...")
        metadata = await generate_metadata(caption)
        metadata["category"] = detect_category(caption)
        ctr_prediction = predict_ctr(metadata["title"])
        performance_score = title_performance_score(metadata["title"])
        shadow_flag = detect_shadowban()
        trend_value = trend_score(metadata["title"])
        risk_score = monetization_risk_score(metadata["title"])

        await progress_msg.edit_text(
            f"🏷 Title: {metadata['title'][:60]}...\n📈 Trend Score: {trend_value}\n🎯 Predicted CTR: {ctr_prediction}%\n"
            f"🏆 Title Score: {performance_score}\n💰 Monetization Risk: {risk_score}%\n🚨 Shadow Risk: {'YES' if shadow_flag else 'NO'}\n\n🚀 Uploading..."
        )

        # Step 3: Upload
        url = await upload_video(temp_path, metadata, progress_msg)
        total_time = round(time.time() - start_time, 2)

        await progress_msg.edit_text(
            f"🎉 UPLOAD SUCCESS 🎉\n🔗 {url}\n⏱ Time: {total_time}s\n🔥 Trend Score: {trend_value}\n💰 Risk: {risk_score}%"
        )

        # Update stats
        update_stats(True)

        # Jika upload selesai tapi ingin antri untuk pengecekan tambahan
        # pending_queue.append({"file": temp_path, "meta": metadata})
        # save_json(QUEUE_FILE, pending_queue)

        os.remove(temp_path)  # Hapus file sementara

    except Exception as e:
        # Masukkan ke retry queue jika gagal
        if temp_path and os.path.exists(temp_path):
            retry_queue.append({"file": temp_path, "meta": metadata})
            save_json(QUEUE_FILE, retry_queue)

        update_stats(False)
        await progress_msg.edit_text(f"⚠️ Upload Failed - Added to Retry Queue\nError: {str(e)[:100]}")


async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = load_json("data/stats.json", {})
    retry_len = len(retry_queue)
    pending_len = len(pending_queue)

    await update.message.reply_text(
        f"📊 Today: {stats.get('today_uploads',0)}\n"
        f"✅ Success: {stats.get('success',0)}\n"
        f"❌ Failed: {stats.get('failed',0)}\n"
        f"📦 Retry Queue: {retry_len}\n"
        f"⏳ Pending Queue: {pending_len}"
    )
