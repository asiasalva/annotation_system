from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QImage, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint, QRect, QSize

class AnnotationDrawing(object):
    
	def __init__(self, dType, pen, pStart, pEnd, rSize, rPoint): 
		
		self.drawingType = dType	# 0 -> LINE, 1 -> RUBBER

		if self.drawingType:
			self.rubberSize = rSize
			self.rubberPoint = rPoint
		else:
			self.painterPen = pen
			self.pointStart = pStart
			self.pointEnd = pEnd
	
	#LINE
	#painterPen		QPen	
	#pointStart		QPoint
	#pointEnd		QPoint

	#RUBBER
	#rubberSize		int
	#point			QPoint


