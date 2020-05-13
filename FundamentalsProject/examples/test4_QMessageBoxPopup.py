# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test4_QMessageBoxPopup.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(800, 600)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.pushButton = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton.setGeometry(QtCore.QRect(130, 220, 93, 28))
		self.pushButton.setObjectName("pushButton")
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		self.pushButton.clicked.connect(self.show_popup)



	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.pushButton.setText(_translate("MainWindow", "Show Popup"))


	def show_popup(self):
		msg = QMessageBox()
		msg.setWindowTitle("Tutorial on PyQt5")
		msg.setText("This is the main text")
		msg.setIcon(QMessageBox.Critical)		# Options for the icon are: Critical, Warning, Question, Information
		msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Retry|QMessageBox.Ignore|QMessageBox.Yes|QMessageBox.No)	# Options for message box buttons: Ok, Open, Save, Cancel, Close, Yes, No, Abort, Retry, Ignore
		msg.setDefaultButton(QMessageBox.Ignore)
		msg.setInformativeText("Informative text")

		msg.buttonClicked.connect(self.popup_button)

		msg.setDetailedText("Details")

		x = msg.exec_()		# Show the message box


	def popup_button(self, i):		# i -> clicked widget
		print(i.text())





if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
