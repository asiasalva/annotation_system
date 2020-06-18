from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QFormLayout, QFrame
from PyQt5.QtCore import Qt


from PyQt5.QtWidgets import QCheckBox, QDialogButtonBox



class AnnotationsProperties(QWidget):

	### "List view" for annotation properties ###

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
		container.addWidget(QLabel("Properties"))
		container.addWidget(self.scroll)









		### EXAMPLE
		self.formLayout.addRow(QLabel("Is visible"), QCheckBox("Yes"))
		self.formLayout.addRow(QLabel("Is visible"), QDialogButtonBox(QDialogButtonBox.Yes|QDialogButtonBox.No))
		self.frame.setLayout(self.formLayout)
		self.scroll.setWidget(self.frame)