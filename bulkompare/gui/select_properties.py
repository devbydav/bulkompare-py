from functools import partial
import pathlib, logging
from typing import Tuple

from PySide2 import QtWidgets, QtCore, QtGui
from pydantic import ValidationError

from api.utils.constants import DEFAULT_HEADER, DEFAULT_ENCODING
from api.utils.exceptions import StopError
from api.csv_set import CsvSet
from gui.design.select_properties_ui import Ui_select_properties


logger = logging.getLogger(__name__)


class SelectPropertiesWidget(QtWidgets.QWidget):
    validated = QtCore.Signal()

    def __init__(self, resource_dir: pathlib.Path, csv_sets: Tuple[CsvSet, CsvSet]):
        super().__init__()
        self._csv_sets: Tuple[CsvSet, CsvSet] = csv_sets

        self._ui = Ui_select_properties()
        self._ui.setupUi(self)

        # set icons widgets
        self._ui.validateBtn.setIcon(QtGui.QIcon(QtGui.QPixmap(str(resource_dir / "svg" / "tick.svg"))))

        # # group ui elements
        self._skipBlankLinesCbs = [self._ui.skipBlankLines0Cb, self._ui.skipBlankLines1Cb]
        self._commentLes = [self._ui.comment0Le, self._ui.comment1Le]
        self._headerLes = [self._ui.heading0Le, self._ui.heading1Le]
        self._encodingLes = [self._ui.encoding0Le, self._ui.encoding1Le]
        self._separatorLes = [self._ui.separator0Le, self._ui.separator1Le]
        self._extensionLes = [self._ui.extension0Le, self._ui.extension1Le]
        self._stripCbs = [self._ui.strip0Cb, self._ui.strip1Cb]

        # update UI with data
        for i in range(2):

            self._skipBlankLinesCbs[i].setChecked(self._csv_sets[i].skip_blank_lines)
            self._commentLes[i].setText(self._csv_sets[i].comment)
            self._headerLes[i].setText(str(self._csv_sets[i].header))
            self._headerLes[i].setPlaceholderText(str(DEFAULT_HEADER))
            self._encodingLes[i].setText(self._csv_sets[i].encoding)
            self._encodingLes[i].setPlaceholderText(str(DEFAULT_ENCODING))
            self._separatorLes[i].setText(self._csv_sets[i].separator)
            self._extensionLes[i].setText(self._csv_sets[i].extension)
            self._stripCbs[i].setChecked(self._csv_sets[i].strip)

        # setup connections
        self._ui.validateBtn.clicked.connect(self._validate)
        self._ui.cancelBtn.clicked.connect(self.hide)

    def _validate(self):
        try:
            for i in range(2):
                header_str = self._headerLes[i].text()
                self._csv_sets[i].update_properties(skip_blank_line=self._skipBlankLinesCbs[i].isChecked(),
                                                    encoding=self._encodingLes[i].text(),
                                                    comment=self._commentLes[i].text(),
                                                    header=header_str if header_str else 0,
                                                    separator=self._separatorLes[i].text(),
                                                    strip=self._stripCbs[i].isChecked())
        except (StopError, ValidationError) as e:
            QtWidgets.QMessageBox.warning(self, "Erreur", str(e))

        else:
            self.hide()
            self.validated.emit()
