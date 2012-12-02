import unittest

from algo import  Exact
from data import  Graph

class TestExact(unittest.TestCase):
    def setUp(self):
        self.exact = Exact.Exact({})

    def test_simple_case(self):
        graph = Graph.Graph(2)
        graph.add_edge(0,1)
        colors = self.exact.getColorsByGraph(graph)
        self.assertEqual(2,len(colors))
        self.assertEqual(0,colors[0])
        self.assertEqual(1,colors[1])

    def test_3_case(self):
        graph = Graph.Graph(3)
        graph.add_edge(0,1)
        graph.add_edge(1,2)
        colors = self.exact.getColorsByGraph(graph)
        self.assertEqual(3,len(colors))
        self.assertEqual(0,colors[0])
        self.assertEqual(1,colors[1])
        self.assertEqual(0,colors[2])

    def test_triangle_case(self):
        graph = Graph.Graph(3)
        graph.add_edge(0,1)
        graph.add_edge(1,2)
        graph.add_edge(0,2)

        colors = self.exact.getColorsByGraph(graph)

        self.assertEqual(3,len(colors))
        self.assertEqual(0,colors[0])
        self.assertEqual(1,colors[1])
        self.assertEqual(2,colors[2])

    def test_square_case(self):
        graph = Graph.Graph(4)
        graph.add_edge(0,1)
        graph.add_edge(1,2)
        graph.add_edge(2,3)
        graph.add_edge(0,3)

        colors = self.exact.getColorsByGraph(graph)

        self.assertEqual(4,len(colors))
        self.assertEqual(0,colors[0])
        self.assertEqual(1,colors[1])
        self.assertEqual(0,colors[2])
        self.assertEqual(1,colors[3])