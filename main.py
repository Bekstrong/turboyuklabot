import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
import yt_dlp

load_dotenv()

BOT_TOKEN = os.getenv("8035007175:AAFgKWyDCEz4Cwi1qFE8fTdHzQ9wEI-Agjk")
API_ID = os.getenv("26385684")
API_HASH = os.getenv("4ac1c8bd9d6acaa")

if BOT_TOKEN is None or API_ID is None or API_HASH is None:
    raise ValueError("BOT_TOKEN, API_ID yoki API_HASH .env fayldan yuklanmadi!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Salom! Instagram, TikTok yoki YouTube link yuboring 🎥")

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text.strip()
    if not any(x in url for x in ["instagram.com", "tiktok.com", "youtube.com", "youtu.be"]):
        await message.reply("Faqat Instagram, TikTok yoki YouTube havolasi yuboring!")
        return

    await message.answer("⏬ Yuklanmoqda...")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'mp4/best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            await message.answer_video(video)

        os.remove(filename)

    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    executor.start_polling(dp)
