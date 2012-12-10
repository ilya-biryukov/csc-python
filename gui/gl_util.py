from itertools import repeat
import random

__author__ = 'ilya'

import numpy
from OpenGL.GLU import *
from OpenGL.GL import *


class MarkedList(object):
    def __init__(self):
        self.__lst = list()
        self.__marks = list()


    def mark(self, m):
        self.__marks.append((len(self.__lst), m))


    def add(self, el):
        self.__lst.append(el)


    def get_marks(self):
        if not len(self.__marks):
            return
        prev_m = self.__marks[0]
        for m in self.__marks[1:]:
            if m[0] != prev_m[0]:
                yield prev_m
            prev_m = m
        if prev_m[0] != len(self.__lst):
            yield prev_m


    def get_marked_intervals(self):
        prev_mark = None
        for m in self.get_marks():
            if prev_mark is None:
                prev_mark = m
                continue
            yield (prev_mark[0], m[0], prev_mark[1])
            prev_mark = m
        if prev_mark is not None:
            yield (prev_mark[0], len(self.__lst), prev_mark[1])



    def get_list(self):
        return self.__lst



class TessellationVertexConsumer(object):
    def vertex_callback(self, triangles, x, y):
        pass



class TriangleConsumer(TessellationVertexConsumer):
    def vertex_callback(self, triangles, x, y):
        triangles.add(x)
        triangles.add(y)



class TriangleStripConsumer(TriangleConsumer):
    def __init__(self):
        self.__prev_1 = None
        self.__prev_2 = None

    def vertex_callback(self, triangles, x, y):
        if not self.__prev_1:
            self.__prev_1 = (x, y)
            return
        if not self.__prev_2:
            self.__prev_2 = (x, y)
            return

        super(TriangleStripConsumer, self).vertex_callback(triangles, self.__prev_1[0], self.__prev_1[1])
        super(TriangleStripConsumer, self).vertex_callback(triangles, self.__prev_2[0], self.__prev_2[1])
        super(TriangleStripConsumer, self).vertex_callback(triangles, x, y)

        self.__prev_1, self.__prev_2 = (self.__prev_2, (x,y))



class TriangleFanConsumer(TriangleConsumer):
    def __init__(self):
        self.__first = None
        self.__prev = None

    def vertex_callback(self, triangles, x, y):
        if not self.__first:
            self.__first = (x, y)
            return
        if not self.__prev:
            self.__prev = (x, y)
            return

        super(TriangleFanConsumer, self).vertex_callback(triangles, self.__first[0], self.__first[1])
        super(TriangleFanConsumer, self).vertex_callback(triangles, self.__prev[0], self.__prev[1])
        super(TriangleFanConsumer, self).vertex_callback(triangles, x, y)

        self.__prev = (x, y)



class Tessellator(object):
    def __init__(self):
        self.__tess = gluNewTess()
        gluTessCallback(self.__tess, GLU_TESS_BEGIN, self.__tess_cb_begin)
        gluTessCallback(self.__tess, GLU_TESS_END, self.__tess_cb_end)
        gluTessCallback(self.__tess, GLU_TESS_COMBINE, self.__tess_cb_combine)
        gluTessCallback(self.__tess, GLU_TESS_VERTEX, self.__tess_cb_vertex)
        self.__triangles = MarkedList()
        self.__current_vertex_consumer = None


    def __tess_cb_vertex(self, v):
        if v is None:
            return
        self.__current_vertex_consumer.vertex_callback(self.__triangles, v[0], v[1])


    def __tess_cb_end(self):
        self.__current_vertex_consumer = None


    def __tess_cb_combine(self, points, vertex_data, weight):
        return points


    def __tess_cb_begin(self, type):
        if type == GL_TRIANGLE_FAN:
            self.__current_vertex_consumer = TriangleFanConsumer()
        elif type == GL_TRIANGLE_STRIP:
            self.__current_vertex_consumer = TriangleStripConsumer()
        elif type == GL_TRIANGLES:
            self.__current_vertex_consumer = TriangleConsumer()
        else:
            raise Error("Incorrect primitive type")


    def tessellate(self, n, poly):
        def yield_points(poly):
            for pt in poly.get_points():
                yield pt.x
                yield pt.y
                yield 0.0

        self.__triangles.mark(n)
        poly_points = numpy.array([p for p in yield_points(poly)], 'd')

        gluTessBeginPolygon(self.__tess, None)
        gluTessBeginContour(self.__tess)
        for pt in xrange(0, len(poly_points), 3):
            gluTessVertex(self.__tess, poly_points[pt : pt + 3], poly_points[pt : pt + 3])
        gluTessEndContour(self.__tess)
        gluTessEndPolygon(self.__tess)


    def compose_result(self, coloring):
        pts = self.__triangles
        colors = self.__compose_colors(None)
        colored_colors = None
        if coloring is not None:
            colored_colors = self.__compose_colors(coloring)
        return PolygonPainter(pts.get_list(), colors, colored_colors)


    def __compose_colors(self, coloring):
        colors = list()
        for mark_interval in self.__triangles.get_marked_intervals():
            points_count = (mark_interval[1] - mark_interval[0]) / 2
            if coloring is not None:
                cl = coloring[mark_interval[2]]
            else:
                cl = mark_interval[2]
            colors.extend(repeat(cl, points_count))
        return colors





def triangulate_and_create_painter(countries, coloring):
    tess = Tessellator()
    for n, country in enumerate(countries):
        for p in country.get_polygons():
            tess.tessellate(n, p)
    return tess.compose_result(coloring)



class PolygonPainter(object):
    def __init__(self, pts, colors, other_colors):
        self.__raw_pts = numpy.array(pts, 'f')
        self.__raw_cls = numpy.array(self.__gen_colors(colors), 'f')
        self.__raw_cls_colored = None
        if other_colors is not None:
            self.__raw_cls_colored = numpy.array(self.__gen_colors(other_colors), 'f')

        self.__raw_render_cls = self.__raw_cls


    def set_use_colors_from_coloring(self, use_coloring):
        if use_coloring and self.__raw_cls_colored is not None:
            self.__raw_render_cls = self.__raw_cls_colored
        elif not use_coloring:
            self.__raw_render_cls = self.__raw_cls


    def init_vbo(self):
        pass


    def paint_vbo(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, self.__raw_pts)
        glColorPointer(4, GL_FLOAT, 0, self.__raw_render_cls)

        points_count = len(self.__raw_pts) / 2
        glDrawArrays(GL_TRIANGLES, 0, points_count)

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)


    def __gen_colors(self, colors):
        color_map = dict()
        generated_colors = list()
        for cl in colors:
            picked_color = None
            if cl not in color_map:
                new_color = (random.random(), random.random(), random.random(), 1.0)
                color_map[cl] = new_color
                picked_color = new_color
            else:
                picked_color = color_map[cl]
            generated_colors.extend(picked_color)
        return generated_colors


