from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QImage, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint, QRect, QSize

from GUI import AnnotationDrawing


class WindowPaint(QWidget):
	def setupUi(self, MainWindow):

		self.mw = MainWindow




		self.image = QImage(self.size(), QImage.Format_ARGB32)
		self.image.fill(QtGui.qRgba(0,0,0,0));

		self.drawing = False
		self.brushSize = 1
		self.brushColor = Qt.red
		self.lastPoint = QPoint()

		self.painterPen = QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

		self.clear = False
		self.rubberSize = 1

		self.trackMouse = False



		


		''' Per provare la GOMMA, togli il commento da questo pezzo
		painter = QPainter(self.image)
		painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(0,0,50,100)

		self.changeColour()
		'''

		#mainMenu = self.menuBar()
		#fileMenu = mainMenu.addMenu("File")
		#brushSize = mainMenu.addMenu("Brush Size")
		#brushColor = mainMenu.addMenu("Brush Color")

		#saveAction = QAction(QIcon("icons/save.png"), "Save",self)
		#saveAction.setShortcut("Ctrl+S")
		#fileMenu.addAction(saveAction)
		#saveAction.triggered.connect(self.save)

		#clearAction = QAction(QIcon("icons/clear.png"), "Clear", self)
		#clearAction.setShortcut("Ctrl+C")
		#fileMenu.addAction(clearAction)
		#clearAction.triggered.connect(self.clear)

		#threepxAction = QAction( QIcon("icons/threepx.png"), "3px", self)
		#brushSize.addAction(threepxAction)
		#threepxAction.triggered.connect(self.threePixel)

		#fivepxAction = QAction(QIcon("icons/fivepx.png"), "5px", self)
		#brushSize.addAction(fivepxAction)
		#fivepxAction.triggered.connect(self.fivePixel)

		#sevenpxAction = QAction(QIcon("icons/sevenpx.png"),"7px", self)
		#brushSize.addAction(sevenpxAction)
		#sevenpxAction.triggered.connect(self.sevenPixel)

		#ninepxAction = QAction(QIcon("icons/ninepx.png"), "9px", self)
		#brushSize.addAction(ninepxAction)
		#ninepxAction.triggered.connect(self.ninePixel)

		#blackAction = QAction(QIcon("icons/black.png"), "Black", self)
		#blackAction.setShortcut("Ctrl+B")
		#brushColor.addAction(blackAction)
		#blackAction.triggered.connect(self.blackColor)


		#whitekAction = QAction(QIcon("icons/white.png"), "White", self)
		#whitekAction.setShortcut("Ctrl+W")
		#brushColor.addAction(whitekAction)
		#whitekAction.triggered.connect(self.whiteColor)


		#redAction = QAction(QIcon("icons/red.png"), "Red", self)
		#redAction.setShortcut("Ctrl+R")
		#brushColor.addAction(redAction)
		#redAction.triggered.connect(self.redColor)

		#greenAction = QAction(QIcon("icons/green.png"), "Green", self)
		#greenAction.setShortcut("Ctrl+G")
		#brushColor.addAction(greenAction)
		#greenAction.triggered.connect(self.greenColor)

		#yellowAction = QAction(QIcon("icons/yellow.png"), "Yellow", self)
		#yellowAction.setShortcut("Ctrl+Y")
		#brushColor.addAction(yellowAction)
		#yellowAction.triggered.connect(self.yellowColor)


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

					# dType = 0 -> LINE, 1 -> RUBBER
					self.createAnnotation(1, None, None, None, self.rubberSize, currentPoint)
				else:
					painter.drawLine(self.lastPoint, currentPoint)
					# dType = 0 -> LINE, 1 -> RUBBER
					self.createAnnotation(0, self.painterPen, self.lastPoint, currentPoint, None, None)


				self.lastPoint = currentPoint
				self.update()
				print("drawing " + str(currentPoint))
			else:
				self.lastPoint = QPoint(event.x() * (self.image.width() / self.width()), event.y() * (self.image.height() / self.height()))



	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.drawing = False


	def paintEvent(self, event):
		canvasPainter  = QPainter(self)
		canvasPainter.drawImage(self.rect(), self.image, self.image.rect() )


	def changeColour(self):
		self.clear = not self.clear
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

	
	def createAnnotation(self, dType, pen, pStart, pEnd, rSize, rPoint):
		self.mw.listOfDrawing.append(
			AnnotationDrawing.AnnotationDrawing(dType, pen, pStart, pEnd, rSize, rPoint)
		)

	def drawAnnotations(self, listOfDrawings):
		
		painter = QPainter(self.image)
		
		for drawing in listOfDrawings:			

			# drawingType = 0 -> LINE, 1 -> RUBBER
			if drawing.drawingType:
				r = QRect(QPoint(), drawing.rubberSize*QSize())
				r.moveCenter(drawing.rubberPoint)
				painter.save()
				painter.setCompositionMode(QPainter.CompositionMode_Clear)
				painter.eraseRect(r)
				painter.restore()
			else:
				painter.setPen(drawing.painterPen)
				painter.drawLine(drawing.pointStart, drawing.pointEnd)







	#LINE
	#painterPen		QPen	
	#pointStart		QPoint
	#pointEnd		QPoint

	#RUBBER
	#rubberSize		int
	#point			QPoint




	#def save(self):
	#	filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

	#	if filePath == "":
	#		return
	#	self.image.save(filePath)



	#def clear(self):
	#	self.image.fill(Qt.white)
	#	self.update()


	#def threePixel(self):
	#	self.brushSize = 3

	#def fivePixel(self):
	#	self.brushSize = 5

	#def sevenPixel(self):
	#	self.brushSize = 7

	#def ninePixel(self):
	#	self.brushSize = 9


	#def blackColor(self):
	#	self.brushColor = Qt.black

	#def whiteColor(self):
	#	self.brushColor = Qt.white

	#def redColor(self):
	#	self.brushColor = Qt.red

	#def greenColor(self):
	#	self.brushColor = Qt.green

	#def yellowColor(self):
	#	self.brushColor = Qt.yellow