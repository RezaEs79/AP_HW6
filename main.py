from __future__ import unicode_literals
import numpy as np
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QMainWindow, QVBoxLayout, QMenu, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy import arange, sin, pi
import sys
import os
import random
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt5 import QtGui, QtCore

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=8, height=8, dpi=100):
        self.c = 10       # Density
        self.h = 10       # y-intercept
        self.lwidth = 2   # thickness of line matplotlib
        self.delay = 100  # Delay

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set(ylim=[0, self.h], xlim=[0, self.h],
                    #   yticks=np.linspace(0, self.h, self.h+1),
                    #   xticks=np.linspace(0, self.h, self.h+1),
                      xticks=[],yticks=[], # Disable x,y ticks
                      aspect="equal"
                      )
        self.axes.spines[['right', 'top']].set_visible(False)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself after Delay with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(self.delay)

    def update_figure(self):
        if self.h > 0:
            x = np.linspace(0, 10, self.c+1)
            m = self.h/(self.h-(10+(10/self.c)))
            self.axes.plot(x, m*x+self.h, 'k', linewidth=self.lwidth)
            print(self.h)
            self.h = self.h-(10/self.c)
            self.draw()


class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_widget = QWidget(self)
        l = QVBoxLayout(self.main_widget)
        dc = MyDynamicMplCanvas(self.main_widget, width=8, height=8, dpi=100)
        l.addWidget(dc)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()


def main():
    qApp = QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("%s" % progname)
    aw.show()
    sys.exit(qApp.exec_())


if __name__ == '__main__':
    main()
