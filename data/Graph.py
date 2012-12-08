class Graph(object):
    def __init__(self, vertices_count):
        # Initialize
        self.__vertices = [list() for n in xrange(vertices_count)]
        self.__vertices_names = ['' for n in xrange(vertices_count)]
        pass

    def __init__(self):
        pass

    def add_vertex_name(self, vertex_id, vertex_name):
        self.__vertices_names[vertex_id] = vertex_name

    def get_vertices_count(self):
        return len(self.__vertices)

    def get_vertex_name(self, vertex_ind):
        return self.__vertices_names[vertex_ind]

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
        new_vertices = [list() for n in xrange(len(id_map.keys()))]
        new_names    = [list() for n in xrange(len(id_map.keys()))]
        for key in id_map.keys():
            for ver in id_map[key]:
                for aver in self.__vertices[ver]:
                    if not aver in new_vertices[key]:
                        new_vertices[key].append(aver)
        self.__vertices = new_vertices
        self.__vertices_names = new_names

    def dump(self, fname):
        f = open(fname, 'w')
        f.write(str(len(self.__vertices)))
        for i in xrange(len(self.__vertices)):
            f.write('{0:d}'.format(i))
            for v in self.__vertices[i]:
                f.write('{0:d} '.format(v))
            f.writelines()
        for i in xrange(len(self.__vertices)):
            if self.__vertices_names[i] != '':
                f.write('{0:d} {1}'.format(i, self.__vertices_names[i]))

    def load(self, fname):
        f = open(fname, 'r')
        n = int(f.readline())
        self.__vertices = [list() for i in xrange(n)]
        self.__vertices_names = [list() for i in xrange(n)]
        for i in xrange(len(self.__vertices)):
            ver = f.readline().split(' ')
            for v in xrange(len(ver)):
                self.__vertices[int(ver[0])].append(int(v))
        s = f.readline()
        while s != '':
            v, name = f.readline().split(' ')
            self.__vertices_names[int(v)] = name
