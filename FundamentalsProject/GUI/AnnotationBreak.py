from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPoint, pyqtSignal, QRect, QByteArray, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit
from PyQt5.QtSvg import QSvgWidget

from GUI import Mode
from GUI import Annotation 

class AnnotationBreak(QWidget):

	### TCONTAINER VARIABLES AND METHODS ###
	#region

	mode = Mode.Mode.NONE
	inFocus = pyqtSignal(bool)
	outFocus = pyqtSignal(bool)
	newGeometry = pyqtSignal(QRect)
	isArrow = None  

	def __init__(self, parent, p, cWidget, MainWindow, currentSecond): # isArrow is used to distinguish which SVG image the user wants to add (LINE or ARROW). If cWidget is a QSvgWidget, then isArrow parameter is passed in setupSvgVariables function.
		super().__init__(parent=parent)

		self.mw = MainWindow
		self.childWidget = None
		# self.setGeometry(500, 500, 500, 500)

		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
		self.setVisible(True)
		self.setAutoFillBackground(False)
		self.setMouseTracking(True)
		self.setFocusPolicy(QtCore.Qt.ClickFocus)
		self.setFocus()
		self.move(p)

		self.vLayout = QVBoxLayout(self)
		self.setChildWidget(cWidget, currentSecond)

		self.m_infocus = True
		self.m_isEditing = True
		self.installEventFilter(parent)


	def setChildWidget(self, cWidget, currentSecond):
		if cWidget:
			self.childWidget = cWidget
			self.childWidget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
			self.childWidget.setParent(self)
			self.childWidget.releaseMouse()
			self.vLayout.addWidget(cWidget)
			self.vLayout.setContentsMargins(0,0,0,0)


			self.setupAnnotationVariables(currentSecond)
			
			# self.setUpVars()


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

	def paintEvent(self, event):
		#♥ print('sto disegnando il cerchio')
		paint = QPainter()
		paint.begin(self)
        ## paint.drawRect(event.rect())
        # draw red circles
		paint.setPen(Qt.red)
		center = QPoint(10, 10)
		paint.setBrush(Qt.blue)
		paint.drawEllipse(10, 10, 15, 15)
		paint.end() 
		# print('ho disegnato il cerchio')

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

	
	### QPLAINTEXTEDIT VARIABLES AND METHODS ###
	#region
			
	def setColor(self, newColor):
		if(isinstance(self.childWidget, QWidget)):
			self.color = newColor

	def mouseDoubleClickEvent(self, event):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			self.childWidget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)
			self.childWidget.installEventFilter(self)
			# self.childWidget.textChanged.connect(self.updateTextboxText)

	def eventFilter(self, obj, event):
		if event.type() == QtCore.QEvent.FocusOut:
			if(isinstance(self.childWidget, QPlainTextEdit)):
				if obj is self.childWidget and event.type() == QtCore.QEvent.FocusOut:
					self.childWidget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

		return super().eventFilter(obj, event)

	def updateTextboxText(self):
		if(isinstance(self.childWidget, QPlainTextEdit)):
			self.textboxText = self.childWidget.toPlainText()
			
#♦endregion