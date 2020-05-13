from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QVBoxLayout, QWidget , QSlider)

from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl



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



		### Widget container
		container = QVBoxLayout(self)
		container.addWidget(self.videoWidget)
		container.addWidget(self.positionSlider)




		#fileName = "C:\\Users\\Brugix\\source\\repos\\FundamentalsProject\\FundamentalsProject\\GUI\\video.mp4"
		#self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
		#self.mediaPlayer.play()	





	### Functions of VideoPlayer

	# Go to specific position/frame/second in video
	def goToPosition(self, position):
		self.mediaPlayer.setPosition(position)

	# Change slider position as video go forward/backward
	def positionChanged(self, position):
		self.positionSlider.setValue(position)

	# Change slider moving speed
	def durationChanged(self, duration):
		self.positionSlider.setRange(0, duration)



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