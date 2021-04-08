import sys

from PySide2 import QtWidgets

from gui.main_window import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(1300, 800)
    window.show()
    app.exec_()
