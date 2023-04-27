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


@app.route('/get_route/<area_name>/<init_point>/<end_point>/<path_way_priority>')
def get_route(area_name, init_point, end_point, path_way_priority):
    data_downloader = DataDownloader(area_name, ophois=contants.DEFAULT_OPHOIS)
    graph_downloaded = data_downloader.get_simplified_graph()
    if graph_downloaded:
        parser = GraphParser(graph_file_path=contants.SIMPLE_GRAPH_FILENAME_TEMPLATE.format(area_name),
                             map_file_path=contants.OSM_FILENAME_TEMPLATE.format(area_name),
                             path_way_priority = path_way_priority)
        graph = parser.parse_simplified_map_to_graph()
        dijkstra = DijkstraSPF(graph, init_point)
        displayer = MapDisplayer(graph_parser=parser, dijkstra=dijkstra)
        displayer.get_quietest_way(init_point, end_point, outfile_path=contants.HTML_OUTPATH.format(area_name=area_name))
        return render_template(contants.HTML_OUTFILE.format(area_name=area_name))

    else:
        # Give error
        return '<p>An error occurred</p>'


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        place_name = request.form['place_name'].strip()
        start_node = request.form['start_node'].strip()
        end_node = request.form['end_node'].strip()
        path_way_priority = request.form['path_way_priority']

        if not place_name:
            flash('Place name is required!')
        elif not start_node:
            flash('Start node is required!')
        elif not end_node:
            flash('End node is required!')
        else:
            return redirect(url_for('get_route', area_name=place_name, init_point=start_node, end_point=end_node,
                                    path_way_priority=path_way_priority))

    return render_template('index.html')
