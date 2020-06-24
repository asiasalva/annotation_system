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
    
    newGeometry = pyqtSignal(QRect)

    def __init__(self, parent, p, cWidget, MainWindow, currentSecond):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)
        # self.setGeometry(300, 300, 350, 350)
        print('sono nella classe giusta')
        self.mw = MainWindow
        self.childWidget = None
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setVisible(True)
        self.vLayout = QVBoxLayout(self)
        self.setChildWidget(cWidget, currentSecond)

    def setChildWidget(self, cWidget, currentSecond):
        if cWidget:
            self.childWidget = cWidget
            self.childWidget.setParent(self)
            self.vLayout.addWidget(cWidget)
            self.vLayout.setContentsMargins(0,0,0,0)
            self.setupAnnotationVariables(currentSecond)

    def setupAnnotationVariables(self, currentSecond):
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
        paint.drawRect(event.rect())
        radx = 50
        rady = 50
        # draw red circles
        # paint.setPen(Qt.red)
        center = QPoint(125, 125)
        paint.setBrush(Qt.blue)
        paint.drawEllipse(100, 100, radx, rady)
        paint.end() 
        print('ho disegnato il cerchio')


