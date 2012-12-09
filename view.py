__author__ = 'Nikita.Tolstikov'

__author__ = 'Nikita.Tolstikov'

import sys
from data import Serializer


"""Script that all glue work in one.
   Arg1 - path to dump of graph
   Arg2 - path to dump colors
   """

graph_file_path = sys.argv[1]
cmap_file_path = sys.argv[2]

serializer = Serializer.Serializer()
graph = serializer.load_graph(graph_file_path)
if graph is None:
    print "Cannot load graph from path"

cmap = serializer.load_color_map(cmap_file_path)
if cmap is None:
    print "Cannot load color map from path"