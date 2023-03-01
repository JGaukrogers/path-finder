# path-finder

## Tools
- Ophois: https://github.com/ethicnology/ophois
- Dijkstra library: https://pypi.org/project/dijkstra/
- Overpass API

## Steps
1. get data from openstreepmap (via Overpass or Ophois)
2. Get simplified map and node relationship (edge)
3. For each edge, get the weight
   1. Use the node ids to get the way(s)
   2. Extract needed information from the ways to calculate the weight
4. Run Dijkstra
5. Display the result (how?)

## Some considerations
- We can mock downloading the osm data at firs by using an already downloaded file
- The user has to be able to choose which criteria is important, but we can mock this at first
  - We can just pretend the user wants to get the quietest way