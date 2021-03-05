import pathlib
from typing import Tuple

from PySide2 import QtWidgets, QtCore, QtGui
from pydantic import ValidationError

from api.csv_set import CsvSet
from gui.design.select_mapping_ui import Ui_select_mapping
from api.utils.exceptions import StopError

STR_VALIDATE = "Valider"

STR_WINDOW_TITLE = "Sélection des colonnes"
STR_UNASSIGNED_COLUMNS_ERROR = "Toutes les colonnes n'ont pas été affectées"

STR_INDEX_TYPE = "Index"
STR_COMPARE_TYPE = "Compare"
STR_ERROR = "Erreur"


class SelectMappingWidget(QtWidgets.QWidget):
    validated = QtCore.Signal()

    def __init__(self, resource_dir: pathlib.Path, csv_sets: Tuple[CsvSet, CsvSet]):
        super().__init__()

        self._csv_sets = csv_sets

        self._ui = Ui_select_mapping()
        self._ui.setupUi(self)

        # group widgets
        self._ui.tableViews = [self._ui.tableView0, self._ui.tableView1]

        self._table_models = [MappingModel(self, csv_sets[i]) for i in range(2)]

        # set tableviews
        for i in range(2):
            self._ui.tableViews[i].setModel(self._table_models[i])

            for j in range(2):
                self._ui.tableViews[i].setColumnWidth(j, 289)
        
        # modify widgets
        self._ui.validateBtn.setIcon(QtGui.QIcon(QtGui.QPixmap(str(resource_dir / "svg" / "tick.svg"))))
        self._ui.groupBox0.setTitle(self._csv_sets[0].name + ":")
        self._ui.groupBox1.setTitle(self._csv_sets[1].name + ":")

        # set connections
        self._ui.validateBtn.clicked.connect(self._validate)
        self._ui.cancelBtn.clicked.connect(self.hide)

    def _validate(self):
        try:
            for i in range(2):
                self._csv_sets[i].update_mapping(self._table_models[i].mapping)

        except (StopError, ValidationError) as e:
            QtWidgets.QMessageBox.warning(self, "Erreur", str(e))

        else:
            self.hide()
            self.validated.emit()


class MappingModel(QtCore.QAbstractTableModel):

    def __init__(self, parent, csv_set: CsvSet):
        super().__init__(parent)
        self._csv_set = csv_set

        self._original_columns = self._csv_set.original_columns or []
        self.mapping = self._csv_set.mapping.copy()

        self._modified_columns = [self.mapping.get(col, "") for col in self._original_columns]

    def rowCount(self, parent=None):
        return len(self._original_columns)

    def columnCount(self, parent=None):
        return 2

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return 'Fichier CSV'
                else:
                    return 'Nouveau nom'

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if index.column() == 0 and role == QtCore.Qt.DisplayRole:
            return self._original_columns[index.row()]

        if index.column() == 1 and (role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole):
            return self._modified_columns[index.row()]

    def flags(self, index):
        if index.column() == 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            if value:
                self.mapping[index.siblingAtColumn(0).data()] = value
                self._modified_columns[index.row()] = value
            else:
                self.mapping.pop(index.siblingAtColumn(0).data(), None)
                self._modified_columns[index.row()] = ""
            self.dataChanged.emit(index, index)
            return True
        return False
