###!!! da togliere !!!


# Class for the drawing annotation

class AnnotationDrawing(object):
    
	def __init__(self, dType, pen, pStart, pEnd, rSize, rPoint): 
		
		self.drawingType = dType	# 0 -> LINE, 1 -> RUBBER
		self.drawingFrameStart = 0
		self.drawingFrameEnd = 0
		self.drawingSecondStart = 0
		self.drawingSecondEnd = 0

		if self.drawingType:
			self.rubberSize = rSize
			self.rubberPoint = rPoint
		else:
			self.painterPen = pen
			self.pointStart = pStart
			self.pointEnd = pEnd
