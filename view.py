import sys
from PyQt4 import QtCore, QtGui
from data import Serializer
from gui import PolygonViewer

__author__ = 'Nikita.Tolstikov'

class ApplicationController(QtCore.QObject):

    appReady = QtCore.pyqtSignal()

    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)

    @QtCore.pyqtSlot(bool)
    def onCountriesPreparing(self, started):
        if started:
            text = "Tessellating polygons..."
        else:
            text = "Tessellation done."
            self.appReady.emit()
        print text



def print_usage():
    print \
    """Usage: python view.py <precalculated_data>"""


def main():
    if len(sys.argv) != 2:
        print_usage()
        return

    filename = sys.argv[1]

    print "Loading precalculated results..."
    countries, color_map = Serializer.Serializer.load_from_file(filename)
    print str.format("Loaded {0} countries.", len(countries))

    app = QtGui.QApplication(["Graph viewer"])

    app_controller = ApplicationController(None)

    viewer = PolygonViewer.PolygonViewer(None)
    viewer.countriesPreparing.connect(app_controller.onCountriesPreparing)
    viewer.tryBeginSetCountries(countries, color_map)

    app_controller.appReady.connect(viewer.show)

    app.exec_()


if __name__ == "__main__":
    main()