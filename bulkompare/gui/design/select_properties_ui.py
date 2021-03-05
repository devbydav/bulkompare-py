# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_properties.ui'
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


class Ui_select_properties(object):
    def setupUi(self, select_properties):
        if select_properties.objectName():
            select_properties.setObjectName(u"select_properties")
        select_properties.resize(930, 865)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(select_properties.sizePolicy().hasHeightForWidth())
        select_properties.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(select_properties)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.properties0GroupBox = QGroupBox(select_properties)
        self.properties0GroupBox.setObjectName(u"properties0GroupBox")
        self.properties0GroupBox.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.properties0GroupBox.sizePolicy().hasHeightForWidth())
        self.properties0GroupBox.setSizePolicy(sizePolicy1)
        self.properties0GroupBox.setAcceptDrops(False)
        self.properties0GroupBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.properties0GroupBox.setFlat(False)
        self.properties0GroupBox.setCheckable(False)
        self.verticalLayout = QVBoxLayout(self.properties0GroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout0 = QFormLayout()
        self.formLayout0.setObjectName(u"formLayout0")
        self.skipBlankLines0Lbl = QLabel(self.properties0GroupBox)
        self.skipBlankLines0Lbl.setObjectName(u"skipBlankLines0Lbl")

        self.formLayout0.setWidget(0, QFormLayout.LabelRole, self.skipBlankLines0Lbl)

        self.skipBlankLines0Cb = QCheckBox(self.properties0GroupBox)
        self.skipBlankLines0Cb.setObjectName(u"skipBlankLines0Cb")

        self.formLayout0.setWidget(0, QFormLayout.FieldRole, self.skipBlankLines0Cb)

        self.comment0Lbl = QLabel(self.properties0GroupBox)
        self.comment0Lbl.setObjectName(u"comment0Lbl")

        self.formLayout0.setWidget(1, QFormLayout.LabelRole, self.comment0Lbl)

        self.comment0Le = QLineEdit(self.properties0GroupBox)
        self.comment0Le.setObjectName(u"comment0Le")

        self.formLayout0.setWidget(1, QFormLayout.FieldRole, self.comment0Le)

        self.heading0Lbl = QLabel(self.properties0GroupBox)
        self.heading0Lbl.setObjectName(u"heading0Lbl")

        self.formLayout0.setWidget(2, QFormLayout.LabelRole, self.heading0Lbl)

        self.heading0Le = QLineEdit(self.properties0GroupBox)
        self.heading0Le.setObjectName(u"heading0Le")

        self.formLayout0.setWidget(2, QFormLayout.FieldRole, self.heading0Le)

        self.encoding0Lbl = QLabel(self.properties0GroupBox)
        self.encoding0Lbl.setObjectName(u"encoding0Lbl")

        self.formLayout0.setWidget(3, QFormLayout.LabelRole, self.encoding0Lbl)

        self.encoding0Le = QLineEdit(self.properties0GroupBox)
        self.encoding0Le.setObjectName(u"encoding0Le")

        self.formLayout0.setWidget(3, QFormLayout.FieldRole, self.encoding0Le)

        self.separator0Lbl = QLabel(self.properties0GroupBox)
        self.separator0Lbl.setObjectName(u"separator0Lbl")

        self.formLayout0.setWidget(4, QFormLayout.LabelRole, self.separator0Lbl)

        self.separator0Le = QLineEdit(self.properties0GroupBox)
        self.separator0Le.setObjectName(u"separator0Le")

        self.formLayout0.setWidget(4, QFormLayout.FieldRole, self.separator0Le)

        self.extension0Lbl = QLabel(self.properties0GroupBox)
        self.extension0Lbl.setObjectName(u"extension0Lbl")

        self.formLayout0.setWidget(5, QFormLayout.LabelRole, self.extension0Lbl)

        self.extension0Le = QLineEdit(self.properties0GroupBox)
        self.extension0Le.setObjectName(u"extension0Le")
        self.extension0Le.setClearButtonEnabled(False)

        self.formLayout0.setWidget(5, QFormLayout.FieldRole, self.extension0Le)

        self.strip0Lbl = QLabel(self.properties0GroupBox)
        self.strip0Lbl.setObjectName(u"strip0Lbl")

        self.formLayout0.setWidget(6, QFormLayout.LabelRole, self.strip0Lbl)

        self.strip0Cb = QCheckBox(self.properties0GroupBox)
        self.strip0Cb.setObjectName(u"strip0Cb")

        self.formLayout0.setWidget(6, QFormLayout.FieldRole, self.strip0Cb)


        self.verticalLayout.addLayout(self.formLayout0)


        self.gridLayout.addWidget(self.properties0GroupBox, 0, 1, 1, 1)

        self.properties1Groupbox = QGroupBox(select_properties)
        self.properties1Groupbox.setObjectName(u"properties1Groupbox")
        self.verticalLayout_3 = QVBoxLayout(self.properties1Groupbox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout1 = QFormLayout()
        self.formLayout1.setObjectName(u"formLayout1")
        self.skipBlankLines1Lbl = QLabel(self.properties1Groupbox)
        self.skipBlankLines1Lbl.setObjectName(u"skipBlankLines1Lbl")

        self.formLayout1.setWidget(0, QFormLayout.LabelRole, self.skipBlankLines1Lbl)

        self.skipBlankLines1Cb = QCheckBox(self.properties1Groupbox)
        self.skipBlankLines1Cb.setObjectName(u"skipBlankLines1Cb")

        self.formLayout1.setWidget(0, QFormLayout.FieldRole, self.skipBlankLines1Cb)

        self.comment1Lbl = QLabel(self.properties1Groupbox)
        self.comment1Lbl.setObjectName(u"comment1Lbl")

        self.formLayout1.setWidget(1, QFormLayout.LabelRole, self.comment1Lbl)

        self.comment1Le = QLineEdit(self.properties1Groupbox)
        self.comment1Le.setObjectName(u"comment1Le")

        self.formLayout1.setWidget(1, QFormLayout.FieldRole, self.comment1Le)

        self.heading1Lbl = QLabel(self.properties1Groupbox)
        self.heading1Lbl.setObjectName(u"heading1Lbl")

        self.formLayout1.setWidget(2, QFormLayout.LabelRole, self.heading1Lbl)

        self.heading1Le = QLineEdit(self.properties1Groupbox)
        self.heading1Le.setObjectName(u"heading1Le")

        self.formLayout1.setWidget(2, QFormLayout.FieldRole, self.heading1Le)

        self.encoding1Lbl = QLabel(self.properties1Groupbox)
        self.encoding1Lbl.setObjectName(u"encoding1Lbl")

        self.formLayout1.setWidget(3, QFormLayout.LabelRole, self.encoding1Lbl)

        self.encoding1Le = QLineEdit(self.properties1Groupbox)
        self.encoding1Le.setObjectName(u"encoding1Le")

        self.formLayout1.setWidget(3, QFormLayout.FieldRole, self.encoding1Le)

        self.separator1Lbl = QLabel(self.properties1Groupbox)
        self.separator1Lbl.setObjectName(u"separator1Lbl")

        self.formLayout1.setWidget(4, QFormLayout.LabelRole, self.separator1Lbl)

        self.separator1Le = QLineEdit(self.properties1Groupbox)
        self.separator1Le.setObjectName(u"separator1Le")

        self.formLayout1.setWidget(4, QFormLayout.FieldRole, self.separator1Le)

        self.extension1Lbl = QLabel(self.properties1Groupbox)
        self.extension1Lbl.setObjectName(u"extension1Lbl")

        self.formLayout1.setWidget(5, QFormLayout.LabelRole, self.extension1Lbl)

        self.extension1Le = QLineEdit(self.properties1Groupbox)
        self.extension1Le.setObjectName(u"extension1Le")

        self.formLayout1.setWidget(5, QFormLayout.FieldRole, self.extension1Le)

        self.strip1Lbl = QLabel(self.properties1Groupbox)
        self.strip1Lbl.setObjectName(u"strip1Lbl")

        self.formLayout1.setWidget(6, QFormLayout.LabelRole, self.strip1Lbl)

        self.strip1Cb = QCheckBox(self.properties1Groupbox)
        self.strip1Cb.setObjectName(u"strip1Cb")

        self.formLayout1.setWidget(6, QFormLayout.FieldRole, self.strip1Cb)


        self.verticalLayout_3.addLayout(self.formLayout1)


        self.gridLayout.addWidget(self.properties1Groupbox, 0, 2, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.cancelBtn = QPushButton(select_properties)
        self.cancelBtn.setObjectName(u"cancelBtn")
        self.cancelBtn.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_4.addWidget(self.cancelBtn, 0, Qt.AlignRight)

        self.validateBtn = QPushButton(select_properties)
        self.validateBtn.setObjectName(u"validateBtn")
        self.validateBtn.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_4.addWidget(self.validateBtn, 0, Qt.AlignLeft)


        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 1, 1, 2)


        self.verticalLayout_2.addLayout(self.gridLayout)

#if QT_CONFIG(shortcut)
        self.skipBlankLines0Lbl.setBuddy(self.skipBlankLines0Cb)
        self.comment0Lbl.setBuddy(self.comment0Le)
        self.heading0Lbl.setBuddy(self.heading0Le)
        self.encoding0Lbl.setBuddy(self.encoding0Le)
        self.separator0Lbl.setBuddy(self.separator0Le)
        self.extension0Lbl.setBuddy(self.extension0Le)
        self.strip0Lbl.setBuddy(self.strip0Cb)
        self.skipBlankLines1Lbl.setBuddy(self.skipBlankLines1Cb)
        self.comment1Lbl.setBuddy(self.comment1Le)
        self.heading1Lbl.setBuddy(self.heading1Le)
        self.encoding1Lbl.setBuddy(self.encoding1Le)
        self.separator1Lbl.setBuddy(self.separator1Le)
        self.extension1Lbl.setBuddy(self.extension1Le)
        self.strip1Lbl.setBuddy(self.strip1Cb)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.skipBlankLines0Cb, self.skipBlankLines1Cb)
        QWidget.setTabOrder(self.skipBlankLines1Cb, self.comment0Le)
        QWidget.setTabOrder(self.comment0Le, self.comment1Le)
        QWidget.setTabOrder(self.comment1Le, self.heading0Le)
        QWidget.setTabOrder(self.heading0Le, self.heading1Le)
        QWidget.setTabOrder(self.heading1Le, self.encoding0Le)
        QWidget.setTabOrder(self.encoding0Le, self.encoding1Le)
        QWidget.setTabOrder(self.encoding1Le, self.separator0Le)
        QWidget.setTabOrder(self.separator0Le, self.separator1Le)
        QWidget.setTabOrder(self.separator1Le, self.extension0Le)
        QWidget.setTabOrder(self.extension0Le, self.extension1Le)
        QWidget.setTabOrder(self.extension1Le, self.strip0Cb)
        QWidget.setTabOrder(self.strip0Cb, self.strip1Cb)
        QWidget.setTabOrder(self.strip1Cb, self.cancelBtn)
        QWidget.setTabOrder(self.cancelBtn, self.validateBtn)

        self.retranslateUi(select_properties)

        QMetaObject.connectSlotsByName(select_properties)
    # setupUi

    def retranslateUi(self, select_properties):
        select_properties.setWindowTitle(QCoreApplication.translate("select_properties", u"Dialog", None))
        self.properties0GroupBox.setTitle(QCoreApplication.translate("select_properties", u"Propri\u00e9t\u00e9s des fichiers CSV", None))
        self.skipBlankLines0Lbl.setText(QCoreApplication.translate("select_properties", u"Ignorer lignes vides", None))
        self.skipBlankLines0Cb.setText("")
        self.comment0Lbl.setText(QCoreApplication.translate("select_properties", u"Commentaire", None))
        self.heading0Lbl.setText(QCoreApplication.translate("select_properties", u"Ligne des en-t\u00eates", None))
        self.encoding0Lbl.setText(QCoreApplication.translate("select_properties", u"Encodage", None))
        self.separator0Lbl.setText(QCoreApplication.translate("select_properties", u"S\u00e9parateur", None))
        self.separator0Le.setPlaceholderText(QCoreApplication.translate("select_properties", u"TAB", None))
        self.extension0Lbl.setText(QCoreApplication.translate("select_properties", u"Extension", None))
        self.strip0Lbl.setText(QCoreApplication.translate("select_properties", u"Ignorer whitespace", None))
        self.properties1Groupbox.setTitle(QCoreApplication.translate("select_properties", u"Propri\u00e9t\u00e9s des fichiers CSV", None))
        self.skipBlankLines1Lbl.setText(QCoreApplication.translate("select_properties", u"Ignorer lignes vides", None))
        self.skipBlankLines1Cb.setText("")
        self.comment1Lbl.setText(QCoreApplication.translate("select_properties", u"Commentaire", None))
        self.heading1Lbl.setText(QCoreApplication.translate("select_properties", u"Ligne des en-t\u00eates", None))
        self.encoding1Lbl.setText(QCoreApplication.translate("select_properties", u"Encodage", None))
        self.separator1Lbl.setText(QCoreApplication.translate("select_properties", u"S\u00e9parateur", None))
        self.separator1Le.setPlaceholderText(QCoreApplication.translate("select_properties", u"TAB", None))
        self.extension1Lbl.setText(QCoreApplication.translate("select_properties", u"Extension", None))
        self.strip1Lbl.setText(QCoreApplication.translate("select_properties", u"Ignorer whitespace", None))
        self.cancelBtn.setText(QCoreApplication.translate("select_properties", u"Annuler", None))
        self.validateBtn.setText(QCoreApplication.translate("select_properties", u"Valider", None))
    # retranslateUi

