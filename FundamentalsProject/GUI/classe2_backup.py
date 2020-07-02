from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *  
from PyQt5.QtCore import Qt 
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPoint, pyqtSignal, QRect, QByteArray, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit
from PyQt5.QtSvg import QSvgWidget
import sys 

from GUI import Annotation
from GUI import Mode

class AnnotationBreak(QWidget):
   
    inFocus = pyqtSignal(bool)
    outFocus = pyqtSignal(bool)
    newGeometry = pyqtSignal(QRect)

    def __init__(self, parent, p, cWidget, MainWindow, currentSecond):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 300, 350, 350)
        print('sono nella classe giusta')

        self.mw = MainWindow
        self.childWidget = None

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setVisible(True)
        self.vLayout = QVBoxLayout(self)
        self.setChildWidget(cWidget, currentSecond)
        print('ho richiamato il setchildwidget')

    def setChildWidget(self, cWidget, currentSecond):
        print('set child widget')
        if cWidget:
            self.childWidget = cWidget
            self.childWidget.setParent(self)
            self.vLayout.addWidget(cWidget)
            self.vLayout.setContentsMargins(0,0,0,0)
            self.setupAnnotationVariables(currentSecond)
            print('ho settato il child widget')

    def setupAnnotationVariables(self, currentSecond):
        print('setupannotation var')
        self.annotationType = self.childWidget.__class__.__name__
        self.annotationFrameStart = 0
        self.annotationFrameEnd = 0
        self.annotationSecondStart = currentSecond
        self.annotationSecondEnd = currentSecond
        self.annotationPosition = self.pos()
        self.annotationWidth = self.width()
        self.annotationHeight = self.height()

    # Draw the circle
    def paintEvent(self, event):
        print('sto disegnando il cerchio')
        paint = QPainter()
        paint.begin(self)
        ## paint.drawRect(event.rect())
        radx = 30
        rady = 30
        # draw red circles
        # paint.setPen(Qt.red)
        ## center = QPoint(10, 10)
        paint.setBrush(Qt.blue)
        paint.drawEllipse(10, 10, radx, rady)
        paint.end() 
        print('ho disegnato il cerchio')


    def setFrameRange(self, fStart, fEnd):
        print('framerange')
        self.annotationFrameStart = fStart
        self.annotationFrameEnd = fEnd

    def setSecRange(self, sStart, sEnd):
        print('second range')
        self.annotationSecondStart = sStart
        self.annotationSecondEnd = sEnd

    def setSecStart(self, sStart):
        print('secstart')
        self.annotationSecondStart = sStart

    def setSecEnd(self, sEnd):
        print('sec end')
        self.annotationSecondEnd = sEnd

    def getFrameRange(self):
        print('get frame range')
        return (self.annotationFrameStart, self.annotationFrameEnd)

    def getSecRange(self):
        print('get sec range')
        return (self.annotationSecondStart, self.annotationSecondEnd)

    def getSecStart(self):
        print('get sec start')
        return self.annotationSecondStart

    def getSecEnd(self):
        print('get sec end')
        return self.annotationSecondEnd

    def setPosition(self, newPos):
        self.annotationPosition = newPos
        self.move(self.annotationPosition)

    def getPosition(self):
        return self.annotationPosition

    def setDimensions(self, width, height):
        self.annotationWidth = width
        self.annotationHeight = height
        self.resize(width, height)

    def getDimensions(self):
        return (self.annotati)




class my_class(object):
    pass




