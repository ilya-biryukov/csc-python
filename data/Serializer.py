__author__ = 'Nikita.Tolstikov'

class Serializer(object):
    def __init__(self):
        pass

    def __dump_obj(self, obj, path):
        f = open(path, "w")
        f.write("I dump something")
        f.close()

    def dump_graph(self, graph, path):
        self.__dump_obj(graph, path)

    def dump_color_map(self, cmap, path):
        self.__dump_obj(cmap, path)

    def __load_obj(self, path):
        f = open(path, "w")
        f.write("I load something")
        f.close()

    def load_graph(self, path):
        self.__load_obj(path)

    def load_color_map(self, path):
        self.__load_obj(path)
