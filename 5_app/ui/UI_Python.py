# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PickAPart.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QTreeView, QVBoxLayout,
    QWidget)

class Ui_wgPick(object):
    def setupUi(self, wgPick):
        if not wgPick.objectName():
            wgPick.setObjectName(u"wgPick")
        wgPick.resize(200, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(wgPick.sizePolicy().hasHeightForWidth())
        wgPick.setSizePolicy(sizePolicy)
        wgPick.setMinimumSize(QSize(200, 0))
        wgPick.setMaximumSize(QSize(500, 425))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(8)
        wgPick.setFont(font)
        wgPick.setWindowTitle(u"Pick-A-Part")
        wgPick.setStyleSheet(u"\n"
"\n"
"/*Main*/\n"
"QWidget {    \n"
"	background-color: rgb(68, 68, 68); \n"
"	font-family: \"Segoe UI\"; \n"
"	font-size: 8pt; \n"
"\n"
"}\n"
"\n"
"/*Line Edit*/\n"
"QLineEdit {    \n"
"	color: rgb(238, 238, 238);\n"
"	border: 0px;\n"
"	background-color: rgb(43, 43, 43);\n"
"}\n"
"\n"
"/*Button*/\n"
"QPushButton {    	\n"
"	background-color: rgb(93, 93, 93);\n"
"	color: rgb(238, 238, 238);\n"
"	border: none;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(112, 112, 112);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgb(29, 29, 29);\n"
"}\n"
"\n"
"/*Lable*/\n"
"QLabel {    \n"
"	color: rgb(238, 238, 238);\n"
"}\n"
"\n"
"/*Combo Box*/\n"
"QComboBox{   \n"
"	background-color: rgb(93, 93, 93);\n"
"	color: rgb(238, 238, 238);\n"
"	border: none;\n"
"	shadow: none; \n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	background-color: rgb(93, 93, 93);\n"
"	color: rgb(238, 238, 238);\n"
"	border: 2px solid rgb(68, 68, 68);\n"
"	outline: 0;\n"
"	selection-background-color: rgb(82, 133, 166);\n"
"\n"
"}"
                        "\n"
"QComboBox QItemView::item{\n"
"	border: 0px solid transparent;\n"
"/**/\n"
"	backgound-color: transparent;\n"
"	border-style: none;\n"
"	outline: 0;\n"
"	padding: 4px;\n"
"/**/\n"
"	font-size: 30pt; \n"
"}\n"
"QComboBox QListView::item::hover{\n"
"	border: 0px solid transparent;\n"
"	border-style: none;\n"
"	outline: 0;\n"
"}\n"
"\n"
"/*QComboBox::down-arrow {\n"
"	color: rgb(170, 255, 0);\n"
"}*/\n"
"\n"
"/*Tree View*/\n"
"QTreeView{   \n"
"	color: rgb(238, 238, 238);\n"
"	border: 0px;\n"
"	background-color: rgb(43, 43, 43);\n"
"}")
        wgPick.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(wgPick)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 6)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 5)
        self.lblMain = QLabel(wgPick)
        self.lblMain.setObjectName(u"lblMain")
        self.lblMain.setMinimumSize(QSize(0, 15))
        self.lblMain.setMaximumSize(QSize(16777215, 15))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(8)
        font1.setBold(True)
        self.lblMain.setFont(font1)
        self.lblMain.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.lblMain)

        self.lneMainInput = QLineEdit(wgPick)
        self.lneMainInput.setObjectName(u"lneMainInput")
        self.lneMainInput.setMinimumSize(QSize(0, 15))
        self.lneMainInput.setMaximumSize(QSize(16777215, 15))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        self.lneMainInput.setFont(font2)
        self.lneMainInput.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.lneMainInput)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.line = QFrame(wgPick)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 5)
        self.lblAddParts = QLabel(wgPick)
        self.lblAddParts.setObjectName(u"lblAddParts")
        self.lblAddParts.setMinimumSize(QSize(0, 15))
        self.lblAddParts.setMaximumSize(QSize(16777215, 15))
        self.lblAddParts.setFont(font1)
        self.lblAddParts.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.lblAddParts)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 5)
        self.lblPart = QLabel(wgPick)
        self.lblPart.setObjectName(u"lblPart")
        self.lblPart.setMinimumSize(QSize(0, 15))
        self.lblPart.setMaximumSize(QSize(30, 16777215))
        self.lblPart.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.lblPart)

        self.cbParts = QComboBox(wgPick)
        self.cbParts.addItem("")
        self.cbParts.addItem("")
        self.cbParts.addItem("")
        self.cbParts.addItem("")
        self.cbParts.addItem("")
        self.cbParts.addItem("")
        self.cbParts.setObjectName(u"cbParts")
        self.cbParts.setMinimumSize(QSize(0, 21))

        self.horizontalLayout.addWidget(self.cbParts)

        self.btnAddPart = QPushButton(wgPick)
        self.btnAddPart.setObjectName(u"btnAddPart")
        self.btnAddPart.setMinimumSize(QSize(0, 21))
        self.btnAddPart.setAutoFillBackground(False)
        self.btnAddPart.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.btnAddPart)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 3)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.btnTreeView = QPushButton(wgPick)
        self.btnTreeView.setObjectName(u"btnTreeView")
        self.btnTreeView.setMinimumSize(QSize(0, 18))
        self.btnTreeView.setFont(font1)
        self.btnTreeView.setLayoutDirection(Qt.LeftToRight)
        self.btnTreeView.setStyleSheet(u"QPushButton {\n"
"	text-align: left;\n"
"	padding-left: 10px;\n"
"}")
        self.btnTreeView.setCheckable(True)
        self.btnTreeView.setChecked(True)
        self.btnTreeView.setFlat(False)

        self.verticalLayout_4.addWidget(self.btnTreeView)

        self.wgsTreeContainer = QWidget(wgPick)
        self.wgsTreeContainer.setObjectName(u"wgsTreeContainer")
        self.wgsTreeContainer.setMinimumSize(QSize(0, 10))
        self.verticalLayout_7 = QVBoxLayout(self.wgsTreeContainer)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.treeView = QTreeView(self.wgsTreeContainer)
        self.treeView.setObjectName(u"treeView")

        self.verticalLayout_7.addWidget(self.treeView)


        self.verticalLayout_4.addWidget(self.wgsTreeContainer)


        self.verticalLayout_3.addLayout(self.verticalLayout_4)

        self.btnDeletePart = QPushButton(wgPick)
        self.btnDeletePart.setObjectName(u"btnDeletePart")
        self.btnDeletePart.setMinimumSize(QSize(0, 20))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(8)
        font3.setBold(False)
        self.btnDeletePart.setFont(font3)

        self.verticalLayout_3.addWidget(self.btnDeletePart)

        self.verticalLayout_3.setStretch(2, 1)

        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.line_2 = QFrame(wgPick)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_5.addWidget(self.line_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 5)
        self.btnCreateGuides = QPushButton(wgPick)
        self.btnCreateGuides.setObjectName(u"btnCreateGuides")
        self.btnCreateGuides.setMinimumSize(QSize(100, 21))
        self.btnCreateGuides.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_3.addWidget(self.btnCreateGuides)

        self.btnDeleteGuides = QPushButton(wgPick)
        self.btnDeleteGuides.setObjectName(u"btnDeleteGuides")
        self.btnDeleteGuides.setMinimumSize(QSize(50, 21))

        self.horizontalLayout_3.addWidget(self.btnDeleteGuides)

        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.line_3 = QFrame(wgPick)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_5.addWidget(self.line_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.btnCreateRig = QPushButton(wgPick)
        self.btnCreateRig.setObjectName(u"btnCreateRig")
        self.btnCreateRig.setMinimumSize(QSize(100, 21))

        self.horizontalLayout_4.addWidget(self.btnCreateRig)

        self.btnDeleteRig = QPushButton(wgPick)
        self.btnDeleteRig.setObjectName(u"btnDeleteRig")
        self.btnDeleteRig.setMinimumSize(QSize(50, 21))

        self.horizontalLayout_4.addWidget(self.btnDeleteRig)

        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.verticalLayout_5.setStretch(0, 1)

        self.verticalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout.setStretch(2, 2)
        QWidget.setTabOrder(self.lneMainInput, self.cbParts)
        QWidget.setTabOrder(self.cbParts, self.btnAddPart)
        QWidget.setTabOrder(self.btnAddPart, self.btnCreateGuides)
        QWidget.setTabOrder(self.btnCreateGuides, self.btnDeleteGuides)
        QWidget.setTabOrder(self.btnDeleteGuides, self.btnCreateRig)
        QWidget.setTabOrder(self.btnCreateRig, self.btnDeleteRig)
        QWidget.setTabOrder(self.btnDeleteRig, self.btnDeletePart)

        self.retranslateUi(wgPick)
        self.btnTreeView.toggled.connect(self.wgsTreeContainer.setVisible)

        QMetaObject.connectSlotsByName(wgPick)
    # setupUi

    def retranslateUi(self, wgPick):
        self.lblMain.setText(QCoreApplication.translate("wgPick", u"SELECT MAIN GROUP NAME", None))
        self.lneMainInput.setPlaceholderText(QCoreApplication.translate("wgPick", u"Main", None))
        self.lblAddParts.setText(QCoreApplication.translate("wgPick", u"ADD PARTS", None))
        self.lblPart.setText(QCoreApplication.translate("wgPick", u"Part", None))
        self.cbParts.setItemText(0, QCoreApplication.translate("wgPick", u"Spine", None))
        self.cbParts.setItemText(1, QCoreApplication.translate("wgPick", u"Neck", None))
        self.cbParts.setItemText(2, QCoreApplication.translate("wgPick", u"Arm", None))
        self.cbParts.setItemText(3, QCoreApplication.translate("wgPick", u"Leg", None))
        self.cbParts.setItemText(4, QCoreApplication.translate("wgPick", u"Hand", None))
        self.cbParts.setItemText(5, QCoreApplication.translate("wgPick", u"Foot", None))

        self.btnAddPart.setText(QCoreApplication.translate("wgPick", u"Add Part", None))
        self.btnTreeView.setText(QCoreApplication.translate("wgPick", u"\u25bc Hierarchy", None))
        self.btnDeletePart.setText(QCoreApplication.translate("wgPick", u"Delete Part", None))
        self.btnCreateGuides.setText(QCoreApplication.translate("wgPick", u"Create Guides", None))
        self.btnDeleteGuides.setText(QCoreApplication.translate("wgPick", u"Delete Guides", None))
        self.btnCreateRig.setText(QCoreApplication.translate("wgPick", u"Create Rig", None))
        self.btnDeleteRig.setText(QCoreApplication.translate("wgPick", u"Delete Rig", None))
        pass
    # retranslateUi

