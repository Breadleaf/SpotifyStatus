# Spotify Status

Please read the docs! They will help a LOT.

## Setup

Start here! When first using this program, ensure you run install the requirements with pip.
Personally, I like to use VENV and `pip install -r requirements.txt` for ease of use.
Once that is done, you need to setup your [spotify dev portal](https://developer.spotify.com/)...
see [REDIRECT URI Notes](#redirect-uri-notes) for more details about setup.
Make a new app in the portal and make sure you have your answers ready for the next step.
After that is done, run `STRICT= python3 ./shared/config/generateConfig.py` to finish setup.

### Field Documentation

I am bad at writing docs for config files, my bad.
Hopefully this helps guide you through the setup process.

```
CLIENT_ID = <Should match the Spotify dev portal>
CLIENT_SECRET = <Should match the Spotify dev portal>
REDIRECT_URI = <Should match the Spotify dev portal>, hint: http://localhost:[port]/[endpoint]>
SCOPE = <TBH don't touch this, its not worth>
CACHE_PATH = <TBH don't touch this, its not worth>
DATA_PATH = <TBH don't touch this, its not worth>
DEFAULT_DATA_PATH = <TBH don't touch this, its not worth>
POLLING_DELAY = <Delay in seconds between polling the Spotify API>
IMAGE_WIDTH = <Width of the image for the HTML embed> // depricated
IMAGE_HEIGHT = <Height of the image for the HTML embed> // depricated
```

#### REDIRECT URI Notes

`REDIRECT_URI` doesn't need to be an actual endpoint on a server.
Spotify will redirect you to to that link and you can just copy and paste from the browser into the app.
For example if it is set to `http://localhost/callback`, after authenticating with spotify, it will
redirect you to `http://localhost/callback?code=<Your code here>`.
You will then paste `<Your code here>` into the python app.

## songFetch

## songAPI
