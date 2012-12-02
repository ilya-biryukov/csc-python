class Graph(object):
    def __init__(self, vertices_count):
        # Initialize
        self.__vertices = [list() for n in xrange(vertices_count)]
        self.__vertices_names = [list() for n in xrange(vertices_count)]
        pass

    def add_vertex_name(self, vertex_id, vertex_name):
        self.__vertices_names[vertex_id] = vertex_name

    def get_vertices_count(self):
        return len(self.__vertices)


    def adjacent_vertices(self, vertex_index):
        return self.__vertices[vertex_index]


    def add_edge(self, from_vertex_id, to_vertex_id):
        self.__vertices[from_vertex_id].append(to_vertex_id)
        self.__vertices[to_vertex_id].append(from_vertex_id)

    def is_adjacent_vertices(self, vertex_id1, vertex_id2):
        for v in self.__vertices[vertex_id1]:
            if v == vertex_id2:
                return True
        return False

    def merge_by_map(self, id_map):
        new_vertices = [list() for n in len(id_map.keys())]
        new_names    = [list() for n in len(id_map.keys())]
        for key in id_map.keys():
            for ver in id_map[key]:
                for aver in self.__vertices[ver]:
                    if not aver in new_vertices[key]:
                        new_vertices[key].append(aver)
        self.__vertices = new_vertices
        self.__vertices_names = new_names
