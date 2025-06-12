import os
import uuid
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom! Menga YouTube yoki TikTok silkasini yuboring — videoni yuboraman."
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not any(x in url for x in ["youtube.com", "youtu.be", "tiktok.com"]):
        await update.message.reply_text("❗ Faqat YouTube yoki TikTok havolasini yuboring.")
        return

    await update.message.reply_text("⏳ Yuklab olinmoqda...")

    temp_file = f"{uuid.uuid4()}.mp4"
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': temp_file,
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        with open(temp_file, 'rb') as video:
            await update.message.reply_video(video=video, caption=f"🎬 {info.get('title', 'Video')}")
    except Exception as e:
        logger.error(f"Xatolik: {e}")
        await update.message.reply_text(f"❌ Xatolik: {e}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == '__main__':
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
    app.run_polling()