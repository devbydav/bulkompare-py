import pathlib
import logging
from typing import Optional, List

from PySide2 import QtWidgets, QtCore, QtGui, QtSvg

import api.utils.logger
from api.csv_comparator import CsvComparator
from api.csv_manager import CsvManager

from gui.about import show_about
from gui.select_sources import SelectSourcesWidget
from gui.select_properties import SelectPropertiesWidget
from gui.select_columns import SelectColumnsWidget
from gui.select_mapping import SelectMappingWidget
from gui.trees import AbstractTreeManager, SummaryTreeManager, DifferencesTreeManager, GenericTreeManager, FilterError
from gui.design.main_window_ui import Ui_MainWindow
from gui.constants import ActionStatus, ACTION_STATUS
from api import bundle_dir
from api.worker import Worker
from api.utils.constants import Status
from api.utils.config import import_gui_config
from api.utils.selection_import import import_selection
from api.utils.exceptions import CustomError


try:
    from gui.custom import Custom
except ModuleNotFoundError:
    from gui.custom_example import Custom

logger = logging.getLogger(__name__)

STR_TB_ACTION_IMPORT_SELECTIONS = "Importer sélections"
STR_TB_ACTION_EXPORT_SELECTIONS = "Exporter sélections"
STR_TB_ACTION_SHOW_ABOUT = "Legal"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # sets/comparator
        self._config = import_gui_config(bundle_dir / "config" / "config.json")
        try:
            self._manager: CsvManager = import_selection(bundle_dir / "selections" / "default.json")
        except Exception as e:
            self._manager = CsvManager()
            self._show_error_dialog(str(e))

        self._current_tree_manager: Optional[AbstractTreeManager] = None

        self._current_comparator_index: int = 0
        self._current_comparator: Optional[CsvComparator] = None

        self._tree_managers: List[AbstractTreeManager] = []

        self._resource_dir: pathlib.Path = bundle_dir / "resources"
        self.setWindowIcon(QtGui.QIcon(str(self._resource_dir / "icons" / "Icon.ico")))

        # icons
        self._ICON_VALID = QtGui.QIcon(QtGui.QPixmap(str(self._resource_dir / "svg" / "tick.svg")))
        self._ICON_INVALID = QtGui.QIcon(QtGui.QPixmap(str(self._resource_dir / "svg" / "round_blue.svg")))
        self._ICON_DISABLED = QtGui.QIcon(QtGui.QPixmap(str(self._resource_dir / "svg" / "round_grey.svg")))
        self._ICON_FILTER = QtGui.QIcon(QtGui.QPixmap(str(self._resource_dir / "svg" / "filter.svg")))
        self._ICON_EXCEL = QtGui.QIcon(QtGui.QPixmap(str(self._resource_dir / "svg" / "excel.svg")))
        self._ICON_OPEN = QtGui.QIcon(QtGui.QPixmap(str(self._resource_dir / "svg" / "document.svg")))
        self._ICON_SAVE = QtGui.QIcon(QtGui.QPixmap(str(self._resource_dir / "svg" / "save.svg")))
        self._ICON_ABOUT = QtGui.QIcon(QtGui.QPixmap(str(self._resource_dir / "svg" / "question.svg")))
        self._ICON_ARROW = QtGui.QIcon(QtGui.QPixmap(str(self._resource_dir / "svg" / "arrow.svg")))

        # dialog widgets
        self._select_columns_widget = None
        self._select_mapping_widget = None

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._logo = QtSvg.QSvgWidget(str(self._resource_dir / "images" / "stork.svg"))
        self._ui.logoWidgetLayout.replaceWidget(self._ui.widget_2, self._logo)
        self._ui.filterLe.hide()
        self._ui.tabWidget.hide()

        self._ui.actionSelectDirs.setIcon(self._ICON_OPEN)
        self._ui.actionToggleFilter.setIcon(self._ICON_FILTER)
        self._ui.actionToggleFilter.setEnabled(False)
        self._ui.actionExportExcel.setIcon(self._ICON_EXCEL)
        self._ui.actionExportExcel.setEnabled(False)

        toolbar_spacing_widget = QtWidgets.QWidget()
        toolbar_spacing_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self._extensionsCb = QtWidgets.QComboBox()
        self._extensionsCb.setMinimumWidth(100)

        self._ui.toolBar.insertWidget(self._ui.actionSelectProperties, self._extensionsCb)

        self._ui.toolBar.addWidget(toolbar_spacing_widget)
        self._ui.actionLoadSelection = self._ui.toolBar.addAction(self._ICON_OPEN, STR_TB_ACTION_IMPORT_SELECTIONS)
        self._ui.actionSaveSelection = self._ui.toolBar.addAction(self._ICON_SAVE, STR_TB_ACTION_EXPORT_SELECTIONS)
        self._ui.actionShowAbout = self._ui.toolBar.addAction(self._ICON_ABOUT, STR_TB_ACTION_SHOW_ABOUT)

        self._statusRightLabel = QtWidgets.QLabel()
        self._ui.statusBar.addPermanentWidget(self._statusRightLabel)

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._clear_status_right_text)

        # setup connections
        self._ui.actionSelectDirs.triggered.connect(self._select_sources_clicked)
        self._ui.actionSelectProperties.triggered.connect(self._select_properties_clicked)
        self._ui.actionSelectColumns.triggered.connect(self._select_columns_clicked)
        self._ui.actionSelectMapping.triggered.connect(self._select_mapping_clicked)
        self._ui.actionCompare.triggered.connect(self._compare)
        self._ui.actionToggleFilter.triggered.connect(self._toggle_filter)
        self._ui.actionLoadSelection.triggered.connect(self._load_selections)
        self._ui.actionSaveSelection.triggered.connect(self._save_selections)
        self._ui.actionShowAbout.triggered.connect(self._show_about)
        self._extensionsCb.currentIndexChanged.connect(self._change_current_extension)
        self._ui.tabWidget.currentChanged.connect(self._current_tab_changed)
        self._ui.differencesTw.doubleClicked.connect(self._tree_widget_double_clicked)
        self._ui.inOneTw.doubleClicked.connect(self._tree_widget_double_clicked)
        self._ui.notComparedTw.doubleClicked.connect(self._tree_widget_double_clicked)
        self._ui.filterLe.returnPressed.connect(self._filter_changed)

        self._custom = Custom(self._config.custom)

        self._update_extensions_list()
        self._update_ui()

    def _display_main_area(self, logo: Optional[bool] = True, animate: Optional[bool] = None):
        """Shows/animates widgets in the main area.
         Params : logo to display logo or tab widget / animate to animate the logo
         No change if argument is not provided"""

        if logo is not None:
            if logo:
                # display tabs
                self._ui.tabWidget.hide()
                self._ui.logoWidget.show()
            else:
                # display tabs
                self._ui.logoWidget.hide()
                self._ui.tabWidget.show()
        if animate is not None:
            if animate:
                self._logo.load(str(self._resource_dir / "images" / "stork_animated.svg"))
            else:
                self._logo.load(str(self._resource_dir / "images" / "stork.svg"))

    def _compare(self):
        """Compares the two csv_sets in a new thread"""
        self._lock_ui()

        self._set_action_status(ActionStatus.DISABLED, action=self._ui.actionCompare)

        self.thread = QtCore.QThread(self)
        self.worker = Worker(manager=self._manager)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.compare)
        self.worker.success.connect(self._compare_success)
        self.worker.error.connect(self._compare_error)
        self.worker.finished.connect(self.thread.quit)
        self.thread.start()
        self._display_main_area(logo=True, animate=True)

    def _compare_error(self):
        """Call back when comparison was not done due to error"""
        QtWidgets.QMessageBox.warning(self, "Erreur", "Erreur pendant la comparaison")
        self._update_ui()
        self._display_main_area(logo=False, animate=False)

    def _compare_success(self):
        """Callback when comparison was done without error"""
        self._update_trees()
        self._update_ui()
        self._display_main_area(logo=False, animate=False)

    def _lock_ui(self):
        """Disable actions while worker is busy"""
        self._ui.actionSelectProperties.setEnabled(False)
        self._ui.actionSelectColumns.setEnabled(False)
        self._ui.actionSelectMapping.setEnabled(False)
        self._ui.actionCompare.setEnabled(False)
        self._ui.actionToggleFilter.setEnabled(False)

    def _select_columns_clicked(self):
        """Callback when select columns action is clicked"""
        self._select_columns_widget = SelectColumnsWidget(self._resource_dir, self._current_comparator)
        self._select_columns_widget.validated.connect(self._select_columns_validated)
        self._select_columns_widget.show()

    def _select_columns_validated(self):
        """Callback when select columns widget is closed"""
        self._select_columns_widget = None
        self._update_ui()

    def _select_sources_clicked(self):
        """Callback when select file action is clicked"""
        self._select_sources_widget = SelectSourcesWidget(self._resource_dir, self._manager, self._config)
        self._select_sources_widget.validated.connect(self._select_sources_validated)
        self._select_sources_widget.show()

    def _select_sources_validated(self):
        """Callback when select file widget is closed"""
        self._select_sources_widget = None
        self._update_extensions_list()
        self._update_ui()

    def _select_properties_clicked(self):
        """Callback when select file action is clicked"""
        self._select_properties_widget = SelectPropertiesWidget(self._resource_dir, self._current_comparator.csv_sets)
        self._select_properties_widget.validated.connect(self._select_properties_validated)
        self._select_properties_widget.show()

    def _select_properties_validated(self):
        """Callback when select file widget is closed"""
        self._select_properties_widget = None
        self._update_ui()

    def _select_mapping_clicked(self):
        """Callback when select mapping action is clicked"""
        self._select_mapping_widget = SelectMappingWidget(self._resource_dir, self._current_comparator.csv_sets)
        self._select_mapping_widget.validated.connect(self._select_mapping_validated)
        self._select_mapping_widget.show()

    def _select_mapping_validated(self):
        """Callback when select mappping widget is closed"""
        self._select_mapping_widget = None
        self._update_ui()

    def _set_action_status(self, status: ActionStatus, action: QtWidgets.QAction,):
        """Enables/disables the action on toolbar and sets its icon"""
        if status == ActionStatus.VALID:
            action.setIcon(self._ICON_VALID)
            action.setEnabled(True)
        elif status == ActionStatus.INVALID:
            action.setIcon(self._ICON_INVALID)
            action.setEnabled(True)
        else:
            # disable
            action.setIcon(self._ICON_DISABLED)
            action.setEnabled(False)

    def _show_about(self):
        """Callback when about action is clicked -> show about dialog"""
        show_about(logo=QtGui.QPixmap(str(self._resource_dir / "images" / "stork.svg")).scaledToWidth(100))

    def _tree_widget_double_clicked(self, item):
        """Callback when tree widget is double-clicked"""
        try:
            has_children = item.model().hasChildren(item)
        except AttributeError:
            pass
        else:
            if not has_children:
                try:
                    text = self._custom.tree_item_double_clicked(item=item)
                except CustomError as e:
                    QtWidgets.QMessageBox.warning(self, "Erreur", str(e))
                else:
                    if text:
                        self._set_status_bar_right_text(text)

    def _update_manager_status_finished(self):
        """Reruns update_ui with updated status if that update was done through worker"""
        self.thread.quit()
        self._display_main_area(animate=False)
        self._update_ui(self._manager.status)

    def _update_extensions_list(self):
        """Updates the combobox list of extensions"""
        logger.debug("updating extensions")
        self._extensionsCb.clear()
        self._extensionsCb.addItems([comp.extension for comp in self._manager.comparators])

    def _change_current_extension(self, new_index):
        """Callback when extension comboBox changes index"""
        logger.debug("changing current extension index to" + str(new_index))
        self._current_comparator_index = new_index
        self._current_comparator = self._manager.comparators[new_index]
        self._update_extension_specific_ui()

    def _update_extension_specific_ui(self):
        """Update the extension-specific parts of the UI"""
        try:
            status = self._manager.comparators[self._current_comparator_index].status
        except IndexError:
            self._set_action_status(ActionStatus.DISABLED, action=self._ui.actionSelectProperties)
            self._set_action_status(ActionStatus.DISABLED, action=self._ui.actionSelectMapping)
            self._set_action_status(ActionStatus.DISABLED, action=self._ui.actionSelectColumns)
        else:
            logger.debug("Updating extension-specific ui with " + str(status))

            status_prop, status_mapping, status_cols = ACTION_STATUS[status]
            self._set_action_status(status_prop, action=self._ui.actionSelectProperties)
            self._set_action_status(status_mapping, action=self._ui.actionSelectMapping)
            self._set_action_status(status_cols, action=self._ui.actionSelectColumns)

    def _update_ui(self, status=None):
        """Updates the status of csv sets and updates the UI accordingly"""
        if status is None:
            # if all file headers need to be read -> move to an other thread
            if self._manager.status < Status.COLUMNS_AVAILABLE:
                self._lock_ui()
                self._display_main_area(logo=True, animate=True)
                self.thread = QtCore.QThread(self)
                self.worker = Worker(manager=self._manager)
                self.worker.moveToThread(self.thread)
                self.thread.started.connect(self.worker.upgrade_manager_status_silently)
                self.worker.finished.connect(self._update_manager_status_finished)
                self.thread.start()
                return  # we come back to update ui through _update_manager_status_finished callback
            else:
                self._manager.upgrade_status_silently()

        status = self._manager.status

        logger.debug("Update UI with " + str(status))

        if status == Status.DATA_IMPORTED:
            self._set_action_status(ActionStatus.DISABLED, action=self._ui.actionCompare)
            self._reset_filter(allow=True)

            # display results
            self._display_main_area(logo=False)

        else:
            self._display_main_area(logo=True)
            self._reset_filter(allow=False)

            if status == Status.READY_TO_IMPORT:
                self._set_action_status(ActionStatus.INVALID, action=self._ui.actionCompare)
            else:
                self._set_action_status(ActionStatus.DISABLED, action=self._ui.actionCompare)

        for i, comp in enumerate(self._manager.comparators):
            if comp.status >= Status.READY_TO_IMPORT:
                self._extensionsCb.setItemIcon(i, self._ICON_VALID)
            else:
                self._extensionsCb.setItemIcon(i, self._ICON_ARROW)

        self._update_extension_specific_ui()

    def _update_trees(self):
        """Updates all trees with the comparison results"""

        display_columns = self._manager.display_columns
        compare_columns = self._manager.compare_columns

        self._tree_managers = []
        summary_tm = SummaryTreeManager(self._ui.summaryTw, self._manager.results)
        self._tree_managers.append(summary_tm)

        differences_tm = DifferencesTreeManager(self._ui.differencesTw,
                                                self._manager.differences,
                                                display_columns=display_columns,
                                                filterable=True)
        self._tree_managers.append(differences_tm)

        in_one_tm = GenericTreeManager(self._ui.inOneTw,
                                       self._manager.in_one,
                                       display_columns=display_columns,
                                       compare_columns=compare_columns,
                                       filterable=True)
        self._tree_managers.append(in_one_tm)

        not_compared_tm = GenericTreeManager(self._ui.notComparedTw,
                                             self._manager.not_compared,
                                             display_columns=display_columns,
                                             compare_columns=compare_columns,
                                             filterable=True)
        self._tree_managers.append(not_compared_tm)

        self._update_current_tree_manager(self._ui.tabWidget.currentIndex())

    def _update_current_tree_manager(self, tab_index):
        self._current_tree_manager = self._tree_managers[tab_index]

    def _update_status_bar(self):
        """Updates the message displayed in status bar"""
        if self._current_tree_manager and self._current_tree_manager.filterable:
            if self._current_tree_manager.filtering:
                self._ui.statusBar.showMessage(f"{self._current_tree_manager.nb_filtered_lines} / {self._current_tree_manager.nb_total_lines} lignes")
            else:
                self._ui.statusBar.showMessage(f"{self._current_tree_manager.nb_total_lines} lignes")
        else:
            self._ui.statusBar.clearMessage()

    def _set_status_bar_right_text(self, text):
        """Display text to the right of status bar. It is cleared at the end of the timer"""
        self._statusRightLabel.setText(text)
        self._timer.start(3000)

    def _clear_status_right_text(self):
        """Clears the right part of status bar. It is called when timer ends"""
        self._statusRightLabel.setText("")

    def _filter_changed(self):
        """Callback when user presses enter on the filter listEdit"""
        text = self._ui.filterLe.text()
        logger.debug("filter changed to " + text)
        try:
            self._tree_managers[self._ui.tabWidget.currentIndex()].filter(text)

        except FilterError as e:
            self._ui.filterLe.setStyleSheet("border: 1px solid red;")
            QtWidgets.QMessageBox.warning(self, "Erreur", str(e))
        else:
            if text:
                self._ui.filterLe.setStyleSheet("border: 1px solid green;")
            else:
                self._ui.filterLe.setStyleSheet("")

        self._update_status_bar()

    def _reset_filter(self, allow: bool = True):
        """Resets and hides the filter lineEdit and enables button according to status"""

        self._ui.filterLe.setText("")
        self._ui.filterLe.hide()

        if allow and self._current_tree_manager and self._current_tree_manager.filterable:
            self._ui.actionToggleFilter.setEnabled(True)
        else:
            self._ui.actionToggleFilter.setEnabled(False)

    def _toggle_filter(self):
        """Callback when filter action is pressed"""
        new_status = self._current_tree_manager.toggle_filtering()
        if new_status:
            self._ui.filterLe.show()
            self._ui.filterLe.setText(self._current_tree_manager.filter_text)
        else:
            self._ui.filterLe.hide()
            self._ui.filterLe.setText("")

            self._update_status_bar()

    def _current_tab_changed(self, index):
        """Callback when selected tab is changed"""

        self._update_current_tree_manager(index)

        # show/hide the filter listEdit
        if self._current_tree_manager and self._current_tree_manager.filtering:
            self._ui.filterLe.setText(self._current_tree_manager.filter_text)
            self._ui.filterLe.show()
        else:
            self._ui.filterLe.hide()

        # enable/disable filtering according to whether tree is filterable
        self._ui.actionToggleFilter.setEnabled(self._current_tree_manager.filterable)

        self._update_status_bar()

    def _show_error_dialog(self, error: str):
        QtWidgets.QMessageBox.warning(self, "Erreur", error)

    def _load_selections(self):
        """Callback when load selection action is clicked"""
        path_str, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Importer une sélection",
                                                            str(self._config.selections_dir),
                                                            "Selections (*.json)")
        if path_str:
            try:
                self._manager = import_selection(pathlib.Path(path_str))

            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Erreur", str(e))
                logger.exception("Selections import")

            finally:
                self._update_extensions_list()
                self._update_ui()

    def _save_selections(self):
        """Callback when save selection action is clicked"""
        path_str, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Exporter la sélection actuelle ",
                                                            str(self._config.selections_dir),
                                                            "*.json")
        self._manager.save_selections(path_str)
