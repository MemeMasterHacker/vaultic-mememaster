#!/usr/bin/env python3
import random, tempfile, subprocess, sys
import requests

SUBS = ["memes", "dankmemes", "ProgrammerHumor", "me_irl"]
EXTS = (".jpg", ".jpeg", ".png", ".gif", ".webp")

def get_meme():
    sub  = random.choice(SUBS)
    sort = random.choice(["hot", "top", "new"])
    r    = requests.get(f"https://www.reddit.com/r/{sub}/{sort}.json?limit=50", timeout=10)
    posts = [p["data"] for p in r.json()["data"]["children"]
             if p["data"].get("url_overridden_by_dest","").lower().endswith(EXTS)]
    return random.choice(posts)["url_overridden_by_dest"]

def download(url):
    ext  = "." + url.split(".")[-1].split("?")[0]
    r    = requests.get(url, timeout=15, stream=True)
    f    = tempfile.NamedTemporaryFile(delete=False, suffix=ext, prefix="meme_")
    [f.write(c) for c in r.iter_content(8192)]
    return f.name

for _ in range(int(sys.argv[1]) if len(sys.argv) > 1 else 1):
    url  = get_meme()
    path = download(url)
    print(url)
    subprocess.Popen(["xdg-open", path])

