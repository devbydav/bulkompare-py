import sys
import pathlib

from PySide2 import QtWidgets

from gui.main_window import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(root_dir=pathlib.Path(__file__).parent)
    window.resize(1300, 800)
    window.show()
    app.exec_()
