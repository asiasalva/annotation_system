from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QPushButton, QFormLayout, QFrame, QComboBox, QSpinBox, QPlainTextEdit, QTimeEdit, QDateTimeEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QColor, QBrush, QPainter, QValidator
from PyQt5.QtSvg import QSvgWidget

import time
import datetime



class MyTimeEdit(QTimeEdit):
	def __init__(self, *args, **kwargs):
		super(MyTimeEdit, self).__init__(*args, **kwargs)

	def stepBy(self, steps):
		#if (self.currentSection() == QDateTimeEdit.MinuteSection):
		#	self.setTime(self.time().addSecs(steps*60))
		#elif (self.currentSection() == QDateTimeEdit.SecondSection):
		#	self.setTime(self.time().addSecs(steps))

		if (self.currentSection() == QDateTimeEdit.MinuteSection):
			m = self.time().minute()
			if ((m == 0) and (steps < 0)):
				self.setTime(self.time().addSecs(-3600))
			elif ((m == 59) and (steps > 0)):
				self.setTime(self.time().addSecs(3600))
		elif (self.currentSection() == QDateTimeEdit.SecondSection):
			s = self.time().second()
			if ((s == 0) and (steps < 0)):
				self.setTime(self.time().addSecs(-60))
			elif ((s == 59) and (steps > 0)):
				self.setTime(self.time().addSecs(60))


class SpinBoxTime(QSpinBox):
	def __init__(self, *args, **kwargs):
		super(SpinBoxTime, self).__init__(*args, **kwargs)

	def textFromValue(self, value):
		return time.strftime("%H:%M:%S", time.gmtime(value))

	def valueFromText(self, text):
		if self.parseString(text):
			time_string = text
			date_time = datetime.datetime.strptime(time_string, "%H:%M:%S")
			a_timedelta = date_time - datetime.datetime(1900, 1, 1)
			seconds = a_timedelta.total_seconds()
			return seconds
	
	def validate(self, text, pos):
		if self.parseString(text):
			return (QValidator.Acceptable, text, pos)
		else:
			return (QValidator.Invalid, text, pos)

	def parseString(self, text):
		try:
			time.strptime(str(text), '%H:%M:%S')
			return True
		except ValueError:
			return False



class AnnotationsPropertiesSubclass(QWidget):

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
		self.spinboxSecStart = QSpinBox()
		self.spinboxSecEnd = QSpinBox()
		self.timeEditSecStart = MyTimeEdit()
		self.timeEditSecStart.setDisplayFormat("hh:mm:ss")
		self.spinboxtime = SpinBoxTime()
		self.spinboxtime.setRange(0, 61)
		self.spinboxtime.valueChanged.connect(self.prova)

		self.setStandardColors(self.comboboxColor)
		self.comboboxColor.activated.connect(self.changeProperties)
		self.spinboxValue1.valueChanged.connect(self.changeProperties)
		self.spinboxValue2.valueChanged.connect(self.changeProperties)
		self.spinboxSecStart.valueChanged.connect(self.changeProperties)
		self.spinboxSecEnd.valueChanged.connect(self.changeProperties)

		self.formLayout.addRow(self.lblColor, self.comboboxColor)
		self.formLayout.addRow(self.lblValue1, self.spinboxValue1)
		self.formLayout.addRow(self.lblValue2, self.spinboxValue2)
		secRange = QHBoxLayout()
		secRange.addWidget(QLabel("On screen (sec):"))
		secRange.addWidget(QLabel(" from "))
		secRange.addWidget(self.spinboxSecStart)
		secRange.addWidget(QLabel(" to "))
		secRange.addWidget(self.spinboxSecEnd)
		self.formLayout.addRow(secRange)
		self.formLayout.addRow(self.timeEditSecStart)
		self.formLayout.addRow(self.spinboxtime)
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

	def prova(self):
		x = self.spinboxtime.value()
		print("x = " + str(x))
		print(self.spinboxtime.text())

		try:
			time.strptime(str(x), '%H:%M:%S')
			print("ok")
		except ValueError:
			print("no")


	def setProperties(self, annotationClass, isArrow, colorString, value1, value2, secStart, secEnd):

		self.spinboxValue1.blockSignals(True)
		self.spinboxValue2.blockSignals(True)
		self.spinboxSecStart.blockSignals(True)
		self.spinboxSecEnd.blockSignals(True)



		self.lblColor.setHidden(False)
		self.lblValue1.setHidden(False)
		self.lblValue2.setHidden(False)
		self.spinboxValue1.setHidden(False)
		self.spinboxValue2.setHidden(False)
		self.comboboxColor.setHidden(False)
		self.spinboxSecStart.setHidden(False)
		self.spinboxSecEnd.setHidden(False)
		





		# Parte comune a tutte le annotazioni
		self.spinboxValue1.setValue(value1)
		self.spinboxValue2.setValue(value2)
		self.spinboxSecStart.setValue(secStart)
		self.spinboxSecEnd.setValue(secEnd)


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


			self.spinboxSecStart.setHidden(True)
			self.spinboxSecEnd.setHidden(True)
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
		self.spinboxSecStart.blockSignals(False)
		self.spinboxSecEnd.blockSignals(False)



	def changeProperties(self):
		selectedColor = self.comboboxColor.currentData()
		selectedValue1 = self.spinboxValue1.value()
		selectedValue2 = self.spinboxValue2.value()
		secondStart = self.spinboxSecStart.value()
		secondEnd = self.spinboxSecEnd.value()

		if secondStart > secondEnd:
			if self.sender() is self.spinboxSecStart:
				self.spinboxSecStart.setValue(secondEnd)
			elif self.sender() is self.spinboxSecEnd:
				self.spinboxSecEnd.setValue(secondStart)
		else:
			self.mw.setNewAnnotationProperties(selectedColor, selectedValue1, selectedValue2, secondStart, secondEnd)
		

	def setDuration(self, duration):
		self.spinboxSecStart.setRange(0, duration)
		self.spinboxSecEnd.setRange(0, duration)

		

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