__author__ = 'Nikita.Tolstikov'

import shapefile
from data import Polygon
from data import SortedPolygon
from data import Country
from data import Graph

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
    def build_sorted_polygon_list(shape_records):
        now_id = 0
        now_sr = 0
        id_map = []
        polygons = []
        for sr in shape_records:
            now_polygons, new_id = Builder.get_sorted_polygons_from_shape(sr, now_id)
            for id in xrange(now_id, new_id):
                id_map[now_sr] = id
            now_id = new_id
            for polygon in now_polygons:
                polygons.append(polygon)
            now_sr += 1

        return polygons, id_map

    @staticmethod
    def merge(points):
        res_points = []
        total_length = 0
        for p in points:
            total_length += len(p)
        inds = [0 for i in xrange(len(points))]
        for i in xrange(total_length):
            min_ind = 0
            for ind in xrange(len(points)):
                if inds[ind] < len(points[ind]) and points[ind][inds[ind]] < points[min_ind][inds[ind]]:
                    min_ind = ind
            res_points.append(points[min_ind][inds[min_ind]])
            inds[min_ind] += 1
        return res_points

    @staticmethod
    def sorted_points(polygons):
        sorted_points = []
        for p in polygons:
            sorted_points.append(p.get_sorted_points())

        return Builder.merge(sorted_points)

    @staticmethod
    def build_polygons_graph(polygons, sorted_points):
        opened = []
        graph = Graph.Graph(len(polygons))
        for p in sorted_points:
            if p.is_first:
                opened.append(p.pid)
            if p.is_last:
                del opened[p.pid]
            for pid in opened:
                if graph.is_adjacent_vertices(p.pid, pid):
                    continue
                if pid == p.id:
                    continue
                assert polygons[pid].id == pid
                if polygons[pid].min_y <= p.y <= polygons[pid].max_y:
                    if Builder.check_in(p, polygons[pid]):
                        graph.add_edge(p.pid, pid)
                        graph.add_edge(pid, p.pid)
        return graph

    @staticmethod
    def build_country_graph(shape_records):
        """Main method returns graph of countries"""

        polygons, id_map  = Builder.build_sorted_polygon_list(shape_records)
        sorted_points = Builder.sorted_points(polygons)
        graph = Builder.build_polygons_graph(polygons, sorted_points)
        graph.merge_by_map(id_map)
        for i in xrange(shape_records):
            graph.add_vertex_name(i, shape_records.record[4])

        return graph

    @staticmethod
    def check_in(point, polygon):

        points = polygon.points
        n = len(points)
        x = point.x
        y = point.y
        inside = False

        #check if point is a vertex
        for p in points:
            if p.x == x and p.y == y:
                return True

        #check if point is on a boundary
        for i in xrange(n):
            if i == 0:
                p1 = polygon[-1]
                p2 = polygon[0]
            else:
                p1 = polygon[i-1]
                p2 = polygon[i]
            if p1.y == p2.y and p1.y == y and min(p1.x, p2.x) < x < max(p1.x, p2.x):
                if p1.x == p2.x and p1.x == x and min(p1.y, p2.y) < y < max(p1.y, p2.y):
                    return True


        p1x = points[0].x
        p1y = points[0].y
        for i in xrange(n + 1):
            p2x = points[i % n].x
            p2y = points[i % n].y
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside
