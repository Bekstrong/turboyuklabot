from pytube import YouTube

def download_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        filename = yt.title + ".mp4"
        stream.download(filename=filename)
        return filename
    except Exception as e:
        return str(e)
