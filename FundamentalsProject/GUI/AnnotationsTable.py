import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QAbstractItemView
from PyQt5.QtGui import QKeyEvent


class AnnotationsTable(QWidget):

	### Table of created annotations ###

	def setupUi(self, MainWindow):

		self.mw = MainWindow

		### Table
		self.table = QTableWidget()
		self.table.setRowCount(0)
		self.table.setColumnCount(3)
		self.table.setHorizontalHeaderLabels(["Start", "End", "Type"])
		
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


	def getSelectedAnnotation(self):
		self.mw.showAnnotationSelected((self.table.selectedItems())[2].data(Qt.UserRole))

	def keyPressEvent(self, e: QKeyEvent):
		if e.key() == Qt.Key_Delete:
			self.mw.removeAnnotationFromTable((self.table.selectedItems())[2].data(Qt.UserRole))


	def insertRows(self, listOfAnnotations):
		self.table.setSortingEnabled(False)		
		for item in listOfAnnotations:
			tableItem = QTableWidgetItem()
			tableItem.setData(Qt.UserRole, str(item))
			tableItem.setData(Qt.DisplayRole, self.aliasAnnotationType(item))

			self.table.insertRow(self.table.rowCount())
			self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(self.convertTime(item.annotationSecondStart)))
			self.table.setItem(self.table.rowCount()-1, 1, QTableWidgetItem(self.convertTime(item.annotationSecondEnd)))
			self.table.setItem(self.table.rowCount()-1, 2, tableItem)

		self.table.setSortingEnabled(True)

	def insertRow(self, annotation):		
		self.table.setSortingEnabled(False)
		tableItem = QTableWidgetItem()
		tableItem.setData(Qt.UserRole, str(annotation))
		tableItem.setData(Qt.DisplayRole, self.aliasAnnotationType(annotation))
		self.table.insertRow(self.table.rowCount())
		self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(self.convertTime(annotation.annotationSecondStart)))
		self.table.setItem(self.table.rowCount()-1, 1, QTableWidgetItem(self.convertTime(annotation.annotationSecondEnd)))
		self.table.setItem(self.table.rowCount()-1, 2, tableItem)
		self.table.setSortingEnabled(True)

	def updateRow(self, annotation):
		self.table.setSortingEnabled(False)
		# Search row to change
		for i in range(0, self.table.rowCount()):
			item = self.table.item(i, 2)
			if item.data(Qt.UserRole) == str(annotation):
				break
		self.table.setItem(item.row(), 0, QTableWidgetItem(self.convertTime(annotation.annotationSecondStart)))
		self.table.setItem(item.row(), 1, QTableWidgetItem(self.convertTime(annotation.annotationSecondEnd)))
		self.table.setSortingEnabled(True)

	def removeRow(self, annotation):
		self.table.setSortingEnabled(False)
		# Search row to remove
		for i in range(0, self.table.rowCount()):
			item = self.table.item(i, 2)			
			if item.data(Qt.UserRole) == str(annotation):
				break
		self.table.removeRow(item.row())
		self.table.setSortingEnabled(True)


	def aliasAnnotationType(self, annotation):
		if annotation.annotationType == "QPlainTextEdit":
			return "Textbox"
		elif annotation.annotationType == "QWidget":
			return "Breakpoint"
		elif annotation.annotationType == "QLabel":
			return "Drawing"
		elif annotation.isArrow:
			return "Arrow"
		else:
			return "Line"


	def convertTime(self, seconds): 
		return time.strftime("%H:%M:%S", time.gmtime(seconds))