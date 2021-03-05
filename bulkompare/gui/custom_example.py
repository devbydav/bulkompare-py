"""This is an example for custom.py. It is used if custom.py file doesn't exist"""
from PySide2 import QtWidgets, QtCore

from api.utils.exceptions import CustomError


class Custom:
    def __init__(self, config):
        self._config = config

    def tree_item_double_clicked(self, item: QtCore.QModelIndex):
        """Callback when an tree item is double clicked"""
        print(f"Copied {item.data()} to clipboard")
        QtWidgets.QApplication.clipboard().setText(item.data())
