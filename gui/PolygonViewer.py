__author__ = 'ilya'

from PyQt4 import QtOpenGL, QtGui, QtCore

from OpenGL.GL import *
from OpenGL.GLU import *

from data.Polygon import Polygon


# Low-level class, handles drawing, scaling, etc
class PolygonViewerImpl(QtOpenGL.QGLWidget):

    scaleChanged = QtCore.pyqtSignal(float)
    centerChanged = QtCore.pyqtSignal(QtCore.QPointF)
    __MAX_SCALE = 5.0
    __MIN_SCALE = 0.01


    def __init__(self, parent):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.scaleChanged.connect(self.updateGL)
        self.centerChanged.connect(self.updateGL)
        self.__scale = 1.0
        self.__center = QtCore.QPointF(0.0, 0.0)
        self.__polygons = []


    def __set_projection(self, w, h):
        # Set up projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        x = float(w) / 500
        y = float(h) / 500
        gluOrtho2D(-x, x, -y, y)
        # Scale
        glScalef(self.scale, self.scale, 1.0)
        # Translate
        glTranslatef(-self.center.x(), -self.center.y(), 0.0)


    def getScale(self):
        return self.__scale


    @QtCore.pyqtSlot(float)
    def setScale(self, new_scale):
        if new_scale < self.__MIN_SCALE:
            new_scale = self.__MIN_SCALE
        elif new_scale > self.__MAX_SCALE:
            new_scale = self.__MAX_SCALE

        self.__scale = new_scale
        self.makeCurrent()
        self.__set_projection(self.width(), self.height())
        self.scaleChanged.emit(self.__scale)


    scale = property(getScale, setScale)


    def getCenter(self):
        return self.__center


    @QtCore.pyqtSlot(QtCore.QPointF)
    def setCenter(self, pt):
        self.__center = pt
        self.centerChanged.emit(pt)
        self.makeCurrent()
        self.__set_projection(self.width(), self.height())


    center = property(getCenter, setCenter)


    def getPolygons(self):
        return self.__polygons


    @QtCore.pyqtSlot(list)
    def setPolygons(self, polygons):
        self.__polygons = polygons


    polygons = property(getPolygons, setPolygons)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        colors = [(0.5, 1.0, 0.0), (1.0, 0.5, 0.0), (0.0, 0.5, 1.0), (0.0, 1.0, 0.5)]
        for n, poly in enumerate(self.polygons):
            cl = colors[n % 4]
            glColor(cl[0], cl[1], cl[2])
            # Draw polygon
            glBegin(GL_POLYGON)
            for pt in poly.points:
                glVertex(pt.x, pt.y, 0.0)
            glEnd()


    def resizeGL(self, w, h):
        # Set up the viewport
        glViewport(0, 0, w, h)

        aspect = float(w) / h
        self.__set_projection(w, h)


    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        self.__set_projection(self.width(), self.height())



# Handles user interaction
class PolygonViewer(PolygonViewerImpl):
    def __init__(self, parent):
        PolygonViewerImpl.__init__(self, parent)

        self.__last_coord = QtCore.QPoint(0, 0)
        self.setMouseTracking(False)


    def __update_center(self, coord_diff):
        # We'll use OpenGL transformations matrices to find new coordinates of the center
        self.makeCurrent()
        (cx, cy, _) = gluProject(self.center.x(), self.center.y(), 0.0)
        (nx, ny, _) = gluUnProject(cx + coord_diff.x(), cy + coord_diff.y(), 0.0)
        self.center = QtCore.QPointF(nx, ny)


    def __set_cursor_shape(self, shape):
        cursor = self.cursor()
        cursor.setShape(shape)
        self.setCursor(cursor)


    def wheelEvent(self, event):
        # Handle scaling
        scale_diff = event.delta() / 3600.
        self.scale += scale_diff



    def mousePressEvent(self, mouse_event):
        # Remember last coordinates
        self.__last_coord = mouse_event.pos()

        self.__set_cursor_shape(QtCore.Qt.ClosedHandCursor)


    def mouseReleaseEvent(self, mouse_event):
        self.__set_cursor_shape(QtCore.Qt.ArrowCursor)


    def mouseMoveEvent(self, mouse_event):
        pos_diff = mouse_event.pos() - self.__last_coord
        self.__last_coord = mouse_event.pos()
        pos_diff.setX(-pos_diff.x())
        self.__update_center(pos_diff)



if __name__ == "__main__":
    app = QtGui.QApplication(["Widget demo"])
    win = PolygonViewer(None)
    win.show()

    app.exec_()