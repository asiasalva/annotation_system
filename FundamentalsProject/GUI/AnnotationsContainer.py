from PyQt5.QtWidgets import QWidget, QPlainTextEdit
from PyQt5.QtCore import QPoint
from PyQt5.QtSvg import QSvgWidget

from GUI import Annotation

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


	def removeAnnotation(self, annotationToRemove):
		self.mw.listOfAnnotations.remove(annotationToRemove)


	def showAnnotations(self, nFrame):
		for annotation in self.mw.listOfAnnotations:

			frameRange = annotation.getFrameRange()

			if frameRange[0] <= nFrame <= frameRange[1]:
				#annotation.setHidden(False)
				annotation.setVisible(True)
				print(annotation.getDimensions())
				print(annotation.width())
				print(annotation.height())
			else:
				#annotation.setHidden(True)
				annotation.setVisible(False)
				print(annotation.getDimensions())
				print(annotation.width())
				print(annotation.height())


