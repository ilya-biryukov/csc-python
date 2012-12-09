__author__ = 'Nikita.Tolstikov'

import sys
from algo import graph_builder
from data import shapefile
from data import Serializer
from algo import Exact
from algo import Heuristics

"""Script that all glue work in one.
   Arg1 - path to shape file
   Arg2 - path to dump of graph
   Arg3 - path to dump colors
   """

shape_file_path = sys.argv[1]
graph_file_path = sys.argv[2]
cmap_file_path = sys.argv[3]
reader = shapefile.Reader(shape_file_path)
serializer = Serializer.Serializer()
if reader is None:
    print 'Cannot load shapefile with path'
    sys.exit(0)
records = reader.records()
record_name_id = 4
countries = []
for r in records:
    countries.append(graph_builder.Builder.Builder.build_country(r, record_name_id))

graph = graph_builder.Builder.Builder.build_country_graph_from_countries(countries)
serializer.dump_graph(graph, graph_file_path)

if len(countries) < 15:
    colors_map = Exact.Exact().get_colors_by_graph(graph)
else:
    colors_map = Heuristics.Heurstics().color_graph(graph)

serializer.dump_color_map(colors_map, cmap_file_path)
