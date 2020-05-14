from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QVBoxLayout, QWidget , QSlider, QLabel)

from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap


import GUI
from GUI import WindowPaint
from PyQt5.QtWidgets import QStackedLayout, QGridLayout


class VideoPlayer(QWidget):
	
	### Video player ###

	def setupUi(self, MainWindow):

		### Media player
		self.videoWidget = QVideoWidget()
		self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
		self.mediaPlayer.setVideoOutput(self.videoWidget)
		self.mediaPlayer.positionChanged.connect(self.positionChanged)
		self.mediaPlayer.durationChanged.connect(self.durationChanged)



		### Slider of video player
		self.positionSlider = QSlider(Qt.Horizontal)
		self.positionSlider.setRange(0, 0)
		self.positionSlider.sliderMoved.connect(self.goToPosition)
		


		self.x = QLabel("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
		self.x.setStyleSheet("background-color: rgba(45, 145, 75, 0)")
		self.x.setAlignment(Qt.AlignHCenter | Qt.AlignCenter)

		self.windowPaint = WindowPaint.WindowPaint()
		self.windowPaint.setupUi(MainWindow)

		#self.layout = QStackedLayout()
		#self.layout.addWidget(self.videoWidget)
		#self.layout.addWidget(self.windowPaint)
		##self.layout.addWidget(self.x)
		#self.layout.setStackingMode(QStackedLayout.StackAll)#StackOne)
		##self.layout.setCurrentIndex(0)

		#self.windowPaint.image.fill(Qt.red)
		#self.background = QLabel(self)
		#self.background.setPixmap(QPixmap("C:\\Users\\Brugix\\source\\repos\\FundamentalsProject\\FundamentalsProject\\GUI\\12.jpg"))

		#self.layout = QGridLayout()
		
		
		
		#self.layout.addWidget(self.background, 0,0)
		#self.layout.addWidget(self.windowPaint, 0,0)
		#self.layout.addWidget(self.videoWidget, 0,0)
		#self.layout.addWidget(self.x, 0,0)


		### Widget container
		container = QVBoxLayout(self)
		container.addWidget(self.videoWidget)
		#container.addLayout(self.layout)
		container.addWidget(self.positionSlider)


		self.time = 1000

		fileName = "C:\\Users\\Brugix\\source\\repos\\FundamentalsProject\\FundamentalsProject\\GUI\\video.mp4"
		#fileName = "D:\\Videos\\Star Wars Episode III - Revenge of the Sith (2005).mkv"
		self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
		self.mediaPlayer.play()

		


	### Functions of VideoPlayer

	# Go to specific position/frame/second in video
	def goToPosition(self, position):
		self.mediaPlayer.setPosition(position)

	# Change slider position as video go forward/backward
	def positionChanged(self, position):
		self.positionSlider.setValue(position)
		if position > self.time/2:
			self.layout.setCurrentIndex(1)

	# Change slider moving speed
	def durationChanged(self, duration):
		self.positionSlider.setRange(0, duration)
		self.time = duration

		print("4 -> " + str(self.mediaPlayer.metaData("Resolution")))



	'''
	def openFile(self):
		fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
		QDir.homePath())

		fileName = "C:\\Users\\Brugix\\source\\repos\\FundamentalsProject\\FundamentalsProject\\GUI\\video.mp4"
		if fileName != '':
			print(fileName)
			self.mediaPlayer.setMedia(
				QMediaContent(QUrl.fromLocalFile(fileName)))
			self.playButton.setEnabled(True)

	def exitCall(self):
		sys.exit(app.exec_())

	def play(self):
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
			self.mediaPlayer.pause()
		else:
			self.mediaPlayer.play()		
	'''