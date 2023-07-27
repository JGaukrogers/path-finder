import os

from dijkstra import DijkstraSPF
from flask import Flask, render_template, request, url_for, flash, redirect

import src.constants as constants
from src.display_map import MapDisplayer
from src.graph_parser import GraphParser
from src.map_downloader import DataDownloader

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
messages = []


@app.route('/get_route/<init_point_lat>/<init_point_lon>/<end_point_lat>/<end_point_lon>/<path_way_priority>')
def get_route(init_point_lat, init_point_lon, end_point_lat, end_point_lon, path_way_priority):
    # TODO: check that the result is a tuple of floats!
    # TODO: show proper error page if not tuple of floats
    area_name = 'test_city'
    init_point = (float(init_point_lat), float(init_point_lon))
    end_point = (float(end_point_lat), float(end_point_lon))

    north = max(init_point_lat, end_point_lat)
    south = min(init_point_lat, end_point_lat)

    east = max(init_point_lon, end_point_lon)
    west = min(init_point_lon, end_point_lon)

    area_boundaries = {'north': north, 'south': south, 'east': east, 'west': west}

    data_downloader = DataDownloader(area_boundaries, ophois=constants.DEFAULT_OPHOIS)
    graph_downloaded = data_downloader.get_simplified_graph()
    if graph_downloaded:
        parser = GraphParser(graph_file_path=constants.SIMPLE_GRAPH_FILENAME_TEMPLATE.format(area_name=area_name),
                             map_file_path=constants.OSM_FILENAME_TEMPLATE.format(area_name=area_name),
                             path_way_priority=path_way_priority)
        graph = parser.parse_simplified_map_to_graph()

        init_point = parser.get_closest_node_id(init_point)
        end_point = parser.get_closest_node_id(end_point)

        dijkstra = DijkstraSPF(graph, parser.nodeId_to_nodes_dict[init_point])
        displayer = MapDisplayer(graph_parser=parser, dijkstra=dijkstra)
        displayer.get_quietest_way(init_point, end_point, outfile_path=constants.HTML_OUTPATH.format(area_name=area_name))
        return render_template(constants.HTML_OUTFILE.format(area_name=area_name))

    else:
        return '<p>An error occurred</p>'


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        path_way_priority = request.json['path_way_priority']
        start_marker = request.json['start_marker']
        end_marker = request.json['end_marker']

        start_marker = (start_marker['lat'], start_marker['lng'])
        end_marker = (end_marker['lat'], end_marker['lng'])

        if not start_marker:
            flash('Start node is required!')
        elif not end_marker:
            flash('End node is required!')
        else:
            return redirect(url_for('get_route', area_name='TEMP', init_point_lat=start_marker[0], init_point_lon=start_marker[1],
                                    end_point_lat=end_marker[0], end_point_lon=end_marker[1],
                                    path_way_priority=path_way_priority))

    return render_template('map.html')
