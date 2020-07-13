from PyQt5.QtCore import QPoint, pyqtSignal, QRect, QByteArray, Qt, QSize, QEvent
from PyQt5.QtGui import QColor, QCursor, QFont, QPalette, QFocusEvent, QPaintEvent, QPainter, QMouseEvent, QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit
from PyQt5.QtSvg import QSvgWidget
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QCursor
from PyQt5.QtCore import Qt, QPoint, QRect, QSize

from GUI import Mode


# Class for the drawing annotation

class AnnotationDraws(QWidget):
    
	### TCONTAINER VARIABLES AND METHODS ###
	#region

	mode = Mode.Mode.NONE
	inFocus = pyqtSignal(bool)
	outFocus = pyqtSignal(bool)
	newGeometry = pyqtSignal(QRect)

	# isArrow is used to distinguish which SVG image the user wants to add (LINE or ARROW). If cWidget is a QSvgWidget, then isArrow parameter is passed in setupSvgVariables function.
	def __init__(self, parent, p, cWidget, isArrow, MainWindow, currentSecond): 
		super().__init__(parent=parent)

		self.mw = MainWindow

		self.frameWidth, self.frameHeight = self.mw.getFrameDimensions()
		self.parentWidth = parent.width()
		self.parentHeight = parent.height()
		self.setMinimumSize(10,10)

		self.childWidget = None
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setVisible(True)
		self.setAutoFillBackground(False)
		self.setMouseTracking(True)
		self.setFocusPolicy(Qt.ClickFocus)
		self.setFocus()
		self.vLayout = QVBoxLayout(self)
		self.setChildWidget(cWidget, isArrow, currentSecond)
		self.setPosition(p)
		self.move(self.getFakePosition(p))
		# Set the focus and the event handler
		self.m_infocus = True
		self.m_isEditing = True
		self.installEventFilter(parent)

	def setChildWidget(self, cWidget, isArrow, currentSecond):
		if cWidget:
			self.childWidget = cWidget
			self.childWidget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
			self.childWidget.setParent(self)
			self.childWidget.releaseMouse()
			self.vLayout.addWidget(cWidget)
			self.vLayout.setContentsMargins(0,0,0,0)
			self.setupAnnotationVariables(currentSecond)
	
			self.mw.setLastFocusAnnotation(self)

	def focusInEvent(self, a0: QFocusEvent):
		self.m_infocus = True
		p = self.parentWidget()
		p.installEventFilter(self)
		p.repaint()
		self.inFocus.emit(True)
		if self.childWidget is not None:
			self.mw.setLastFocusAnnotation(self)

	def focusOutEvent(self, a0: QFocusEvent):
		if not self.m_isEditing:
			return
		self.mode = Mode.Mode.NONE
		self.outFocus.emit(False)
		self.m_infocus = False

	def paintEvent(self, e: QPaintEvent):
		painter = QPainter(self)
		color = (r, g, b, a) = (255, 0, 0, 0)
		painter.fillRect(e.rect(), QColor(r, g, b, a))
		if self.m_infocus:
			rect = e.rect()
			rect.adjust(0,0,-1,-1)
			painter.setPen(QColor(r, g, b))
			painter.drawRect(rect)

	def mousePressEvent(self, e: QMouseEvent):
		self.position = QPoint(e.globalX() - self.geometry().x(), e.globalY() - self.geometry().y())
		if not self.m_isEditing:
			return
		if not self.m_infocus:
			return
		if not e.buttons() and Qt.LeftButton:
			self.setCursorShape(e.pos())
			return
		# Raises this widget to the top of the parent widget’s stack.
		self.raise_()

	def keyPressEvent(self, e: QKeyEvent):
		if not self.m_isEditing: return
		# Remove annotation
		if e.key() == Qt.Key_Delete:
			self.deleteLater()
			self.mw.removeAnnotation(self)
		# Moving container with arrows
		if QApplication.keyboardModifiers() == Qt.ControlModifier:
			newPos = QPoint(self.x(), self.y())
			if e.key() == Qt.Key_Up:
				newPos.setY(newPos.y() - 1)
			if e.key() == Qt.Key_Down:
				newPos.setY(newPos.y() + 1)
			if e.key() == Qt.Key_Left:
				newPos.setX(newPos.x() - 1)
			if e.key() == Qt.Key_Right:
				newPos.setX(newPos.x() + 1)

			if newPos.x() < 0:return
			if newPos.y() < 0:return
			if newPos.x() > self.parentWidget().width() - self.width(): return
			if newPos.y() > self.parentWidget().height() - self.height(): return
			self.move(newPos)

		if QApplication.keyboardModifiers() == Qt.ShiftModifier:
			if e.key() == Qt.Key_Up:
				self.resize(self.width(), self.height() - 1)
			if e.key() == Qt.Key_Down:
				self.resize(self.width(), self.height() + 1)
			if e.key() == Qt.Key_Left:
				self.resize(self.width() - 1, self.height())
			if e.key() == Qt.Key_Right:
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
				self.setCursor(QCursor(Qt.SizeBDiagCursor))
				# Right - Bottom
			if ((e_pos.y() > self.y() + self.height() - diff) and # Bottom
			(e_pos.x() > self.x() + self.width() - diff)): # Right
				self.mode = Mode.Mode.RESIZEBR
				self.setCursor(QCursor(Qt.SizeFDiagCursor))
			# Left - Top
			if ((e_pos.y() < self.y() + diff) and # Top
			(e_pos.x() < self.x() + diff)): # Left
				self.mode = Mode.Mode.RESIZETL
				self.setCursor(QCursor(Qt.SizeFDiagCursor))
			# Right - Top
			if ((e_pos.y() < self.y() + diff) and # Top
			(e_pos.x() > self.x() + self.width() - diff)): # Right
				self.mode = Mode.Mode.RESIZETR
				self.setCursor(QCursor(Qt.SizeBDiagCursor))
		# check cursor horizontal position
		elif ((e_pos.x() < self.x() + diff) or # Left
			(e_pos.x() > self.x() + self.width() - diff)): # Right
			if e_pos.x() < self.x() + diff: # Left
				self.setCursor(QCursor(Qt.SizeHorCursor))
				self.mode = Mode.Mode.RESIZEL
			else: # Right
				self.setCursor(QCursor(Qt.SizeHorCursor))
				self.mode = Mode.Mode.RESIZER
		# check cursor vertical position
		elif ((e_pos.y() > self.y() + self.height() - diff) or # Bottom
			(e_pos.y() < self.y() + diff)): # Top
			if e_pos.y() < self.y() + diff: # Top
				self.setCursor(QCursor(Qt.SizeVerCursor))
				self.mode = Mode.Mode.RESIZET
			else: # Bottom
				self.setCursor(QCursor(Qt.SizeVerCursor))
				self.mode = Mode.Mode.RESIZEB
		else:
			self.setCursor(QCursor(Qt. ArrowCursor))
			self.mode = Mode.Mode.MOVE

	def mouseReleaseEvent(self, e: QMouseEvent):
		QWidget.mouseReleaseEvent(self, e)
		# Save new annotation's position
		self.setPosition(self.getRealPosition(self.pos()))
		dim = self.getRealDimensions(self.width(), self.height())
		self.setDimensions(dim.width(), dim.height())

	def mouseMoveEvent(self, e: QMouseEvent):
		QWidget.mouseMoveEvent(self, e)
		if not self.m_isEditing:
			return
		if not self.m_infocus:
			return
		if not e.buttons() and Qt.LeftButton:
			p = QPoint(e.x() + self.geometry().x(), e.y() + self.geometry().y())
			self.setCursorShape(p)
			return

		if (self.mode == Mode.Mode.MOVE or self.mode == Mode.Mode.NONE) and e.buttons() and Qt.LeftButton:
			toMove = e.globalPos() - self.position
			if toMove.x() < 0:return
			if toMove.y() < 0:return
			if toMove.x() > self.parentWidget().width() - self.width(): return
			if toMove.y() > self.parentWidget().height() - self.height(): return
			self.move(toMove)
			self.newGeometry.emit(self.geometry())
			self.parentWidget().repaint()
			return
		if (self.mode != Mode.Mode.MOVE) and e.buttons() and Qt.LeftButton:
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
		self.annotationPosition = 0
		self.isArrow = None
		self.listOfDrawings = list()

		# These two lines of code (which change annotation's size and put it back 
		#	are used to prevent that Qt automatically adjust the widget's size 
		#	to a useful default using adjustSize()
		# For more information -> https://doc.qt.io/qt-5/qwidget.html#visible-prop
		# "If its size or position has changed, Qt guarantees that a widget 
		#	gets move and resize events just before it is shown.
		#	If the widget has not been resized yet, Qt will adjust the widget's size 
		#	to a useful default using adjustSize()."
		self.resize(self.width()+1, self.height()+1)
		self.resize(self.width()-1, self.height()-1)
		self.annotationWidth = self.width()
		self.annotationHeight = self.height()
		self.resize(self.getFakeDimensions(self.annotationWidth, self.annotationHeight))


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
		self.move(self.getFakePosition(self.annotationPosition))

	def getPosition(self):
		return self.annotationPosition

	def setDimensions(self, width, height):
		self.annotationWidth = width
		self.annotationHeight = height
		self.resize(self.getFakeDimensions(self.annotationWidth, self.annotationHeight))

	def getDimensions(self):
		return (self.annotationWidth, self.annotationHeight)

	#endregion

	### RESIZE FUNCTIONS
	#region

	def setParentDimensions(self, width, height):
		self.parentWidth = width
		self.parentHeight = height

		self.move(self.getFakePosition(self.annotationPosition))
		dim = self.getDimensions()
		self.resize(self.getFakeDimensions(dim[0], dim[1]))


	def getRealPosition(self, fakePos):
		#	realX:frameWidth = fakeX:parentWidth
		#	realY:frameHeight = fakeY:parentHeight

		realX = round((self.frameWidth * fakePos.x()) / self.parentWidth)
		realY = round((self.frameHeight * fakePos.y()) / self.parentHeight)

		return QPoint(realX, realY)

	def getFakePosition(self, realPos):
		#	realX:frameWidth = fakeX:parentWidth
		#	realY:frameHeight = fakeY:parentHeight
		
		fakeX = round((self.parentWidth * realPos.x()) / self.frameWidth)
		fakeY = round((self.parentHeight * realPos.y()) / self.frameHeight)

		return QPoint(fakeX, fakeY)


	def getRealDimensions(self, fakeW, fakeH):
		#	realW:frameWidth = fakeW:parentWidth
		#	realH:frameHeight = fakeH:parentHeight

		realW = round((self.frameWidth * fakeW) / self.parentWidth)
		realH = round((self.frameHeight * fakeH) / self.parentHeight)

		return QSize(realW, realH)

	def getFakeDimensions(self, realW, realH):
		#	realW:frameWidth = fakeW:parentWidth
		#	realH:frameHeight = fakeH:parentHeight
		
		fakeW = round((self.parentWidth * realW) / self.frameWidth)
		fakeH = round((self.parentHeight * realH) / self.frameHeight)

		return QSize(fakeW, fakeH)

	#endregion




	def drawAnnotations(self, listOfDrawings):
		
		### self.mw.listOfDrawing.append([pen, pStart, pEnd])

		## find dimensions for child widget
		#self.childWidget = QImage(self.size(), QImage.Format_ARGB32)
		#self.childWidget(QtGui.qRgba(0,0,0,0));
		self.childWidget.setStyleSheet("border: 5px solid black;")
		self.childWidget.setScaledContents(True)
		x = self.childWidget.size()
		img = QImage(x, QImage.Format_ARGB32)
		img.fill(QtGui.qRgba(0,0,0,0))
		

		painter = QPainter(img)
		
		for drawing in listOfDrawings:
			painter.setPen(drawing[0])
			painter.drawLine(drawing[1], drawing[2])

			self.listOfDrawings.append(drawing)

		
		pix = QPixmap.fromImage(img)
		self.childWidget.setPixmap(pix)
		painter.end()