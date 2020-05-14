from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QAction, QFileDialog, QWidget
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtGui
import sys


class WindowPaint(QWidget):
	def setupUi(self, MainWindow):
	

		#title = "Paint Application"
		#top = 400
		#left = 400
		#width = 800
		#height = 600

		#icon = "icons/pain.png"

		#self.setWindowTitle(title)
		#self.setGeometry(top, left, width, height)
		#self.setWindowIcon(QIcon(icon))

		#self.image = QImage(self.size(), QImage.Format_RGB32)
		#self.image.fill(Qt.white)
		self.image = QImage(self.size(), QImage.Format_ARGB32)
		self.image.fill(QtGui.qRgba(0,0,0,0));

		self.drawing = False
		self.brushSize = 15
		self.brushColor = Qt.black
		self.lastPoint = QPoint()

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
		if event.button() == Qt.LeftButton:
			self.drawing = True
			self.lastPoint = QPoint(event.x() * (self.image.width() / self.width()), event.y() * (self.image.height() / self.height()))
			#self.x = 0


	def mouseMoveEvent(self, event):
		if(event.buttons() & Qt.LeftButton) & self.drawing:
			if ((0 <= event.x() <= self.width()) and (0 <= event.y() <= self.height())):
				painter = QPainter(self.image)
				painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

				currentPoint = QPoint(event.x() * (self.image.width() / self.width()), event.y() * (self.image.height() / self.height()))

				painter.drawLine(self.lastPoint, currentPoint)
				self.lastPoint = currentPoint
				self.update()
				print("drawing " + str(currentPoint))
				#print("drawing " + str(self.x))
				#self.x += 1
			else:
				self.lastPoint = QPoint(event.x() * (self.image.width() / self.width()), event.y() * (self.image.height() / self.height()))



	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.drawing = False


	def paintEvent(self, event):
		canvasPainter  = QPainter(self)
		canvasPainter.drawImage(self.rect(),self.image, self.image.rect() )





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