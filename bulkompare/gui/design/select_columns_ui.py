# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_columns.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_select_columns(object):
    def setupUi(self, select_columns):
        if select_columns.objectName():
            select_columns.setObjectName(u"select_columns")
        select_columns.resize(700, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(select_columns.sizePolicy().hasHeightForWidth())
        select_columns.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(select_columns)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ignoreAllBtn = QToolButton(select_columns)
        self.ignoreAllBtn.setObjectName(u"ignoreAllBtn")

        self.horizontalLayout.addWidget(self.ignoreAllBtn, 0, Qt.AlignRight)

        self.compareAllBtn = QToolButton(select_columns)
        self.compareAllBtn.setObjectName(u"compareAllBtn")

        self.horizontalLayout.addWidget(self.compareAllBtn, 0, Qt.AlignLeft)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tableWidget = QWidget(select_columns)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableLayout0 = QHBoxLayout(self.tableWidget)
        self.tableLayout0.setObjectName(u"tableLayout0")
        self.tableLayout0.setContentsMargins(1, -1, -1, -1)
        self.horizontalSpacerL = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.tableLayout0.addItem(self.horizontalSpacerL)

        self.tableView = QTableView(self.tableWidget)
        self.tableView.setObjectName(u"tableView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy1)
        self.tableView.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tableLayout0.addWidget(self.tableView)

        self.horizontalSpacerR = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.tableLayout0.addItem(self.horizontalSpacerR)


        self.horizontalLayout_2.addWidget(self.tableWidget)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, -1, -1, 0)
        self.cancelBtn = QPushButton(select_columns)
        self.cancelBtn.setObjectName(u"cancelBtn")
        self.cancelBtn.setMaximumSize(QSize(100, 16777215))
        self.cancelBtn.setAutoDefault(False)
        self.cancelBtn.setFlat(False)

        self.horizontalLayout_3.addWidget(self.cancelBtn, 0, Qt.AlignRight)

        self.validateBtn = QPushButton(select_columns)
        self.validateBtn.setObjectName(u"validateBtn")
        self.validateBtn.setMaximumSize(QSize(100, 16777215))
        self.validateBtn.setAutoDefault(False)

        self.horizontalLayout_3.addWidget(self.validateBtn, 0, Qt.AlignLeft)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.retranslateUi(select_columns)

        QMetaObject.connectSlotsByName(select_columns)
    # setupUi

    def retranslateUi(self, select_columns):
        select_columns.setWindowTitle(QCoreApplication.translate("select_columns", u"Choix des colonnes", None))
        self.ignoreAllBtn.setText(QCoreApplication.translate("select_columns", u"Tout ignorer", None))
        self.compareAllBtn.setText(QCoreApplication.translate("select_columns", u"Tout comparer", None))
        self.cancelBtn.setText(QCoreApplication.translate("select_columns", u"Annuler", None))
        self.validateBtn.setText(QCoreApplication.translate("select_columns", u"Valider", None))
    # retranslateUi

