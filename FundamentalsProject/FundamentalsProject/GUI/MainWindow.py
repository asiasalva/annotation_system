from PyQt5 import QtCore, QtWidgets, QtGui

from GUI import VideoPlayerOpenCV, VideoPlayerControlBar, AnnotationsTable, AnnotationsProperties, AnnotationsList
from GUI import Annotation, WindowPaint, AnnotationsContainer, AnnotationDrawing

class Ui_MainWindow(object):

	### Main window ###

	def setupUi(self, MainWindow):

		# Set main window, 
		# set central widget (i.e., main container),
		# set vertical layout (i.e., main layout)
		# N.B.: you need to put a layout (any kind of layout) in order to make content auto resizable
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1280, 720)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
		self.verticalLayout.setObjectName("verticalLayout")
	

		# Splitter for "video side" and "annotations side" (main splitter)
		self.splitterWindow = QtWidgets.QSplitter(self.centralwidget)
		self.splitterWindow.setOrientation(QtCore.Qt.Horizontal)
		self.splitterWindow.setObjectName("splitterWindow")
		self.splitterWindow.setChildrenCollapsible(False)
		
		# Vertical container for "video side" components
		self.vboxVideoLayoutWidget = QtWidgets.QWidget(self.splitterWindow)
		self.vboxVideoLayoutWidget.setObjectName("vboxLayoutWidget")
		self.vboxVideo = QtWidgets.QVBoxLayout(self.vboxVideoLayoutWidget)
		self.vboxVideo.setContentsMargins(0, 0, 0, 0)
		self.vboxVideo.setObjectName("vboxVideo")
		
		# Splitter container for "annotations side" components
		self.splitterAnnotation = QtWidgets.QSplitter(self.splitterWindow)
		self.splitterAnnotation.setOrientation(QtCore.Qt.Vertical)
		self.splitterAnnotation.setObjectName("splitterAnnotation")
		self.splitterAnnotation.setChildrenCollapsible(False)
		

		# Put main splitter inside main layout
		self.verticalLayout.addWidget(self.splitterWindow)
		# Set main container for main window
		MainWindow.setCentralWidget(self.centralwidget)
		

		# Menu and status bar
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 26))
		self.menubar.setObjectName("menubar")
		self.menuFile = QtWidgets.QMenu(self.menubar)
		self.menuFile.setObjectName("menuFile")
		MainWindow.setMenuBar(self.menubar)
		
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		
		self.actionOpen_Video = QtWidgets.QAction(MainWindow)
		self.actionOpen_Video.setObjectName("actionOpen_Video")
		self.actionOpen_Project = QtWidgets.QAction(MainWindow)
		self.actionOpen_Project.setObjectName("actionOpen_Project")
		self.actionSave = QtWidgets.QAction(MainWindow)
		self.actionSave.setObjectName("actionSave")
		self.actionExport = QtWidgets.QAction(MainWindow)
		self.actionExport.setObjectName("actionExport")
		self.actionClose = QtWidgets.QAction(MainWindow)
		self.actionClose.setObjectName("actionClose")
		self.actionExit = QtWidgets.QAction(MainWindow)
		self.actionExit.setObjectName("actionExit")
		self.menuFile.addAction(self.actionOpen_Video)
		self.menuFile.addAction(self.actionOpen_Project)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionSave)
		self.menuFile.addAction(self.actionExport)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionClose)
		self.menuFile.addAction(self.actionExit)
		self.menubar.addAction(self.menuFile.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)


		### Custom widgets - Annotations

		self.windowPaint = WindowPaint.WindowPaint()
		self.windowPaint.setupUi(self)
		self.annotationsContainer = AnnotationsContainer.AnnotationsContainer(self)


		### Custom widgets - "Video side"

		# Add VideoPlayer widget
		self.videoPlayer = VideoPlayerOpenCV.VideoPlayerOpenCV()
		self.videoPlayer.setupUi(self)

		# Add VideoPlayerControlBar widget
		self.videoPlayerControlBar = VideoPlayerControlBar.VideoPlayerControlBar()
		self.videoPlayerControlBar.setupUi(self)
		
		# Put "video side" components inside vertical container previously defined
		self.vboxVideo.addWidget(self.videoPlayer)
		self.vboxVideo.addWidget(self.videoPlayerControlBar)



		### Custom widgets - "Annotations side"

		# Add AnnotationsList widget
		self.annotationsList = AnnotationsList.AnnotationsList()
		self.annotationsList.setupUi(self)

		# Add AnnotationsProperties widget
		self.annotationsProperties = AnnotationsProperties.AnnotationsProperties()
		self.annotationsProperties.setupUi(self)
		
		# Add TableAnnotations widget
		self.annotationsTable = AnnotationsTable.AnnotationsTable()
		self.annotationsTable.setupUi(self)

		# Put "annotations side" components inside splitter container previously defined
		self.splitterAnnotation.addWidget(self.annotationsList)
		self.splitterAnnotation.addWidget(self.annotationsProperties)
		self.splitterAnnotation.addWidget(self.annotationsTable)
		


	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.menuFile.setTitle(_translate("MainWindow", "File"))
		self.actionOpen_Video.setText(_translate("MainWindow", "Open Video"))
		self.actionOpen_Project.setText(_translate("MainWindow", "Open Project"))
		self.actionOpen_Project.setShortcut(_translate("MainWindow", "Ctrl+O"))
		self.actionSave.setText(_translate("MainWindow", "Save"))
		self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
		self.actionExport.setText(_translate("MainWindow", "Export"))
		self.actionClose.setText(_translate("MainWindow", "Close Project"))
		self.actionExit.setText(_translate("MainWindow", "Exit"))
		self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))



	def setupAnnotations(self, command, fileName = ""):
		print("setupAnnotations")

		if(command == 0):					# First setup
			self.listOfAnnotations = list()
			self.listOfDrawing = list()
			self.lastFocusAnnotation = None
			#self.lastFocusAnnotationIndex = -1


			'''
			# Prova di "windowPaint.drawAnnotations"
			self.listOfDrawing.append(
			AnnotationDrawing.AnnotationDrawing(0, QtGui.QPen(QtCore.Qt.black, 25, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin), QtCore.QPoint(10,10), QtCore.QPoint(10,50), None, None)
			)
			self.listOfDrawing.append(
			AnnotationDrawing.AnnotationDrawing(1, None, None, None, 5, QtCore.QPoint(10,25))
			)

			self.windowPaint.drawAnnotations(self.listOfDrawing)
			'''


	def setLastFocusAnnotation(self, lastFocusAnnotation):
		self.lastFocusAnnotation = lastFocusAnnotation

		#print("Widget on focus")
		#print(self.lastFocusAnnotation.childWidget.__class__.__name__)
		#print(self.lastFocusAnnotation.childWidget.__class__)
		#print(QtWidgets.QPlainTextEdit)
		#print(isinstance(self.lastFocusAnnotation.childWidget, QtWidgets.QPlainTextEdit))
		#print(isinstance(self.lastFocusAnnotation.childWidget.__class__, QtWidgets.QPlainTextEdit))
		#print(self.lastFocusAnnotation.childWidget.__class__ is QtWidgets.QPlainTextEdit)
		#print(isinstance(None, QtWidgets.QPlainTextEdit))

		self.windowPaint.setRubber(False)


		if(isinstance(self.lastFocusAnnotation.childWidget, QtWidgets.QPlainTextEdit)):
			self.annotationsProperties.setProperties(
				self.lastFocusAnnotation.childWidget.__class__, 
				False, 
				None, 
				None, 
				None
			)
		elif self.lastFocusAnnotation.isArrow:
			self.annotationsProperties.setProperties(
				self.lastFocusAnnotation.childWidget.__class__, 
				self.lastFocusAnnotation.isArrow, 
				self.lastFocusAnnotation.svgColor, 
				int(float(self.lastFocusAnnotation.svgExtraAttribute)*100), 
				int(self.lastFocusAnnotation.svgTransform)
			)
		else:
			self.annotationsProperties.setProperties(
				self.lastFocusAnnotation.childWidget.__class__, 
				self.lastFocusAnnotation.isArrow, 
				self.lastFocusAnnotation.svgColor, 
				int(self.lastFocusAnnotation.svgExtraAttribute), 
				int(self.lastFocusAnnotation.svgTransform)
			)
		

	def setNewAnnotationProperties(self, colorString, value1, value2):
		
		# DRAWING
		if self.lastFocusAnnotation is None:
			# RUBBER
			if colorString is None:
				self.windowPaint.setRubber(True)
				self.windowPaint.setRubberSize(value2)
			# DRAW
			else:
				self.windowPaint.setPainterPen(QtGui.QPen(QtGui.QColor(colorString), value1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
				self.windowPaint.setRubber(False)
				self.windowPaint.setRubberSize(value2)
		# TEXTBOX
		elif(isinstance(self.lastFocusAnnotation.childWidget, QtWidgets.QPlainTextEdit)):
			print("textbox...per ora niente proprieta'")
		# ARROW
		elif self.lastFocusAnnotation.isArrow:
			self.lastFocusAnnotation.setSvgColor(colorString)
			self.lastFocusAnnotation.setSvgExtraAttribute(str(value1/100))
			self.lastFocusAnnotation.setSvgTransform(str(value2))
		# LINE
		else:
			self.lastFocusAnnotation.setSvgColor(colorString)
			self.lastFocusAnnotation.setSvgExtraAttribute(str(value1))
			self.lastFocusAnnotation.setSvgTransform(str(value2))







	### ACTIONS: VideoPlayerControlBar -> VideoPlayerOpenCV

	def controlBarCommand(self, command):
		print("controlBarCommand -> " + str(command))

		if(command == 0):
			self.videoPlayer.play()
		elif(command == 1):
			self.videoPlayer.pause()
		elif(command == 2):
			self.videoPlayer.stop()
		elif(command == 3):
			self.videoPlayer.backward()
		elif(command == 4):
			self.videoPlayer.decreaseSpeed()
		elif(command == 5):
			self.videoPlayer.increaseSpeed()
		elif(command == 6):
			self.videoPlayer.forward()
		elif(command == 7):
			self.videoPlayer.nextBreakpoint()



	### ACTIONS: AnnotationsList -> ???

	def annotationsListCommand(self, command):
		print("annotationsListCommand -> " + str(command))

		# 0 -> line
		# 1 -> arrow
		# 2 -> textbox
		# 3 -> breakpoint
		# 4 -> drawing

		if(command == 4):

			self.lastFocusAnnotation = None
			self.annotationsProperties.setProperties(
				None, 
				False, 
				self.windowPaint.getPainterPen().color().name(),
				self.windowPaint.getPainterPen().width(),
				self.windowPaint.getRubberSize()
			)

			if self.windowPaint.getTrackingMouse():
				self.annotationsList.changeDrawButtonText(False)
				self.windowPaint.setTrackingMouse(False)
				self.videoPlayer.setLayoutWidget(2)
				self.windowPaint.setRubber(False)
			else:
				self.annotationsList.changeDrawButtonText(True)
				self.windowPaint.setTrackingMouse(True)
				self.videoPlayer.setLayoutWidget(1)
		else:
			self.annotationsList.changeDrawButtonText(False)
			self.windowPaint.setTrackingMouse(False)
			self.videoPlayer.setLayoutWidget(2)

			self.annotationsContainer.createAnnotation(command)

	