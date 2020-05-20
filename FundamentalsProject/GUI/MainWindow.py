# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import GUI
from GUI import (VideoPlayerControlBar, VideoPlayer, AnnotationsTable, AnnotationsProperties, AnnotationsList)
from GUI import VideoPlayerOpenCV


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







		### Custom widgets - "Video side"

		# Add VideoPlayer widget
		###self.videoPlayer = VideoPlayer.VideoPlayer()
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
		










		#self.videoPlayerControlBar.provaControlBar(123)
		#self.annotationsProperties.prova(12)
		self.videoPlayer.start()





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



	#def prova(doNotCareYouNeedThisArgumentToMakeFuncionWork, text):
	#	print("MainWindow -> " + text)
