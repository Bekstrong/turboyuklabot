import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("🔽 YouTube yoki TikTok link yuboring!")

@dp.message_handler()
async def download_handler(message: types.Message):
    url = message.text
    await message.answer("⏬ Yuklab olinmoqda...")

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

        with open(video_path, 'rb') as video:
            await message.reply_video(video)
        os.remove(video_path)

    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
