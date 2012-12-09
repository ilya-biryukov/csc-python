# -*- coding: utf-8 -*-

from copy import deepcopy
from itertools import repeat

__author__ = 'Sergey Aganezov Jr.'

class Heurstics(object):

    def __init__(self):
        pass

    @classmethod
    def color_graph(cls, graph):
        current_color,  colored = 1, 0
        vertices = sorted(enumerate(deepcopy(graph.get_vertices())), key = lambda a: len(a[1]), reverse=True)
        colored_vertices = [0 for x in repeat(None, len(vertices))]
        result = {}
        while colored != len(vertices):
            colored_this_time = []
            index = colored_vertices.index(0)
            colored_vertices[index] = current_color
            colored += 1
            colored_this_time.append(index)
            for vertex in xrange(len(vertices)):
                if colored_vertices[vertex] == 0 and \
                    not any(graph.is_adjacent_vertices(vertices[vertex][0], vertices[c_vertex][0]) for c_vertex in colored_this_time):
                    colored_vertices[vertex] = current_color
                    colored_this_time.append(vertex)
                    colored += 1
            current_color += 1
        for index, item in enumerate(vertices):
            result[item[0]] = colored_vertices[index]
        return result




