from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPoint, pyqtSignal, QRect, QByteArray
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit
from PyQt5.QtSvg import QSvgWidget

from GUI import Mode

class Annotation(QWidget):

	### TCONTAINER VARIABLES AND METHODS ###
	#region

	mode = Mode.Mode.NONE
	inFocus = pyqtSignal(bool)
	outFocus = pyqtSignal(bool)
	newGeometry = pyqtSignal(QRect)

	def __init__(self, parent, p, cWidget, isArrow, MainWindow, currentSecond): # isArrow is used to distinguish which SVG image the user wants to add (LINE or ARROW). If cWidget is a QSvgWidget, then isArrow parameter is passed in setupSvgVariables function.
		super().__init__(parent=parent)

		self.mw = MainWindow
		self.childWidget = None

		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
		self.setVisible(True)
		self.setAutoFillBackground(False)
		self.setMouseTracking(True)
		self.setFocusPolicy(QtCore.Qt.ClickFocus)
		self.setFocus()
		self.move(p)

		self.vLayout = QVBoxLayout(self)
		self.setChildWidget(cWidget, isArrow, currentSecond)

		self.m_infocus = True
		self.m_isEditing = True
		self.installEventFilter(parent)

	def setChildWidget(self, cWidget, isArrow, currentSecond):
		if cWidget:
			self.childWidget = cWidget
			self.childWidget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
			self.childWidget.setParent(self)
			self.childWidget.releaseMouse()
			self.vLayout.addWidget(cWidget)
			self.vLayout.setContentsMargins(0,0,0,0)


			self.setupAnnotationVariables(currentSecond)
			
			if(isinstance(self.childWidget, QPlainTextEdit)):
				self.setupTextboxVariables()
			elif(isinstance(self.childWidget, QSvgWidget)):
				self.setupSvgVariables(isArrow)


			self.mw.setLastFocusAnnotation(self)

	
	def focusInEvent(self, a0: QtGui.QFocusEvent):
		self.m_infocus = True
		p = self.parentWidget()
		p.installEventFilter(self)
		p.repaint()
		self.inFocus.emit(True)

		if self.childWidget is not None:
			self.mw.setLastFocusAnnotation(self)

	def focusOutEvent(self, a0: QtGui.QFocusEvent):
		if not self.m_isEditing:
			return
		self.mode = Mode.Mode.NONE
		self.outFocus.emit(False)
		self.m_infocus = False

	def paintEvent(self, e: QtGui.QPaintEvent):
		painter = QtGui.QPainter(self)
		color = (r, g, b, a) = (255, 0, 0, 0)
		painter.fillRect(e.rect(), QColor(r, g, b, a))

		if self.m_infocus:
			rect = e.rect()
			rect.adjust(0,0,-1,-1)
			painter.setPen(QColor(r, g, b))
			painter.drawRect(rect)

	def mousePressEvent(self, e: QtGui.QMouseEvent):
		self.position = QPoint(e.globalX() - self.geometry().x(), e.globalY() - self.geometry().y())
		if not self.m_isEditing:
			return
		if not self.m_infocus:
			return
		if not e.buttons() and QtCore.Qt.LeftButton:
			self.setCursorShape(e.pos())
			return
		if e.button() == QtCore.Qt.RightButton:
			self.popupShow(e.pos())
			e.accept()

		# Raises this widget to the top of the parent widget’s stack.
		self.raise_()

	def keyPressEvent(self, e: QtGui.QKeyEvent):
		if not self.m_isEditing: return
		# Remove annotation
		if e.key() == QtCore.Qt.Key_Delete:
			self.deleteLater()
			self.parentWidget().removeAnnotation(self)
		# Moving container with arrows
		if QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
			newPos = QPoint(self.x(), self.y())
			if e.key() == QtCore.Qt.Key_Up:
				newPos.setY(newPos.y() - 1)
			if e.key() == QtCore.Qt.Key_Down:
				newPos.setY(newPos.y() + 1)
			if e.key() == QtCore.Qt.Key_Left:
				newPos.setX(newPos.x() - 1)
			if e.key() == QtCore.Qt.Key_Right:
				newPos.setX(newPos.x() + 1)
			self.move(newPos)

		if QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
			if e.key() == QtCore.Qt.Key_Up:
				self.resize(self.width(), self.height() - 1)
			if e.key() == QtCore.Qt.Key_Down:
				self.resize(self.width(), self.height() + 1)
			if e.key() == QtCore.Qt.Key_Left:
				self.resize(self.width() - 1, self.height())
			if e.key() == QtCore.Qt.Key_Right:
				self.resize(self.width() + 1, self.height())
		self.newGeometry.emit(self.geometry())

	def setCursorShape(self, e_pos: QPoint):
		diff = 3
		# Left - Bottom
		if (((e_pos.y() > self.y() + self.height() - diff) and # Bottom
			(e_pos.x() < self.x() + diff)) or # Left
		# Right-Bottom
		((e_pos.y() > self.y() + self.height() - diff) and # Bottom
		(e_pos.x() > self.x() + self.width() - diff)) or # Right
		# Left-Top
		((e_pos.y() < self.y() + diff) and # Top
		(e_pos.x() < self.x() + diff)) or # Left
		# Right-Top
		(e_pos.y() < self.y() + diff) and # Top
		(e_pos.x() > self.x() + self.width() - diff)): # Right
			# Left - Bottom
			if ((e_pos.y() > self.y() + self.height() - diff) and # Bottom
			(e_pos.x() < self.x()
				+ diff)): # Left
				self.mode = Mode.Mode.RESIZEBL
				self.setCursor(QCursor(QtCore.Qt.SizeBDiagCursor))
				# Right - Bottom
			if ((e_pos.y() > self.y() + self.height() - diff) and # Bottom
			(e_pos.x() > self.x() + self.width() - diff)): # Right
				self.mode = Mode.Mode.RESIZEBR
				self.setCursor(QCursor(QtCore.Qt.SizeFDiagCursor))
			# Left - Top
			if ((e_pos.y() < self.y() + diff) and # Top
			(e_pos.x() < self.x() + diff)): # Left
				self.mode = Mode.Mode.RESIZETL
				self.setCursor(QCursor(QtCore.Qt.SizeFDiagCursor))
			# Right - Top
			if ((e_pos.y() < self.y() + diff) and # Top
			(e_pos.x() > self.x() + self.width() - diff)): # Right
				self.mode = Mode.Mode.RESIZETR
				self.setCursor(QCursor(QtCore.Qt.SizeBDiagCursor))
		# check cursor horizontal position
		elif ((e_pos.x() < self.x() + diff) or # Left
			(e_pos.x() > self.x() + self.width() - diff)): # Right
			if e_pos.x() < self.x() + diff: # Left
				self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
				self.mode = Mode.Mode.RESIZEL
			else: # Right
				self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
				self.mode = Mode.Mode.RESIZER
		# check cursor vertical position
		elif ((e_pos.y() > self.y() + self.height() - diff) or # Bottom
			(e_pos.y() < self.y() + diff)): # Top
			if e_pos.y() < self.y() + diff: # Top
				self.setCursor(QCursor(QtCore.Qt.SizeVerCursor))
				self.mode = Mode.Mode.RESIZET
			else: # Bottom
				self.setCursor(QCursor(QtCore.Qt.SizeVerCursor))
				self.mode = Mode.Mode.RESIZEB
		else:
			self.setCursor(QCursor(QtCore.Qt. ArrowCursor))
			self.mode = Mode.Mode.MOVE

	def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
		QWidget.mouseReleaseEvent(self, e)
		# Save new annotation's position
		self.annotationPosition = self.pos()
		self.annotationWidth = self.width()
		self.annotationHeight = self.height()

	def mouseMoveEvent(self, e: QtGui.QMouseEvent):
		QWidget.mouseMoveEvent(self, e)
		if not self.m_isEditing:
			return
		if not self.m_infocus:
			return
		if not e.buttons() and QtCore.Qt.LeftButton:
			p = QPoint(e.x() + self.geometry().x(), e.y() + self.geometry().y())
			self.setCursorShape(p)
			return

		if (self.mode == Mode.Mode.MOVE or self.mode == Mode.Mode.NONE) and e.buttons() and QtCore.Qt.LeftButton:
			toMove = e.globalPos() - self.position
			if toMove.x() < 0:return
			if toMove.y() < 0:return
			if toMove.x() > self.parentWidget().width() - self.width(): return
			if toMove.y() > self.parentWidget().height() - self.height(): return
			self.move(toMove)
			self.newGeometry.emit(self.geometry())
			self.parentWidget().repaint()
			return
		if (self.mode != Mode.Mode.MOVE) and e.buttons() and QtCore.Qt.LeftButton:
			if self.mode == Mode.Mode.RESIZETL: # Left - Top
				newwidth = e.globalX() - self.position.x() - self.geometry().x()
				newheight = e.globalY() - self.position.y() - self.geometry().y()
				toMove = e.globalPos() - self.position
				self.resize(self.geometry().width() - newwidth, self.geometry().height() - newheight)
				self.move(toMove.x(), toMove.y())
			elif self.mode == Mode.Mode.RESIZETR: # Right - Top
				newheight = e.globalY() - self.position.y() - self.geometry().y()
				toMove = e.globalPos() - self.position
				self.resize(e.x(), self.geometry().height() - newheight)
				self.move(self.x(), toMove.y())
			elif self.mode== Mode.Mode.RESIZEBL: # Left - Bottom
				newwidth = e.globalX() - self.position.x() - self.geometry().x()
				toMove = e.globalPos() - self.position
				self.resize(self.geometry().width() - newwidth, e.y())
				self.move(toMove.x(), self.y())
			elif self.mode == Mode.Mode.RESIZEB: # Bottom
				self.resize(self.width(), e.y())
			elif self.mode == Mode.Mode.RESIZEL: # Left
				newwidth = e.globalX() - self.position.x() - self.geometry().x()
				toMove = e.globalPos() - self.position
				self.resize(self.geometry().width() - newwidth, self.height())
				self.move(toMove.x(), self.y())
			elif self.mode == Mode.Mode.RESIZET:# Top
				newheight = e.globalY() - self.position.y() - self.geometry().y()
				toMove = e.globalPos() - self.position
				self.resize(self.width(), self.geometry().height() - newheight)
				self.move(self.x(), toMove.y())
			elif self.mode == Mode.Mode.RESIZER: # Right
				self.resize(e.x(), self.height())
			elif self.mode == Mode.Mode.RESIZEBR:# Right - Bottom
				self.resize(e.x(), e.y())
			self.parentWidget().repaint()
		self.newGeometry.emit(self.geometry())

	#endregion



	### ANNOTATION VARIABLES AND METHODS ###
	#region

	def setupAnnotationVariables(self, currentSecond):
		self.annotationType = self.childWidget.__class__.__name__
		self.annotationFrameStart = 0
		self.annotationFrameEnd = 0
		self.annotationSecondStart = currentSecond
		self.annotationSecondEnd = currentSecond
		self.annotationPosition = self.pos()
		self.annotationWidth = self.width()
		self.annotationHeight = self.height()

	def setFrameRange(self, fStart, fEnd):
		self.annotationFrameStart = fStart
		self.annotationFrameEnd = fEnd

	def setSecRange(self, sStart, sEnd):
		self.annotationSecondStart = sStart
		self.annotationSecondEnd = sEnd

	def setSecStart(self, sStart):
		self.annotationSecondStart = sStart

	def setSecEnd(self, sEnd):
		self.annotationSecondEnd = sEnd

	def getFrameRange(self):
		return (self.annotationFrameStart, self.annotationFrameEnd)

	def getSecRange(self):
		return (self.annotationSecondStart, self.annotationSecondEnd)

	def getSecStart(self):
		return self.annotationSecondStart

	def getSecEnd(self):
		return self.annotationSecondEnd

	def setPosition(self, newPos):
		self.annotationPosition = newPos
		self.move(self.annotationPosition)

	def getPosition(self):
		return self.annotationPosition

	def setDimensions(self, width, height):
		self.annotationWidth = width
		self.annotationHeight = height
		self.resize(width, height)

	def getDimensions(self):
		return (self.annotationWidth, self.annotationHeight)

	#endregion



	### QPLAINTEXTEDIT VARIABLES AND METHODS ###
	#region

	def setupTextboxVariables(self):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			self.textboxText = ""
			self.textboxBackgroundOpacity = 100
			self.textboxFontColor = "#000000"
			self.textboxFontSize = 10
			self.setTextboxPalette()
			

	def setTextboxPalette(self):
		textboxPalette = self.childWidget.palette()
		self.childWidget.setFont(QtGui.QFont(self.childWidget.font().rawName(), self.textboxFontSize))
		textboxPalette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Text, QColor(self.textboxFontColor))
		textboxPalette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, QColor(255, 255, 255, (int(self.textboxBackgroundOpacity*2.55))))
		self.childWidget.setPalette(textboxPalette)

		self.setTextboxText(self.getTextboxText())


	def mouseDoubleClickEvent(self, event):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			self.childWidget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)
			self.childWidget.installEventFilter(self)
			self.childWidget.textChanged.connect(self.updateTextboxText)

	def eventFilter(self, obj, event):
		if event.type() == QtCore.QEvent.FocusOut:
			if(isinstance(self.childWidget, QPlainTextEdit)):
				if obj is self.childWidget and event.type() == QtCore.QEvent.FocusOut:
					self.childWidget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

		return super().eventFilter(obj, event)

	def updateTextboxText(self):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			self.textboxText = self.childWidget.toPlainText()

	def setTextboxText(self, newText):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			self.textboxText = newText
			self.childWidget.setPlainText(self.textboxText)

	def setTextboxBackgroundOpacity(self, newOpacity):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			self.textboxBackgroundOpacity = newOpacity
			self.setTextboxPalette()

	def setTextboxFontColor(self, newColor):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			self.textboxFontColor = newColor
			self.setTextboxPalette()

	def setTextboxFontSize(self, newSize):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			self.textboxFontSize = newSize
			self.setTextboxPalette()

	def getTextboxText(self):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			return self.textboxText

	def getTextboxBackgroundOpacity(self):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			return self.textboxBackgroundOpacity

	def getTextboxFontColor(self):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			return self.textboxFontColor

	def getTextboxFontSize(self):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			return self.textboxFontSize
	

	#endregion



	### QSVGWIDGET VARIABLES AND METHODS ###
	#region

	def setupSvgVariables(self, isArrow):
		if(isinstance(self.childWidget, QSvgWidget)):

			'''
				Arrow SVG code:
					<svg xmlns="http://www.w3.org/2000/svg" height="24" width="24">
						<rect stroke="none" fill="none" y="0" x="0" height="100%" width="100%"/>
						<path d="M24 11.871l-5-4.871v3h-19v4h19v3z" fill="#000000" fill-opacity="1" transform="rotate(0,12,12)"/>
					</svg>

				Line SVG code:
					<svg xmlns="http://www.w3.org/2000/svg" height="24" width="24">
						<rect stroke="none" fill="none" y="0" x="0" height="100%" width="100%"/>
						<path d="M0,12h24" stroke="#000000" stroke-width="1" transform="rotate(0,12,12)"/>
					</svg>
			'''

			self.isArrow = isArrow

			if self.isArrow:
				self.svgString_start = r'<svg xmlns="http://www.w3.org/2000/svg" height="24" width="24"><rect stroke="none" fill="none" y="0" x="0" height="100%" width="100%"/><path d="M24 11.871l-5-4.871v3h-19v4h19v3z"'
			else:
				self.svgString_start = r'<svg xmlns="http://www.w3.org/2000/svg" height="24" width="24"><rect stroke="none" fill="none" y="0" x="0" height="100%" width="100%"/><path d="M0,12h24"'

			self.svgString_end = r',12,12)"/></svg>'

			self.svgColor = "#000000"			# Color of the SVG image (both LINE or ARROW)
			self.svgExtraAttribute = "1"		# Extra attribute of the SVG image ('stroke-width' for LINE, 'fill-opacity' for ARROW)
			self.svgTransform = "0"				# Rotation of the SVG image



			self.showSVG()


	def setSvgColor(self, newColor):
		if(isinstance(self.childWidget, QSvgWidget)):
			self.svgColor = newColor
			self.showSVG()

	def setSvgExtraAttribute(self, newExtraAttribute):
		if(isinstance(self.childWidget, QSvgWidget)):
			self.svgExtraAttribute = newExtraAttribute
			self.showSVG()

	def setSvgTransform(self, newTransform):
		if(isinstance(self.childWidget, QSvgWidget)):
			self.svgTransform = newTransform
			self.showSVG()

	def getSvgColor(self):
		if(isinstance(self.childWidget, QSvgWidget)):
			return self.svgColor

	def getSvgExtraAttribute(self):
		if(isinstance(self.childWidget, QSvgWidget)):
			return self.svgExtraAttribute

	def getSvgTransform(self):
		if(isinstance(self.childWidget, QSvgWidget)):
			return self.svgTransform


	def showSVG(self):
		if(isinstance(self.childWidget, QSvgWidget)):
			qba = QByteArray()

			if self.isArrow:
				qba.append(
					 self.svgString_start +  
					 ' fill="' + self.svgColor + 
					 '" fill-opacity="' + self.svgExtraAttribute +
					 '" transform="rotate(' + self.svgTransform + 
					 self.svgString_end)
			else:
				qba.append(
					 self.svgString_start +  
					 ' stroke="' + self.svgColor + 
					 '" stroke-width="' + self.svgExtraAttribute +
					 '" transform="rotate(' + self.svgTransform + 
					 self.svgString_end)


			self.childWidget.load(qba)


	#endregion