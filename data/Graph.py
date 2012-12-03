from itertools import repeat

class Graph(object):
    def __init__(self, vertices_count):
        # Initialize
        self.__vertices = [[] for n in repeat(None, vertices_count)]
        self.__vertices_names = [[] for n in repeat(None,vertices_count)]
        pass

    def add_vertex_name(self, vertex_id, vertex_name):
        self.__vertices_names[vertex_id] = vertex_name

    def get_vertices_count(self):
        return len(self.__vertices)

    def get_vertices(self):
        return self.__vertices

    def get_vertex_name(self, vertex_ind):
        return self.__vertices_names[vertex_ind]

    def adjacent_vertices(self, vertex_index):
        return self.__vertices[vertex_index]

    def add_edge(self, from_vertex_id, to_vertex_id):
        self.__vertices[from_vertex_id].append(to_vertex_id)
        self.__vertices[to_vertex_id].append(from_vertex_id)

    def is_adjacent_vertices(self, vertex_id1, vertex_id2):
        return vertex_id2 in self.__vertices[vertex_id1]

    def merge_by_map(self, id_map):
        new_vertices = [[] for n in repeat(None,len(id_map.keys()))]
        new_names    = [[] for n in repeat(None,len(id_map.keys()))]
        for key in id_map.keys():
            for ver in id_map[key]:
                for aver in self.__vertices[ver]:
                    if not aver in new_vertices[key]:
                        new_vertices[key].append(aver)
        self.__vertices = new_vertices
        self.__vertices_names = new_names
