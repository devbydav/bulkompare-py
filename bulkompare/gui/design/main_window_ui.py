# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1010, 778)
        self.actionSelectDirs = QAction(MainWindow)
        self.actionSelectDirs.setObjectName(u"actionSelectDirs")
        self.actionSelectProperties = QAction(MainWindow)
        self.actionSelectProperties.setObjectName(u"actionSelectProperties")
        self.actionSelectMapping = QAction(MainWindow)
        self.actionSelectMapping.setObjectName(u"actionSelectMapping")
        self.actionSelectColumns = QAction(MainWindow)
        self.actionSelectColumns.setObjectName(u"actionSelectColumns")
        self.actionCompare = QAction(MainWindow)
        self.actionCompare.setObjectName(u"actionCompare")
        self.actionToggleFilter = QAction(MainWindow)
        self.actionToggleFilter.setObjectName(u"actionToggleFilter")
        self.actionExportExcel = QAction(MainWindow)
        self.actionExportExcel.setObjectName(u"actionExportExcel")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.infoLbl = QLabel(self.centralwidget)
        self.infoLbl.setObjectName(u"infoLbl")
        self.infoLbl.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.infoLbl)

        self.filterLe = QLineEdit(self.centralwidget)
        self.filterLe.setObjectName(u"filterLe")

        self.verticalLayout.addWidget(self.filterLe)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.summaryTab = QWidget()
        self.summaryTab.setObjectName(u"summaryTab")
        self.verticalLayout_5 = QVBoxLayout(self.summaryTab)
        self.verticalLayout_5.setSpacing(20)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_5.setContentsMargins(15, 12, 15, 15)
        self.summaryTw = QTreeWidget(self.summaryTab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.summaryTw.setHeaderItem(__qtreewidgetitem)
        self.summaryTw.setObjectName(u"summaryTw")

        self.verticalLayout_5.addWidget(self.summaryTw)

        self.tabWidget.addTab(self.summaryTab, "")
        self.differencesTab = QWidget()
        self.differencesTab.setObjectName(u"differencesTab")
        self.verticalLayout_2 = QVBoxLayout(self.differencesTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(15, -1, 15, 15)
        self.differencesTw = QTreeWidget(self.differencesTab)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.differencesTw.setHeaderItem(__qtreewidgetitem1)
        self.differencesTw.setObjectName(u"differencesTw")

        self.verticalLayout_2.addWidget(self.differencesTw)

        self.tabWidget.addTab(self.differencesTab, "")
        self.inOneTab = QWidget()
        self.inOneTab.setObjectName(u"inOneTab")
        self.verticalLayout_3 = QVBoxLayout(self.inOneTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(15, -1, 15, 15)
        self.inOneTw = QTreeWidget(self.inOneTab)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setText(0, u"1");
        self.inOneTw.setHeaderItem(__qtreewidgetitem2)
        self.inOneTw.setObjectName(u"inOneTw")

        self.verticalLayout_3.addWidget(self.inOneTw)

        self.tabWidget.addTab(self.inOneTab, "")
        self.notComparedTab = QWidget()
        self.notComparedTab.setObjectName(u"notComparedTab")
        self.verticalLayout_4 = QVBoxLayout(self.notComparedTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(15, -1, 15, 15)
        self.notComparedTw = QTreeWidget(self.notComparedTab)
        __qtreewidgetitem3 = QTreeWidgetItem()
        __qtreewidgetitem3.setText(0, u"1");
        self.notComparedTw.setHeaderItem(__qtreewidgetitem3)
        self.notComparedTw.setObjectName(u"notComparedTw")

        self.verticalLayout_4.addWidget(self.notComparedTw)

        self.tabWidget.addTab(self.notComparedTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.logoWidget = QWidget(self.centralwidget)
        self.logoWidget.setObjectName(u"logoWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.logoWidget.sizePolicy().hasHeightForWidth())
        self.logoWidget.setSizePolicy(sizePolicy)
        self.logoWidget.setMinimumSize(QSize(100, 100))
        self.logoWidget.setMaximumSize(QSize(500, 500))
        self.logoWidget.setAutoFillBackground(False)
        self.logoWidget.setStyleSheet(u"")
        self.logoWidgetLayout = QVBoxLayout(self.logoWidget)
        self.logoWidgetLayout.setObjectName(u"logoWidgetLayout")
        self.logoWidgetLayout.setContentsMargins(-1, 12, -1, -1)
        self.widget_2 = QWidget(self.logoWidget)
        self.widget_2.setObjectName(u"widget_2")

        self.logoWidgetLayout.addWidget(self.widget_2)


        self.verticalLayout.addWidget(self.logoWidget, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolBar.setMovable(False)
        self.toolBar.setAllowedAreas(Qt.NoToolBarArea)
        self.toolBar.setIconSize(QSize(15, 15))
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolBar.setFloatable(False)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionSelectDirs)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSelectProperties)
        self.toolBar.addAction(self.actionSelectMapping)
        self.toolBar.addAction(self.actionSelectColumns)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCompare)
        self.toolBar.addAction(self.actionToggleFilter)
        self.toolBar.addAction(self.actionExportExcel)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Bulkompare", None))
        self.actionSelectDirs.setText(QCoreApplication.translate("MainWindow", u"R\u00e9pertoires et extensions", None))
        self.actionSelectProperties.setText(QCoreApplication.translate("MainWindow", u"Propri\u00e9t\u00e9s CSV", None))
#if QT_CONFIG(tooltip)
        self.actionSelectProperties.setToolTip(QCoreApplication.translate("MainWindow", u"Propri\u00e9t\u00e9s CSV", None))
#endif // QT_CONFIG(tooltip)
        self.actionSelectMapping.setText(QCoreApplication.translate("MainWindow", u"Renommer des colonnes", None))
        self.actionSelectColumns.setText(QCoreApplication.translate("MainWindow", u"Choisir les colonnes", None))
        self.actionCompare.setText(QCoreApplication.translate("MainWindow", u"Lancer la comparaison", None))
        self.actionToggleFilter.setText(QCoreApplication.translate("MainWindow", u"Filtrage", None))
        self.actionExportExcel.setText(QCoreApplication.translate("MainWindow", u"Export Excel", None))
        self.infoLbl.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.summaryTab), QCoreApplication.translate("MainWindow", u"R\u00e9sum\u00e9", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.differencesTab), QCoreApplication.translate("MainWindow", u"Diff\u00e9rences", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.inOneTab), QCoreApplication.translate("MainWindow", u"Un set seulement", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.notComparedTab), QCoreApplication.translate("MainWindow", u"Indexes multiples", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

