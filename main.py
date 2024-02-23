import base64
from typing import Union

from flask import Flask, render_template
from werkzeug import serving

import logic

# The source of the media to be displayed.
WANTED_SOURCE = "chrome"

app = Flask(__name__, static_url_path='/',
            static_folder='./templates',
            template_folder='./templates')

default_log_request = serving.WSGIRequestHandler.log_request


def log_request(self, *args, **kwargs):
    """
    Overrides the default log_request method to prevent logging of requests to the /update route.
    """
    if self.path == '/update':
        return

    default_log_request(self, *args, **kwargs)


def create_thumbnail(raw_thumbnail: Union[bytes, None]):
    """
    Creates a thumbnail URL from raw thumbnail data.
    """
    raw_thumbnail = base64.b64encode(raw_thumbnail).decode('utf-8')
    thumbnail = "data:image/png;base64," + raw_thumbnail if raw_thumbnail else "https://iili.io/HlHy9Yx.png"
    return thumbnail


@app.route('/update')
async def update():
    """
    Route to update media information asynchronously.
    """
    info = await logic.get_media_info(WANTED_SOURCE)
    thumbnail = create_thumbnail(info.thumbnail)
    played = info.current_position / info.length
    remain = 1 - played
    title = info.title
    return {"thumbnail": thumbnail, "played": played, "remain": remain, "title": title}


@app.route('/')
async def index():
    """
    Route to render the main index page asynchronously.
    """
    info = await logic.get_media_info(WANTED_SOURCE)
    thumbnail = create_thumbnail(info.thumbnail)
    played = info.current_position / info.length
    remain = 1 - played
    title = info.title
    return render_template('index.html', thumbnail=thumbnail, played=played, remain=remain, title=title)


if __name__ == "__main__":
    serving.WSGIRequestHandler.log_request = log_request
    app.run("127.0.0.1", 5000)
