from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QFormLayout, QFrame, QComboBox, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QColor, QBrush, QPainter
from PyQt5.QtSvg import QSvgWidget



class AnnotationsProperties(QWidget):

	### "List view" for annotation properties ###

	def setupUi(self, MainWindow):

		self.mw = MainWindow


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
		#self.comboboxColor.activated.connect(self.getSelectedColor)
		self.comboboxColor.activated.connect(self.changeProperties)
		self.spinboxValue1.valueChanged.connect(self.changeProperties)
		self.spinboxValue2.valueChanged.connect(self.changeProperties)

		#self.setProperties(None, False, "#000000", 1, 10)

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



	def setProperties(self, annotationClass, isArrow, colorString, value1, value2):
		print("Choosing properties")

		self.spinboxValue1.blockSignals(True)
		self.spinboxValue2.blockSignals(True)

		if annotationClass is None:
			# DRAWING
			self.lblColor.setText("Brush color:")
			self.lblValue1.setText("Brush size:")
			self.lblValue2.setText("Rubber size:")
			self.spinboxValue1.setRange(1, 100)
			self.spinboxValue1.setValue(value1)
			self.spinboxValue2.setRange(1, 100)
			self.spinboxValue2.setValue(value2)

			if(self.comboboxColor.itemData(0) is not None):
				self.insertRubber(self.comboboxColor, 0)

			self.comboboxColor.setCurrentIndex(self.comboboxColor.findData(colorString))
		else:
			# Annotation -> remove rubber from colors
			if(self.comboboxColor.itemData(0) is None):
				self.removeRubber(self.comboboxColor, 0)

			#if(isinstance(annotation.childWidget, QtWidgets.QPlainTextEdit)):
				# TEXTBOX
				# ???

			if annotationClass is QSvgWidget:
				# SVG
				if isArrow:
					# ARROW
					self.lblColor.setText("Arrow color:")
					self.lblValue1.setText("Arrow opacity:")
					self.lblValue2.setText("Arrow rotation:")
					self.spinboxValue1.setRange(0, 100)
					self.spinboxValue1.setValue(value1)
					self.spinboxValue2.setRange(0, 360)
					self.spinboxValue2.setValue(value2)
					self.comboboxColor.setCurrentIndex(self.comboboxColor.findData(colorString))
				else:
					# LINE
					self.lblColor.setText("Line color:")
					self.lblValue1.setText("Line width:")
					self.lblValue2.setText("Line rotation:")
					self.spinboxValue1.setRange(1, 25)
					self.spinboxValue1.setValue(value1)
					self.spinboxValue2.setRange(0, 360)
					self.spinboxValue2.setValue(value2)
					self.comboboxColor.setCurrentIndex(self.comboboxColor.findData(colorString))


		
		self.spinboxValue1.blockSignals(False)
		self.spinboxValue2.blockSignals(False)



	def changeProperties(self):
		selectedColor = self.comboboxColor.currentData()
		selectedValue1 = self.spinboxValue1.value()
		selectedValue2 = self.spinboxValue2.value()


		self.mw.setNewAnnotationProperties(selectedColor, selectedValue1, selectedValue2)


		



	def getSelectedColor(self):
		print(self.comboboxColor.currentData())

	def insertRubber(self, combobox, index):
		combobox.insertItem(index, QIcon(QPixmap("C:\\Users\\Brugix\\source\\repos\\FundamentalsProject\\FundamentalsProject\\GUI\\rubber.svg").scaled(12,12)), "Rubber", None)

	def removeRubber(self, combobox, index):
		combobox.removeItem(index)
	
	def insertColor(self, combobox, brushColor, name):
		pix = QPixmap(12, 12)
		painter = QPainter(pix)

		painter.setPen(Qt.gray)
		painter.setBrush(brushColor)
		painter.drawRect(0, 0, 12, 12)

		painter.end()

		combobox.addItem(QIcon(pix), name, brushColor.color().name())


	def setStandardColors(self, combobox):
		self.insertColor(combobox, QBrush(Qt.black), "Black")					# 2		#000000
		self.insertColor(combobox, QBrush(Qt.white), "White")					# 3		#ffffff
		self.insertColor(combobox, QBrush(Qt.red), "Red")						# 7		#ff0000
		self.insertColor(combobox, QBrush(Qt.darkRed), "Dark red")				# 13	#800000
		self.insertColor(combobox, QBrush(Qt.green), "Green")					# 8		#00ff00
		self.insertColor(combobox, QBrush(Qt.darkGreen), "Dark green")			# 14	#008000
		self.insertColor(combobox, QBrush(Qt.blue), "Blue")						# 9		#0000ff
		self.insertColor(combobox, QBrush(Qt.darkBlue), "Dark blue")			# 15	#000080
		self.insertColor(combobox, QBrush(Qt.cyan), "Cyan")						# 10	#00ffff
		self.insertColor(combobox, QBrush(Qt.darkCyan), "Dark cyan")			# 16	#008080
		self.insertColor(combobox, QBrush(Qt.magenta), "Magenta")				# 11	#ff00ff
		self.insertColor(combobox, QBrush(Qt.darkMagenta), "Dark magenta")		# 17	#800080
		self.insertColor(combobox, QBrush(Qt.yellow), "Yellow")					# 12	#ffff00
		self.insertColor(combobox, QBrush(Qt.darkYellow), "Dark yellow")		# 18	#808000
		self.insertColor(combobox, QBrush(Qt.gray), "Gray")						# 5		#a0a0a4
		self.insertColor(combobox, QBrush(Qt.darkGray), "Dark gray")			# 4		#808080
		self.insertColor(combobox, QBrush(Qt.lightGray), "Light gray")			# 6		#c0c0c0