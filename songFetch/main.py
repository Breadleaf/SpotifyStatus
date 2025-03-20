import requests
import json
import time
import sys
import os

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT_DIR = os.path.join(FILE_PATH, "..")
sys.path.append(PROJECT_ROOT_DIR)

from config import config

import spotipy
from spotipy.oauth2 import SpotifyOAuth

spOAuth = SpotifyOAuth(
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    redirect_uri=config.REDIRECT_URI,
    scope=config.SCOPE,
    cache_path=os.path.join(PROJECT_ROOT_DIR, config.CACHE_PATH),
)

sp = spotipy.Spotify(auth_manager=spOAuth)

token_info = spOAuth.get_cached_token()
if not token_info:
    token_info = spOAuth.get_access_token()

def makeSpotipyCall(callback, *args, **kwargs):
    global token_info
    if spOAuth.is_token_expired(token_info):
        token_info = spOAuth.get_access_token()
    return callback(*args, **kwargs)


def getCurrentPlaying():
    track = makeSpotipyCall(sp.current_playback)

    if track and track["item"]:
        if not track["is_playing"]:
            return None

        return {
            "url" : track["item"]["album"]["external_urls"]["spotify"],
            "title" : track["item"]["name"],
            "album" : track["item"]["album"]["name"],
            "cover" : track["item"]["album"]["images"][0]["url"],
            "length" : track["item"]["duration_ms"],
            "progress" : track["progress_ms"],
            "artists" : ", ".join(
              artist["name"] for artist in track["item"]["artists"]
            ),
            # "default" : False
        }

    return None


def writeToDataFile(songInformation):
    if songInformation is None:
        defaultDataPath = os.path.join(PROJECT_ROOT_DIR, config.DEFAULT_DATA_PATH)
        try:
            if os.path.getsize(defaultDataPath) == 0:
                raise ValueError("Default daat file is empty.")

            defaultDataFile = open(defaultDataPath, "r")
            songInformation = json.load(defaultDataFile)
            defaultDataFile.close()
        except (json.JSONDecodeError, ValueError) as ex:
            print(f"Error loading default data: {ex}", type(ex))
            songInformation = {  # Use a safe default structure
                "url": "",
                "title": "N/a",
                "album": "N/a",
                "cover": "default_cover.jpg", #NOTE: add a reminder to not remove default_cover.jpg as it is a fallback
                "length": 0,
                "progress": 0,
                "artists": "N/a",
                # "default": True
            }
        except Exception as ex:
            print(ex, type(ex))
            sys.exit(1)

    try:
        dataFile = open(os.path.join(PROJECT_ROOT_DIR, config.DATA_PATH), "w")
        jsObject = json.dumps(songInformation, indent=2)
        dataFile.write(jsObject)
        dataFile.close()
    except Exception as ex:
        print(ex, type(ex))
        sys.exit(1)


if __name__ == "__main__":
    while True:
        try:
            gcp = getCurrentPlaying()
            print(gcp)
            writeToDataFile(gcp)
        except requests.exceptions.ReadTimeout as ex:
            print("Read timeout occurred, skipping this poll...", ex)
        time.sleep(config.POLLING_DELAY)
