from flask import Flask
from flask import escape
from flask import render_template

from src.map_downloader import DataDownloader

OPHOIS = './bin/ophois'

app = Flask(__name__)


@app.route('/get_route/<area_name>')
def get_route(area_name):
    data_downloader = DataDownloader(area_name, ophois=OPHOIS)
    graph_downloaded = data_downloader.get_simplified_graph()
    if graph_downloaded:
        pass
    else:
        # Give error
        pass
    return f'<h1>Route {escape(area_name)}</h1><p>Map downloaded: {graph_downloaded}</p>'


@app.route('/')
def index(area_name):
    return render_template('index.html')
