import os
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("80AFgKWyDCEz4Cwi1qFE8fTdHzQ9wEI-Agjk")
API_ID = os.getenv("2)
API_HASH = os.getenv("4ac1")

if not all([BOT_TOKEN, API_ID, API_HASH]):
    raise ValueError("BOT_TOKEN, API_ID yoki API_HASH belgilanmagan.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    text = (
        "📥 *Video yuklab olish botiga xush kelibsiz!*\n\n"
        "👉 Instagram, TikTok yoki YouTube linkini yuboring, "
        "bot sizga videoni qaytaradi."
    )
    await message.answer(text, parse_mode="Markdown")

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text.strip()
    await message.answer("⏳ Video yuklab olinmoqda...")

    try:
        ydl_opts = {
    'outtmpl': 'video.%(ext)s',
    'format': 'mp4',
    'quiet': True,
    'noplaylist': True,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            await message.reply_video(video, caption="✅ Mana, videongiz tayyor!")

        os.remove(filename)

    except Exception as e:
        await message.answer(f"❌ Video yuklab bo‘lmadi:\n`{e}`", parse_mode="Markdown")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
