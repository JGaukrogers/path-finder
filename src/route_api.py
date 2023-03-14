from flask import Flask
from flask import escape
from flask import render_template, request, url_for, flash, redirect

import src.constants as contants
from src.display_map import MapDisplayer
from src.graph_parser import GraphParser
from src.map_downloader import DataDownloader
from dijkstra import DijkstraSPF

HTML_OUTFILE = '{}.html'
HTML_OUTPATH = 'src/templates/{}.html'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'askjnvnswldkcmclmv'
messages = []


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


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        place_name = request.form['place_name'].strip()
        start_node = request.form['start_node'].strip()
        end_node = request.form['end_node'].strip()

        if not place_name:
            flash('Place name is required!')
        elif not start_node:
            flash('Start node is required!')
        elif not end_node:
            flash('End node is required!')
        else:
            return redirect(url_for('get_route', area_name=place_name, init_point=start_node, end_point=end_node))

    return render_template('index.html')
