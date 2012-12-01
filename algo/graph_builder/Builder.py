__author__ = 'Nikita.Tolstikov'

import shapefile
from data import Polygon
from data import SortedPolygon
from data import Country

class Builder(object):
    def __init__(self):
        pass

    @staticmethod
    def get_polygons_from_shape(shape):
        parts = shape.parts
        del parts[0]
        num = len(shape.points)
        buf = []
        res_polygons = []
        for i in xrange(num):
            if i == parts[0] and len(buf) > 0:
                res_polygons.append(Polygon.Polygon(buf))
                buf = []
                del parts[0]
            buf.append(shape.points[i])

        return res_polygons

    @staticmethod
    def get_sorted_polygons_from_shape(shape, now_ind):
        parts = shape.parts
        del parts[0]
        num = len(shape.points)
        buf = []
        res_polygons = []
        for i in xrange(num):
            if i == parts[0] and len(buf) > 0:
                res_polygons.append(SortedPolygon.SortedPolygon(buf, now_ind))
                now_ind += 1
                buf = []
                del parts[0]
            buf.append(shape.points[i])

        return res_polygons, now_ind

    @staticmethod
    def build_country(shape_record, country_name_record_id):
        polygons =  Builder.get_polygons_from_shape(shape_record.shape)
        name = shape_record.record[country_name_record_id]
        return Country.Country(name, polygons)

    @staticmethod
    def build_country_sorted(shape_record, country_name_record_id, now_id):
        polygons, new_id =  Builder.get_sorted_polygons_from_shape(shape_record.shape, now_id)
        name = shape_record.record[country_name_record_id]
        return Country.Country(name, polygons), now_id

    @staticmethod
    def build_country_graph(shape_records):
