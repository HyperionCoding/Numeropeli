from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
import sys

from MainWindow import MainWindow

GRID_SIZE = 10
CELL_SIZE = 50


def window():
    app = QApplication(sys.argv)
    window = MainWindow(GRID_SIZE, CELL_SIZE)
    window.setGeometry(400, 400, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
    window.setWindowTitle("10x10 Numeropeli")

    window.show()
    sys.exit(app.exec_())

window()