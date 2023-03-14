from flask import Flask
from flask import escape
from flask import render_template

import src.constants as contants
from src.display_map import MapDisplayer
from src.graph_parser import GraphParser
from src.map_downloader import DataDownloader
from dijkstra import DijkstraSPF

HTML_OUTFILE = '{}.html'
HTML_OUTPATH = 'src/templates/{}.html'

app = Flask(__name__)


@app.route('/get_route/<area_name>/<init_point>/<end_point>')
def get_route(area_name, init_point, end_point):
    data_downloader = DataDownloader(area_name, ophois=contants.DEFAULT_OPHOIS)
    graph_downloaded = data_downloader.get_simplified_graph()
    if graph_downloaded:
        parser = GraphParser(graph_file_path=contants.SIMPLE_GRAPH_FILENAME_TEMPLATE.format(area_name),
                             map_file_path=contants.OSM_FILENAME_TEMPLATE.format(area_name))
        graph = parser.parse_simplified_map_to_graph()
        dijkstra = DijkstraSPF(graph, init_point)
        displayer = MapDisplayer(graph_parser=parser, dijkstra=dijkstra)
        displayer.get_quietest_way(init_point, end_point, outfile_path=HTML_OUTPATH.format(area_name))
        return render_template(HTML_OUTFILE.format(area_name))

    else:
        # Give error
        return '<p>An error occurred</p>'


@app.route('/')
def index():
    return f'<h1>Index site</h1>'
