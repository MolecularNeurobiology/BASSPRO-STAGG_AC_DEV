# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auto_simp_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Auto_simp(object):
    def setupUi(self, Auto_simp):
        Auto_simp.setObjectName("Auto_simp")
        Auto_simp.resize(3800, 2000)
        self.gridLayout = QtWidgets.QGridLayout(Auto_simp)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(Auto_simp)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.load_simp = QtWidgets.QPushButton(Auto_simp)
        self.load_simp.setObjectName("load_simp")
        self.horizontalLayout.addWidget(self.load_simp)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.save_simp = QtWidgets.QPushButton(Auto_simp)
        self.save_simp.setObjectName("save_simp")
        self.horizontalLayout.addWidget(self.save_simp)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.simp_table = QtWidgets.QTableWidget(Auto_simp)
        self.simp_table.setObjectName("simp_table")
        self.simp_table.setColumnCount(0)
        self.simp_table.setRowCount(0)
        self.horizontalLayout_3.addWidget(self.simp_table)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.horizontalLayout_3.setStretch(1, 8)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem9)
        self.ok_simp = QtWidgets.QPushButton(Auto_simp)
        self.ok_simp.setObjectName("ok_simp")
        self.horizontalLayout_2.addWidget(self.ok_simp)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem10)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem11)
        self.verticalLayout.setStretch(3, 8)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Auto_simp)
        self.ok_simp.clicked.connect(Auto_simp.hide)
        self.load_simp.clicked.connect(Auto_simp.load_auto_simp_file)
        self.save_simp.clicked.connect(Auto_simp.save_auto_simp_files)
        QtCore.QMetaObject.connectSlotsByName(Auto_simp)

    def retranslateUi(self, Auto_simp):
        _translate = QtCore.QCoreApplication.translate
        Auto_simp.setWindowTitle(_translate("Auto_simp", "Form"))
        self.label.setText(_translate("Auto_simp", "Autosections"))
        self.load_simp.setText(_translate("Auto_simp", "Load"))
        self.save_simp.setText(_translate("Auto_simp", "Save"))
        self.ok_simp.setText(_translate("Auto_simp", "Ok"))
