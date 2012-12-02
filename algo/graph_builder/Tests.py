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
                                                         (7., 4.),
                                                         (8., 6.),
                                                         (7., 1.),
                                                         (4., 3.)], 0)

    def test_check_in_in(self):
        """
         Test for correct work check_in function for in
        """
        pointsIn = [SortedPoint.SortedPoint(2., 2., 1),
                    SortedPoint.SortedPoint(3., 2., 2),
                    SortedPoint.SortedPoint(4., 3., 3),
                    SortedPoint.SortedPoint(2., 3., 4),
                    SortedPoint.SortedPoint(7.5, 3.5, 5),
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
            self.assertFalse(Builder.Builder.check_in(p, self.test_polygon))

if __name__ == '__main__':
    unittest.main()