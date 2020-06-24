from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QAbstractItemView

class AnnotationsTable(QWidget):

	### Table of created annotations ###

	def setupUi(self, MainWindow):

		self.mw = MainWindow

		### Table
		self.table = QTableWidget()
		self.table.setRowCount(0)
		self.table.setColumnCount(3)
		self.table.setHorizontalHeaderLabels(["Start", "End", "Type"])#, "ID"])
		
		header = self.table.horizontalHeader()  
		header.setSectionResizeMode(0, QHeaderView.Stretch)
		header.setSectionResizeMode(1, QHeaderView.Stretch)
		header.setSectionResizeMode(2, QHeaderView.Stretch)

		# When a cell is selected, all the row is automatically highlighted
		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

		# Disable text changes
		self.table.setEditTriggers(QTableWidget.NoEditTriggers)

		# Double click event
		self.table.itemDoubleClicked.connect(self.getSelectedAnnotation)

		# Sort items by column
		self.table.sortByColumn(0, Qt.AscendingOrder)


		### Widget container
		container = QVBoxLayout(self)
		container.addWidget(QLabel("Annotations"))
		container.addWidget(self.table)

		### COSA FA:
		# Tabella con 4 colonne: (sec) Start, (sec) End, (annotation) Type, (annotation) ID
		# Colonna ID nascosta
		# Ogni riga della tabella conterra' i 4 valori da mostrare dell'annotazione:
		#	- annotationSecondStart
		#	- annotationSecondEnd
		#	- annotationType
		#	- str(self) -> ovvero l'annotazione sotto forma di stringa
		# Al doppio click su un elemento, prendo il valore della quarta colonna (ID) 
		#	e la passo ad una funzione della MainWindow che si occupera'
		#	di identificare l'annotazione selezionata





	def getSelectedAnnotation(self):
		self.mw.showAnnotationSelected((self.table.selectedItems())[2].data(Qt.UserRole))

	def insertRows(self, listOfAnnotations):

		self.table.setSortingEnabled(False)
		
		for item in listOfAnnotations:
			tableItem = QTableWidgetItem()
			tableItem.setData(Qt.UserRole, str(item))
			tableItem.setData(Qt.DisplayRole, self.aliasAnnotationType(item))

			self.table.insertRow(self.table.rowCount())
			self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(str(item.annotationSecondStart)))
			self.table.setItem(self.table.rowCount()-1, 1, QTableWidgetItem(str(item.annotationSecondEnd)))
			self.table.setItem(self.table.rowCount()-1, 2, tableItem)

		self.table.setSortingEnabled(True)

	def insertRow(self, annotation):
		
		self.table.setSortingEnabled(False)

		tableItem = QTableWidgetItem()
		tableItem.setData(Qt.UserRole, str(annotation))
		tableItem.setData(Qt.DisplayRole, self.aliasAnnotationType(annotation))
		
		self.table.insertRow(self.table.rowCount())
		self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(str(annotation.annotationSecondStart)))
		self.table.setItem(self.table.rowCount()-1, 1, QTableWidgetItem(str(annotation.annotationSecondEnd)))
		self.table.setItem(self.table.rowCount()-1, 2, tableItem)

		self.table.setSortingEnabled(True)

	def updateRow(self, annotation):

		self.table.setSortingEnabled(False)

		# Search row to change
		for i in range(0, self.table.rowCount()):
			item = self.table.item(i, 2)
			
			if item.data(Qt.UserRole) == str(annotation):
				break

		self.table.setItem(item.row(), 0, QTableWidgetItem(str(annotation.annotationSecondStart)))
		self.table.setItem(item.row(), 1, QTableWidgetItem(str(annotation.annotationSecondEnd)))

		self.table.setSortingEnabled(True)

	def aliasAnnotationType(self, annotation):

		if annotation.annotationType == "QPlainTextEdit":
			return "Textbox"
		elif annotation.annotationType == "QWidget":
			return "Breakpoint"
		elif annotation.isArrow:
			return "Arrow"
		else:
			return "Line"


	'''

	def getSelectedAnnotation(self):
		print((self.table.selectedItems())[2].data(Qt.UserRole))
		print((self.table.selectedItems())[2].data(Qt.DisplayRole))
		self.mw.showAnnotationSelected((self.table.selectedItems())[2].text())

	def insertRows(self, listOfAnnotations):

		self.table.setSortingEnabled(False)
		
		for item in listOfAnnotations:


			self.table.insertRow(self.table.rowCount())
			self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(str(item.annotationSecondStart)))
			self.table.setItem(self.table.rowCount()-1, 1, QTableWidgetItem(str(item.annotationSecondEnd)))

			
			tableItem = QTableWidgetItem()
			tableItem.setData(Qt.UserRole, str(item))
			tableItem.setData(Qt.DisplayRole, str(item.annotationType))

			self.table.setItem(self.table.rowCount()-1, 2, tableItem)

			#self.table.setItem(self.table.rowCount()-1, 2, QTableWidgetItem(str(item.annotationType)))
			#self.table.setItem(self.table.rowCount()-1, 3, QTableWidgetItem(str(item)))

		self.table.setSortingEnabled(True)

	def insertRow(self, annotation):
		
		self.table.setSortingEnabled(False)
		
		self.table.insertRow(self.table.rowCount())
		self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(str(annotation.annotationSecondStart)))
		self.table.setItem(self.table.rowCount()-1, 1, QTableWidgetItem(str(annotation.annotationSecondEnd)))

		tableItem = QTableWidgetItem()
		tableItem.setData(Qt.UserRole, str(annotation))
		tableItem.setData(Qt.DisplayRole, str(annotation.annotationType))

		self.table.setItem(self.table.rowCount()-1, 2, tableItem)

		print(tableItem.data(Qt.UserRole))
		print(tableItem)
		print(self.table.item(self.table.rowCount()-1, 2))
		print(self.table.item(self.table.rowCount()-1, 2) is tableItem)
		print(self.table.item(self.table.rowCount()-1, 2) == tableItem)
		print((self.table.item(self.table.rowCount()-1, 2)).data(Qt.UserRole))
		print((self.table.item(self.table.rowCount()-1, 2)).data(Qt.DisplayRole))
		print((self.table.item(self.table.rowCount()-1, 0)).data(Qt.UserRole))
		print((self.table.item(self.table.rowCount()-1, 0)).data(Qt.DisplayRole))
		print((self.table.item(self.table.rowCount()-1, 1)).data(Qt.UserRole))
		print((self.table.item(self.table.rowCount()-1, 1)).data(Qt.DisplayRole))

		x = self.table.item(self.table.rowCount()-1, 2)
		print(x.data(Qt.UserRole))
		print(x.data(Qt.DisplayRole))

		#self.table.setItem(self.table.rowCount()-1, 2, QTableWidgetItem(str(item.annotationType)))
		#self.table.setItem(self.table.rowCount()-1, 3, QTableWidgetItem(str(item)))


		for i in range(0, self.table.rowCount()):
			for j in range(0, self.table.columnCount()):
				value = self.table.item(i, j)
				print(value.data(Qt.DisplayRole))
				print(value.data(Qt.UserRole))


		self.table.setSortingEnabled(True)

	def updateRow(self, annotation):

		self.table.setSortingEnabled(False)

		#self.table.items()

		#print(self.table.findItems(str(annotation), Qt.MatchFixedString))
		#print(self.table.findItems(str(annotation), Qt.MatchExactly))


		for i in range(0, self.table.rowCount()):
			for j in range(0, self.table.columnCount()):
				value = self.table.itemAt(i, j)
				print(value.data(Qt.DisplayRole))
				print(value.data(Qt.UserRole))


		itemRow = (self.table.findItems(str(annotation), Qt.MatchFixedString))[0].row()
		self.table.setItem(itemRow, 0, QTableWidgetItem(str(annotation.annotationSecondStart)))
		self.table.setItem(itemRow, 1, QTableWidgetItem(str(annotation.annotationSecondEnd)))
		tableItem = QTableWidgetItem()
		tableItem.setData(Qt.UserRole, str(annotation))
		tableItem.setData(Qt.DisplayRole, str(annotation.annotationType))

		self.table.setItem(self.table.rowCount()-1, 2, tableItem)
		#self.table.setItem(itemRow, 2, QTableWidgetItem(str(annotation.annotationType)))
		#self.table.setItem(itemRow, 3, QTableWidgetItem(str(annotation)))

		self.table.setSortingEnabled(True)

	'''