import logging
import pathlib

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Signal
from pydantic import ValidationError

from api.csv_comparator import CsvComparator
from api.utils.exceptions import StopError
from gui.design.select_columns_ui import Ui_select_columns

logger = logging.getLogger(__name__)

COLOR_INDEX = QtGui.QColor(153, 38, 0)
COLOR_COMPARE = QtGui.QColor(65, 0, 128)
COLOR_DISPLAY = QtGui.QColor(27, 126, 77)
COLOR_IGNORE = QtGui.QColor(59, 59, 59)

STR_TITLE = "Sélection des colonnes"
STR_VALIDATE = "Valider"
STR_COMPARE_ALL = "Tout comparer"
STR_IGNORE_ALL = "Tout ignorer"
STR_COPY_RIGHT = "Copier à droite"
STR_COLUMNS_SELECTIONS = ["Nom", "Index", "Comp", "Afficher", "Ignorer"]
STR_ERR_DIFFERENT_NB_INDEX = "Sélectionner le même nombre de colonnes pour indexer les deux sets"
STR_ERR_DIFFERENT_NB_COMPARE = "Sélectionner le même nombre de colonnes à comparer dans les deux sets"


class SelectColumnsWidget(QtWidgets.QDialog):
    validated = Signal()

    def __init__(self, resource_dir: pathlib.Path, csv_comparator: CsvComparator):
        super().__init__()

        self._csv_comparator = csv_comparator

        self._table_model = ColumnsModel(self, csv_comparator)

        self._ui = Ui_select_columns()
        self._ui.setupUi(self)

        # set icons
        self._ui.validateBtn.setIcon(QtGui.QIcon(QtGui.QPixmap(str(resource_dir / "svg" / "tick.svg"))))

        # set tableview
        self._ui.tableView.setModel(self._table_model)

        self._ui.tableView.setColumnWidth(0, 290)
        for j in range(1, 5):
            self._ui.tableView.setColumnWidth(j, 60)

        # set connections
        self._ui.cancelBtn.clicked.connect(self._cancel)
        self._ui.validateBtn.clicked.connect(self._validate)

        self._ui.tableView.clicked.connect(self.column_selection)
        self._ui.ignoreAllBtn.clicked.connect(self._ignore_all)
        self._ui.compareAllBtn.clicked.connect(self._compare_all)

    def column_selection(self, index):
        # call the setData as if EditRole
        self._table_model.setData(index, None, QtCore.Qt.EditRole)

    def _ignore_all(self,):
        self._table_model.ignore_all()
        
    def _compare_all(self, i):
        self._table_model.compare_all()

    def _cancel(self):
        self.hide()

    def _validate(self):

        index_cols = {column for ((v, _, _, _), column)
                      in zip(self._table_model.columns_selections, self._table_model.available_columns) if v}
        compare_cols = {column for ((_, v, _, _), column)
                        in zip(self._table_model.columns_selections, self._table_model.available_columns) if v}
        display_cols = [column for ((_, _, v, _), column)
                        in zip(self._table_model.columns_selections, self._table_model.available_columns) if v]

        try:
            self._csv_comparator.update_selected_columns(index_columns=index_cols,
                                                         compare_columns=compare_cols,
                                                         display_columns=display_cols)

        except (StopError, ValidationError) as e:
            QtWidgets.QMessageBox.warning(self, "Erreur", str(e))

        else:
            self.hide()
            self.validated.emit()


class ColumnsModel(QtCore.QAbstractTableModel):

    def __init__(self, parent=None, csv_comparator: CsvComparator = None):
        super().__init__(parent)
        self._csv_comparator = csv_comparator

        self.available_columns = [col for col in self._csv_comparator.csv_sets[0].renamed_columns
                                  if col in self._csv_comparator.csv_sets[1].renamed_columns_set]

        self._index_columns = self._csv_comparator.csv_sets[0].index_columns or set()
        self._compare_columns = self._csv_comparator.csv_sets[0].compare_columns or set()
        self._display_columns = self._csv_comparator.csv_sets[0].display_columns or []

        self.columns_selections = []
        for column in self.available_columns:
            index = column in self._index_columns
            compare = column in self._compare_columns
            display = column in self._display_columns
            ignore = not (index or compare or display)
            self.columns_selections.append((index, compare, display, ignore))

    def rowCount(self, parent=None):
        return len(self.columns_selections)

    def columnCount(self, parent=None):
        return 5

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return STR_COLUMNS_SELECTIONS[section]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if index.column() == 0 and (role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole):
            return self.available_columns[index.row()]

        if role == QtCore.Qt.BackgroundRole :
            column_details = self.columns_selections[index.row()]
            if index.column() == 1 and column_details[0]:
                return QtGui.QBrush(COLOR_INDEX)
            if index.column() == 2 and column_details[1]:
                return QtGui.QBrush(COLOR_COMPARE)
            if index.column() == 3 and column_details[2]:
                return QtGui.QBrush(COLOR_DISPLAY)
            if index.column() == 4 and column_details[3]:
                return QtGui.QBrush(COLOR_IGNORE)

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            sel_index, sel_compare, sel_display, sel_ignore = self.columns_selections[row]
            col_clicked = index.column()

            if col_clicked == 4:
                # we ignore all in any case
                sel_index = False
                sel_compare = False
                sel_display = False
            elif col_clicked == 1:
                sel_index = not sel_index
                sel_compare = sel_compare if not sel_index else False
            elif col_clicked == 2:
                sel_compare = not sel_compare
                sel_index = sel_index if not sel_compare else False
            elif col_clicked == 3:
                sel_display = not sel_display

            sel_ignore = not sel_index and not sel_compare and not sel_display

            self.columns_selections[row] = (sel_index, sel_compare, sel_display, sel_ignore)
            self.dataChanged.emit(self.index(row, 1), self.index(row, 4))
            return True
        return False

    def compare_all(self):
        self.layoutAboutToBeChanged.emit()
        self.columns_selections = [(True, False, d, False) if i else (False, True, d, False)
                                   for (i, _, d, _) in self.columns_selections]
        self.layoutChanged.emit()

    def ignore_all(self):
        self.layoutAboutToBeChanged.emit()
        self.columns_selections = [(False, False, False, True)]*len(self.columns_selections)
        self.layoutChanged.emit()

    def set_selection(self, new_selections):
        self.layoutAboutToBeChanged.emit()
        self.columns_selections = [new_selections[col] if col in new_selections else (False, False, False, True)
                                   for col in self.available_columns]
        self.layoutChanged.emit()