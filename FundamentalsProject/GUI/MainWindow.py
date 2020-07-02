from PyQt5 import QtCore, QtWidgets, QtGui
import os
from GUI import VideoPlayerOpenCV, VideoPlayerControlBar, AnnotationsTable, AnnotationsProperties, AnnotationsList
from GUI import Annotation, WindowPaint, AnnotationsContainer, AnnotationDrawing, XMLSerializer

class Ui_MainWindow(object):

	### Main window ###

	def setupUi(self, MainWindow):
		self.mw = MainWindow
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
		
		self.actionNew_Project = QtWidgets.QAction(MainWindow)
		self.actionNew_Project.setObjectName("actionNew_Project")
		self.actionOpen_Project = QtWidgets.QAction(MainWindow)
		self.actionOpen_Project.setObjectName("actionOpen_Project")
		self.actionAdd_Video = QtWidgets.QAction(MainWindow)
		self.actionAdd_Video.setObjectName("actionAdd_Video")
		self.actionSave_Project = QtWidgets.QAction(MainWindow)
		self.actionSave_Project.setObjectName("actionSave_Project")
		self.actionExport = QtWidgets.QAction(MainWindow)
		self.actionExport.setObjectName("actionExport")
		#--self.actionClose = QtWidgets.QAction(MainWindow)
		#--self.actionClose.setObjectName("actionClose")
		self.actionExit = QtWidgets.QAction(MainWindow)
		self.actionExit.setObjectName("actionExit")
		self.menuFile.addAction(self.actionNew_Project)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionOpen_Project)
		self.menuFile.addAction(self.actionAdd_Video)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionSave_Project)
		self.menuFile.addAction(self.actionExport)
		self.menuFile.addSeparator()
		#--self.menuFile.addAction(self.actionClose)
		self.menuFile.addAction(self.actionExit)
		self.menubar.addAction(self.menuFile.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)


		### Custom widgets - Annotations

		self.windowPaint = WindowPaint.WindowPaint()
		self.windowPaint.setupUi(self)
		self.windowPaint.setEnabled(False)
		self.annotationsContainer = AnnotationsContainer.AnnotationsContainer(self)
		self.annotationsContainer.setEnabled(False)
		self.xmlSerializer = XMLSerializer.XMLSerializer(self)

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
		self.annotationsList.setEnabled(False)

		# Add AnnotationsProperties widget
		self.annotationsProperties = AnnotationsProperties.AnnotationsProperties()
		self.annotationsProperties.setupUi(self)
		self.annotationsProperties.setEnabled(False)
		
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
		self.actionNew_Project.setText(_translate("MainWindow", "New Project"))
		self.actionNew_Project.setShortcut(_translate("MainWindow", "Ctrl+N"))
		self.actionOpen_Project.setText(_translate("MainWindow", "Open Project"))
		self.actionOpen_Project.setShortcut(_translate("MainWindow", "Ctrl+O"))
		self.actionAdd_Video.setText(_translate("MainWindow", "Add Video"))
		self.actionSave_Project.setText(_translate("MainWindow", "Save Project"))
		self.actionSave_Project.setShortcut(_translate("MainWindow", "Ctrl+S"))
		self.actionExport.setText(_translate("MainWindow", "Export"))
		#--self.actionClose.setText(_translate("MainWindow", "Close Project"))
		self.actionExit.setText(_translate("MainWindow", "Exit"))
		self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))

		self.actionNew_Project.triggered.connect(self.newProject)
		self.actionOpen_Project.triggered.connect(self.openProject)
		self.actionAdd_Video.triggered.connect(self.addVideo)
		self.actionSave_Project.triggered.connect(self.saveProject)
		self.actionExport.triggered.connect(self.exportVideo)
		#--self.actionClose.triggered.connect(self.closeProject)
		self.actionExit.triggered.connect(self.exitProgram)

		self.actionNew_Project.setEnabled(True)
		self.actionOpen_Project.setEnabled(True)
		self.actionAdd_Video.setEnabled(False)
		self.actionSave_Project.setEnabled(True)
		self.actionExport.setEnabled(False)
		#--self.actionClose.setEnabled(False)
		self.actionExit.setEnabled(True)



	def setupAnnotations(self, command, projectPath = "", nFrame = None):
		print("setupAnnotations")

		if(command == 0):					# First setup
			self.listOfAnnotations = list()
			self.listOfDrawing = list()
			self.listOfBreaks = list()
			self.lastFocusAnnotation = None
			#--self.setDurationProperty()
			self.projectPath = ""
			self.actionAdd_Video.setEnabled(True)

		elif(command == 1):
			print("Load annotations from file")
			projectName, videoPath = self.xmlSerializer.readXML(projectPath)

			if projectName != "":
				self.videoPlayer.setupVariables(videoPath, os.path.dirname(videoPath), os.path.basename(videoPath))
				self.setDurationProperty()
				self.actionAdd_Video.setEnabled(False)
				self.videoPlayerControlBar.enablePlayButton(True)

			self.annotationsTable.insertRows(self.listOfAnnotations)
			self.annotationsContainer.showAnnotations(0)

		elif(command == 2):
			print("Frame n°: " + str(nFrame))

			# Load annotations present in this specific frame
			self.annotationsContainer.showAnnotations(nFrame)


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
		
		self.annotationsProperties.setPropertiesVisible(True)

		self.lastFocusAnnotation = lastFocusAnnotation

		self.windowPaint.setRubber(False)


		if(isinstance(self.lastFocusAnnotation.childWidget, QtWidgets.QPlainTextEdit)):
			self.annotationsProperties.setProperties(
				self.lastFocusAnnotation.childWidget.__class__, 
				False, 
				self.lastFocusAnnotation.getTextboxFontColor(), 
				self.lastFocusAnnotation.getTextboxFontSize(),
				self.lastFocusAnnotation.getTextboxBackgroundOpacity(),
				self.lastFocusAnnotation.getSecStart(),
				self.lastFocusAnnotation.getSecEnd()
			)
		elif self.lastFocusAnnotation.isArrow:
			self.annotationsProperties.setProperties(
				self.lastFocusAnnotation.childWidget.__class__, 
				self.lastFocusAnnotation.isArrow, 
				self.lastFocusAnnotation.svgColor, 
				int(float(self.lastFocusAnnotation.svgExtraAttribute)*100), 
				int(self.lastFocusAnnotation.svgTransform),
				self.lastFocusAnnotation.getSecStart(),
				self.lastFocusAnnotation.getSecEnd()
			)
		elif self.lastFocusAnnotation.isArrow == False:
			self.annotationsProperties.setProperties(
				self.lastFocusAnnotation.childWidget.__class__, 
				self.lastFocusAnnotation.isArrow, 
				self.lastFocusAnnotation.svgColor, 
				int(self.lastFocusAnnotation.svgExtraAttribute), 
				int(self.lastFocusAnnotation.svgTransform),
				self.lastFocusAnnotation.getSecStart(),
				self.lastFocusAnnotation.getSecEnd()
			)
		else:
			self.annotationsProperties.setProperties(
				self.lastFocusAnnotation.childWidget.__class__, 
				None,
				False, 
				0, 
				0,
				self.lastFocusAnnotation.getSecStart(),
				self.lastFocusAnnotation.getSecEnd()
			)
		

	def setNewAnnotationProperties(self, colorString, value1, value2, secStart, secEnd):
		
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
			self.lastFocusAnnotation.setTextboxFontColor(colorString)
			self.lastFocusAnnotation.setTextboxFontSize(value1)
			self.lastFocusAnnotation.setTextboxBackgroundOpacity(value2)
			self.lastFocusAnnotation.setSecRange(secStart, secEnd)
			self.lastFocusAnnotation.setFrameRange(self.videoPlayer.getNumberFrameBySecond(secStart), self.videoPlayer.getNumberFrameBySecond(secEnd))
			self.annotationsTable.updateRow(self.lastFocusAnnotation)
		#BREAKPOINT 
		elif(isinstance(self.lastFocusAnnotation.childWidget, QtWidgets.QWidget)):
			self.lastFocusAnnotation.setSecRange(secStart, secEnd)
			self.lastFocusAnnotation.setFrameRange(self.videoPlayer.getNumberFrameBySecond(secStart), self.videoPlayer.getNumberFrameBySecond(secEnd))
			self.annotationsTable.updateRow(self.lastFocusAnnotation)
		# ARROW
		elif self.lastFocusAnnotation.isArrow:
			self.lastFocusAnnotation.setSvgColor(colorString)
			self.lastFocusAnnotation.setSvgExtraAttribute(str(value1/100))
			self.lastFocusAnnotation.setSvgTransform(str(value2)),
			self.lastFocusAnnotation.setSecRange(secStart, secEnd)
			self.lastFocusAnnotation.setFrameRange(self.videoPlayer.getNumberFrameBySecond(secStart), self.videoPlayer.getNumberFrameBySecond(secEnd))
			self.annotationsTable.updateRow(self.lastFocusAnnotation)
		# LINE
		else:
			self.lastFocusAnnotation.setSvgColor(colorString)
			self.lastFocusAnnotation.setSvgExtraAttribute(str(value1))
			self.lastFocusAnnotation.setSvgTransform(str(value2)),
			self.lastFocusAnnotation.setSecRange(secStart, secEnd)
			self.lastFocusAnnotation.setFrameRange(self.videoPlayer.getNumberFrameBySecond(secStart), self.videoPlayer.getNumberFrameBySecond(secEnd))
			self.annotationsTable.updateRow(self.lastFocusAnnotation)

		self.orderAnnotations()




	def setDurationProperty(self):
		self.annotationsProperties.setDuration(self.videoPlayer.getDuration())







	### ACTIONS: VideoPlayerControlBar -> VideoPlayerOpenCV

	def controlBarCommand(self, command):
		print("controlBarCommand -> " + str(command))

		if(command == 0):
			self.videoPlayer.play()
			self.videoPlayerControlBar.enableButtons(True)
			self.annotationsList.setEnabled(False)
			self.annotationsProperties.setEnabled(False)
			self.annotationsContainer.setEnabled(False)
			self.windowPaint.setEnabled(False)
		elif(command == 1):
			self.videoPlayer.pause()
			self.annotationsList.setEnabled(True)
			self.annotationsProperties.setEnabled(True)
			self.annotationsContainer.setEnabled(True)
			self.windowPaint.setEnabled(True)
		elif(command == 2):
			self.videoPlayer.stop()
			self.videoPlayerControlBar.enableButtons(False)
			self.videoPlayerControlBar.enablePlayButton(True)
			self.annotationsList.setEnabled(False)
			self.annotationsProperties.setEnabled(False)
			self.annotationsContainer.setEnabled(False)
			self.windowPaint.setEnabled(False)
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
				self.windowPaint.getRubberSize(),
				0,0
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

			self.annotationsContainer.createAnnotation(command, self.videoPlayer.getCurrentSecond())
			self.listOfAnnotations[-1].setFrameRange(self.videoPlayer.getCurrentFrameNumber(), self.videoPlayer.getCurrentFrameNumber())
			self.annotationsTable.insertRow(self.listOfAnnotations[-1])	# [-1] get the last element of the list
			self.orderAnnotations()


	### ACTIONS: AnnotationsTable -> ???
	def showAnnotationSelected(self, annotationID):

		# If user is drawing, stop WindowPaint from drawing
		if self.windowPaint.getTrackingMouse():
			self.annotationsList.changeDrawButtonText(False)
			self.windowPaint.setTrackingMouse(False)
			self.videoPlayer.setLayoutWidget(2)
			self.windowPaint.setRubber(False)

		# Find annotation selected and show it
		for item in self.listOfAnnotations:
			if annotationID == str(item):
				item.setFocus()
				self.videoPlayer.goToPosition(item.getSecStart())
				self.setLastFocusAnnotation(item)


	def removeAnnotation(self, annotationToRemove):
		self.annotationsTable.removeRow(annotationToRemove)
		self.listOfAnnotations.remove(annotationToRemove)
		self.annotationsProperties.setPropertiesVisible(False)






	### MENU FUNCTIONS

	def newProject(self):
		print("newProject")

		retval = self.messageBox()

		if retval == QtWidgets.QMessageBox.Save:
			# Save previous changes and create a new project
			if self.saveProject():
				self.setupAnnotations(0)
				self.setupUi(self.mw)
		elif retval == QtWidgets.QMessageBox.Discard:
			# Close current project and create new one
			self.setupAnnotations(0)
			self.setupUi(self.mw)



	def addVideo(self):
		print("openVideo")

		# If a video is not already loaded
		if self.videoPlayer.getvideoPath() == "":
			videoPath, _ = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QWidget(), "Open Video", QtCore.QDir.homePath())#, "Video files")

			if videoPath != "":
				videoDir = os.path.dirname(videoPath)
				videoName = os.path.basename(videoPath)
				self.videoPlayer.setupVariables(videoPath, videoDir, videoName)
				self.setDurationProperty()
				self.actionAdd_Video.setEnabled(False)
				self.videoPlayerControlBar.enablePlayButton(True)


		



	def openProject(self):
		print("openProject")

		retval = self.messageBox()

		if retval == QtWidgets.QMessageBox.Save:
			# Save previous changes and open a project
			if self.saveProject():
				self.projectPath, _ = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QWidget(), "Open Project", QtCore.QDir.homePath(), "XML files (*.xml)")

				if self.projectPath != "":
					# Load project (video + annotations)
					self.setupUi(self.mw)
					self.setupAnnotations(1, self.projectPath)
		elif retval == QtWidgets.QMessageBox.Discard:
			# Close current project and load a project
			self.projectPath, _ = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QWidget(), "Open Project", QtCore.QDir.homePath(), "XML files (*.xml)")

			if self.projectPath != "":
				# Load project (video + annotations)
				self.setupUi(self.mw)
				self.setupAnnotations(1, self.projectPath)



	def saveProject(self):
		print("saveProject")

		# If project has not been saved yet (so it's a new project)
		if self.projectPath == "":
			self.projectPath, _ = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QWidget(), "Save Project", QtCore.QDir.homePath(), "XML files (*.xml)")
			#projectDir = os.path.dirname(projectPath[0])
			#projectName = os.path.basename(projectPath[0])

		if self.projectPath != "":
			# Save previous changes and write XML
			self.xmlSerializer.writeXML(
				self.projectPath,
				os.path.basename(self.projectPath),
				self.videoPlayer.getvideoPath(),
				self.listOfAnnotations
			)
			return True
		else:
			return False

		



	def exportVideo(self):
		print("exportVideo")
		# TENERE ???

	#--def closeProject(self):
	#--	print("closeProject")
	#--	# TENERE ???
	#--	self.newProject()


	def exitProgram(self):
		print("exitProgram")

		retval = self.messageBox()

		if retval == QtWidgets.QMessageBox.Save:
			# Save previous changes and close
			if self.saveProject():
				QtCore.QCoreApplication.instance().quit()
		elif retval == QtWidgets.QMessageBox.Discard:
			# Close application
			QtCore.QCoreApplication.instance().quit()

		return retval
		

		

	def messageBox(self):
		if self.projectPath == "":
			projectName = "Untitled"
		else:
			projectName = os.path.basename(self.projectPath)

		msg = QtWidgets.QMessageBox()
		msg.setIcon(QtWidgets.QMessageBox.Warning)
		msg.setText("Do You want to save changes to " + projectName + "?")
		msg.setWindowTitle(projectName)
		msg.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)

		return msg.exec_()





	def byFrameStart(self, elem):
		return elem.getFrameRange()[0]

	def orderAnnotations(self):
		self.listOfAnnotations.sort(key=self.byFrameStart)
		self.listOfBreaks.sort(key=self.byFrameStart)