import cv2
import os

from PyQt5.QtWidgets import QVBoxLayout, QWidget , QSlider, QLabel, QStackedLayout
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QPixmap, QImage

from GUI import WindowPaint


class VideoPlayerOpenCV(QWidget):
	
	### Video player ###

	def setupUi(self, MainWindow):

		self.mw = MainWindow


		### Video path
		dirname = os.path.dirname(__file__)
		fileName = os.path.join(dirname, 'video.mp4')
		# fileName = "C:\\Users\\Brugix\\source\\repos\\asiasalva\\annotation_system\\FundamentalsProject\\GUI\\video.mp4"
		#fileName = str(pathlib.Path("video.mp4").parent.absolute()) + "\\video.mp4" # NOT WORKING -> prende il path del file di startup
			

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


		### QLabel where video frames will be shown
		self.videoFrame = QLabel()
		self.videoFrame.setStyleSheet("border: 5px solid black;")
		self.videoFrame.setScaledContents(True)
		


		### Media player (for audio only) (??? TOGLIERE O LASCIARE ???)
		#self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
		#self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))


		### Slider of video player
		self.positionSlider = QSlider(Qt.Horizontal)
		self.positionSlider.setRange(0, self.duration)
		self.positionSlider.sliderMoved.connect(self.goToPosition)
		self.positionSlider.setTickPosition(QSlider.TicksBelow)
		self.positionSlider.setTickInterval(10)


		### QStackedLayout
		self.stackedLayout = QStackedLayout()
		self.stackedLayout.addWidget(self.videoFrame)
		self.stackedLayout.addWidget(self.mw.windowPaint)
		self.stackedLayout.addWidget(self.mw.annotationsContainer)
		self.stackedLayout.setStackingMode(QStackedLayout.StackAll)


		### Widget container
		container = QVBoxLayout(self)
		container.addLayout(self.stackedLayout)
		container.addWidget(self.positionSlider)


		self.speed = 1.0
		self.timer = QTimer()
		self.timer.timeout.connect(self.nextFrameSlot)
		self.timer.setInterval((1000./self.videoCapture_fps) * self.speed)





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
			#self.start()
			self.timer.start()


	def pause(self):
		if(self.timer.isActive()):
			print("pause")
			self.timer.stop()


	def stop(self): ### Cosa fa lo STOP? (??? TOGLIERE O LASCIARE ???)
		if(self.timer.isActive()):
			print("stop")
			self.timer.stop()


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

	# Change slider position as video go forward/backward
	def positionChanged(self, position):
		self.positionSlider.setValue(position)



	'''
	# Python Program to Convert seconds 
	# into hours, minutes and seconds 
  
	import time 
  
	def convert(seconds): 
		return time.strftime("%H:%M:%S", time.gmtime(n)) 
      
	# Driver program 
	n = 12345
	print(convert(n)) 
	'''



	'''

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