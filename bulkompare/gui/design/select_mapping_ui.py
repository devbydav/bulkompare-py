# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_mapping.ui'
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


class Ui_select_mapping(object):
    def setupUi(self, select_mapping):
        if select_mapping.objectName():
            select_mapping.setObjectName(u"select_mapping")
        select_mapping.resize(700, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(select_mapping.sizePolicy().hasHeightForWidth())
        select_mapping.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(select_mapping)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox0 = QGroupBox(select_mapping)
        self.groupBox0.setObjectName(u"groupBox0")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox0.sizePolicy().hasHeightForWidth())
        self.groupBox0.setSizePolicy(sizePolicy1)
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.tableView0 = QTableView(self.groupBox0)
        self.tableView0.setObjectName(u"tableView0")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.tableView0.sizePolicy().hasHeightForWidth())
        self.tableView0.setSizePolicy(sizePolicy2)
        self.tableView0.setMinimumSize(QSize(600, 0))
        self.tableView0.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)

        self.horizontalLayout_2.addWidget(self.tableView0)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.groupBox0)

        self.groupBox1 = QGroupBox(select_mapping)
        self.groupBox1.setObjectName(u"groupBox1")
        sizePolicy1.setHeightForWidth(self.groupBox1.sizePolicy().hasHeightForWidth())
        self.groupBox1.setSizePolicy(sizePolicy1)
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox1)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.tableView1 = QTableView(self.groupBox1)
        self.tableView1.setObjectName(u"tableView1")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.tableView1.sizePolicy().hasHeightForWidth())
        self.tableView1.setSizePolicy(sizePolicy3)
        self.tableView1.setMinimumSize(QSize(600, 0))
        self.tableView1.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)

        self.horizontalLayout_4.addWidget(self.tableView1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addWidget(self.groupBox1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, -1, -1, 0)
        self.cancelBtn = QPushButton(select_mapping)
        self.cancelBtn.setObjectName(u"cancelBtn")
        self.cancelBtn.setMaximumSize(QSize(100, 16777215))
        self.cancelBtn.setAutoDefault(False)
        self.cancelBtn.setFlat(False)

        self.horizontalLayout_3.addWidget(self.cancelBtn, 0, Qt.AlignRight)

        self.validateBtn = QPushButton(select_mapping)
        self.validateBtn.setObjectName(u"validateBtn")
        self.validateBtn.setMaximumSize(QSize(100, 16777215))
        self.validateBtn.setAutoDefault(False)

        self.horizontalLayout_3.addWidget(self.validateBtn, 0, Qt.AlignLeft)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)

        self.label = QLabel(select_mapping)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)


        self.retranslateUi(select_mapping)

        QMetaObject.connectSlotsByName(select_mapping)
    # setupUi

    def retranslateUi(self, select_mapping):
        select_mapping.setWindowTitle(QCoreApplication.translate("select_mapping", u"Renommer des colonnes", None))
        self.groupBox0.setTitle(QCoreApplication.translate("select_mapping", u"Set A", None))
        self.groupBox1.setTitle(QCoreApplication.translate("select_mapping", u"Set B", None))
        self.cancelBtn.setText(QCoreApplication.translate("select_mapping", u"Annuler", None))
        self.validateBtn.setText(QCoreApplication.translate("select_mapping", u"Valider", None))
        self.label.setText(QCoreApplication.translate("select_mapping", u"Indiquer dans la colonne de droite le nom \u00e0 utiliser pour la comparaison (laisser vide pour ne pas renommer)\n"
"Les fichiers originaux ne sont pas modifi\u00e9s", None))
    # retranslateUi

