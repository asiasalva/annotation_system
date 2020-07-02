from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QPushButton, QFormLayout, QFrame, QComboBox, QSpinBox, QPlainTextEdit, QTimeEdit
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QPixmap, QIcon, QColor, QBrush, QPainter
from PyQt5.QtSvg import QSvgWidget



class AnnotationsPropertiesTime(QWidget):

	### "List view" for annotation properties ###

	def setupUi(self, MainWindow):

		self.mw = MainWindow


		### Widgets simulating a list view
		self.formLayout = QFormLayout()
		self.frame = QFrame()
		self.scroll = QScrollArea()



		self.lblColor = QLabel("Color:")
		self.lblValue1 = QLabel("Value1:")
		self.lblValue2 = QLabel("Value2:")
		self.comboboxColor = QComboBox()
		self.spinboxValue1 = QSpinBox()
		self.spinboxValue2 = QSpinBox()
		#self.spinboxSecStart = QSpinBox()
		#self.spinboxSecEnd = QSpinBox()
		self.timeEditSecStart = QTimeEdit()
		self.timeEditSecEnd = QTimeEdit()

		self.timeEditSecStart.setDisplayFormat("hh:mm:ss")
		self.timeEditSecEnd.setDisplayFormat("hh:mm:ss")
		self.timeEditSecStart.stepBy(1)

		self.setStandardColors(self.comboboxColor)
		self.comboboxColor.activated.connect(self.changeProperties)
		self.spinboxValue1.valueChanged.connect(self.changeProperties)
		self.spinboxValue2.valueChanged.connect(self.changeProperties)
		#self.spinboxSecStart.valueChanged.connect(self.changeProperties)
		#self.spinboxSecEnd.valueChanged.connect(self.changeProperties)
		self.timeEditSecStart.timeChanged.connect(self.changeProperties)
		self.timeEditSecEnd.timeChanged.connect(self.changeProperties)

		self.formLayout.addRow(self.lblColor, self.comboboxColor)
		self.formLayout.addRow(self.lblValue1, self.spinboxValue1)
		self.formLayout.addRow(self.lblValue2, self.spinboxValue2)
		secRange = QHBoxLayout()
		secRange.addWidget(QLabel("On screen (sec):"))
		secRange.addWidget(QLabel(" from "))
		#secRange.addWidget(self.spinboxSecStart)
		secRange.addWidget(self.timeEditSecStart)
		secRange.addWidget(QLabel(" to "))
		#secRange.addWidget(self.spinboxSecEnd)
		secRange.addWidget(self.timeEditSecEnd)
		self.formLayout.addRow(secRange)
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



	def setProperties(self, annotationClass, isArrow, colorString, value1, value2, secStart, secEnd):

		self.spinboxValue1.blockSignals(True)
		self.spinboxValue2.blockSignals(True)
		#self.spinboxSecStart.blockSignals(True)
		#self.spinboxSecEnd.blockSignals(True)
		self.timeEditSecStart.blockSignals(True)
		self.timeEditSecEnd.blockSignals(True)



		self.lblColor.setHidden(False)
		self.lblValue1.setHidden(False)
		self.lblValue2.setHidden(False)
		self.spinboxValue1.setHidden(False)
		self.spinboxValue2.setHidden(False)
		self.comboboxColor.setHidden(False)
		#self.spinboxSecStart.setHidden(False)
		#self.spinboxSecEnd.setHidden(False)
		self.timeEditSecStart.setHidden(False)
		self.timeEditSecEnd.setHidden(False)
		





		# Parte comune a tutte le annotazioni
		self.spinboxValue1.setValue(value1)
		self.spinboxValue2.setValue(value2)
		#self.spinboxSecStart.setValue(secStart)
		#self.spinboxSecEnd.setValue(secEnd)
		self.timeEditSecStart.setTime(QTime(0,0,0,0).addSecs(secStart))
		self.timeEditSecEnd.setTime(QTime(0,0,0,0).addSecs(secEnd))



		if annotationClass is None:
			# DRAWING
			self.lblColor.setText("Brush color:")
			self.lblValue1.setText("Brush size:")
			self.lblValue2.setText("Rubber size:")
			self.spinboxValue1.setRange(1, 100)
			self.spinboxValue2.setRange(1, 100)

			if(self.comboboxColor.itemData(0) is not None):
				self.insertRubber(self.comboboxColor, 0)

			self.comboboxColor.setCurrentIndex(self.comboboxColor.findData(colorString))


			#self.spinboxSecStart.setHidden(True)
			#self.spinboxSecEnd.setHidden(True)
			self.timeEditSecStart.setHidden(True)
			self.timeEditSecEnd.setHidden(True)
		else:
			# Annotation -> remove rubber from colors
			if(self.comboboxColor.itemData(0) is None):
				self.removeRubber(self.comboboxColor, 0)

			if annotationClass is QPlainTextEdit:
				# TEXTBOX
				self.lblColor.setText("Text color:")
				self.lblValue1.setText("Text size:")
				self.lblValue2.setText("Background opacity:")
				self.spinboxValue1.setRange(1, 100)
				self.spinboxValue2.setRange(0, 100)
				self.comboboxColor.setCurrentIndex(self.comboboxColor.findData(colorString))

			if annotationClass is QSvgWidget:
				# SVG
				if isArrow:
					# ARROW
					self.lblColor.setText("Arrow color:")
					self.lblValue1.setText("Arrow opacity:")
					self.lblValue2.setText("Arrow rotation:")
					self.spinboxValue1.setRange(0, 100)
					self.spinboxValue2.setRange(0, 360)
					self.comboboxColor.setCurrentIndex(self.comboboxColor.findData(colorString))
				else:
					# LINE
					self.lblColor.setText("Line color:")
					self.lblValue1.setText("Line width:")
					self.lblValue2.setText("Line rotation:")
					self.spinboxValue1.setRange(1, 25)
					self.spinboxValue2.setRange(0, 360)
					self.comboboxColor.setCurrentIndex(self.comboboxColor.findData(colorString))


		
		self.spinboxValue1.blockSignals(False)
		self.spinboxValue2.blockSignals(False)
		#self.spinboxSecStart.blockSignals(False)
		#self.spinboxSecEnd.blockSignals(False)
		self.timeEditSecStart.blockSignals(False)
		self.timeEditSecEnd.blockSignals(False)



	def changeProperties(self):
		selectedColor = self.comboboxColor.currentData()
		selectedValue1 = self.spinboxValue1.value()
		selectedValue2 = self.spinboxValue2.value()
		#secondStart = self.spinboxSecStart.value()
		#secondEnd = self.spinboxSecEnd.value()
		secondStart = (-1)*(self.timeEditSecStart.time()).secsTo(QTime(0,0,0.0))
		secondEnd = (-1)*(self.timeEditSecEnd.time()).secsTo(QTime(0,0,0,0))

		if secondStart > secondEnd:
			if self.sender() is self.timeEditSecStart:#self.spinboxSecStart:
				#self.spinboxSecStart.setValue(secondEnd)
				self.timeEditSecStart.setTime(QTime(0,0,0,0).addSecs(secondEnd))
			elif self.sender() is self.timeEditSecEnd:#self.spinboxSecEnd:
				#self.spinboxSecEnd.setValue(secondStart)
				self.timeEditSecEnd.setTime(QTime(0,0,0,0).addSecs(secondStart))
		else:
			self.mw.setNewAnnotationProperties(selectedColor, selectedValue1, selectedValue2, secondStart, secondEnd)
		

	def setDuration(self, duration):
		#self.spinboxSecStart.setRange(0, duration)
		#self.spinboxSecEnd.setRange(0, duration)
		#self.timeEditSecStart.setTimeRange(QTime(0,0,0), QTime(0,0,50))#QTime(0,0,0).addSecs(duration))
		self.timeEditSecEnd.setTimeRange(QTime(0,0,0,0), QTime(0,0,50,0))#QTime(0,0,0).addSecs(duration))

		

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