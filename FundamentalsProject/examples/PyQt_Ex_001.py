from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys




class MyWindow(QMainWindow): # Take properties of QMainWindow and change them in MyWindow

	def __init__(self):
		super(MyWindow, self).__init__()
		self.setGeometry(200, 200, 300, 300)
		self.setWindowTitle("PyQt5 Ex 001")
		self.initUI()

	def initUI(self):
		self.label = QtWidgets.QLabel(self)
		self.label.setText("My first label")
		self.label.move(50, 50)

		self.b1 = QtWidgets.QPushButton(self)
		self.b1.setText("Click me")
		self.b1.clicked.connect(self.button_clicked)

	def button_clicked(self):
		self.label.setText("You pressed the button")
		self.update()

	def update(self):
		self.label.adjustSize()




def window():
	app = QApplication(sys.argv)
	win = MyWindow()


	win.show()
	#sys.exit(app.exec_())	# Default exit
	app.exec_()				# Exit under Visual Studio


window()