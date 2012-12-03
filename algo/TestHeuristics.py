# -*- coding: utf-8 -*-

__author__ = 'Sergey Aganezov Jr.'

import unittest
from algo.Heuristics import *
from data.Graph import *

class TestHeuristics(unittest.TestCase):
    def setUp(self):
        self.heuristics = Heurstics({})

    def test_size_3_graph(self):
        graph = Graph(3)
        graph.add_edge(0,1)
        graph.add_edge(1,2)
        colors = Heurstics.color_graph(graph)
        self.assertEqual(3, len(colors))
        self.assertEqual(2,len(set(colors.values())))

    def test_triangle_graph(self):
        graph = Graph(3)
        graph.add_edge(0,1)
        graph.add_edge(1,2)
        graph.add_edge(2,0)
        colors = Heurstics.color_graph(graph)
        self.assertEqual(3, len(colors))
        self.assertEqual(3, len(set(colors.values())))

    def test_full_4_graph(self):
        graph = Graph(4)
        graph.add_edge(0,1)
        graph.add_edge(0,2)
        graph.add_edge(0,3)

        graph.add_edge(1,2)
        graph.add_edge(1,3)

        graph.add_edge(2,3)

        colors = Heurstics.color_graph(graph)

        self.assertEqual(4, len(colors))
        self.assertEqual(4, len(set(colors.values())))

    def test_square_graph(self):
        graph = Graph(4)
        graph.add_edge(0,1)
        graph.add_edge(1,2)
        graph.add_edge(2,3)
        graph.add_edge(3,0)

        colors = Heurstics.color_graph(graph)

        self.assertEqual(4, len(colors))
        self.assertEqual(2, len(set(colors.values())))


