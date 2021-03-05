import pathlib
from functools import partial

from PySide2 import QtWidgets, QtCore, QtGui
from pydantic import ValidationError

from api.csv_manager import CsvManager
from api.utils.config import GuiConfig
from api.utils.exceptions import StopError
from gui.design.select_dirs_ui import Ui_select_dirs

STR_ERR_EMPTY_NAME = "Entrer un nom pour chaque set"


class SelectSourcesWidget(QtWidgets.QWidget):
    validated = QtCore.Signal()

    def __init__(self, resource_dir: pathlib.Path, manager: CsvManager, config: GuiConfig):
        super().__init__()
        self._resource_dir = resource_dir
        self._manager = manager
        self._config = config

        self._ui = Ui_select_dirs()
        self._ui.setupUi(self)

        # set icons widgets
        self._ui.validateBtn.setIcon(QtGui.QIcon(QtGui.QPixmap(str(self._resource_dir / "svg" / "tick.svg"))))

        # group ui elements
        self._nameLes = [self._ui.nameLe0, self._ui.nameLe1]
        self._dirLes = [self._ui.dir0Le, self._ui.dir1Le]
        self._openBtns = [self._ui.open0Btn, self._ui.open1Btn]

        # update UI with data
        for i in range(2):
            self._nameLes[i].setText(self._manager.names[i])
            self._dirLes[i].setText(str(self._manager.directories[i]))

        for comparator in self._manager.comparators:
            self._ui.extensionsLw.addItem(comparator.extension)

        # setup connections
        self._ui.validateBtn.clicked.connect(self._validate)
        self._ui.cancelBtn.clicked.connect(self.hide)
        self._ui.addBtn.clicked.connect(self._add_extension)
        self._ui.clearBtn.clicked.connect(self._clear_lw)

        sc1 = QtWidgets.QShortcut(QtGui.QKeySequence("Backspace"), self._ui.extensionsLw, self._rm_selected_extension)
        sc2 = QtWidgets.QShortcut(QtGui.QKeySequence("Delete"), self._ui.extensionsLw, self._rm_selected_extension)
        sc1.setContext(QtCore.Qt.WidgetShortcut)
        sc2.setContext(QtCore.Qt.WidgetShortcut)

        for i in range(2):
            self._openBtns[i].clicked.connect(partial(self._open_dir, set_id=i))

    def _rm_selected_extension(self):
        for file_item in self._ui.extensionsLw.selectedItems():
            row = self._ui.extensionsLw.row(file_item)
            self._ui.extensionsLw.takeItem(row)

    def _add_extension(self):
        text, ok = QtWidgets.QInputDialog().getText(self, "Ajout",
                                                    "Extension :",
                                                    QtWidgets.QLineEdit.Normal,
                                                    "")
        if ok and text:
            self._ui.extensionsLw.addItem(text)

    def _clear_lw(self):
        self._ui.extensionsLw.clear()

    def _open_dir(self, set_id):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(str(self._config.csv_dir))
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        if dialog.exec_():
            self._config.csv_dir = dialog.directory().path()  # validator will convert to pathlib
            self._dirLes[set_id].setText(dialog.selectedFiles()[0])

    def _validate(self):
        if self._nameLes[0].text() == "" or self._nameLes[1].text() == "":
            QtWidgets.QMessageBox.warning(self, "Erreur", STR_ERR_EMPTY_NAME)
        else:
            try:
                self._manager.update_sources(names=(self._nameLes[0].text(), self._nameLes[1].text()),
                                             directories=(self._dirLes[0].text(), self._dirLes[1].text()),
                                             extensions=[self._ui.extensionsLw.item(index).text()
                                                         for index in range(self._ui.extensionsLw.count())])

            except (StopError, ValidationError) as e:
                QtWidgets.QMessageBox.warning(self, "Erreur", str(e))

            else:
                self.hide()
                self.validated.emit()
