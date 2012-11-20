__author__ = 'ilya'

from PyQt4 import QtOpenGL, QtGui

from OpenGL.GL import *
from OpenGL.GLU import *

class PolygonViewer(QtOpenGL.QGLWidget):

    def __init__(self, parent):
        QtOpenGL.QGLWidget.__init__(self, parent)


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