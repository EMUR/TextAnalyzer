from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QTextEdit, QLabel, QTableWidget,QTableWidgetItem, QHeaderView, QTabWidget
from PyQt5 import QtCore, QtGui
from typing import Any
import sys, re


MARGIN = 20 #Margin used for styling and positioning objects

# Main QT View class
class TextAnalyzer(QWidget):	
	wordsDictionary = {}
	textBox = charTable = wordTable = linesLabel = sentencesLabel = wordsLabel = None
	
	def __init__(self): 
		super().__init__()
		self.setupView()
		
	def setupView(self):
		self.setFixedSize(850, 550)
		self.move(300, 300)
		self.setWindowTitle('Text Analyzer')
		self.setupUI()
		self.show()

	def initLabel(self,title,posx,posy,sizex,sizey):
		 label = QLabel(self)
		 label.setText(title)
		 label.move(posx, posy)
		 label.resize(sizex,sizey)
		 return label
					
	def setupUI(self):		
		button = QPushButton('import text file', self)
		button.move(0,MARGIN)
		button.clicked.connect(lambda: self.openFile())
		
		self.linesLabel = self.initLabel("Lines: 0",button.pos().x() + MARGIN , button.pos().y() + MARGIN*2,button.width(),button.height())
		self.wordsLabel = self.initLabel("Words: 0",button.pos().x() + MARGIN , button.pos().y() + MARGIN*3,button.width(),button.height())
		self.sentencesLabel = self.initLabel("Sentences: 0",button.pos().x() + MARGIN , button.pos().y() + MARGIN*4,button.width(),button.height())
		
		self.textBox = QTextEdit(self)
		self.textBox.setAlignment(QtCore.Qt.AlignTop)
		self.textBox.resize(self.width() - button.width() * 3.8, self.height() - MARGIN*2)
		self.textBox.move(button.width() + MARGIN*1.5, MARGIN)
		self.textBox.setReadOnly(True)
		
		tabView = QTabWidget(self)
		tabView.move(self.textBox.pos().x() + self.textBox.width() + MARGIN,MARGIN)
		tableSizeX = self.width() - self.textBox.width() - button.width() - MARGIN*3
		tableSizeY = self.height() - MARGIN*6 
		charTab, self.charTable = self.createTabWithTable("Characters Frequancy Table:", ["Character","Occurrences"],tableSizeX,tableSizeY)
		wordTab, self.wordTable = self.createTabWithTable("Words Frequancy Table:", ["Word","Occurrences"],tableSizeX,tableSizeY)
		tabView.addTab(charTab, "Characters")
		tabView.addTab(wordTab,"Words")
		tabView.resize(tableSizeX, tableSizeY + MARGIN*4)
	
	def createTabWithTable(self, title, tableLabels, sizex, sizey):
		newTab = QWidget()	
		
		newTable = QTableWidget(newTab)
		newTable.setColumnCount(2)
		newTable.setHorizontalHeaderLabels(tableLabels)
		newTable.setSortingEnabled(True)
		
		header = newTable.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.Stretch)
		header.setSectionResizeMode(1, QHeaderView.Stretch)
		
		newTable.move(0, MARGIN*2)
		newTable.resize(sizex, sizey)
		
		label = QLabel(newTab)
		label.setText(title)
		label.move(0, MARGIN/2)
		
		return newTab, newTable

			
	def openFile(self):
		fileName, _ = QFileDialog.getOpenFileName((self),"Open text file to analyze", "","Text files (*.txt)")
		self.wordsDictionary = {}
		if fileName:
			with open(fileName, 'r') as f:
				lineStr = f.read()
				self.textBox.setText(lineStr)
				self.setupFreq(lineStr)
				
	def setupFreq(self, _str):
		dic = {}
		lines = 1
		sentencesCount = 0
		self.charTable.clearContents()
		self.wordTable.clearContents()
		self.charTable.setRowCount(0)
		self.wordTable.setRowCount(0)
		wordList = re.sub("[^\w !' !,]", " ",  _str).split()
		wordsList = re.sub("[^\w]", " ",  _str).split()

		for word in wordsList:
			upperWord = word.upper()
			if upperWord in self.wordsDictionary:
				val = self.wordsDictionary[upperWord] + 1
				self.wordsDictionary.update({upperWord:val})
			else:
				self.wordsDictionary.update({upperWord:1})
				
		for c in _str:
			if(c is '\n'): 
				lines = lines + 1
			if(c is '.'):
				sentencesCount = sentencesCount + 1
				continue
			if(c is not " "):
				cc = c.upper()
				if cc in dic:
					val = dic[cc] + 1
					dic.update({cc:val})
				else:
					dic.update({cc:1})
		self.linesLabel.setText("Lines: " + str(lines))
		self.wordsLabel.setText("Words: " + str(len(wordList)))
		self.sentencesLabel.setText("Sentences: " + str(sentencesCount))
		self.printFreq(dic)


	def printFreq(self, dic):
		r = 0
		self.charTable.setRowCount(len(dic))
		self.wordTable.setRowCount(len(self.wordsDictionary))
		for c in dic:
			self.charTable.setItem(r, 0, QTableWidgetItem(c))
			self.charTable.setItem(r, 1, QTableWidgetItem(str(dic[c])))
			r+=1
			
		r = 0
		for w in self.wordsDictionary:
			self.wordTable.setItem(r, 0, QTableWidgetItem(w))
			self.wordTable.setItem(r, 1, QTableWidgetItem(str(self.wordsDictionary[w])))
			r+=1
			
		self.charTable.sortByColumn( 1, QtCore.Qt.DescendingOrder)
		self.charTable.update()
		self.wordTable.sortByColumn( 1, QtCore.Qt.DescendingOrder)
		self.wordTable.update()

				
# Main Function
if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainWindow = TextAnalyzer()
	sys.exit(app.exec_())