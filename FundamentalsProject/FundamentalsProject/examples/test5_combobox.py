# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test5_combobox.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(800, 600)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.comboX = QtWidgets.QComboBox(self.centralwidget)
		self.comboX.setGeometry(QtCore.QRect(30, 60, 231, 181))
		font = QtGui.QFont()
		font.setPointSize(36)
		self.comboX.setFont(font)
		self.comboX.setObjectName("comboX")
		self.comboX.addItem("")
		self.comboX.addItem("")
		self.comboY = QtWidgets.QComboBox(self.centralwidget)
		self.comboY.setGeometry(QtCore.QRect(380, 60, 231, 181))
		font = QtGui.QFont()
		font.setPointSize(36)
		self.comboY.setFont(font)
		self.comboY.setObjectName("comboY")
		self.comboY.addItem("")
		self.comboY.addItem("")
		self.btn_submit = QtWidgets.QPushButton(self.centralwidget)
		self.btn_submit.setGeometry(QtCore.QRect(250, 410, 181, 71))
		font = QtGui.QFont()
		font.setPointSize(22)
		self.btn_submit.setFont(font)
		self.btn_submit.setObjectName("btn_submit")
		self.label_result = QtWidgets.QLabel(self.centralwidget)
		self.label_result.setGeometry(QtCore.QRect(190, 300, 311, 61))
		font = QtGui.QFont()
		font.setPointSize(22)
		self.label_result.setFont(font)
		self.label_result.setObjectName("label_result")
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)



		
		#### Set default combobox item to show...
		
		#self.comboX.addItem("Hello")

		### ...by setting the index of the string (needs to be present, otherwise the index will be -1 -> not found)
		#index = self.comboX.findText("Hello", QtCore.Qt.MatchFixedString)
		#self.comboX.setCurrentIndex(index)
		### ...by setting the string of the item (needs to be present, otherwise it sets the first value as default)
		##self.comboX.setCurrentText("Hello")
		

		self.btn_submit.clicked.connect(self.pressed)



		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.comboX.setItemText(0, _translate("MainWindow", "0"))
		self.comboX.setItemText(1, _translate("MainWindow", "1"))
		self.comboY.setItemText(0, _translate("MainWindow", "0"))
		self.comboY.setItemText(1, _translate("MainWindow", "1"))
		self.btn_submit.setText(_translate("MainWindow", "Submit"))
		self.label_result.setText(_translate("MainWindow", "X XOR Y = "))


	def pressed(self):
		x = int(self.comboX.currentText())
		y = int(self.comboY.currentText())
		xor = (x and not y) or (not x and y)

		self.label_result.setText("X XOR Y = " + str(xor))



if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
