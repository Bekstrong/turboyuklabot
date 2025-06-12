import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Salom! YouTube video link yuboring.")

@dp.message_handler()
async def download_video(message: types.Message):
    import yt_dlp
    import asyncio
    from os import remove

    url = message.text
    await message.answer("⬇️ Yuklab olinmoqda...")

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

        with open(video_path, 'rb') as video:
            await message.reply_video(video)

        remove(video_path)

    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)