__author__ = 'Nikita.Tolstikov'

import shapefile
import random
from data import Point
from data import Polygon
from data import SortedPolygon
from data import SortedPoint
from data import Country
from data import Graph

class Builder(object):
    def __init__(self):
        pass

    @staticmethod
    def get_polygons_from_shape(shape):
        parts = list(shape.parts)
        del parts[0]
        num = len(shape.points)
        buf = []
        res_polygons = []
        for i in xrange(num):
            if len(parts) > 0 and i == parts[0] and len(buf) > 0:
                res_polygons.append(Polygon.Polygon(buf))
                buf = []
                del parts[0]
            buf.append(shape.points[i])
        if len(buf) > 0:
            res_polygons.append(Polygon.Polygon(buf))
        return res_polygons

    @staticmethod
    def get_sorted_polygons_from_shape(shape, now_ind):
        parts = shape.parts
        current_part = 1
        num = len(shape.points)
        buf = []
        res_polygons = []
        for i in xrange(num):
            if len(parts) > current_part and i == parts[current_part] and len(buf) > 0:
                res_polygons.append(SortedPolygon.SortedPolygon(buf, now_ind))
                now_ind += 1
                buf = []
                current_part += 1
            buf.append(shape.points[i])
        if len(buf) > 0:
            res_polygons.append(SortedPolygon.SortedPolygon(buf, now_ind))
            now_ind += 1
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
        return Country.Country(name, polygons), new_id

    @staticmethod
    def build_sorted_polygon_list(shape_records):
        now_id = 0
        now_sr = 0
        id_map = {}
        polygons = []
        for sr in shape_records:
            id_map[now_sr] = list()
            now_polygons, new_id = Builder.get_sorted_polygons_from_shape(sr.shape, now_id)
            for id in xrange(now_id, new_id):
                id_map[now_sr].append(id)
            now_id = new_id
            for polygon in now_polygons:
                polygons.append(polygon)
            now_sr += 1

        return polygons, id_map

    @staticmethod
    def merge(points):
        #res_points = []
        total_length = 0
        for p in points:
            total_length += len(p)
        inds = [0 for i in xrange(len(points))]
        print total_length
        for i in xrange(total_length):
            min_ind = 0
            for ind in xrange(len(points)):
                if inds[min_ind] >=len(points[min_ind]) or inds[ind] < len(points[ind]) and points[ind][inds[ind]].x < points[min_ind][inds[min_ind]].x:
                    min_ind = ind
            #res_points.append(points[min_ind][inds[min_ind]])
            yield points[min_ind][inds[min_ind]]
            inds[min_ind] += 1

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
                if not p.pid in opened:
                    opened.append(p.pid)
            for pid in opened:
                if graph.is_adjacent_vertices(p.pid, pid):
                    continue
                if pid == p.pid:
                    continue
                assert polygons[pid].id == pid
                if polygons[pid].min_y <= p.y <= polygons[pid].max_y:
                    if Builder.check_in(p, polygons[pid]):
                        graph.add_edge(p.pid, pid)
                        graph.add_edge(pid, p.pid)
            if p.is_last:
                assert p.pid in opened
                opened.remove(p.pid)
        return graph

    @staticmethod
    def build_country_graph(shape_records):
        """Main method returns graph of countries"""
        polygons, id_map  = Builder.build_sorted_polygon_list(shape_records)
        print 'Build all polygons'
        sorted_points = Builder.sorted_points(polygons)
        #print 'Merged points' + str(len(sorted_points))
        graph = Builder.build_polygons_graph(polygons, sorted_points)
        print 'Build graph'
        graph.merge_by_map(id_map)
        for i in xrange(len(shape_records)):
            graph.add_vertex_name(i, shape_records[i].record[4])

        return graph

    EPS = 0.00000001
    @staticmethod
    def __det(a, b, c, d):
        return a * d - b * c

    @staticmethod
    def __between(left, right, point):
        return min(left, right) <= point + Builder.EPS <= max(left, right) + Builder.EPS

    @staticmethod
    def __intersection1d(a1, a2, b1, b2):
        if a1 > a2:
            a1, a2 = a2, a1
        if b1 > b2:
            b1, b2 = b2, b1
        return max(a1, b1) <= min(a2, b2)

    @staticmethod
    def __intersection2d(p1, p2, p3, p4):

        if p2 == p3 or p2 == p4 or p1 == p3 or p1 == p4:
            return 'On'

        A1, B1 = p1.y - p2.y, p2.x - p1.x
        C1 = -A1*p1.x - B1*p1.y

        A2, B2 = p3.y - p4.y, p4.x - p3.x
        C2 = -A2*p3.x - B2*p3.y

        ux = p3.x if p3.y > p4.y else p4.x
        uy = p3.y if p3.y > p4.y else p4.y

        det = Builder.__det(A1, B1, A2, B2)
        if abs(det) - Builder.EPS > 0 :
            x = - Builder.__det(C1, B1, C2, B2) / det
            y = - Builder.__det(A1, C1, A2, C2) / det

            #f1 - check is in first segment
            f1 = Builder.__between(p1.x, p2.x, x) and Builder.__between(p1.y, p2.y, y)
            #f2 - check is in second segment
            f2 = Builder.__between(p3.x, p4.x, x) and Builder.__between(p3.y, p4.y, y)
            #f3 - x and y not upper point
            f3 = abs(ux - x) < Builder.EPS and abs(uy - y) < Builder.EPS
            if abs(p2.x - x) < Builder.EPS and abs(p2.y - y) < Builder.EPS and f1 and f2:
                return 'On'
            return f1 and f2 and not f3
        else:
            #det == 0 => parallel lines
            #f1 = matching lines test
            f1 = abs(Builder.__det(A1, C1, A2, C2)) < 0 and abs(Builder.__det(B1, C1, B2, C2))
            #f2 = simple 1d intersection
            f2 = Builder.__intersection1d(p1.x, p2.x, p3.x, p4.x) and Builder.__intersection1d(p1.y, p2.y, p3.y, p4.y)
            return  f1 and f2

    @staticmethod
    def __check_in_polygon(point1, point2, polygon):
        x1, y1, x2, y2 = point1.x, point1.y, point2.x, point2.y
        maxx, minx = max(x1,x2), min(x1,x2)
        maxy, miny = max(y1,y2), min(y1,y2)
        points = polygon.points
        n = len(points)
        lp1 = points[0]
        lx1 = lp1.x
        ly1 = lp1.y
        isIn = False
        for i in xrange(n + 1):
            lp2 = points[i % n]
            lx2 = lp2.x
            ly2 = lp2.y
            if lp1 == lp2:
                continue
            maxxl, minxl = max(lx1,lx2), min(lx1,lx2)
            maxyl, minyl = max(ly1,ly2), min(ly1,ly2)
            if minx > maxxl or maxx < minxl or miny > maxyl or maxy < minyl:
                lp1, lx1, ly1 = lp2, lx2, ly2
                continue
            res = Builder.__intersection2d(point1, point2, lp1, lp2)
            if res == 'On':
                return True
            if res:
                isIn = not isIn
            lp1, lx1, ly1 = lp2, lx2, ly2
        return isIn

    @staticmethod
    def check_in(point, polygon):
        rightx = polygon.get_sorted_points()[-1].x
        leftx = polygon.get_sorted_points()[0].x
        upy = polygon.max_y
        downy = polygon.min_y
        point1 = Point.Point(random.uniform(leftx - 20., leftx - 10.), random.uniform(upy + 10., upy + 20.))
        test1 = Builder.__check_in_polygon(point1, point, polygon)
        point1 = Point.Point(random.uniform(rightx + 10., rightx + 20.), random.uniform(upy + 10., upy + 20.))
        test2 = Builder.__check_in_polygon(point1, point, polygon)
        if test1 != test2:

            point1 = Point.Point(random.uniform(rightx + 10., rightx + 20.), random.uniform(downy - 20., downy - 10.))
            return Builder.__check_in_polygon(point1, point, polygon)
        else:
            return test1

