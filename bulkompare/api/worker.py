import logging

from PySide2 import QtCore, QtWidgets

from api.csv_manager import CsvManager

logger = logging.getLogger(__name__)


class Worker(QtCore.QObject):
    finished = QtCore.Signal()
    success = QtCore.Signal()
    error = QtCore.Signal()

    def __init__(self, manager: CsvManager):
        super().__init__()
        self._manager = manager

    def upgrade_manager_status_silently(self):
        try:
            self._manager.upgrade_status_silently()
        except Exception as e:
            logger.exception(f"unexpected exception: {e}")
            QtWidgets.QMessageBox.warning(self, "Erreur", str(e))
        finally:
            self.finished.emit()

    def compare(self):
        try:
            self._manager.compare()

        except ValueError as e:
            logger.exception(f"ValueError: {e}")
            QtWidgets.QMessageBox.warning(self, "Erreur", str(e))
        except Exception as e:
            logger.exception(f"unexpected exception: {e}")
            QtWidgets.QMessageBox.warning(self, "Erreur", str(e))
        else:
            self.success.emit()

        finally:
            self.finished.emit()
