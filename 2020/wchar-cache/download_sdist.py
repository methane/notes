import requests
import traceback
import json
import os

session = requests.Session()


def projects():
    with open("./top-pypi-packages-365-days.json", "rb") as f:
        top = json.load(f)
    return [p["project"] for p in top["rows"]]

def find_url(proj):
    resp = session.get(f"https://pypi.org/pypi/{proj}/json")
    resp.raise_for_status()
    for u in resp.json()["urls"]:
        if u["packagetype"] == "sdist":
            return u["url"]
    return None

def download_sdist(proj):
    url = find_url(proj)
    if not url:
        # Universal wheel only, maybe.
        print(f"Can not find url for {proj}")
        return
    filename = url[url.rfind('/')+1:]
    if os.path.exists(filename):
        print(f"Exists: {filename}")
        return
    print(f"Saving to {filename}")
    resp = session.get(url)
    resp.raise_for_status()
    with open(filename, "wb") as f:
        f.write(resp.content)

def main():
    projs = projects()
    for p in projs:
        try:
            download_sdist(p)
        except Exception as e:
            traceback.print_exc()
            print(f"Failed to download {p}")

main()
