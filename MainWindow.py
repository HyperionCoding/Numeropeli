from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5.QtGui import QFontMetrics
from dataclasses import dataclass


@dataclass
class Coordinate:
    x: int
    y: int


class LineEdit(QLineEdit):
    def __init__(self, parent):
        super(LineEdit, self).__init__(parent)

        self.mainwindow = parent

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        if a0.button() == QtCore.Qt.RightButton:
            if self.text() == "":
                self.setText(str(self.mainwindow.next_number))
            else:
                if self.text() != "1":
                    self.mainwindow.clear_tiles(int(self.text()) - 1)
                    self.mainwindow.update_tiles()
        else:
            super(LineEdit, self).mousePressEvent(a0)
        a0.accept()

    # Disable double click and context menu
    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        a0.accept()

    def contextMenuEvent(self, a0: QtGui.QContextMenuEvent) -> None:
        a0.accept()


class MainWindow(QMainWindow):
    def __init__(self, grid_size, cell_size, automark):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.automark = automark

        self.tiles = []
        self.next_number = 1
        self.chain = []

        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        for x in range(0, self.grid_size):
            self.tiles.append([])
            for y in range(0, self.grid_size):
                # Make tile
                textbox = LineEdit(self)
                textbox.setGeometry(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                textbox.setAlignment(QtCore.Qt.AlignCenter)
                font = textbox.font()
                font.setPointSize(4 * self.cell_size / self.grid_size)

                # Resize font to fit 3 characters
                metrics = QFontMetrics(font)
                factor = textbox.rect().width() / metrics.width("999")
                font.setPointSize(font.pointSize() * factor - 5)

                textbox.setFont(font)

                textbox.textChanged.connect(self.update_tiles)

                self.tiles[x].append(textbox)

        self.tiles[0][0].setText("1")

    def update_tiles(self):
        # Reset all tiles
        for x in range(0, self.grid_size):
            for y in range(0, self.grid_size):
                tile = self.tiles[x][y]
                style = "color: red; QLineEdit {background-color: white;}"
                tile.setStyleSheet(style)

        self.chain.clear()

        # Basic coloring
        number = 1
        x = 0
        y = 0
        self.tiles[x][y].setStyleSheet("color: black;")
        while True:
            self.chain.append(Coordinate(x, y))

            tile = self.get_tile(x, y)
            next = self.find_next(x, y, str(number + 1))

            brightness = (100 - number / 2) / 100 * 255

            # No next tile found
            # Mark current green -> last found tile
            if next is None:
                style = "QLineEdit {{background-color: rgb({}, {}, {}); color: green; }}".format(
                    int(brightness), int(brightness), int(127))
                tile.setStyleSheet(style)
                break
            else:  # Mark current black
                style = "QLineEdit {{background-color: rgb({}, {}, {}); color: black; }}".format(
                    int(brightness), int(brightness), int(255))
                tile.setStyleSheet(style)

                x = next.x
                y = next.y
                number = number + 1

        self.next_number = number + 1

        # Mark next possible cells
        neighbours = self.find_neighbours(x, y, True)
        for n in neighbours:
            style = "QLineEdit {{background-color: rgb({}, {}, {}); color: black; }}".format(
                0, 191, 0)
            self.get_tile(n.x, n.y).setStyleSheet(style)

        # Automatically mark tiles when there is only one possibility
        if self.automark:
            if len(neighbours) == 1:
                self.get_tile(neighbours[0].x, neighbours[0].y).setText(str(self.next_number))
                return

        # Mark dead cells
        # A cell is dead when it has only one other cell as possible connection
        for x in range(0, self.grid_size):
            for y in range(0, self.grid_size):
                tile = self.tiles[x][y]

                if tile.text() == "":
                    neighbours = self.find_neighbours(x, y, True)

                    if len(neighbours) < 2:
                        style = "QLineEdit {{background-color: rgb({}, {}, {}); color: black; }}".format(
                            191, 0, 0)
                        tile.setStyleSheet(style)

    # Clear all tiles after this number
    def clear_tiles(self, number):
        for i in range(number, len(self.chain)):
            coord = self.chain[i]
            tile = self.get_tile(coord.x, coord.y)
            tile.blockSignals(True)
            tile.setText("")
            tile.blockSignals(False)

    # Find where the next tile in order is
    def find_next(self, x, y, num):
        for c in self.find_neighbours(x, y):
            if self.get_tile(c.x, c.y).text() == str(num):
                return c

        return None

    # Find coordinates of neighbouring cells
    # Set is_empty True to count only cells that don't have a value
    def find_neighbours(self, x, y, is_empty=False):
        lookup = [Coordinate(x + 3, y),
                  Coordinate(x - 3, y),
                  Coordinate(x, y + 3),
                  Coordinate(x, y - 3),
                  Coordinate(x + 2, y + 2),
                  Coordinate(x + 2, y - 2),
                  Coordinate(x - 2, y + 2),
                  Coordinate(x - 2, y - 2), ]

        neighbours = []

        for c in lookup:
            tile = self.get_tile(c.x, c.y)
            if tile is not None:
                if is_empty:
                    if tile.text() == "":
                        neighbours.append(c)
                else:
                    neighbours.append(c)

        return neighbours

    def get_tile(self, x, y):
        if (x < 0) or (x >= self.grid_size) or (y < 0) or (y >= self.grid_size):
            return None
        else:
            return self.tiles[x][y]
