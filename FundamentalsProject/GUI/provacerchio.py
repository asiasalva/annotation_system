from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import QtCore 
from PyQt5.QtCore import Qt

class DrawCircles(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 300, 350, 350)

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        # optional
        # paint.setRenderHint(QPainter.Antialiasing)
        # make a white drawing background
       # paint.setBrush(Qt.white)
        paint.drawRect(event.rect())
        # for circle make the ellipse radii match
        radx = 50
        rady = 50
        # draw red circles
        # paint.setPen(Qt.red)
        center = QPoint(125, 125)
        # optionally fill each circle yello
        paint.setBrush(Qt.blue)
        paint.drawEllipse(300, 300, radx, rady)
        paint.end()

app = QApplication([])
circles = DrawCircles()
circles.show()
app.exec_()