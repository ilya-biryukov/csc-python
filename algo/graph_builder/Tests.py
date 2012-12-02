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
        sorted_points = list(Builder.Builder.sorted_points(polygons))
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

    def test_build_country(self):
        for sr in self.shape_records:
            country = Builder.Builder.build_country(sr, 4)
            self.assertEquals(country.name, sr.record[4], 'Name not equals Country - {0}, SR{1}'.format(country.name, sr.record[4]))
            self.assertEqual(len(country.polygons), len(sr.shape.parts), 'Parts count not equals Country - {0}, SR{1}'.format(country.name, sr.record[4]))
            pnum = 0
            for pol in country.polygons:
                pnum += len(pol.points)
            self.assertEqual(pnum, len(sr.shape.points), 'Points number not equals Country - {0}, SR{1}'.format(country.name, sr.record[4]))

    def test_build_sorted_country(self):
        now_id = 0
        for sr in self.shape_records:
            country, new_id = Builder.Builder.build_country_sorted(sr, 4, now_id)
            self.assertEqual(new_id - now_id, len(country.polygons), 'Bad new index on {0}'.format(country.name))
            self.assertEquals(country.name, sr.record[4], 'Name not equals Country - {0}, SR {1}'.format(country.name, sr.record[4]))
            self.assertEqual(len(country.polygons), len(sr.shape.parts), 'Parts count not equals Country - {0}-{1:d}, SR {2}-{3:d}'.format(country.name,len(country.polygons), sr.record[4], len(sr.shape.parts)))
            pnum = 0
            for pol in country.polygons:
                pnum += len(pol.points)
            self.assertEqual(pnum, len(sr.shape.points), 'Points number not equals Country - {0}, SR{1}'.format(country.name, sr.record[4]))

    def test_build_country_graph_2_not_adj(self):
        records = [self.shape_records[0], self.shape_records[1]]
        graph = Builder.Builder.build_country_graph(records)
        self.assertEqual(graph.get_vertices_count(), 2, 'Count of vertex not correct')
        self.assertEqual(graph.get_vertex_name(0), records[0].record[4], 'Names not equals')
        self.assertEqual(graph.get_vertex_name(1), records[1].record[4], 'Names not equals')


    def test_build_part_countries_graph(self):
        records = self.shape_records[0:2]
        graph = Builder.Builder.build_country_graph(records)
        self.assertEquals(graph.get_vertices_count(), len(records), 'Length not equals')
        for i in xrange(len(records)):
            self.assertEquals(graph.get_vertex_name(i), records[i].record[4], 'Name not equals Graph - {0}, SR {1}'.format(graph.get_vertex_name(i), records[i].record[4]))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(BuilderTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
