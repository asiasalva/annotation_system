from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QFormLayout, QFrame


class AnnotationsList(QWidget):

	### "List view" for annotation types ###

	def setupUi(self, MainWindow):
		self.mw = MainWindow
		
		### Widgets simulating a list view
		self.formLayout = QFormLayout()
		self.frame = QFrame()
		self.scroll = QScrollArea()
		
		### Annotations type buttons:

		# Line button
		self.btnLine = QPushButton("Line")
		self.btnLine.setEnabled(True)
		self.btnLine.clicked.connect(lambda: self.sendCommand(0))

		# Arrow button
		self.btnArrow = QPushButton("Arrow")
		self.btnArrow.setEnabled(True)
		self.btnArrow.clicked.connect(lambda: self.sendCommand(1))

		# Textbox button
		self.btnTextbox = QPushButton("Textbox")
		self.btnTextbox.setEnabled(True)
		self.btnTextbox.clicked.connect(lambda: self.sendCommand(2))

		# Breakpoint button
		self.btnBreakpoint = QPushButton("Breakpoint")
		self.btnBreakpoint.setEnabled(True)
		self.btnBreakpoint.clicked.connect(lambda: self.sendCommand(3))

		# BlackBoard button
		self.btnBoard = QPushButton("BlackBoard: OFF")
		self.btnBoard.setEnabled(True)
		self.btnBoard.clicked.connect(lambda: self.sendCommand(4))

		# Drawing button
		self.btnDraw = QPushButton("Draws: OFF")
		self.btnDraw.setEnabled(True)
		self.btnDraw.clicked.connect(lambda: self.sendCommand(5))

		### Widget container
		self.formLayout.addRow(self.btnLine)
		self.formLayout.addRow(self.btnArrow)
		self.formLayout.addRow(self.btnTextbox)
		self.formLayout.addRow(self.btnBreakpoint)
		self.formLayout.addRow(self.btnBoard)
		self.formLayout.addRow(self.btnDraw)

		self.frame.setLayout(self.formLayout)
		self.scroll.setWidget(self.frame)
		self.scroll.setWidgetResizable(True)

		container = QVBoxLayout(self)
		container.addWidget(QLabel("Types"))
		container.addWidget(self.scroll)

	def sendCommand(self, command):
		self.mw.annotationsListCommand(command)

	def changeDrawButtonText(self, drawing):
		if drawing:
			self.btnDraw.setText("Drawing: ON")
		else:
			self.btnDraw.setText("Drawing: OFF")
	
	def changeBlackBoardButtonText(self, blackboard):
		if blackboard:
			self.btnBoard.setText("BlackBoard: ON")
		else:
			self.btnBoard.setText("BlackBoard: OFF")
