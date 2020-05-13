from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QHBoxLayout, QWidget, QPushButton, QStyle, QFrame)


'''
Come funzioni di camcorder metterei quelle classiche
(avanti, indietro, pausa, stop, possibilmente con un variatore di velocità 0.5x 1x 2x 4x)
e poi, importante, un "vai a breakpoint".
'''


class VideoPlayerControlBar(QWidget):

	### Control bar for video player ###

	def setupUi(self, MainWindow):
		
		### Control buttons:

		# Play button
		self.btnPlay = QPushButton()
		self.btnPlay.setEnabled(False)
		self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		#self.btnPlay.clicked.connect(self.play)
		
		# Stop button
		self.btnStop = QPushButton()
		self.btnStop.setEnabled(False)
		self.btnStop.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
		#self.btnStop.clicked.connect(self.play)
		
		# Pause button
		self.btnPause = QPushButton()
		self.btnPause.setEnabled(False)
		self.btnPause.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
		#self.btnPause.clicked.connect(self.play)
		
		# Forward button
		self.btnForward = QPushButton()
		self.btnForward.setEnabled(False)
		self.btnForward.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
		#self.btnForward.clicked.connect(self.play)
		
		# Backward button
		self.btnBackward = QPushButton()
		self.btnBackward.setEnabled(False)
		self.btnBackward.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
		#self.btnBackward.clicked.connect(self.play)

		# Increase speed button
		self.btnIncreaseSpeed = QPushButton()
		self.btnIncreaseSpeed.setEnabled(False)
		self.btnIncreaseSpeed.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
		#self.btnIncreaseSpeed.clicked.connect(self.play)

		# Decrease speed button
		self.btnDecreaseSpeed = QPushButton()
		self.btnDecreaseSpeed.setEnabled(False)
		self.btnDecreaseSpeed.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
		#self.btnDecreaseSpeed.clicked.connect(self.play)

		# Go to next breakpoint
		self.btnNextBreakpoint = QPushButton()
		self.btnNextBreakpoint.setEnabled(False)
		self.btnNextBreakpoint.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
		#self.btnNextBreakpoint.clicked.connect(self.play)

		print(str(self.btnBackward.minimumHeight()))

		### Separator lines
		self.separatorLine = QFrame()
		self.separatorLine.setFrameShape( QFrame.VLine )
		self.separatorLine.setFrameShadow( QFrame.Raised )
		self.separatorLine2 = QFrame()
		self.separatorLine2.setFrameShape( QFrame.VLine )
		self.separatorLine2.setFrameShadow( QFrame.Raised )



		### Widget container
		container = QHBoxLayout(self)
		container.setContentsMargins(0, 0, 0, 0)
		container.addWidget(self.btnPlay)
		container.addWidget(self.btnPause)
		container.addWidget(self.btnStop)
		container.addWidget(self.separatorLine)
		container.addWidget(self.btnBackward)
		container.addWidget(self.btnDecreaseSpeed)
		container.addWidget(self.btnIncreaseSpeed)
		container.addWidget(self.btnForward)
		container.addWidget(self.separatorLine2)
		container.addWidget(self.btnNextBreakpoint)
		
		self.setFixedHeight(self.btnBackward.sizeHint().height())


		#MainWindow.prova("sjkdfsjdfsdjfb")




	#def provaControlBar(doNotCareYouNeedThisArgumentToMakeFuncionWork, text):
	#	print("Control Bar -> ")
	#	print(text + 10000)