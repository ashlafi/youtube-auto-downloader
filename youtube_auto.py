import requests
import feedparser
import os
import subprocess
import json

CHANNEL_ID = os.getenv("YT_CHANNEL_ID")
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHANNEL = os.getenv("TG_CHANNEL_ID")

LAST_FILE = "last_video.json"


def load_last_video():
    if not os.path.exists(LAST_FILE):
        return None
    return json.load(open(LAST_FILE, "r"))


def save_last_video(video_id):
    json.dump({"id": video_id}, open(LAST_FILE, "w"))


def download_video(url):
    subprocess.run(["yt-dlp", "-f", "best", url, "-o", "video.mp4"])


def send_to_telegram():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    files = {"video": open("video.mp4", "rb")}
    data = {"chat_id": TG_CHANNEL}
    requests.post(url, files=files, data=data)


def run():
    feed = feedparser.parse(RSS_URL)
    latest = feed.entries[0]
    video_id = latest.yt_videoid
    video_url = latest.link

    last = load_last_video()

    if last is None or last["id"] != video_id:
        download_video(video_url)
        send_to_telegram()
        save_last_video(video_id)
        print("New video processed:", video_url)
    else:
        print("No new videos.")


if __name__ == "__main__":
    run()
