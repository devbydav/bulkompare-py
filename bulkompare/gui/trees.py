import re
import logging

from PySide2 import QtGui, QtWidgets

from api.utils.constants import SET_NAME

logger = logging.getLogger(__name__)

COLOR_COLUMN_NAME = QtGui.QColor(218, 224, 227)
COLOR_MODIFICATION = QtGui.QColor(245, 217, 188)
COLOR_DIFFERENT = QtGui.QColor(205, 0, 0)
COLOR_IDENTICAL = QtGui.QColor(0, 155, 0)


class FilterError(Exception):
    """Filter is not valid"""
    pass


def format_row(row):
    col1 = f"{row[0]}: {row[1]}->{row[2]}"
    col2 = ", ".join(row[3:])
    return col1, col2


class AbstractTreeManager:

    def __init__(self,
                 widget: QtWidgets.QTreeWidget,
                 dfs: dict,
                 filterable: bool = False,
                 display_columns: dict = None,
                 compare_columns: dict = None):

        self._widget = widget
        self._original_dfs = dfs
        self._filtered_dfs = dfs  # filtered dfs, this is the source for displayed data

        self._display_columns = display_columns or {}
        self._compare_columns = compare_columns or {}
        self.filterable = filterable  # can we filter ?
        self.filtering = False  # are we filtering ?
        self.nb_total_lines = sum(df.shape[0] for df in dfs.values())
        self.nb_filtered_lines = self.nb_total_lines
        self.filter_text = ""
        self._current_queries = []

        self._make_tree(dfs)

    def _make_tree(self, dfs):
        pass

    def toggle_filtering(self):
        """Change the filtering status"""
        self.filtering = not self.filtering
        if self.nb_total_lines != self.nb_filtered_lines:  # don't remake tree if filtered and original are the same
            if self.filtering:
                logger.debug("toggle and remake tree with filtered")
                self._make_tree(self._filtered_dfs)
            else:
                logger.debug("toggle and remake tree with original")
                self._make_tree(self._original_dfs)

        return self.filtering

    def filter(self, text):
        """Filter the tree with text query"""
        self.filtering = True

        self.filter_text = text
        queries = self.prepare_queries(text)

        if queries != self._current_queries:

            if queries:
                self._filtered_dfs = dict()
                for ext, df in self._original_dfs.items():
                    for positive, column, value in queries:
                        if column in df:
                            try:
                                df = df.query(f"{'' if positive else 'not '} `{column}`.str.match('{value}$')")
                            except re.error as e:
                                raise FilterError(str(e))
                    self._filtered_dfs[ext] = df.copy()
            else:
                self._filtered_dfs = self._original_dfs

            self._current_queries = queries
            self.nb_filtered_lines = sum(df.shape[0] for df in self._filtered_dfs.values())

            self._make_tree(self._filtered_dfs)

    @staticmethod
    def prepare_queries(text):
        """Returns list of tuples containing the query elements"""
        queries = []
        if text != "":
            for filter_str in text.split(" and "):
                search = re.search(r"[:=]", filter_str)
                if not search:
                    raise FilterError(": ou = manquant")

                operator = search.group(0)

                column, value = [v.strip() for v in filter_str.split(operator, maxsplit=1)]

                if column.lower().startswith("not "):
                    column = column[3:].strip()
                    positive = False
                else:
                    positive = True

                if not re.match(r"^[\w?*:,.!% ]+$", value):
                    raise FilterError("Valeur non autorisée dans le filtre")

                value = value.replace(".", "\.").replace("*", ".*").replace("?", ".?")

                queries.append((positive, column, value))
        return queries

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
        # this tree never gets filtered
        self.filterable = False
        self.filtering = False

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
