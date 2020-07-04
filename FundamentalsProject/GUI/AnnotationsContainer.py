from PyQt5.QtWidgets import QWidget, QPlainTextEdit
from PyQt5.QtCore import QPoint
from PyQt5.QtSvg import QSvgWidget

from GUI import Annotation
from GUI import AnnotationBreak
from GUI import VideoPlayerOpenCV

#Creates the lists of annotations needed

class AnnotationsContainer(QWidget):
	def __init__(self, MainWindow):
		super().__init__()
		self.mw = MainWindow	

	def createAnnotation(self, annotationType, currentSecond):
		if(annotationType == 0):	# LINE
			self.mw.listOfAnnotations.append(
				Annotation.Annotation(self, QPoint(10,10), QSvgWidget(), False, self.mw, currentSecond)
			)
		elif(annotationType == 1):	# ARROW
			self.mw.listOfAnnotations.append(
				Annotation.Annotation(self, QPoint(10,10), QSvgWidget(), True, self.mw, currentSecond)
			)
		elif(annotationType == 2):	# TEXTBOX
			self.mw.listOfAnnotations.append(
				Annotation.Annotation(self, QPoint(10,10), QPlainTextEdit(), False, self.mw, currentSecond)
			)
		elif(annotationType == 3):	# BREAKPOINT
			# append to the annotations list 
			self.mw.listOfAnnotations.append(
				AnnotationBreak.AnnotationBreak(self, QPoint(50,50), QWidget(), self.mw, currentSecond)
			)
			#append to the only brealpoints list needed to the function nextbreakpoint
			self.mw.listOfBreaks.append(self.mw.listOfAnnotations[-1])

	def showAnnotations(self, nFrame):
		for annotation in self.mw.listOfAnnotations:
			frameRange = annotation.getFrameRange()
			if frameRange[0] <= nFrame <= frameRange[1]:
				annotation.setHidden(False)
				if annotation.annotationType == "QWidget":
					# Annotation is a breakpoint -> pause the video
					self.mw.controlBarCommand(1)
			else:
				annotation.setHidden(True)