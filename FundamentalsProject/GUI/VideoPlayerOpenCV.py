from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QVBoxLayout, QWidget , QSlider, QLabel)

from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QImage


import GUI
from GUI import WindowPaint
from PyQt5.QtWidgets import QStackedLayout, QGridLayout
import cv2 


class VideoPlayerOpenCV(QWidget):
	
	### Video player ###

	def setupUi(self, MainWindow):

		### Video path
		fileName = "C:\\Users\\Brugix\\source\\repos\\FundamentalsProject\\FundamentalsProject\\GUI\\video.mp4"
			

		### OpenCV video capture
		# Select file to capture
		self.videoCapture = cv2.VideoCapture(fileName)
		# Get video FPS
		self.videoCapture_fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
		# Get video number of frames
		self.videoCapture_nFrame = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
		# Get video frame width
		self.videoCapture_frameWidth = self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
		# Get video frame height
		self.videoCapture_frameHeight = self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
		

		### QLabel where video frames will be shown
		self.videoFrame = QLabel()


		### Media player (for audio only) (??? TOGLIERE O LASCIARE ???)
		self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
		self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))


		### Window paint
		self.windowPaint = WindowPaint.WindowPaint()
		self.windowPaint.setupUi(MainWindow)


		### Slider of video player
		self.positionSlider = QSlider(Qt.Horizontal)
		#self.positionSlider.setRange(0, 0)
		#self.positionSlider.sliderMoved.connect(self.goToPosition)


		### QStackedLayout
		self.stackedLayour = QStackedLayout()
		self.stackedLayour.addWidget(self.videoFrame)
		self.stackedLayour.addWidget(self.windowPaint)
		self.stackedLayour.setStackingMode(QStackedLayout.StackAll)


		### Widget container
		container = QVBoxLayout(self)
		container.addLayout(self.stackedLayour)
		container.addWidget(self.positionSlider)






		


	def nextFrameSlot(self):
		ret, frame = self.videoCapture.read()
		# OpenCV yields frames in BGR format
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)
		self.videoFrame.setPixmap(pix)

	def start(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.nextFrameSlot)
		self.timer.start(1000./self.videoCapture_fps)
		self.mediaPlayer.play()

		


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
		self.time = duration

		#print("4 -> " + str(self.mediaPlayer.metaData("Resolution")))



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