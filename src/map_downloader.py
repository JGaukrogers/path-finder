import subprocess

COMMAND_DOWNLOAD_CITY = './../bin/ophois-3.0-x86_64-linux-musl --help'

res = subprocess.check_output(COMMAND_DOWNLOAD_CITY, shell=True)

print('Return type: ', type(res))

print('Decoded string: ', res.decode('utf-8'))


from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


'''
BS
52.27892

10.52013 10.53462

52.27495


<osm-script>
  <bbox-query e="7.157" n="50.748" s="50.746" w="7.154"/>
  <print/>
</osm-script>


way(10.53462, 52.27892, 52.27495, 10.52013);
out body;



node
  [amenity=drinking_water]
  ({{bbox}});
out;

'''
'''
Ophois usage example:
=====================
$ CITY=Balaguer
$ ./ophois-3.0-x86_64-linux-musl download --city $CITY
$ cat $CITY.osm | ./ophois-3.0-x86_64-linux-musl format | ./ophois-3.0-x86_64-linux-musl extract > $CITY-extracted.graph
$ cat $CITY-extracted.graph | ./ophois-3.0-x86_64-linux-musl simplify --delta 10.0 > $CITY-simplified.graph
'''