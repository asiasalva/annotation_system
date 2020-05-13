from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QFormLayout, QFrame
from PyQt5.QtCore import Qt

class AnnotationsList(QWidget):

	### "List view" for annotation types ###

	def setupUi(self, MainWindow):

		### Widgets simulating a list view
		self.formLayout = QFormLayout()
		self.frame = QFrame()
		self.scroll = QScrollArea()

		#f = QFormLayout()
		#f.addRow(QLabel("PROPERTIES"))
		#f.setLabelAlignment(Qt.AlignCenter)
		#self.formLayout.addRow(f)
		#self.formLayout.addRow("\t\t\t\t\t", QLabel("PROPERTIES"))

		#self.frame.setLayout(self.formLayout)
		#self.scroll.setWidget(self.frame)

		### Widget container
		container = QVBoxLayout(self)
		container.addWidget(QLabel("Types"))
		container.addWidget(self.scroll)




		### EXAMPLE
		self.formLayout.addRow(QPushButton("TextBox"))
		self.frame.setLayout(self.formLayout)
		self.scroll.setWidget(self.frame)




	'''
	### Insert items in "list view"
	def prova(self, val):
		labelLis = []
		comboList = []
		for i in  range(val):
			labelLis.append(QLabel("Property " + str(i)))
			comboList.append(QPushButton("Change me"))
			self.formLayout.addRow(labelLis[i], comboList[i])

		f = QFormLayout()
		f.addRow(QLabel("Propuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuerties"),QLabel("Properties"))
		self.formLayout.addRow(QLabel("Properties"))
		self.formLayout.addRow(QLabel("Properties"),QLabel("Properties"))
		self.formLayout.addRow(QLabel("1"),f)
		
		self.frame.setLayout(self.formLayout)
		self.scroll.setWidget(self.frame)
	'''