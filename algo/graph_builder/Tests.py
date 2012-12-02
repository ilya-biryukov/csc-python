__author__ = 'Tolstikov.Nikita'

import unittest
import shapefile
import Builder
from data import SortedPoint
from data import SortedPolygon

class BuilderTests(unittest.TestCase):
    def setUp(self):
        self.shape_records = reader = shapefile.Reader('WORLD_MAP/WORLD_MAP').shapeRecords();
        self.test_polygon = SortedPolygon.SortedPolygon([(4., 3.),
                                                         (4., 1.),
                                                         (1., 1.),
                                                         (1., 2.),
                                                         (3., 4.),
                                                         (5., 4.),
                                                         (8., 6.),
                                                         (7., 1.),
                                                         (4., 3.)], 0)

        self.additional_polygon_1 = SortedPolygon.SortedPolygon([(7., 4.),
                                                                 (7., 7.),
                                                                 (2., 7.),
                                                                 (2., 4.),
                                                                 (7., 4.)], 1)
        self.additional_polygon_2 = SortedPolygon.SortedPolygon([(8., 1.),
                                                                 (6., 1.),
                                                                 (5., 2.),
                                                                 (4., 0.),
                                                                 (8., 0.)], 2)

    def test_check_in_in(self):
        """
         Test for correct work check_in function for in
        """
        pointsIn = [SortedPoint.SortedPoint(2., 2., 1),
                    SortedPoint.SortedPoint(3., 2., 2),
                    SortedPoint.SortedPoint(4., 3., 3),
                    SortedPoint.SortedPoint(2., 3., 4),
                    SortedPoint.SortedPoint(7.5, 3.5, 5),
                    SortedPoint.SortedPoint(6., 4., 6),
                    ]
        for p in pointsIn:
            self.assertTrue(Builder.Builder.check_in(p, self.test_polygon),'Incorrect point %s' % p)

    def test_check_in_out(self):
        """
         Test for correct work check_in function for out
        """
        pointsIn = [SortedPoint.SortedPoint(1., 4., 1),
                    SortedPoint.SortedPoint(4., 5., 2),
                    SortedPoint.SortedPoint(5., 1., 3),
                    SortedPoint.SortedPoint(0., 0., 4),
                    SortedPoint.SortedPoint(-1., -1., 5),
                    SortedPoint.SortedPoint(9., 4., 6)
                    ]
        for p in pointsIn:
            self.assertFalse(Builder.Builder.check_in(p, self.test_polygon), 'Incorrect point %s' % p)

    def test_sorted_points(self):
        polygons = [self.test_polygon, self.additional_polygon_1, self.additional_polygon_2]
        n = len(self.additional_polygon_1.points)
        n += len(self.additional_polygon_2.points)
        n += len(self.test_polygon.points)
        sorted_points = Builder.Builder.sorted_points(polygons)
        self.assertEquals(len(sorted_points), n)
        for i in xrange(1, n):
            self.assertTrue(sorted_points[i].x >= sorted_points[i - 1], 'Bad point {0} with index {1: d}'.format(str(sorted_points[i]), i))

    def test_build_polygons_graph(self):
        polygons = [self.test_polygon, self.additional_polygon_1, self.additional_polygon_2]
        sorted_points = Builder.Builder.sorted_points(polygons)
        graph = Builder.Builder.build_polygons_graph(polygons, sorted_points)
        self.assertTrue(graph.is_adjacent_vertices(0, 1), '0 and 1 dont adj')
        self.assertTrue(graph.is_adjacent_vertices(1, 0), '1 and 0 dont adj')
        self.assertTrue(graph.is_adjacent_vertices(0, 2), '0 and 2 dont adj')
        self.assertTrue(graph.is_adjacent_vertices(2, 0), '2 and 0 dont adj')
        self.assertFalse(graph.is_adjacent_vertices(1, 2), '2 and 0 is adj')