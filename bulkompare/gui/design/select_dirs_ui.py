# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_dirs.ui'
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


class Ui_select_dirs(object):
    def setupUi(self, select_dirs):
        if select_dirs.objectName():
            select_dirs.setObjectName(u"select_dirs")
        select_dirs.resize(930, 865)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(select_dirs.sizePolicy().hasHeightForWidth())
        select_dirs.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(select_dirs)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.name0GroupBox = QGroupBox(select_dirs)
        self.name0GroupBox.setObjectName(u"name0GroupBox")
        self.verticalLayout_6 = QVBoxLayout(self.name0GroupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.nameLe0 = QLineEdit(self.name0GroupBox)
        self.nameLe0.setObjectName(u"nameLe0")
        self.nameLe0.setMaximumSize(QSize(150, 16777215))

        self.verticalLayout_7.addWidget(self.nameLe0)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.dir0Le = QLineEdit(self.name0GroupBox)
        self.dir0Le.setObjectName(u"dir0Le")

        self.horizontalLayout_5.addWidget(self.dir0Le)

        self.open0Btn = QToolButton(self.name0GroupBox)
        self.open0Btn.setObjectName(u"open0Btn")

        self.horizontalLayout_5.addWidget(self.open0Btn)


        self.verticalLayout_7.addLayout(self.horizontalLayout_5)


        self.verticalLayout_6.addLayout(self.verticalLayout_7)


        self.gridLayout.addWidget(self.name0GroupBox, 0, 1, 1, 1)

        self.name1GroupBox = QGroupBox(select_dirs)
        self.name1GroupBox.setObjectName(u"name1GroupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.name1GroupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.nameLe1 = QLineEdit(self.name1GroupBox)
        self.nameLe1.setObjectName(u"nameLe1")
        self.nameLe1.setMaximumSize(QSize(150, 16777215))

        self.verticalLayout_4.addWidget(self.nameLe1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.dir1Le = QLineEdit(self.name1GroupBox)
        self.dir1Le.setObjectName(u"dir1Le")

        self.horizontalLayout_6.addWidget(self.dir1Le)

        self.open1Btn = QToolButton(self.name1GroupBox)
        self.open1Btn.setObjectName(u"open1Btn")

        self.horizontalLayout_6.addWidget(self.open1Btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.gridLayout.addWidget(self.name1GroupBox, 0, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.files1GroupBox = QGroupBox(select_dirs)
        self.files1GroupBox.setObjectName(u"files1GroupBox")
        self.verticalLayout_5 = QVBoxLayout(self.files1GroupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.clearBtn = QToolButton(self.files1GroupBox)
        self.clearBtn.setObjectName(u"clearBtn")

        self.horizontalLayout_3.addWidget(self.clearBtn)

        self.addBtn = QToolButton(self.files1GroupBox)
        self.addBtn.setObjectName(u"addBtn")

        self.horizontalLayout_3.addWidget(self.addBtn)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.extensionsLw = QListWidget(self.files1GroupBox)
        self.extensionsLw.setObjectName(u"extensionsLw")

        self.verticalLayout_5.addWidget(self.extensionsLw)


        self.verticalLayout_2.addWidget(self.files1GroupBox)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.cancelBtn = QPushButton(select_dirs)
        self.cancelBtn.setObjectName(u"cancelBtn")
        self.cancelBtn.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_4.addWidget(self.cancelBtn, 0, Qt.AlignRight)

        self.validateBtn = QPushButton(select_dirs)
        self.validateBtn.setObjectName(u"validateBtn")
        self.validateBtn.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_4.addWidget(self.validateBtn, 0, Qt.AlignLeft)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        QWidget.setTabOrder(self.clearBtn, self.addBtn)
        QWidget.setTabOrder(self.addBtn, self.extensionsLw)
        QWidget.setTabOrder(self.extensionsLw, self.cancelBtn)
        QWidget.setTabOrder(self.cancelBtn, self.validateBtn)

        self.retranslateUi(select_dirs)

        QMetaObject.connectSlotsByName(select_dirs)
    # setupUi

    def retranslateUi(self, select_dirs):
        select_dirs.setWindowTitle(QCoreApplication.translate("select_dirs", u"Dialog", None))
        self.name0GroupBox.setTitle(QCoreApplication.translate("select_dirs", u"Nom", None))
        self.open0Btn.setText(QCoreApplication.translate("select_dirs", u"Ouvrir", None))
        self.name1GroupBox.setTitle(QCoreApplication.translate("select_dirs", u"Nom", None))
        self.open1Btn.setText(QCoreApplication.translate("select_dirs", u"Ouvrir", None))
        self.files1GroupBox.setTitle(QCoreApplication.translate("select_dirs", u"Fichiers", None))
        self.clearBtn.setText(QCoreApplication.translate("select_dirs", u"Vider", None))
        self.addBtn.setText(QCoreApplication.translate("select_dirs", u"Ajouter", None))
        self.cancelBtn.setText(QCoreApplication.translate("select_dirs", u"Annuler", None))
        self.validateBtn.setText(QCoreApplication.translate("select_dirs", u"Valider", None))
    # retranslateUi

