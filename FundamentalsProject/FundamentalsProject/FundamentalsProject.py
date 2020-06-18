import sys

from PyQt5 import QtWidgets

from GUI import MainWindow



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = QtWidgets.QMainWindow()
	ui = MainWindow.Ui_MainWindow()
	ui.setupUi(mainWindow)
	ui.setupAnnotations(0)
	mainWindow.show()
	sys.exit(app.exec_())