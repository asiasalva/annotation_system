from PyQt5.QtWidgets import QWidget, QPlainTextEdit
from PyQt5.QtCore import QPoint
from PyQt5.QtSvg import QSvgWidget

from GUI import Annotation
from GUI import AnnotationBreak
from GUI import VideoPlayerOpenCV

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
			print('sono in annotation container')
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
			# append alla lista di annotazioni generale
			self.mw.listOfAnnotations.append(
				AnnotationBreak.AnnotationBreak(self, QPoint(50,50), QWidget(), self.mw, currentSecond)
			)
			#append alla lista di soli breaks che serve per poi saltare da un break all'altro
			self.mw.listOfBreaks.append(self.mw.listOfAnnotations[-1])
			print('ho aggiunto il break point alla lista e ora ci sono: ', len(self.mw.listOfBreaks))
			# print('ho aggiunto il breakpoint alla lista')


	def removeAnnotation(self, annotationToRemove):
		self.mw.listOfAnnotations.remove(annotationToRemove)


	def showAnnotations(self, nFrame):
		# print('sono nella funzione di stampa dell annotazione')
		for annotation in self.mw.listOfAnnotations:
			# print('annotation type: ', type(annotation))
			if annotation.annotationType == 'QWidget':
				print('sono nell if')
				self.mw.controlBarCommand(1)

			frameRange = annotation.getFrameRange()

			if frameRange[0] <= nFrame <= frameRange[1]:
				annotation.setHidden(False)
			else:
				annotation.setHidden(True)


