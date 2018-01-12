import copy	# dla operacji które wymagają kopiowania struktur
import math #dla operacji matematycznych
import random	# dla generowania losowych plansz i losowego wybierania
# Klasa opisująca diagram, za pomocą której możliwe jest przenoszenie diagramów w spójnym formacie
# n - baza diagramu
# colorsList - diagram w postaci listy do skopiowania
class Diagram:
	def __init__(self,n,colorsList=None):
		self.n = n
		self.N = int(math.pow(self.n,2))
		if isinstance(colorsList,Diagram):
			self.n = colorsList.n
			self.N = colorsList.N
			self.colors = copy.copy(colorsList.colors)
		elif isinstance(colorsList,list):
			if len(colorsList) == int(self.N*self.N):
				self.colors = copy.copy(colorsList)
			else:
				self.colors = [0 for x in range(int(self.N*self.N))]
		else:
			self.colors = [0 for x in range(int(self.N*self.N))]

# Klasa której zadaniem jest załadowanie testów z plików i udostępnianie ich.
class Database:
	# Konstruktor. Tworzy listy zadań sudoku, i wypełnia je danymi z plików
	# doLoad - jeżeli ustawione na False, Database nie będzie ładował danych z plików
	def __init__(self,doLoad = True):
		self.EasyList4 = []
		self.EasyList3 = []
		self.EasyList2 = []
		self.Test4 = []
		self.Test3 = []
		self.Test2 = []
		for x in range(4):
			self.Test4.append([])
			self.Test3.append([])
			self.Test2.append([])
		if doLoad:
			self.fillEasy3(self.EasyList3)
			self.fillEasy2(self.EasyList2)
			self.fillEasy(self.EasyList4,'sudoku_16_test_diagrams.txt',4)
			self.fillTest(self.Test4,'sudoku_16_test_diagrams.txt',4)
			self.fillTest(self.Test3,'sudoku_9_test_diagrams.csv',3)
			self.fillTest(self.Test2,'sudoku_4_test_diagrams.csv',2)
	# Udostępnia jedno losowe 'proste' zadanie sudoku
	# n - baza sudoku
	def getEasy(self,n):
		if n==2:
			return random.choice(self.EasyList2)
		elif n==3:
			return random.choice(self.EasyList3)
		elif n==4:
			return random.choice(self.EasyList4)
	# Udostępnia jedno testowe zadanie sudoku. Zwraca None jeżeli nie posiada opisanego zadania.
	# n - baza sudoku
	# difficulty - trudność zadania, 0 najprostrza, 3 najtrudniejsza
	# index - numer zadania w liście
	def getTest(self,n,difficulty,index):
		if n==2:
			if index < len(self.Test2[difficulty]):
				return self.Test2[difficulty][index]
		elif n == 3:
			if index < len(self.Test3[difficulty]):
				return self.Test3[difficulty][index]
		elif n == 4:
			if index < len(self.Test4[difficulty]):
				return self.Test4[difficulty][index]
		return None
	# Zwraca liczbę ilości zadań testowych dla danej bazy i stopnia trudności
	# n - baza sudoku
	# difficulty - trudność zadania
	def getAmountOfTests(self,n,difficulty):
		if n==2:
			return len(self.Test2[difficulty])
		elif n==3:
			return len(self.Test3[difficulty])
		elif n==4:
			return len(self.Test4[difficulty])
		return -1
	# Wypełnia listę z zadaniami o bazie 3
	# list - referencja na listę do wypełnienia
	def fillEasy3(self,list):
		ListOfLists = []
		ListOfLists.append([9,0,1,0,0,2,7,0,8,0,4,0,8,9,0,0,1,0,8,7,0,5,0,3,0,0,9,5,6,7,0,0,0,0,0,0,0,0,9,0,0,0,8,0,0,0,0,0,0,0,0,1,7,2,7,0,0,6,0,8,0,2,3,0,3,0,0,2,9,0,5,0,2,0,4,3,0,0,6,0,1])
		file = None
		try:
			file = open('sudokuDiagrams3.txt','r')
		except:
			print('couldn\'t open file \'sudokuDiagrams3.txt\' ')
			return
		for line in file:
			newList = []
			for letter in line:
				if letter == '.':
					newList.append(0)
				if letter.isdigit():
					newList.append(int(letter))
			ListOfLists.append(copy.copy(newList))
		file.close()
		for l in ListOfLists:
			if len(l) == 81:
				list.append(Diagram(3,l))
			else:
				print("list {} is wrong!".format(l.__str__()))			
	# Wypełnia listę z zadaniami o bazie 2
	# list - referencja na listę do wypełnienia
	def fillEasy2(self,list):
		ListOfLists = []
		file = None
		try:
			file = open('sudokuDiagrams2.txt','r')
		except:
			print('couldn\'t open file \'sudokuDiagrams2.txt\' ')
			return
		for line in file:
			newList = []
			for letter in line:
				if letter == '.':
					newList.append(0)
				if letter.isdigit():
					newList.append(int(letter))
			ListOfLists.append(copy.copy(newList))
		file.close()
		for l in ListOfLists:
			if len(l) == 16:
				list.append(Diagram(2,l))
			else:
				print("list {} is wrong!".format(l.__str__()))
	
	def fillEasy(self,list,fileName,n):
		ListOfLists = []
		file = None
		try:
			file = open(fileName,'r')
		except:
			print('couldn\'t open file \'{}\' '.format(fileName))
			return
		for line in file:
			newList = []
			for letter in line:
				if letter == '.':
					newList.append(0)
				elif letter.isdigit():
					newList.append(int(letter))
				elif ord(letter)>=ord('a'):
					newList.append(ord(letter) - ord('a') + 10)
			ListOfLists.append(copy.copy(newList))
		file.close()
		for l in ListOfLists:
			if len(l) == math.pow(n,4):
				list.append(Diagram(n,l))
			else:
				print("list {} is wrong!".format(l.__str__()))

	# Wypełnia listę z zadaniami testowymi o bazie base
	# listsToFill - referencja na listę do wypełnienia
	# fileName - nazwa pliku z którego mamy zebrać zadania
	# base - baza zadań sudoku
	def fillTest(self,listsToFill,fileName,base):
		file = None
		try:
			file = open(fileName,'r')
		except:
			print('couldn\'t open file \'{}\' '.format(fileName))
			return
		ListOfListsOfLists = []
		for i in range(4):
			ListOfListsOfLists.append([])
		for line in file:
			newList = []
			splitted = line.split(',')
			if splitted[0][0] == 'P':
				continue
			for letter in splitted[0]:
				if letter == '.':
					newList.append(0)
				elif letter.isdigit():
					newList.append(int(letter))
				elif ord(letter)>=ord('a'):
					newList.append(ord(letter) - ord('a') + 10)
			if len(splitted) > 11:
				if splitted[11] == 'Simple':
					ListOfListsOfLists[0].append(copy.copy(newList))
				elif splitted[11] == 'Easy':
					ListOfListsOfLists[1].append(copy.copy(newList))
				elif splitted[11] == 'Intermediate':
					ListOfListsOfLists[2].append(copy.copy(newList))
				elif splitted[11] == 'Expert':
					ListOfListsOfLists[3].append(copy.copy(newList))
			else:
				ListOfListsOfLists[0].append(copy.copy(newList))
		file.close()
		for x in range(4):
			ListOfLists = ListOfListsOfLists[x]
			for l in ListOfLists:
				if len(l) == math.pow(base,4):
					listsToFill[x].append(Diagram(base,l))
				else:
					print("list {} is wrong!".format(l.__str__()))			