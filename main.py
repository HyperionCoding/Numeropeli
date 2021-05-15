import argparse
import sys

from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow

parser = argparse.ArgumentParser(description="Numeropeli")
parser.add_argument("--g", "--grid_size", type=int, metavar="", help="Grid size", default=10)
parser.add_argument("--t", "--tile_size", type=int, metavar="", help="Tile size", default=50)
parser.add_argument("--a", "--auto_mark", action="store_true", help="Number tiles automatically")
args = parser.parse_args()


def window():
    app = QApplication(sys.argv)
    automark = False
    if args.a:
        automark = True
    window = MainWindow(args.g, args.t, automark)
    window.setGeometry(400, 400, args.g * args.t, args.g * args.t)
    window.setWindowTitle("Numeropeli")

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()
