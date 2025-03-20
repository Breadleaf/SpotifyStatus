import json
import time
import sys
import os

FILE_PATH = os.path.dirname( os.path.abspath(__file__) )
PROJECT_ROOT_DIR = os.path.join(FILE_PATH, "..")
sys.path.append(PROJECT_ROOT_DIR)

from config import config

from flask import Flask, Response, render_template, send_file

app = Flask(__name__)

def readTrackInfo():
    try:
        dataFile = open(os.path.join(PROJECT_ROOT_DIR, config.DATA_PATH), "r")
        trackInfo = json.load(dataFile)
        dataFile.close()
        return trackInfo
    except Exception as ex:
        print(ex, type(ex))
        sys.exit(1)


@app.route("/stream")
def stream():
    formatResponse = lambda data: "data: " + json.dumps(data) + "\n\n"

    def formatTime(ms):
        totalSec = int(ms) // 1000
        hours, remainder = divmod(totalSec, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"

    def patchData(data):
        data["progress"] = formatTime(data["progress"])
        data["length"] = formatTime(data["length"])

    def eventStream():
        lastData = readTrackInfo()
        patchData(lastData)
        yield formatResponse(lastData)
        while True:
            # TODO: make this value in the config SELF_POLLING_DELAY
            # time.sleep(config.POLLING_DELAY)
            time.sleep(0.6)
            currentData = readTrackInfo()
            patchData(currentData)
            if currentData != lastData:
                yield formatResponse(currentData)
                lastData = currentData

    return Response(eventStream(), mimetype="text/event-stream")


@app.route("/embed")
def embed():
    initialData = readTrackInfo()
    return render_template(
        "embed.html",
        # url = initialData.get("url"),
        cover = initialData.get("cover"),
        artists = initialData.get("artists"),
        title = initialData.get("title"),
        progress = initialData.get("progress"),
        length = initialData.get("length"),
        # height = config.IMAGE_HEIGHT,
        # width = config.IMAGE_WIDTH,
    )


@app.route("/default_cover.jpg")
def default_cover():
    filePath = os.path.join(PROJECT_ROOT_DIR, "default_cover.jpg")
    return send_file(filePath, mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
