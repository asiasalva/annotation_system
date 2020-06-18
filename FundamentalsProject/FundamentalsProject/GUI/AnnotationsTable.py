from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLabel

class AnnotationsTable(QWidget):

	### Table of created annotations ###

	def setupUi(self, MainWindow):

		### Table
		self.table = QTableWidget()
		self.table.setRowCount(0)
		self.table.setColumnCount(3)
		self.table.setHorizontalHeaderLabels(("Frame", "Sec", "Type"))
		
		header = self.table.horizontalHeader()       
		header.setSectionResizeMode(0, QHeaderView.Stretch)
		header.setSectionResizeMode(1, QHeaderView.Stretch)
		header.setSectionResizeMode(2, QHeaderView.Stretch)



		### Widget container
		container = QVBoxLayout(self)
		container.addWidget(QLabel("Annotations"))
		container.addWidget(self.table)








		### EXAMPLE
		self.table.setRowCount(1)
		self.table.setItem(0,0, QTableWidgetItem("10"))
		self.table.setItem(0,1, QTableWidgetItem("00:01:00"))
		self.table.setItem(0,2, QTableWidgetItem("TextBox"))


		### TODO

		## Disable text changes
		##self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

		## Set items
		#self.table.setItem(0,0, QTableWidgetItem("1"))
		#self.table.setItem(0,1, QTableWidgetItem("2"))
		#self.table.setItem(1,0, QTableWidgetItem("9"))
		#self.table.setItem(1,2, QTableWidgetItem("4"))
		#self.table.setItem(2,0, QTableWidgetItem("ddddd"))
		#self.table.setItem(2,1, QTableWidgetItem("6"))
		#self.table.setItem(3,0, QTableWidgetItem("7"))
		#self.table.setItem(3,1, QTableWidgetItem("1"))
		#self.table.setItem(3,2, QTableWidgetItem("1"))

		## Sort items by column
		#self.table.sortByColumn(1, Qt.DescendingOrder)


		## Print all items
		#for row in range(self.table.rowCount()):
		#	for col in range(self.table.columnCount()):

		#		item = self.table.item(row, col)

		#		if(item is not None):
		#			print(str(self.table.item(row, col).text()))

		#			# Set text alignment
		#			(self.table.item(row, col)).setTextAlignment(Qt.AlignCenter)




		