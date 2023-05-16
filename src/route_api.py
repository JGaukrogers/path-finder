import os

from dijkstra import DijkstraSPF
from flask import Flask, render_template, request, url_for, flash, redirect
# from decouple import config

import src.constants as contants
from src.display_map import MapDisplayer
from src.graph_parser import GraphParser
from src.map_downloader import DataDownloader

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
messages = []


def str_to_tuple(str_to_convert: str) -> tuple:
    # TODO: find something that does not run code
    converted_str = eval(str_to_convert)
    if type(converted_str) != tuple:
        raise TypeError
    return converted_str


@app.route('/get_route/<area_name>/<init_point>/<end_point>/<path_way_priority>')
def get_route(area_name, init_point, end_point, path_way_priority):
    # TODO: check that the result is a tuple of floats!
    # TODO: show proper error page if not tuple of floats
    init_point = str_to_tuple(init_point)
    end_point = str_to_tuple(end_point)

    data_downloader = DataDownloader(area_name, ophois=contants.DEFAULT_OPHOIS)
    graph_downloaded = data_downloader.get_simplified_graph()
    if graph_downloaded:
        parser = GraphParser(graph_file_path=contants.SIMPLE_GRAPH_FILENAME_TEMPLATE.format(area_name=area_name),
                             map_file_path=contants.OSM_FILENAME_TEMPLATE.format(area_name=area_name),
                             path_way_priority=path_way_priority)
        graph = parser.parse_simplified_map_to_graph()

        init_point = parser.get_closest_node_id(init_point)
        end_point = parser.get_closest_node_id(end_point)

        dijkstra = DijkstraSPF(graph, init_point)
        displayer = MapDisplayer(graph_parser=parser, dijkstra=dijkstra)
        displayer.get_quietest_way(init_point, end_point, outfile_path=contants.HTML_OUTPATH.format(area_name=area_name))
        return render_template(contants.HTML_OUTFILE.format(area_name=area_name))

    else:
        return '<p>An error occurred</p>'


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        place_name = request.json['place_name'].strip()
        path_way_priority = request.json['path_way_priority']
        start_marker = request.json['start_marker']
        end_marker = request.json['end_marker']

        start_marker = (start_marker['lat'], start_marker['lng'])
        end_marker = (end_marker['lat'], end_marker['lng'])

        if not place_name:
            flash('Place name is required!')
        elif not start_marker:
            flash('Start node is required!')
        elif not end_marker:
            flash('End node is required!')
        else:
            return redirect(url_for('get_route', area_name=place_name, init_point=start_marker, end_point=end_marker,
                                    path_way_priority=path_way_priority))

    return render_template('map.html')
