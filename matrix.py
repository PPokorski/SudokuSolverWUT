import math #dla operacji matematycznych
import random	# dla generowania losowych plansz
import copy	# dla operacji które wymagają kopiowania struktur
import matrix_database # dostęp do wygenerowanych wcześniej zadań sudoku
import sys	# dostęp do argumentów z linii poleceń
import time	# aby móc policzyć ilość czasu które zajmują testy
		
# Klasa odpowiadająca za generowanie i rozwiązywanie zadań sudoku
class Sudoku:
	# Kostruktor. Jako dane przyjmuje bazę sudoku. Baza sudoku równa się pierwiastkowi dłogości boku.
	# Konstruktor ten ma za zadanie wygenerować macierz na której będą zapisane numery na polach zadania sudoku. Wygenerowuje również macierz sąsiedztwa dla grafu którego pokolorowanie odpowiada rozwiązaniu zadania sudoku.
	# number - baza sudoku
	# colorsList - lista kolorów do skopiowania jeżeli jest taka potrzeba
	def __init__(self,number,colorsList=None):
		self.logToTestFile = True
		self.n = number	#stopien sudoku	Tablica sudoku jest n^n x n^n
		self.N = int(math.pow(self.n,2))
		self.colors = []
		if not isinstance(colorsList,list):
			self.colors = [0 for x in range(int(self.N*self.N))]
		else:
			self.colors = colorsList
		self.matrix = [0 for x in range(int(math.pow(len(self.colors),2)))]
		amountOfPoints = int(len(self.colors))
		for a in range(amountOfPoints):
			for x in range(amountOfPoints):
				if a!=x:
					if (a%self.N) == (x%self.N) or (a//self.N) == (x//self.N):
						self.matrix[a+x*amountOfPoints] = 1
					elif ((a//self.N)//self.n)== ((x//self.N)//self.n) and ((a%self.N)//self.n)==((x%self.N)//self.n):
						self.matrix[a+x*amountOfPoints] = 1
		self.globalFifoActionList = []
		self.emptyData = [-1,[]]
		self.globalData = copy.copy(self.emptyData)
	# Wypisuje dane o kolorach sudoku na konsoli
	def printColors(self):
		print(self.stringColors())
	# Wytwarza i zwraca string zawierający informacje o kolorach pól sudoku. Zero oznacza brak koloru.
	def stringColors(self):
		toPrint = " "
		unitWidth = 2+self.N//10
		bar = '-'*int(unitWidth*(self.N)+2*(self.n-1)-1)
		for i in range(int(self.N*self.N)):
			if i%self.N == 0:
				toPrint+='\n\t'
				if i!=0 and int(i/self.N)%self.n == 0:
					toPrint+=bar
					toPrint+='\n\t'
			elif i%self.n == 0:
				toPrint+='| '
			toPrint+="{0: <{1}}".format(int(self.colors[i]),unitWidth)
		return toPrint
	# Wytwarza i zwraca string zawierający informacje o nasyceniu pól sudoku.
	# satrationDictionary - słownik z informacją o nasyceniu każdego pola
	def stringSaturation(self,saturationDictionary):
		toPrint = " "
		unitWidth = 2+self.N//10
		bar = '-'*int(unitWidth*(self.N)+2*(self.n-1)-1)
		for i in range(int(self.N*self.N)):
			if i%self.N == 0:
				toPrint+='\n\t'
				if i!=0 and int(i/self.N)%self.n == 0:
					toPrint+=bar
					toPrint+='\n\t'
			elif i%self.n == 0:
				toPrint+='| '
			numberToPrint = len(saturationDictionary[i])
			toPrint+="{0: <{1}}".format(int(numberToPrint),unitWidth)
		return toPrint	
	# Wypisuje do konsoli macierz sąsiedztwa grafu.
	def printMatrixList(self):
		toPrint = " "
		matrixWidth = (self.N*self.N)
		for i in range(int(matrixWidth*matrixWidth)):
			if i%(matrixWidth) == 0:
				toPrint+='\n'
			toPrint+=str(int(self.matrix[i]))
		print(toPrint)	
	# Oblicza i zwraca nasycenie danego pola point.
	# point - pole którego nasycenie jest zwracane
	def getSaturation(self,point):
		neighbourColors = {0}
		amountOfPoints = int(len(self.colors))
		for i in range(amountOfPoints):
			if self.matrix[point+i*amountOfPoints] == 1:
				neighbourColors.add(self.colors[i])
		return neighbourColors
	# Sprawdza, czy zadanie sudoku zostało rozwiązane czy nie. Zwraca odpowiednią wartość boolean w obu przypadkach.
	def isUncolored(self):
		amountOfPoints = int(len(self.colors))
		for i in range(amountOfPoints):
			if self.colors[i] == 0:
				return True
		return False
	# Prosty generator zadań sudoku z 'toColor' zamalowanymi polami. Zadanie może nie być możliwe do rozwiązania. 
	# toColor - ilość pól do zamalowania
	def generateRandomMaybeSolvable(self,toColor):
		self.globalFifoActionList = []
		setOfAllColors = {x+1 for x in range(self.N)}
		amountOfPoints = int(len(self.colors))
		setOfUncoloredPoints = {x for x in range(amountOfPoints)}
		self.colors = [0 for x in range(int(self.N*self.N))]
		if toColor>amountOfPoints:
			toColor = amountOfPoints
		for n in range(toColor):
			t = True
			while t:
				notAllowedColors = set()
				newPoint = random.sample(setOfUncoloredPoints,1)[0]
				for i in range(amountOfPoints):
					if self.matrix[newPoint+i*amountOfPoints] == 1:
						notAllowedColors.add(self.colors[i]) 
				avaliableColors = setOfAllColors - notAllowedColors
				if len(avaliableColors) == 0:
					t = True
				else:
					t = False
					newColor = random.sample(avaliableColors,1)[0]
					setOfUncoloredPoints.remove(newPoint)
					self.colors[newPoint] = newColor			
	# Skomplikowany generator zadań sudoku, z 'toColor' zamalowanymi polami. Zadanie jest pewne do rozwiązania, jako że wytwarzane zostaje całe sudoku, którego pola potem zostają czyszczone. Generacja zadań dla sudoku o bazie większej niż 2 zajmuje zauważalną ilość czasu.
	# toColor - ilość pól do zamalowania
	def generateRandomSolvable(self,toColor):
		self.globalFifoActionList = []
		setOfAllColors = {x+1 for x in range(self.N)}
		self.colors = [0 for x in range(int(self.N*self.N))]
		amountOfPoints = int(len(self.colors))
		
		listOfIndependentSets = []
		
		newISet = None
		self.controlledPrint('*New color')
		while newISet==None:
			newISet = self.createIndependentSet(1,listOfIndependentSets)
			self.controlledPrint('++generating new set')
		listOfIndependentSets.append(copy.copy(newISet))
		self.controlledPrint('listOfIndependentSets:{}'.format(listOfIndependentSets))
		for n in range(1,len(setOfAllColors)):
			newISet = self.createMoreSets(n+1,listOfIndependentSets)
			if newISet is None:
				self.controlledPrint ("Unable to find next independent set")
			else:
				listOfIndependentSets.append(copy.copy(newISet))
		for s in listOfIndependentSets:
			self.controlledPrint(s)
			
		setOfColoredPoints = set()
		maxToColor = 0
		for s in listOfIndependentSets:
			maxToColor+=len(s)
		if maxToColor < toColor:
			toColor = maxToColor
		setOfAvaliableColors = {x+1 for x in range(len(listOfIndependentSets))}
		for n in range(toColor):
			newColor = random.sample(setOfAvaliableColors,1)[0]
			newPoint = random.sample(listOfIndependentSets[newColor-1],1)[0]
			setOfColoredPoints.add(newPoint)
			listOfIndependentSets[newColor-1].remove(newPoint)
			if len(listOfIndependentSets[newColor-1]) == 0:
				setOfAvaliableColors.remove(newColor)	
			self.colors[newPoint] = newColor
	# Tworzy losowy maksymalny zbiór niezależny. Nie ma pewności utworzenia zbioru, jeżeli inne punkty zostały wyłączone do innych zbiorów niezależnych oryginalnego grafu którego pokolorowanie rozwiązuje zadanie sudoku. n jest liczbą iteracji, listOfIndependentSets jest listą dotychczasowo znalezionych zbiorów niezależnych.
	# n - numer iteracji operacji.
	# listOfIndependentSets - lista z wcześniej znalezionymi zbiorami niezależnymi.
	def createIndependentSet(self,n,listOfIndependentSets):
		newISet = set()
		setOfTakenPoints = set()
		setOfAllColors = {x+1 for x in range(self.N)}
		amountOfPoints = int(len(self.colors))
		for s in listOfIndependentSets:
			setOfTakenPoints |=s
		setOfUntakenPoints = {x for x in range(amountOfPoints)} - setOfTakenPoints
		
		while len(newISet)<self.N:
			setOfPossiblePoints = setOfUntakenPoints - newISet
			setOfConfirmedPoints = set()
			newPoint = -1
			if len(newISet) != 0:
				for point in setOfPossiblePoints:
					pointIsGood = True
					for setPoint in newISet:
						if self.matrix[point+setPoint*amountOfPoints] == 1:
							pointIsGood = False
							break
					if pointIsGood:
						setOfConfirmedPoints.add(point)
						self.controlledPrint('Point Added {}'.format(point))
			else:
				setOfConfirmedPoints = setOfPossiblePoints
			if len(setOfConfirmedPoints)!=0:
				newPoint = random.sample(setOfConfirmedPoints,1)[0]
				newISet.add(newPoint)
			else:
				return None
			self.controlledPrint("n:{0} newISet:{1} newPoint:{2}  setOfConfirmedPoints:{3}, list of Independent Sets:{4}, setOfUntakenPoints:{5}".format(n,newISet.__str__(),newPoint,setOfConfirmedPoints.__str__(),listOfIndependentSets.__str__(),setOfUntakenPoints.__str__()))
		return newISet
	# Tworzy maksymalny zbiór niezależny. Ma pewność utworzenia zbioru, jednakże z powodu braku elementu losowego zbiory są te zawsze takie same dla takiego samego listOfIndependentSets. n jest liczbą iteracji, listOfIndependentSets jest listą dotychczasowo znalezionych zbiorów niezależnych.
	# n - numer iteracji operacji.
	# listOfIndependentSets - lista z wcześniej znalezionymi zbiorami niezależnymi.
	def createMoreSets(self,n,listOfIndependentSets):
		setOfTakenPoints = set()
		setOfAllColors = {x+1 for x in range(self.N)}
		amountOfPoints = int(len(self.colors))
		for s in listOfIndependentSets:
			setOfTakenPoints |=s
		setOfUntakenPoints = {x for x in range(amountOfPoints)} - setOfTakenPoints
		listOfUntakenPoints = list(setOfUntakenPoints)
		for index in range(0, len(listOfUntakenPoints)):
			newISet = set()
			newPoint = listOfUntakenPoints[index]
			newISet.add(newPoint)
			for i in range(0,len(setOfUntakenPoints)):
				for x in range(i,len(setOfUntakenPoints)):
					isOK = True	
					consideredPoint = listOfUntakenPoints[x]
					if newPoint == consideredPoint:
						isOK = False
					else:
						for setPoint in newISet:
							if self.matrix[consideredPoint+setPoint*amountOfPoints] == 1:
								isOK = False
					if isOK:
						newISet.add(consideredPoint)
						self.controlledPrint("n:{0} newISet:{1} newPoint:{2}, listOfUntakenPoints:{3}, index:{4}, i:{5}".format(n,newISet.__str__(),consideredPoint,listOfUntakenPoints.__str__(),index,i))
				if len(newISet) == self.N:
					return newISet
				else:
					newISet = set()
					newPoint = listOfUntakenPoints[index]
					newISet.add(newPoint)
		return None	
	# Ustawia obecne rozwiązanie na podany diagram diagram.
	# diagram - diagram na który ustawiamy
	def setColorsFromDiagram(self,diagram):
		self.colors = copy.copy(diagram.colors)
	# Rozwiązuje obecne zadanie sudoku. Jeżeli nie jest w stanie go rozwiązać, pozostawia zadanie nienaruszone, i zwraca odpowiedni komunikat.
	def colorGraphNew(self):
		if not self.isUncolored():
			return "The graph is solved"
		amountOfPoints = int(len(self.colors))
		saturationDictionary = {}
		setOfAllColors = {x+1 for x in range(self.N)}
		setOfUncoloredPoints = set()
		fifoActionList = self.globalFifoActionList
		data = copy.copy(self.emptyData)
		for i in range(amountOfPoints):
			if self.colors[i] == 0:
				setOfUncoloredPoints.add(i)	
				saturationDictionary[i] = self.getSaturation(i)
			else:
				saturationDictionary[i] = {0}				
		iteration = 0
		while self.isUncolored():
			iteration+=1
			self.controlledPrint("========================= {}\ndata: \n choosing the point to color\n[avaliable colors of compared point]\n (picked point) min color >? min color(compared point)".format(iteration))
			max = 0
			maxPoint = data[0]
			for i in range(amountOfPoints):
				if self.colors[i] == 0:
					setOfUncoloredPoints.add(i)	
					saturationDictionary[i] = self.getSaturation(i)
				else:
					saturationDictionary[i] = {0}	
			if maxPoint == -1:
				listOfPointsWithMaxSaturation = []
				for i in setOfUncoloredPoints:
					if len(saturationDictionary[i])> max:
						maxPoint = i
						max = len(saturationDictionary[i])
						listOfPointsWithMaxSaturation = []
						listOfPointsWithMaxSaturation.append(i)
					elif len(saturationDictionary[i])== max:
						listOfPointsWithMaxSaturation.append(i)
				lowestPossibleColor = self.N+1
				self.controlledPrint('list of points with max saturation {}'.format(listOfPointsWithMaxSaturation))
				for point in listOfPointsWithMaxSaturation:
					pointLowestColor = min((setOfAllColors - saturationDictionary[point])|{self.N+1})
					self.controlledPrint((setOfAllColors - saturationDictionary[point])|{self.N+1})
					self.controlledPrint("({0}){1} >? {2}({3})".format(maxPoint,lowestPossibleColor,pointLowestColor,point))
					if lowestPossibleColor > pointLowestColor:
						lowestPossibleColor = pointLowestColor
						maxPoint = point
						self.controlledPrint("new picked point = {}".format(maxPoint))
			self.controlledPrint(data,"")
			self.controlledPrint(" point:({0})({1},{2})".format(maxPoint,maxPoint%self.N,maxPoint//self.N))
			self.controlledPrint(fifoActionList)
			self.controlledPrint(setOfUncoloredPoints)
			self.controlledPrint("color table:"+self.stringColors())
			self.controlledPrint("saturation table:"+self.stringSaturation(saturationDictionary))
			triedColors = set(data[1])
			allowedColors = setOfAllColors - saturationDictionary[maxPoint]
			allowedColors = allowedColors - triedColors
			if not allowedColors:	# jeśli nie możemy znaleźć koloru, cofamy się
				self.controlledPrint('allowedColors is empty')
				if not fifoActionList:	# jeżeli cofnięcie się jest niemożliwe, to konczymy
					return "Can't color the point:{0}({1},{2})".format(maxPoint,maxPoint%self.N,maxPoint//self.N)	
				data = copy.copy(fifoActionList.pop())
				setOfUncoloredPoints.add(data[0])
				self.colors[data[0]] = 0
				for i in setOfUncoloredPoints:
					if self.matrix[i+data[0]*amountOfPoints] == 1:
						saturationDictionary[i] = self.getSaturation(i)
			else:	# jeśli dobranie nowego koloru byo możliwe
				newColor = allowedColors.pop()
				self.colors[maxPoint] = newColor
				self.controlledPrint("point removed from uncolored: {}".format(maxPoint))
				setOfUncoloredPoints.remove(maxPoint)
				for i in setOfUncoloredPoints:
					if self.matrix[i+maxPoint*amountOfPoints] == 1:
						saturationDictionary[i] = self.getSaturation(i)
				saturationDictionary[maxPoint] = {0}
				self.controlledPrint("newColor: {}".format(newColor))
				newTriedColors = copy.copy(data[1])
				newTriedColors.append(newColor)
				fifoActionList.append([maxPoint,newTriedColors])
				data = copy.copy(self.emptyData)
		return "No errors"
	# Wypisuje dane dotyczące działania programu do loga. Używana podczas debugowania. Ponieważ otwieranie i zamykanie plików są kosztownymi czasowo operacjami, funkcja ta została wyłączona.
	# toPrint - string do zapisania
	# thisEnd - ostatni znak
	def controlledPrint(self,toPrint,thisEnd="\n"):
		pass
		#if(self.logToTestFile):
		#	file = open('log.txt','a')
		#	file.write(toPrint.__str__()+thisEnd)
		#	file.close()
	# Wykonuje jeden krok rozwiązywania zadania sudoku. Jeżeli nie jest w stanie go rozwiązać, pozostawia zadanie nienaruszone, i zwraca odpowiedni komunikat.
	def colorGraphOneStepNew(self):
		if not self.isUncolored():
			return "The graph is solved"
		data = self.globalData
		amountOfPoints = int(len(self.colors))
		saturationDictionary = {}
		setOfAllColors = {x+1 for x in range(self.N)}
		setOfUncoloredPoints = set()
		for i in range(amountOfPoints):
			if self.colors[i] == 0:
				setOfUncoloredPoints.add(i)	
				saturationDictionary[i] = self.getSaturation(i)
			else:
				saturationDictionary[i] = {0}				
		max = 0
		maxPoint = data[0]
		if maxPoint == -1:
			listOfPointsWithMaxSaturation = []
			for i in setOfUncoloredPoints:
				if len(saturationDictionary[i])> max:
					maxPoint = i
					max = len(saturationDictionary[i])
					listOfPointsWithMaxSaturation = []
					listOfPointsWithMaxSaturation.append(i)
				elif len(saturationDictionary[i])== max:
					listOfPointsWithMaxSaturation.append(i)
			lowestPossibleColor = self.N+1
			for point in listOfPointsWithMaxSaturation:
				pointLowestColor = min((setOfAllColors - saturationDictionary[point])|{self.N+1})
				if lowestPossibleColor > pointLowestColor:
					lowestPossibleColor = pointLowestColor
					maxPoint = point
		triedColors = set(data[1])
		allowedColors = setOfAllColors - saturationDictionary[maxPoint]
		allowedColors = allowedColors - triedColors
		if not allowedColors:
			if not self.globalFifoActionList:	# jeżeli cofnięcie się jest niemożliwe, to konczymy
				return "Can't color the point:{0}({1},{2}). This sudoku is unsolvable.".format(maxPoint,maxPoint%self.N,maxPoint//self.N)	
			data = copy.copy(self.globalFifoActionList.pop())
			self.colors[data[0]] = 0
			self.globalData = data
			return "Couldn't find a color for point: {0}. Recoloring point: {1} in next step.".format(maxPoint,data[0])
		else:
			newColor = allowedColors.pop()
			self.colors[maxPoint] = newColor
			
			newTriedColors = copy.copy(data[1])
			newTriedColors.append(newColor)
			self.globalFifoActionList.append([maxPoint,newTriedColors])
			self.globalData = copy.copy(self.emptyData)
				
			return "No errors, colored point:{0}({1},{2}) to {3}".format(maxPoint,maxPoint%self.N,maxPoint//self.N,newColor)
	# Zwraca obecny stan zadania sudoku jako string znaków.
	def getColorsAsTemplate(self):
		toReturn = ""
		for c in self.colors:
			if c == 0:
				toReturn+='.'
			else:
				if c > 9:
					toReturn+=chr(ord('a')+c-10)
				else:
					toReturn+=str(c)
		return toReturn
	# Zwraca obecny stan zadania sudoku jako diagram
	def getColorsAsDiagram(self):
		return matrix_database.Diagram(self.n,self.colors)
# Funkcja kontrolująca interface użytkownika
def consoleInterface():
	print('loading tests')
	database = matrix_database.Database()
	print('loading complete')
	data = int(input('please input sudoku base: '))
	s = Sudoku(data)
	s.printColors()
	file = open('log.txt','w')
	file.close()
	while True:
		print("1 to exit, 2 to solve, 3 for new diagram, 4 else for step, 5 for settings")
		key = input('type number of your choice: ')
		try:
			key = int(key)
		except ValueError:
			print("Please enter an integer")
			continue
		print("pressed key: "+str(key),end="\t")
		if key == 1:
			print('Good Bye')
			break
		elif key == 2:
			print(s.colorGraphNew())
			s.printColors()
		elif key == 3:
			file = open('log.txt','w')
			file.close()
			data = int(input("1 to retry, 2 to generate, 3 for Database Easy,\ntype number of your choice: "))
			if data == 1:
				print("retry")
			elif data == 2:
				data = int(input("Enter a number of solved points: "))
				s.generateRandomSolvable(data)
				s.printColors()
				print('Graph generated')
			elif data == 3:
				s.setColorsFromDiagram(database.getEasy(s.n))
				s.printColors()
				print('Graph set')
		elif key == 4:
			print(s.colorGraphOneStepNew())
			s.printColors()
		elif key == 5:
			data = int(input("Enter 1 to retry. Enter 2 if you want to print test data to a file, 3 otherwise. Enter 4 if you want to generate sudoku diagrams: "))
			if data == 1:
				print("retry")
			elif data == 2:
				s.logToTestFile = True
				print("test data will be printed in 'log.txt' file in your directory")
			elif data == 3:
				s.logToTestFile = False
				print("test data will not be saved")
			elif data == 4:
				print("specify parameters:")
				base = 0
				hints = 0
				amount = 0
				try:
					base = input('type base: ')
					base = int(base)
					hints = input('type amount of hints: ')
					hints = int(hints)
					amount = input('type amount of tests to make: ')
					amount = int(amount)
				except ValueError:
					print("Unable to proceed, because integers were not inputted")
				else:
					print('result will be stored in {0}x{0}sudokus{1}({2}).txt file'.format(base*base,hints,amount))
					print('preparing to create Puzzles')
					createPuzzles(base,hints,amount)
			elif data == 5:
				s.setColorsFromDiagram(matrix_database.Diagram(3,[0,0,0,0,0,0,2,0,0,8,6,0,1,0,0,0,0,4,0,0,0,0,0,0,3,9,6,0,0,0,3,0,4,0,0,0,0,0,9,6,2,1,0,0,0,4,0,0,8,9,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,5,0,4,0,0,0,8,3,9]))
			else:
				print("unknown input - settings unchanged")
		else:
			print('unsupported integer')

# Funkcja przeprowadzająca testy. base - baza sudoku, numberOfTests - ilość testów. Testy zostają przeprowadzone, a dane o czasie przeprowadzania testów zostają zwrócone.
# base - baza sudoku
# numberOfTests - jeżeli testy nie zostały wczytane z pliku, program wygeneruje testy w podanej liczbie
def test(base,numberOfTests):
	print('loading tests')
	database = matrix_database.Database()
	print('loading complete')
	s = Sudoku(base)
	file = open('log.txt','w')
	file.close()
	results = 'diagram number,solving result,difficulty,time\n'
	timeResults = ""
	if base == 3 or base == 2 or base == 4:
		for dif in range(4):
			amountOfTests = database.getAmountOfTests(base,dif)
			timeSum = 0
			for i in range(amountOfTests):
				diagram = database.getTest(base,dif,i)
				#startTime = time.process_time()
				startTime = time.perf_counter()
				if diagram is not None:
					s.setColorsFromDiagram(database.getTest(base,dif,i))
					result = s.colorGraphNew()
				#endTime = time.process_time()
				endTime = time.perf_counter()
				timeOfTest = endTime-startTime
				results += "{0},{1},{2},{3}\n".format(i,result,dif,timeOfTest)
				timeSum+=timeOfTest
				print('\r test {0} of {1} | difficulty {2}     '.format(i+1,amountOfTests,dif),end = '\r')
			if amountOfTests != 0:
				timeResults +="\n Time of all tests {0}s, average {1}s per test, difficulty {2}".format(timeSum,(timeSum)/amountOfTests,dif)
	else:
		startTime = time.process_time()
		for i in range(numberOfTests):
			s.generateRandomSolvable(base*base)
			results += "\n=====(test number({})) ".format(i)+ s.colorGraphNew()
			print('\r test {0} of {1}     '.format(i+1,numberOfTests),end = '\r')
		endTime = time.process_time()
		if numberOfTests!=0:
			timeResults +="\n\n Time of all tests {0}s, average {1}s per test".format(endTime-startTime,(endTime-startTime)/numberOfTests)
	print()
	return results

# Funkcja decydująca o tym, czy uruchomić konsolę użytkownika, czy przeprowadzać testy na podstawie danych z konsoli.
def start():
	helpMessage = 'in order to activate the test mode you need to type \'test\' followed by two integers, sudoku base and number of tests respectivly\n'
	if len(sys.argv) > 2:
		if sys.argv[1] == 'test' and sys.argv[2].isdigit():
			base = int(sys.argv[2])
			numberOfTests = 0
			if len(sys.argv) > 3:
				numberOfTests = int(sys.argv[3])
			print('ready to test')
			file = open('test_Result.csv','w')
			file.write(test(base,numberOfTests))
			file.close()
		else:
			print(helpMessage)
			consoleInterface()			
	elif len(sys.argv) > 1:
		print(helpMessage)
	else:
		consoleInterface()			

# Wytwarza zadania sudoku o bazie base, ilości podpowiedzi hints. Zadań jest amount. Zapisywane są one w pliku 'NxNsudokusA(B).txt', gdzie N jest bokiem zadania sudoku, A jest ilością podpowiedzi, a B jest ilością zadań.
# base - baza sudoku
# hints - ilość podpowiedzi w zadaniach
# amount - ilość zadań		
def createPuzzles(base,hints,amount):
	database = matrix_database.Database(False)
	s = Sudoku(base)
	file = open('log.txt','w')
	file.close()
	templatesSet = set()
	for i in range(amount):
		print('\r test {0} of {1}'.format(i+1,amount),end = '\r')
		s.generateRandomSolvable(hints)
		newTemplate = s.getColorsAsTemplate()
		if len(newTemplate) == math.pow(base,4):
			templatesSet.add(newTemplate)
	file  = open('{0}x{0}sudokus{1}({2}).txt'.format(base*base,hints,amount),'w')
	for t in templatesSet:
		file.write(t+'\n')
	file.close()
	
if __name__ == '__main__':
    start()
		



		
	
