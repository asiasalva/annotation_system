import cv2
import os, time

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget , QSlider, QLabel, QStackedLayout
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QPixmap, QImage


class VideoPlayerOpenCV(QWidget):
	
	### Video player ###

	def setupUi(self, MainWindow):

		self.mw = MainWindow
		self.videoPath = ""

		'''
		### Video path
		dirname = os.path.dirname(__file__)
		fileName = os.path.join(dirname, 'video.mp4')

		self.dir = dirname#print(dirname)
		self.fi = fileName#print(fileName)
		'''
		'''
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

		# Video duration (in seconds)
		self.duration = int(self.videoCapture_nFrame / self.videoCapture_fps)
		'''

		### QLabel where video frames will be shown
		self.videoFrame = QLabel()
		self.videoFrame.setStyleSheet("border: 5px solid black;")
		self.videoFrame.setScaledContents(True)
		


		### Media player (for audio only) (??? TOGLIERE O LASCIARE ???)
		#self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
		#self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))

		### QLabel where video time will be shown
		self.lblTime = QLabel(time.strftime("%H:%M:%S", time.gmtime(0)) + " / " + time.strftime("%H:%M:%S", time.gmtime(0)))

		### Slider of video player
		self.positionSlider = QSlider(Qt.Horizontal)
		self.positionSlider.setRange(0, 0)
		self.positionSlider.sliderMoved.connect(self.goToPosition)
		self.positionSlider.setTickPosition(QSlider.TicksBothSides)
		self.positionSlider.setTickInterval(10)

		### Slider and time label container
		timeSlider = QHBoxLayout()
		timeSlider.addWidget(self.positionSlider)
		timeSlider.addWidget(self.lblTime)


		### QStackedLayout
		self.stackedLayout = QStackedLayout()
		self.stackedLayout.addWidget(self.videoFrame)
		self.stackedLayout.addWidget(self.mw.windowPaint)
		self.stackedLayout.addWidget(self.mw.annotationsContainer)
		self.stackedLayout.setStackingMode(QStackedLayout.StackAll)


		### Widget container
		container = QVBoxLayout(self)
		container.addLayout(self.stackedLayout)
		container.addLayout(timeSlider)

		'''
		self.speed = 1.0
		self.timer = QTimer()
		self.timer.timeout.connect(self.nextFrameSlot)
		self.timer.setInterval((1000./self.videoCapture_fps) * self.speed)
		'''




	def setLayoutWidget(self, index):
		self.stackedLayout.setCurrentIndex(index)
		


	def nextFrameSlot(self):
		ret, frame = self.videoCapture.read()
		
		if(ret == True):
			# OpenCV yields frames in BGR format
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
			pix = QPixmap.fromImage(img)

			self.videoFrame.setPixmap(pix)

			self.positionChanged(
				self.videoCapture.get(cv2.CAP_PROP_POS_MSEC) / 1000)

			self.mw.setupAnnotations(2, "", self.videoCapture.get(cv2.CAP_PROP_POS_FRAMES))
		else:
			self.pause()

		






	### Functions of VideoPlayer

	def play(self):
		if(not self.timer.isActive()):
			print("play")
			self.timer.start()


	def pause(self):
		if(self.timer.isActive()):
			print("pause")
			self.timer.stop()


	def stop(self): ### Cosa fa lo STOP? (??? TOGLIERE O LASCIARE ???)
		#if(self.timer.isActive()):
		print("stop")
		self.timer.stop()
		# Set videoCapture position
		self.videoCapture.set(cv2.CAP_PROP_POS_MSEC, 0)
		self.nextFrameSlot()


	def backward(self):
		print("backward")

		# Get videoCapture position (in milliseconds)
		videoPos = self.videoCapture.get(cv2.CAP_PROP_POS_MSEC)

		# Move 10 seconds backward (if pos < 10000 milliseconds set pos to 0 milliseconds)
		if(videoPos < 10000):
			videoPos = 0
		else:
			videoPos -= 10000

		# Set videoCapture position
		self.videoCapture.set(cv2.CAP_PROP_POS_MSEC, videoPos)


	def decreaseSpeed(self):
		print("decreaseSpeed")

		if(self.speed < 4.0):
			self.speed *= 2.0

		self.timer.setInterval((1000./self.videoCapture_fps) * self.speed)


	def increaseSpeed(self):
		print("increaseSpeed")
		
		if(self.speed > 0.25):
			self.speed /= 2.0

		self.timer.setInterval((1000./self.videoCapture_fps) * self.speed)


	def forward(self):
		print("forward")

		# Get videoCapture position (in milliseconds)
		videoPos = self.videoCapture.get(cv2.CAP_PROP_POS_MSEC)

		# Move 10 seconds forward (if pos+10s > video duration do nothing)
		if(videoPos < (self.duration - 10)*1000):
			videoPos += 10000

		# Set videoCapture position
		self.videoCapture.set(cv2.CAP_PROP_POS_MSEC, videoPos)


	def nextBreakpoint(self):
		print("nextBreakpoint")


	def getDuration(self):
		return self.duration

	def getNumberFrameBySecond(self, second):
		return (second * self.videoCapture_fps)

	def getCurrentFrameNumber(self):
		return self.videoCapture.get(cv2.CAP_PROP_POS_FRAMES)

	def getCurrentSecond(self):
		return (self.videoCapture.get(cv2.CAP_PROP_POS_MSEC) / 1000)


	### Functions of QSlider

	# Go to specific position (second) in video
	def goToPosition(self, position):
		self.videoCapture.set(cv2.CAP_PROP_POS_MSEC, (position*1000))
		self.nextFrameSlot()

	# Change slider position as video go forward/backward
	def positionChanged(self, position):
		self.positionSlider.setValue(position)
		self.lblTime.setText(time.strftime("%H:%M:%S", time.gmtime(position)) + " / " + time.strftime("%H:%M:%S", time.gmtime(self.duration)))









	def setupVariables(self, videoPath, videoDir, videoName):

		### Video path, directory, and name
		self.videoPath =  videoPath
		self.videoDir = videoDir
		self.videoName = videoName

		### OpenCV video capture
		# Select file to capture
		self.videoCapture = cv2.VideoCapture(self.videoPath)
		# Get video FPS
		self.videoCapture_fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
		# Get video number of frames
		self.videoCapture_nFrame = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
		# Get video frame width
		self.videoCapture_frameWidth = self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
		# Get video frame height
		self.videoCapture_frameHeight = self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
		# Video duration (in seconds)
		self.duration = int(self.videoCapture_nFrame / self.videoCapture_fps)

		### VideoPlayer speed
		self.speed = 1.0
		self.timer = QTimer()
		self.timer.timeout.connect(self.nextFrameSlot)
		self.timer.setInterval((1000./self.videoCapture_fps) * self.speed)

		### Set labels with new duration
		self.positionSlider.setRange(0, self.duration)
		self.lblTime.setText(time.strftime("%H:%M:%S", time.gmtime(0)) + " / " + time.strftime("%H:%M:%S", time.gmtime(self.duration)))


	def getvideoPath(self):
		return self.videoPath