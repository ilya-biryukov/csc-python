import sys
from algo import graph_builder
from data import shapefile
from data import Serializer
from algo import Exact
from algo import Heuristics

__author__ = 'Nikita.Tolstikov'

def print_usage():
    print \
    """Usage: python convert.py <shapefile-path> <output-file-path>"""

def load_countries(shape_file_path):
    reader = shapefile.Reader(shape_file_path)
    records = reader.shapeRecords()
    record_name_id = 4
    countries = []
    for r in records:
        countries.append(graph_builder.Builder.build_country(r, record_name_id))
    return countries


def main():
    if len(sys.argv) != 3:
        print_usage()
        return
    shape_file_path = sys.argv[1]
    out_file_path = sys.argv[2]

    print "Loading countries..."
    countries = load_countries(shape_file_path)
    print str.format("Loaded {0} countries", len(countries))

    print "Building graph..."
    graph = graph_builder.Builder.build_country_graph_from_countries(countries)
    print str.format("Loaded graph of {0} vertices", graph.get_vertices_count())

    print "Coloring graph..."
    if len(countries) < 15:
        print "Using exact algorithm"
        colors_map = Exact.Exact().get_colors_by_graph(graph)
    else:
        print "Using approximation algorithm"
        colors_map = Heuristics.Heurstics().color_graph(graph)

    print "Dumping results..."
    Serializer.Serializer.dump_to_file(countries, colors_map, out_file_path)



if __name__ == "__main__":
    main()
