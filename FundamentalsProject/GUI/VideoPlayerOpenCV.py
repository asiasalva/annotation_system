import cv2
import os, time, ffmpeg

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget , QSlider, QLabel, QStackedLayout
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QPixmap, QImage

class VideoPlayerOpenCV(QWidget):
	
	### Video player ###

	def setupUi(self, MainWindow):
		self.mw = MainWindow
		self.videoPath = ""

		### QLabel where video frames will be shown
		self.videoFrame = QLabel()
		self.videoFrame.setStyleSheet("border: 5px solid black;")
		self.videoFrame.setScaledContents(True)
		
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
		self.stackedLayout.addWidget(self.mw.windowBlackboard)
		self.stackedLayout.setStackingMode(QStackedLayout.StackAll)

		### Widget container
		container = QVBoxLayout(self)
		container.addLayout(self.stackedLayout)
		container.addLayout(timeSlider)

	def setLayoutWidget(self, index):
		self.stackedLayout.setCurrentIndex(index)

	def nextFrameSlot(self):
		ret, frame = self.videoCapture.read()
		if(ret == True):
			# OpenCV yields frames in BGR format
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

			# If frame needs rotation
			if self.rotateCode is not None:
				frame = self.correctVideoRotation(frame, self.rotateCode)

			img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
			pix = QPixmap.fromImage(img)
			self.videoFrame.setPixmap(pix)
			self.positionChanged(self.videoCapture.get(cv2.CAP_PROP_POS_MSEC) / 1000)
			self.mw.setupAnnotations(2, "", self.videoCapture.get(cv2.CAP_PROP_POS_FRAMES))
		else:
			self.pause()

	### Functions of VideoPlayer

	def play(self):
		if(not self.timer.isActive()):
			self.timer.start()

	def pause(self):
		if(self.timer.isActive()):
			self.timer.stop()

	def stop(self):
		self.timer.stop()
		# Set videoCapture position
		self.videoCapture.set(cv2.CAP_PROP_POS_MSEC, 0)
		self.nextFrameSlot()

	def backward(self):
		# Get videoCapture position (in milliseconds)
		videoPos = self.videoCapture.get(cv2.CAP_PROP_POS_MSEC)
		# Move 10 seconds backward (if pos < 10000 milliseconds set pos to 0 milliseconds)
		if(videoPos < 10000):
			videoPos = 0
		else:
			videoPos -= 10000
		# Set videoCapture position
		self.videoCapture.set(cv2.CAP_PROP_POS_MSEC, videoPos)
		if(not self.timer.isActive()):
			self.nextFrameSlot()

	def decreaseSpeed(self):
		if(self.speed < 4.0):
			self.speed *= 2.0
		self.timer.setInterval((1000./self.videoCapture_fps) * self.speed)

	def increaseSpeed(self):
		if(self.speed > 0.25):
			self.speed /= 2.0
		self.timer.setInterval((1000./self.videoCapture_fps) * self.speed)

	def forward(self):
		# Get videoCapture position (in milliseconds)
		videoPos = self.videoCapture.get(cv2.CAP_PROP_POS_MSEC)
		# Move 10 seconds forward (if pos+10s > video duration do nothing)
		if(videoPos < (self.duration - 10)*1000):
			videoPos += 10000
		# Set videoCapture position
		self.videoCapture.set(cv2.CAP_PROP_POS_MSEC, videoPos)
		if(not self.timer.isActive()):
			self.nextFrameSlot()

	def nextBreakpoint(self):
		videoPos = self.videoCapture.get(cv2.CAP_PROP_POS_FRAMES)
		breakpointFound = False
		# Scan breakpoints annotations
		for i in range(len(self.mw.listOfBreaks)):
			tmp =  (self.mw.listOfBreaks[i]).getFrameRange()[0]
			if videoPos < tmp :
				videoPos = tmp
				breakpointFound = True
				break
			elif i == (len(self.mw.listOfBreaks) - 1):
				videoPos = self.mw.listOfBreaks[0].getFrameRange()[0]
				breakpointFound = True
				break

		if breakpointFound:
			# Set videoCapture position
			self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES, videoPos-1)
			self.pause()
			self.nextFrameSlot()

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


	### Support functions

	def setupVariables(self, videoPath):

		success = False

		try:
			### Video path, directory, and name
			self.videoPath =  videoPath
			#self.onBreakpoint = False

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

			### Check if video requires rotation
			self.rotateCode = self.checkVideoRotation(self.videoPath)

			self.mw.setFrameDimensions(self.videoCapture_frameWidth, self.videoCapture_frameHeight)

			success = True
		except:
			success = False

		return success

	def getvideoPath(self):
		return self.videoPath

	def checkVideoRotation(self, path_video_file):
		# This returns meta-data of the video file in form of a dictionary
		meta_dict = ffmpeg.probe(path_video_file)
		rotateCode = None

		if 'rotate' in meta_dict['streams'][0]['tags']:
		
			# From the dictionary, meta_dict['streams'][0]['tags']['rotate'] is the key
			#	we are looking for
			
			if int(meta_dict['streams'][0]['tags']['rotate']) == 90:
				rotateCode = cv2.ROTATE_90_CLOCKWISE
			elif int(meta_dict['streams'][0]['tags']['rotate']) == 180:
				rotateCode = cv2.ROTATE_180
			elif int(meta_dict['streams'][0]['tags']['rotate']) == 270:
				rotateCode = cv2.ROTATE_90_COUNTERCLOCKWISE

		return rotateCode

	def correctVideoRotation(self, frame, rotateCode):  
		return cv2.rotate(frame, rotateCode) 