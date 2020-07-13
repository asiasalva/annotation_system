from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QFormLayout, QFrame, QComboBox, QSpinBox, QPlainTextEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QBrush, QPainter, QValidator
from PyQt5.QtSvg import QSvgWidget

import time
import datetime
import os 

#Class annotation Properties needed to show properties on the GUI 

class SpinBoxTime(QSpinBox):
	def __init__(self, *args, **kwargs):
		super(SpinBoxTime, self).__init__(*args, **kwargs)

	def textFromValue(self, value):
		return time.strftime("%H:%M:%S", time.gmtime(value))

	def valueFromText(self, text):
		if self.parseString(text):
			date_time = datetime.datetime.strptime(text, "%H:%M:%S")
			timedelta = date_time - datetime.datetime(1900, 1, 1)
			return (timedelta.total_seconds())
	
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

class AnnotationsProperties(QWidget):

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
		self.lblTime = QLabel("On screen (sec):")
		self.lblFrom = QLabel(" from ")
		self.lblTo = QLabel(" to ")
		self.comboboxColor = QComboBox()
		self.spinboxValue1 = QSpinBox()
		self.spinboxValue2 = QSpinBox()
		self.spinboxSecStart = SpinBoxTime()
		self.spinboxSecEnd = SpinBoxTime()
		self.btnClear = QPushButton("Clear drawings")
		
		self.setStandardColors(self.comboboxColor)
		self.comboboxColor.activated.connect(self.changeProperties)
		self.spinboxValue1.valueChanged.connect(self.changeProperties)
		self.spinboxValue2.valueChanged.connect(self.changeProperties)
		self.spinboxSecStart.valueChanged.connect(self.changeProperties)
		self.spinboxSecEnd.valueChanged.connect(self.changeProperties)
		self.btnClear.clicked.connect(self.clearWindowPaint)

		self.formLayout.addRow(self.lblColor, self.comboboxColor)
		self.formLayout.addRow(self.lblValue1, self.spinboxValue1)
		self.formLayout.addRow(self.lblValue2, self.spinboxValue2)
		secRange = QHBoxLayout()
		secRange.addWidget(self.lblTime)
		secRange.addWidget(self.lblFrom)
		secRange.addWidget(self.spinboxSecStart)
		secRange.addWidget(self.lblTo)
		secRange.addWidget(self.spinboxSecEnd)
		self.formLayout.addRow(secRange)
		self.formLayout.addRow(self.btnClear)
		self.frame.setLayout(self.formLayout)
		self.scroll.setWidget(self.frame)
		self.scroll.setWidgetResizable(True)
				
		### Widget container
		container = QVBoxLayout(self)
		container.addWidget(QLabel("Properties"))
		container.addWidget(self.scroll)

	def setProperties(self, annotationClass, isArrow, isDraw, colorString, value1, value2, secStart, secEnd):
		
		self.spinboxValue1.blockSignals(True)
		self.spinboxValue2.blockSignals(True)
		self.spinboxSecStart.blockSignals(True)
		self.spinboxSecEnd.blockSignals(True)

		if annotationClass is QWidget:
			# BREAKPOINT
			self.lblColor.setHidden(True)
			self.lblValue1.setHidden(True)
			self.lblValue2.setHidden(True)
			self.lblTime.setHidden(False)
			self.lblFrom.setHidden(False)
			self.lblTo.setHidden(False)
			self.spinboxValue1.setHidden(True)
			self.spinboxValue2.setHidden(True)
			self.comboboxColor.setHidden(True)
			self.spinboxSecStart.setHidden(False)
			self.spinboxSecEnd.setHidden(True)
			self.spinboxSecStart.setValue(secStart)
			self.btnClear.setHidden(True)
			
			# Breakpoint -> remove rubber from colors
			if(self.comboboxColor.itemData(0) is None):
				self.removeRubber(self.comboboxColor, 0)
		else:
			# Common section to all the annotations
			self.lblColor.setHidden(False)
			self.lblValue1.setHidden(False)
			self.lblValue2.setHidden(False)
			self.lblTime.setHidden(False)
			self.lblFrom.setHidden(False)
			self.lblTo.setHidden(False)
			self.spinboxValue1.setHidden(False)
			self.spinboxValue2.setHidden(False)
			self.comboboxColor.setHidden(False)
			self.spinboxSecStart.setHidden(False)
			self.spinboxSecEnd.setHidden(False)
			self.spinboxValue1.setValue(value1)
			self.spinboxValue2.setValue(value2)
			self.spinboxSecStart.setValue(secStart)
			self.spinboxSecEnd.setValue(secEnd)
			self.btnClear.setHidden(True)

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

				self.lblTime.setHidden(True)
				self.lblFrom.setHidden(True)
				self.lblTo.setHidden(True)
				self.spinboxSecStart.setHidden(True)
				self.spinboxSecEnd.setHidden(True)
				self.btnClear.setHidden(False)
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

		# If RUBBER is not present in combobox (so I'm not drawing) and spinboxSecEnd is hidden (so I'm changing breakpoint's properties)
		#if (self.comboboxColor.itemData(0) is not None) and (self.spinboxSecEnd.isHidden()):
		# If btnClear is hidden (so I'm not drawing) and spinboxSecEnd is hidden (so I'm changing breakpoint's properties)
		if (self.btnClear.isHidden() and self.spinboxSecEnd.isHidden()):
			self.mw.setNewAnnotationProperties(None, 0, 0, self.spinboxSecStart.value(), self.spinboxSecStart.value())

		else:
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

	def clearWindowPaint(self):
		self.mw.clearWindowPaint()
		
	def setDuration(self, duration):
		self.spinboxSecStart.blockSignals(True)
		self.spinboxSecEnd.blockSignals(True)

		self.spinboxSecStart.setRange(0, duration)
		self.spinboxSecEnd.setRange(0, duration)

		self.spinboxSecStart.blockSignals(False)
		self.spinboxSecEnd.blockSignals(False)

	def insertRubber(self, combobox, index):
		dirname = os.path.dirname(__file__)
		fileName = os.path.join(dirname, 'rubber.svg')
		# combobox.insertItem(index, QIcon(QPixmap("C:\\Users\\Brugix\\source\\repos\\FundamentalsProject\\FundamentalsProject\\GUI\\rubber.svg").scaled(12,12)), "Rubber", None)
		combobox.insertItem(index, QIcon(QPixmap(fileName).scaled(12,12)), "Rubber", None)

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

	def setPropertiesVisible(self, visible):
		self.setVisible(visible)
