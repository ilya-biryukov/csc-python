__author__ = 'ilya'

from PyQt4 import QtOpenGL, QtGui, QtCore

from OpenGL.GL import *
from OpenGL.GLU import *


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
        self.__center = QtCore.QPointF(1.0, 1.0)


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


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glColor(0.5, 1.0, 0.0)
        glBegin(GL_POLYGON)
        glVertex(0.0, 0.0, 0.0)
        glVertex(0.0, 1.0, 0.0)
        glVertex(1.0, 0.0, 0.0)
        glEnd()

        glColor(1.0, 0.5, 0.0)
        glBegin(GL_POLYGON)
        glVertex(0.0, 0.0, 0.0)
        glVertex(0.0, -1.0, 0.0)
        glVertex(-1.0, 0.0, 0.0)
        glEnd()

        glColor(0.0, 0.5, 1.0)
        glBegin(GL_POLYGON)
        glVertex(0.0, 0.0, 0.0)
        glVertex(0.0, 1.0, 0.0)
        glVertex(-1.0, 0.0, 0.0)
        glEnd()

        glColor(0.0, 1.0, 0.5)
        glBegin(GL_POLYGON)
        glVertex(0.0, 0.0, 0.0)
        glVertex(0.0, -1.0, 0.0)
        glVertex(1.0, 0.0, 0.0)
        glEnd()


    def __set_projection(self, w, h):
        # Set up projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        left = -2. / 500 * w
        right = -left
        bottom = -2. / 500 * h
        top = -bottom
        gluOrtho2D(left, right, bottom, top)


    def resizeGL(self, w, h):
        # Set up the viewport
        glViewport(0, 0, w, h)

        aspect = float(w) / h
        self.__set_projection(w, h)


    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        self.__set_projection(self.width(), self.height())



if __name__ == "__main__":
    app = QtGui.QApplication(["Widget demo"])
    win = PolygonViewer(None)
    win.show()
    app.exec_()