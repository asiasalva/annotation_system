import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from GUI import MainWindow


# This is the launcer class of the project

class MyMainWindow(QMainWindow):
	def __init__(self, ui, parent = None):
		return super(MyMainWindow, self).__init__(parent)

	def closeEvent(self, event):
		if ui.exitProgram() == QMessageBox.Cancel:
			event.ignore()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = MainWindow.Ui_MainWindow()
	mainWindow = MyMainWindow(ui)
	ui.setupUi(mainWindow)
	ui.setupAnnotations(0)
	mainWindow.show()
	sys.exit(app.exec_())