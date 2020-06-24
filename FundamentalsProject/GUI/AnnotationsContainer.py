from PyQt5.QtWidgets import QWidget, QPlainTextEdit
from PyQt5.QtCore import QPoint
from PyQt5.QtSvg import QSvgWidget

from GUI import Annotation
from GUI import AnnotationBreak

class AnnotationsContainer(QWidget):
	def __init__(self, MainWindow):
		super().__init__()

		self.mw = MainWindow
		

	def createAnnotation(self, annotationType, currentSecond):
		print("Creating annotation")

		if(annotationType == 0):	# LINE
			print("Creating LINE")
			self.mw.listOfAnnotations.append(
				Annotation.Annotation(self, QPoint(10,10), QSvgWidget(), False, self.mw, currentSecond)
			)
		elif(annotationType == 1):	# ARROW
			print("Creating ARROW")
			self.mw.listOfAnnotations.append(
				Annotation.Annotation(self, QPoint(10,10), QSvgWidget(), True, self.mw, currentSecond)
			)
		elif(annotationType == 2):	# TEXTBOX
			print("Creating TEXTBOX")
			self.mw.listOfAnnotations.append(
				Annotation.Annotation(self, QPoint(10,10), QPlainTextEdit(), False, self.mw, currentSecond)
			)
		elif(annotationType == 3):	# BREAKPOINT
			print("Creating BREAKPOINT")
			self.mw.listOfAnnotations.append(
				AnnotationBreak.AnnotationBreak(self, QPoint(100,100), QWidget(), self.mw, currentSecond)
			)
			print('ho aggiunto il breakpoint alla lista')


	def removeAnnotation(self, annotationToRemove):
		self.mw.listOfAnnotations.remove(annotationToRemove)


	def showAnnotations(self, nFrame):
		print('sono nella funzione di stampa dell annotazione')
		for annotation in self.mw.listOfAnnotations:

			frameRange = annotation.getFrameRange()

			if frameRange[0] <= nFrame <= frameRange[1]:
				annotation.setHidden(False)
			else:
				annotation.setHidden(True)


