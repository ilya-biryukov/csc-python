# -*- coding: utf-8 -*-

__author__ = 'Sergey Aganezov Jr.'

import unittest
from algo.Heuristics import *
from data.Graph import *
from algo.Exact import *

class TestSpeed(unittest.TestCase):
    def setUp(self):
        self.heuristics = Heurstics
        self.exact = Exact({})

    def add_rays(self, graph):
        size = graph.get_vertices_count()
        for i in xrange(1, size):
            graph.add_edge(0, i)

    def add_circuit(self, graph):
        size = graph.get_vertices_count()
        for i in xrange(size):
            graph.add_edge(i, (i+1) % size)

    def test_size_10_graph(self):
        graph = Graph(10)

        self.add_rays(graph)

        colors_1 = self.heuristics.color_graph(graph)
        colors_2 = self.exact.get_colors_by_graph(graph)

        self.assertEqual(10, len(colors_1))
        self.assertEqual(2, len(set(colors_1.values())))

        self.assertEqual(10, len(colors_2))
        self.assertEqual(2, len(set(colors_2)))

        self.add_circuit(graph)

        self.exact = Exact({})
        colors_1 = self.heuristics.color_graph(graph)
        colors_2 = self.exact.get_colors_by_graph(graph)

        self.assertEqual(10, len(colors_1))
        self.assertEqual(3, len(set(colors_1.values())))

        self.assertEqual(10, len(colors_2))
        self.assertEqual(3, len(set(colors_2)))

    def test_size_25(self):
        graph = Graph(25)

        self.add_rays(graph)

        colors_1 = self.heuristics.color_graph(graph)
        #why toooo long
        #colors_2 = self.exact.get_colors_by_graph(graph)

        self.assertEqual(25, len(colors_1))
        self.assertEqual(2, len(set(colors_1.values())))

        #self.assertEqual(25, len(colors_2))
        #self.assertEqual(3, len(set(colors_2)))

        self.add_circuit(graph)

        colors_1 = self.heuristics.color_graph(graph)
        #why toooo long
        #colors_2 = self.exact.get_colors_by_graph(graph)

        self.assertEqual(25, len(colors_1))
        self.assertEqual(3, len(set(colors_1.values())))

        #self.assertEqual(25, len(colors_2))
        #self.assertEqual(3, len(set(colors_2)))

    def test_size_100_graph(self):
        graph = Graph(100)

        self.add_rays(graph)

        colors = self.heuristics.color_graph(graph)

        self.assertEqual(100, len(colors))
        self.assertEqual(2, len(set(colors.values())))

        self.add_circuit(graph)

        colors = self.heuristics.color_graph(graph)

        self.assertEqual(100, len(colors))
        self.assertEqual(3, len(set(colors.values())))

    def test_size_300_graph(self):
        graph = Graph(300)

        self.add_rays(graph)

        colors = self.heuristics.color_graph(graph)

        self.assertEqual(300, len(colors))
        self.assertEqual(2, len(set(colors.values())))

        self.add_circuit(graph)

        colors = self.heuristics.color_graph(graph)
        self.assertEqual(300, len(colors))
        self.assertEqual(3, len(set(colors.values())))

if __name__ == "__main__":
    unittest.main()





