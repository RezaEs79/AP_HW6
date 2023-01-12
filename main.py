from __future__ import unicode_literals
import numpy as np
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QMainWindow, QVBoxLayout, QMenu, QSizePolicy,QLabel, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy import arange, sin, pi
import sys
import os
import random
from matplotlib.backends import qt_compat
from PyQt5 import uic, QtCore, QtGui, QtWidgets

use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt5 import QtGui, QtCore

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None,C=20):
        self.c = C       # Density
        self.h = 10       # y-intercept
        self.lwidth = 2   # thickness of line matplotlib
        self.delay = 100  # Delay
        dpi=100
        fig = Figure(figsize=(5, 8), dpi=dpi)
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
    """A canvas that updates itself every second with a new plot."""

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
            # print(f"h={self.h} , c={self.c}" )
            self.h = self.h-(10/self.c)
            self.draw()
        


class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(800, 600)
        self.main_widget = QWidget(self)
        layout = QVBoxLayout(self.main_widget)
        dc = MyDynamicMplCanvas(self.main_widget)
        self.lineEdit_thickness = QtWidgets.QLineEdit("2")
        self.lineEdit_Delay = QtWidgets.QLineEdit("100")
        self.lineEdit_Num = QtWidgets.QLineEdit("20")
        layout.addWidget(dc)
        layout.addWidget(QtWidgets.QLabel("Thickness"))
        layout.addWidget(self.lineEdit_thickness)
        layout.addWidget(QtWidgets.QLabel("Delay"))
        layout.addWidget(self.lineEdit_Delay)
        layout.addWidget(QtWidgets.QLabel("Number of ticks"))
        layout.addWidget(self.lineEdit_Num)
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.lineEdit_thickness.textEdited.connect(self.generate)
        self.lineEdit_Delay.textEdited.connect(self.generate)
        self.lineEdit_Num.textEdited.connect(self.generate)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(self.widget)
    def generate(self):
        """PyQt5 SLOT""" 
        print("Hello world")
        


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
