import os

import math
import time

from dijkstra import DijkstraSPF
from flask import Flask, render_template, request, url_for, flash, redirect

from src.constants import MapPoint
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
    test_timestamp = time.time_ns()
    file_name = str(test_timestamp)
    init_point_lat = float(init_point_lat)
    init_point_lon = float(init_point_lon)
    end_point_lat =float(end_point_lat)
    end_point_lon = float(end_point_lon)

    init_point = MapPoint(init_point_lat, init_point_lon)
    end_point = MapPoint(end_point_lat, end_point_lon)

    area_boundaries = get_area_boundaries(init_point, end_point)

    data_downloader = DataDownloader(file_name, area_boundaries, ophois=constants.DEFAULT_OPHOIS)
    graph_downloaded = data_downloader.get_simplified_graph()
    if graph_downloaded:
        parser = GraphParser(graph_file_path=constants.SIMPLE_GRAPH_FILENAME_TEMPLATE.format(file_name=file_name),
                             map_file_path=constants.OSM_FILENAME_TEMPLATE.format(file_name=file_name),
                             path_way_priority=path_way_priority)
        graph = parser.parse_simplified_map_to_graph()

        init_point = parser.get_closest_node_id(init_point)
        end_point = parser.get_closest_node_id(end_point)

        dijkstra = DijkstraSPF(graph, parser.nodeId_to_nodes_dict[init_point])
        displayer = MapDisplayer(graph_parser=parser, dijkstra=dijkstra)
        displayer.get_quietest_way(init_point, end_point, outfile_path=constants.HTML_OUTPATH.format(file_name=file_name))
        return render_template(constants.HTML_OUTFILE.format(file_name=file_name))

    else:
        return '<p>An error occurred</p>'


def three_km_latitude():
    r_earth = 6378 #km
    return (3 / r_earth) * (180 / math.pi)


def three_km_longitude(latitude: float):
    # new_longitude = longitude + (dx / r_earth) * (180 / pi) / cos(latitude * pi/180);
    r_earth = 6378 #km
    return (3 / r_earth) * (180 / math.pi) / math.cos(latitude * math.pi / 180)


def get_area_boundaries(init_point: MapPoint[float], end_point: MapPoint[float]):
    north = max(init_point.lat, end_point.lat)# - three_km_longitude(init_point.lat)
    south = min(init_point.lat, end_point.lat)# + three_km_longitude(end_point.lat)
    east = max(init_point.lon, end_point.lon) + three_km_latitude()
    west = min(init_point.lon, end_point.lon) - three_km_latitude()
    area_boundaries = {'north': north, 'south': south, 'east': east, 'west': west}

    return area_boundaries


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
            return redirect(url_for('get_route', init_point_lat=start_marker[0], init_point_lon=start_marker[1],
                                    end_point_lat=end_marker[0], end_point_lon=end_marker[1],
                                    path_way_priority=path_way_priority))

    return render_template('map.html')
