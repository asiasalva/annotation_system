from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QCursor
from PyQt5.QtCore import Qt, QPoint, QRect, QSize


class WindowBlackboard(QWidget):

	def setupUi(self, MainWindow):

		self.mw = MainWindow

		# Image to draw on (like a transparent blackboard)
		self.image = QImage(self.size(), QImage.Format_ARGB32)
		self.image.fill(QtGui.qRgba(0,0,0,0));

		# Default pen
		self.brushSize = 1
		self.brushColor = Qt.red
		self.lastPoint = QPoint()
		self.painterPen = QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

		# Default rubber
		self.clear = False
		self.rubberSize = 1

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

				if self.clear:
					r = QRect(QPoint(), self.rubberSize*QSize())
					r.moveCenter(currentPoint)
					painter.save()
					painter.setCompositionMode(QPainter.CompositionMode_Clear)
					painter.eraseRect(r)
					painter.restore()
				else:
					painter.drawLine(self.lastPoint, currentPoint)

				self.lastPoint = currentPoint
				self.update()
			else:
				self.lastPoint = QPoint(event.x() * (self.image.width() / self.width()), event.y() * (self.image.height() / self.height()))


	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.drawing = False


	def paintEvent(self, event):
		canvasPainter  = QPainter(self)
		canvasPainter.drawImage(self.rect(), self.image, self.image.rect() )


	def setRubber(self, active):
		self.clear = active
		if self.clear:
			pixmap = QtGui.QPixmap(QSize(1, 1)*self.rubberSize)
			pixmap.fill(Qt.transparent)
			painter = QtGui.QPainter(pixmap)
			painter.setPen(QtGui.QPen(Qt.black, 2))
			painter.drawRect(pixmap.rect())
			painter.end()
			cursor = QtGui.QCursor(pixmap)
			QApplication.setOverrideCursor(cursor)
		else:
			QApplication.restoreOverrideCursor()


	def setTrackingMouse(self, tracking):
		self.trackMouse = tracking

	def getTrackingMouse(self):
		return self.trackMouse

	def setPainterPen(self, pen):
		self.painterPen = pen

	def getPainterPen(self):
		return self.painterPen

	def setRubberSize(self, size):
		self.rubberSize = size

	def getRubberSize(self):
		return self.rubberSize


	def clearWindowBlackboard(self):
		self.image.fill(QtGui.qRgba(0,0,0,0));
		self.update()
