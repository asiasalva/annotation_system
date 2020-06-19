from PyQt5.QtWidgets import QWidget, QPlainTextEdit
from PyQt5.QtCore import QPoint
from PyQt5.QtSvg import QSvgWidget

from GUI import Annotation

class AnnotationsContainer(QWidget):
	def __init__(self, MainWindow):
		super().__init__()

		self.mw = MainWindow
		

	def createAnnotation(self, annotationType):
		print("Creating annotation")

		if(annotationType == 0):	# LINE
			print("Creating LINE")
			self.mw.listOfAnnotations.append(
				Annotation.Annotation(self, QPoint(10,10), QSvgWidget(), False, self.mw)
			)
		elif(annotationType == 1):	# ARROW
			print("Creating ARROW")
			self.mw.listOfAnnotations.append(
				Annotation.Annotation(self, QPoint(10,10), QSvgWidget(), True, self.mw)
			)
		elif(annotationType == 2):	# TEXTBOX
			print("Creating TEXTBOX")
			self.mw.listOfAnnotations.append(
				Annotation.Annotation(self, QPoint(10,10), QPlainTextEdit(), False, self.mw)
			)
		elif(annotationType == 3):	# BREAKPOINT
			print("Creating BREAKPOINT")


	def removeAnnotation(self, annotationToRemove):
		self.mw.listOfAnnotations.remove(annotationToRemove)


