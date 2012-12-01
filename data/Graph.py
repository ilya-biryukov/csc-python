class Graph(object):
    def __init__(self, vertices_count):
        # Initialize
        self.__vertices = [list() for n in vertices_count]
        self.__vertices_names = [list() for n in vertices_count]
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

