import math #dla operacji matematycznych
import random	# dla generowania losowych plansz
import copy	# dla operacji które wymagają kopiowania struktur
import matrix_database
import sys
import time
		
class Sudoku:
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
	def printColors(self):
		print(self.stringColors())
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
	def printMatrixList(self):
		toPrint = " "
		matrixWidth = (self.N*self.N)
		for i in range(int(matrixWidth*matrixWidth)):
			if i%(matrixWidth) == 0:
				toPrint+='\n'
			toPrint+=str(int(self.matrix[i]))
		print(toPrint)	
	def getSaturation(self,point):
		neighbourColors = {0}
		amountOfPoints = int(len(self.colors))
		for i in range(amountOfPoints):
			if self.matrix[point+i*amountOfPoints] == 1:
				neighbourColors.add(self.colors[i])
		return neighbourColors
	def isUncolored(self):
		amountOfPoints = int(len(self.colors))
		for i in range(amountOfPoints):
			if self.colors[i] == 0:
				return True
		return False
	def generateRandomMaybeSolvable(self,toColor):
		self.globalFifoActionList = []
		setOfAllColors = {x+1 for x in range(self.N)}
		amountOfPoints = int(len(self.colors))
		setOfUncoloredPoints = {x for x in range(amountOfPoints)}
		self.colors = [0 for x in range(int(self.N*self.N))]
		if toColor>amountOfPoints:
			toColor = amountOfPoints
		for n in range(toColor):
			newColor = random.sample(setOfAllColors,1)[0]
			newPoint = random.sample(setOfUncoloredPoints,1)[0]
			setOfUncoloredPoints.remove(newPoint)
			self.colors[newPoint] = newColor			
	def generateRandomMaybeSolvable2(self,toColor):
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
	def createIndependentSet(self,n,listOfIndependentSets ):
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
	def setColorsFromDiagram(self,diagram):
		self.colors = copy.copy(diagram.colors)
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
	def controlledPrint(self,toPrint,thisEnd="\n"):
		pass
		#if(self.logToTestFile):
		#	file = open('log.txt','a')
		#	file.write(toPrint.__str__()+thisEnd)
		#	file.close()
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

def consoleInterface():
	database = matrix_database.Database()
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
			data = int(input("Enter 1 if you want to print test data to a file. 0 otherwise: "))
			if data == 1:
				s.logToTestFile = True
				print("test data will be printed in 'log.txt' file in your directory")
			elif data == 0:
				s.logToTestFile = False
				print("test data will not be saved")
			else:
				print("unknown input - settings unchanged")
		else:
			print('unsupported integer')

def test(base,numberOfTests):
	database = matrix_database.Database()
	s = Sudoku(base)
	file = open('log.txt','w')
	file.close()
	results = "Begining the test of {0}x{0} sudoku, {1} times\n\n".format(base*base,numberOfTests)
	startTime = time.process_time()
	if base == 3:
		for i in range(numberOfTests):
			s.setColorsFromDiagram(database.getEasy(s.n))
			results += "\n=====(test number({})) ".format(i)+ s.colorGraphNew()
			print('\r test {0} of {1}'.format(i+1,numberOfTests),end = '\r')
	else:
		for i in range(numberOfTests):
			s.generateRandomSolvable(base*base)
			results += "\n=====(test number({})) ".format(i)+ s.colorGraphNew()
			print('\r test {0} of {1}'.format(i+1,numberOfTests),end = '\r')
	endTime = time.process_time()
	results +="\n\n Time of all tests {0}s, average {1}s per test".format(endTime-startTime,(endTime-startTime)/numberOfTests)
	print()
	return results
helpMessage = 'in order to activate the test mode you need to type \'test\' followed by two integers, sudoku base and number of tests respectivly\n'
if len(sys.argv) > 3:
	if sys.argv[1] == 'test' and sys.argv[2].isdigit() and sys.argv[3].isdigit():
		base = int(sys.argv[2])
		numberOfTests = int(sys.argv[3])
		print('ready to test')
		file = open('testResult.txt','w')
		file.write(test(base,numberOfTests))
		file.close()
	else:
		print(helpMessage)
		consoleInterface()			
elif len(sys.argv) > 1:
	print(helpMessage)
else:
	consoleInterface()			