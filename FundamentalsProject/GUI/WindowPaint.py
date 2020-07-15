from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QCursor
from PyQt5.QtCore import Qt, QPoint, QRect, QSize

from GUI import AnnotationDraws


class WindowPaint(QWidget):

	def setupUi(self, MainWindow):

		self.mw = MainWindow
		self.listOfDrawings = list()

		# Image to draw on (like a transparent blackboard)
		self.image = QImage(self.size(), QImage.Format_ARGB32)
		self.image.fill(QtGui.qRgba(0,0,0,0));

		# Default pen
		self.brushSize = 1
		self.brushColor = Qt.red
		self.lastPoint = QPoint()
		self.painterPen = QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

		# Drawing checks
		self.drawing = False
		self.trackMouse = False


	def mousePressEvent(self, event):
		if self.trackMouse and event.button() == Qt.LeftButton:
			self.drawing = True
			self.lastPoint = QPoint(event.x() * (self.image.width() / self.width()), event.y() * (self.image.height() / self.height()))


	def mouseMoveEvent(self, event):
		if(event.buttons() & Qt.LeftButton) & self.drawing:
			if ((0 <= event.x() <= self.width()) and (0 <= event.y() <= self.height())):
				painter = QPainter(self.image)
				painter.setPen(self.painterPen)

				currentPoint = QPoint(event.x() * (self.image.width() / self.width()), event.y() * (self.image.height() / self.height()))

				
				painter.drawLine(self.lastPoint, currentPoint)

				self.listOfDrawings.append([self.painterPen, self.lastPoint, currentPoint])

				self.lastPoint = currentPoint
				self.update()
			else:
				self.lastPoint = QPoint(event.x() * (self.image.width() / self.width()), event.y() * (self.image.height() / self.height()))


	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.drawing = False
			self.mw.copyDraw(self.listOfDrawings)
			self.clearWindowPaint()

				

	def paintEvent(self, event):
		canvasPainter  = QPainter(self)
		canvasPainter.drawImage(self.rect(), self.image, self.image.rect() )


	def setTrackingMouse(self, tracking):
		self.trackMouse = tracking

	def getTrackingMouse(self):
		return self.trackMouse

	def setPainterPen(self, pen):
		self.painterPen = pen

	def getPainterPen(self):
		return self.painterPen


	def clearWindowPaint(self):
		self.listOfDrawings.clear()
		self.image.fill(QtGui.qRgba(0,0,0,0))
		self.update()
