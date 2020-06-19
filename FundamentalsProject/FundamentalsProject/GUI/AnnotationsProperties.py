from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QFormLayout, QFrame, QComboBox, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QColor, QBrush, QPainter
from PyQt5.QtSvg import QSvgWidget



class AnnotationsProperties(QWidget):

	### "List view" for annotation properties ###

	def setupUi(self, MainWindow):

		### Widgets simulating a list view
		self.formLayout = QFormLayout()
		self.frame = QFrame()
		self.scroll = QScrollArea()


		

		'''
		### EXAMPLE
		self.comboBox = QComboBox()
		self.comboBox.activated.connect(self.getSelectedColor)

		self.setStandardColors()


		self.formLayout.addRow(QLabel("Is visible"), QCheckBox("Yes"))
		self.formLayout.addRow(QLabel("Is visible"), QDialogButtonBox(QDialogButtonBox.Yes|QDialogButtonBox.No))
		self.formLayout.addRow(QLabel("Is visible"), QPushButton("Ciao"))
		self.formLayout.addRow(QLabel("Is visible"), QPushButton("Ciao"))
		self.formLayout.addRow(QLabel("Is visible"), self.comboBox)
		self.frame.setLayout(self.formLayout)
		self.scroll.setWidget(self.frame)
		self.scroll.setWidgetResizable(True)
		'''


		self.lblColor = QLabel("Color:")
		self.lblValue1 = QLabel("Value1:")
		self.lblValue2 = QLabel("Value2:")
		self.spinboxValue1 = QSpinBox()
		self.spinboxValue2 = QSpinBox()
		self.comboboxColor = QComboBox()

		self.setStandardColors(self.comboboxColor)
		self.comboboxColor.activated.connect(self.getSelectedColor)

		self.setProperties(None)

		self.formLayout.addRow(self.lblColor, self.comboboxColor)
		self.formLayout.addRow(self.lblValue1, self.spinboxValue1)
		self.formLayout.addRow(self.lblValue2, self.spinboxValue2)
		self.frame.setLayout(self.formLayout)
		self.scroll.setWidget(self.frame)
		self.scroll.setWidgetResizable(True)
		

		''' 
		List of properties for each type of annotation

		LINE:
			color			QComboBox
			width			QSpinBox	(range: 1, 25)	(default: 1)
			rotation		QSpinBox	(range: 0, 360)	(default: 0)

		ARROW:
			color			QComboBox
			opacity			QSpinBox	(range: 0, 100)	(default: 100)
			rotation		QSpinBox	(range: 0, 360)	(default: 0)

		TEXTBOX:
			background color ???	QComboBox
			???

		BREAKPOINT:
			???

		DRAWING:
			LINE:
				color		QComboBox	(add rubber on top position)
				size		QSpinBox	(range: 1, 100)	(default: 1)
			
			RUBBER:
				size		QSpinBox	(range: 1, 100)	(default: 10)
		'''
		
		### Widget container
		container = QVBoxLayout(self)
		container.addWidget(QLabel("Properties"))
		container.addWidget(self.scroll)



	def setProperties(self, annotation):
		print("Choosing properties")

		if annotation is None:
			# DRAWING
			self.lblColor.setText("Brush color:")
			self.lblValue1.setText("Brush size:")
			self.lblValue2.setText("Rubber size:")
			self.spinboxValue1.setRange(1, 100)
			self.spinboxValue1.setValue(1)
			self.spinboxValue2.setRange(1, 100)
			self.spinboxValue2.setValue(10)

			if(self.comboboxColor.itemData(0) != 0):
				self.insertRubber(self.comboboxColor, 0)
		else:
			# Annotation -> remove rubber from colors
			if(self.comboboxColor.itemData(0) == 0):
				self.removeRubber(self.comboboxColor, 0)

			#if(isinstance(annotation.childWidget, QtWidgets.QPlainTextEdit)):
				# TEXTBOX
				# ???

			if(isinstance(annotation.childWidget, QSvgWidget)):
				# SVG
				if annotation.isArrow:
					# ARROW
					self.lblColor.setText("Arrow color:")
					self.lblValue1.setText("Arrow opacity:")
					self.lblValue2.setText("Arrow rotation:")
					self.spinboxValue1.setRange(0, 100)
					self.spinboxValue1.setValue(100)
					self.spinboxValue2.setRange(0, 360)
					self.spinboxValue2.setValue(0)
				else:
					# LINE
					self.lblColor.setText("Line color:")
					self.lblValue1.setText("Line width:")
					self.lblValue2.setText("Line rotation:")
					self.spinboxValue1.setRange(1, 25)
					self.spinboxValue1.setValue(1)
					self.spinboxValue2.setRange(0, 360)
					self.spinboxValue2.setValue(0)






	def getSelectedColor(self):
		print(self.comboboxColor.currentData())

	def insertRubber(self, combobox, index):
		combobox.insertItem(index, QIcon(QPixmap("C:\\Users\\Brugix\\source\\repos\\FundamentalsProject\\FundamentalsProject\\GUI\\rubber.svg").scaled(12,12)), "Rubber", 0)

	def removeRubber(self, combobox, index):
		combobox.removeItem(index)
	
	def insertColor(self, combobox, color, name):
		pix = QPixmap(12, 12)
		painter = QPainter(pix)

		painter.setPen(Qt.gray)
		painter.setBrush(QBrush(color))
		painter.drawRect(0, 0, 12, 12)
		painter.end()

		combobox.addItem(QIcon(pix), name, color)

	def setStandardColors(self, combobox):
		self.insertColor(combobox, Qt.black, "Black")					# 2
		self.insertColor(combobox, Qt.white, "White")					# 3
		self.insertColor(combobox, Qt.red, "Red")						# 7
		self.insertColor(combobox, Qt.darkRed, "Dark red")				# 13
		self.insertColor(combobox, Qt.green, "Green")					# 8
		self.insertColor(combobox, Qt.darkGreen, "Dark green")			# 14
		self.insertColor(combobox, Qt.blue, "Blue")						# 9
		self.insertColor(combobox, Qt.darkBlue, "Dark blue")			# 15
		self.insertColor(combobox, Qt.cyan, "Cyan")						# 10
		self.insertColor(combobox, Qt.darkCyan, "Dark cyan")			# 16
		self.insertColor(combobox, Qt.magenta, "Magenta")				# 11
		self.insertColor(combobox, Qt.darkMagenta, "Dark magenta")		# 17
		self.insertColor(combobox, Qt.yellow, "Yellow")					# 12
		self.insertColor(combobox, Qt.darkYellow, "Dark yellow")		# 18
		self.insertColor(combobox, Qt.gray, "Gray")						# 5
		self.insertColor(combobox, Qt.darkGray, "Dark gray")			# 4
		self.insertColor(combobox, Qt.lightGray, "Light gray")			# 6