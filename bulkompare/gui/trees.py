from PySide2 import QtGui, QtWidgets

from api.utils.constants import SET_NAME

COLOR_COLUMN_NAME = QtGui.QColor(218, 224, 227)
COLOR_MODIFICATION = QtGui.QColor(245, 217, 188)
COLOR_DIFFERENT = QtGui.QColor(205, 0, 0)
COLOR_IDENTICAL = QtGui.QColor(0, 155, 0)


def format_row(row):
    col1 = f"{row[0]}: {row[1]}->{row[2]}"
    col2 = ", ".join(row[3:])
    return col1, col2


class AbstractTreeManager:

    def __init__(self,
                 widget: QtWidgets.QTreeWidget,
                 dfs: dict,
                 display_columns: dict = None,
                 compare_columns: dict = None):

        self._widget = widget
        self._original_dfs = dfs

        self._display_columns = display_columns or {}
        self._compare_columns = compare_columns or {}

        self._make_tree(dfs)

    def _make_tree(self, dfs):
        pass


class DifferencesTreeManager(AbstractTreeManager):
    def _make_tree(self, dfs):
        self._widget.setHeaderHidden(True)
        self._widget.setColumnCount(len(max(self._display_columns.values(), key=len))+1)
        self._widget.clear()

        for extension, df in dfs.items():
            nb_diffs = df.shape[0]
            diff = "différences" if nb_diffs > 1 else "différence"
            root = QtWidgets.QTreeWidgetItem(None, [f"{extension}: {nb_diffs} {diff}"])
            self._widget.insertTopLevelItems(0, [root])
            if not df.empty:
                for group_id, item in df.groupby("id"):
                    nb_diffs = item.shape[0]
                    diff = "différences" if nb_diffs > 1 else "différence"
                    node = QtWidgets.QTreeWidgetItem(None, [f"{group_id}: {nb_diffs} {diff}"])
                    root.addChild(node)

                    for row in item.iloc[:, 1:].itertuples(index=False):
                        line = (
                                [f"{row[0]}: {row[1]}->{row[2]}"] +
                                [col + ": " + getattr(row, col) for col in self._display_columns[extension]]
                        )
                        subnode = QtWidgets.QTreeWidgetItem(None, line)
                        node.addChild(subnode)
        header = self._widget.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)

class GenericTreeManager(AbstractTreeManager):
    def _make_tree(self, dfs):
        self._widget.setHeaderHidden(True)
        self._widget.setColumnCount(len(max(self._display_columns.values(), key=len))+1)
        self._widget.clear()

        for extension, df in dfs.items():
            root = QtWidgets.QTreeWidgetItem(None, [extension])

            self._widget.insertTopLevelItems(0, [root])
            if not df.empty:
                for group_id, item in df.groupby("id"):
                    node = QtWidgets.QTreeWidgetItem(None, [group_id])
                    root.addChild(node)

                    for row in item.iloc[:, :].itertuples(index=False, name='Ligne'):
                        line = (
                                [f"set: {getattr(row, SET_NAME)}"] +
                                [col + ": " + getattr(row, col) for col in self._display_columns[extension]]
                        )
                        subnode = QtWidgets.QTreeWidgetItem(None, line)
                        subnode.is_leaf = True
                        node.addChild(subnode)

            root.setExpanded(True)
        header = self._widget.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)


class SummaryTreeManager:
    def __init__(self, widget, results: dict):

        widget.clear()
        widget.setHeaderHidden(True)

        for extension, result in results.items():

            root = QtWidgets.QTreeWidgetItem(None, [f"{extension} : {result.conclusion}"])
            if result.nb_differences + sum(result.nb_in_one) > 0:
                root.setForeground(0, COLOR_DIFFERENT)
            else:
                root.setForeground(0, COLOR_IDENTICAL)
            widget.insertTopLevelItems(0, [root])

            for detail in result.details:
                    node = QtWidgets.QTreeWidgetItem(None, [detail])

                    root.addChild(node)

        header = widget.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)
