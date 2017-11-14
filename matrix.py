import math #dla operacji matematycznych
import random	# dla generowania losowych plansz
from msvcrt import getch	#dla interface z użytkownikiem (nieużywane)
import copy	# dla operacji które wymagają kopiowania struktur
class Sudoku:
	def __init__(self,number,colorsList=None):
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
		print(toPrint)	
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
	def getLowestPossibleColorFromSaturationSet(self,sSet):
		min = 10
		for color in sSet:
			if min > color:
				min = color
		return min
	def colorGraph(self):
		if not self.isUncolored():
			return "The graph is solved"
		amountOfPoints = int(len(self.colors))
		saturationDictionary = {}
		setOfAllColors = {x+1 for x in range(self.N)}
		setOfUncoloredPoints = set()
		for i in range(amountOfPoints):
			saturationDictionary[i] = self.getSaturation(i)
			if self.colors[i] == 0:
				setOfUncoloredPoints.add(i)
		while self.isUncolored():
			max = 0
			maxPoint = 0
			for i in setOfUncoloredPoints:
				if len(saturationDictionary[i])> max:
					maxPoint = i
					max = len(saturationDictionary[i])
			allowedColors = setOfAllColors - saturationDictionary[maxPoint]
			if not allowedColors:
				return "Can't color the point:{0}({1},{2})".format(maxPoint,maxPoint%self.N,maxPoint//self.N)
			newColor = allowedColors.pop()
			self.colors[maxPoint] = newColor
			setOfUncoloredPoints.remove(maxPoint)
			for i in range(amountOfPoints):
				if self.matrix[i+maxPoint*amountOfPoints] == 1:
					saturationDictionary[i] = self.getSaturation(i)
		return "No errors"
	def colorGraphOneStep(self):
		if not self.isUncolored():
			return "The graph is solved"
		amountOfPoints = int(len(self.colors))
		saturationDictionary = {}
		setOfAllColors = {x+1 for x in range(self.N)}
		setOfUncoloredPoints = set()
		for i in range(amountOfPoints):
			saturationDictionary[i] = self.getSaturation(i)
			if self.colors[i] == 0:
				setOfUncoloredPoints.add(i)
		max = 0
		maxPoint = 0
		for i in setOfUncoloredPoints:
			if len(saturationDictionary[i])> max:
				maxPoint = i
				max = len(saturationDictionary[i])
		allowedColors = setOfAllColors - saturationDictionary[maxPoint]
		if not allowedColors:
			return "Can't color the point:{0}({1},{2})".format(maxPoint,maxPoint%self.N,maxPoint//self.N)
		newColor = allowedColors.pop()
		self.colors[maxPoint] = newColor
		return "No errors, colored point:{0}({1},{2}) to {3}".format(maxPoint,maxPoint%self.N,maxPoint//self.N,newColor)
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
			max = 0
			maxPoint = data[0]
			if maxPoint == -1:
				listOfPointsWithMaxSaturation:list = []
				for i in setOfUncoloredPoints:
					if len(saturationDictionary[i])> max:
						maxPoint = i
						max = len(saturationDictionary[i])
						listOfPointsWithMaxSaturation = []
						listOfPointsWithMaxSaturation.append(i)
					elif len(saturationDictionary[i])== max:
						listOfPointsWithMaxSaturation.append(i)
				lowestPossibleColor = 10
				for point in listOfPointsWithMaxSaturation:
					pointLowestColor = self.getLowestPossibleColorFromSaturationSet(saturationDictionary[point])
					if lowestPossibleColor > pointLowestColor:
						lowestPossibleColor = pointLowestColor
						maxPoint = point
			iteration+=1
			self.controlledPrint("========================= {}\ndata: ".format(iteration))
			self.controlledPrint(data,"")
			self.controlledPrint(" point:({0})({1},{2})".format(maxPoint,maxPoint%self.N,maxPoint//self.N))
			self.controlledPrint(fifoActionList)
			self.controlledPrint(setOfUncoloredPoints)
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
				for i in range(amountOfPoints):
					if self.matrix[i+data[0]*amountOfPoints] == 1:
						saturationDictionary[i] = self.getSaturation(i)
			else:	# jeśli dobranie nowego koloru byo możliwe
				newColor = allowedColors.pop()
				self.colors[maxPoint] = newColor
				self.controlledPrint("point removed from uncolored: {}".format(maxPoint))
				setOfUncoloredPoints.remove(maxPoint)
				for i in range(amountOfPoints):
					if self.matrix[i+maxPoint*amountOfPoints] == 1:
						saturationDictionary[i] = self.getSaturation(i)
				self.controlledPrint("newColor: {}".format(newColor))
				newTriedColors = copy.copy(data[1])
				newTriedColors.append(newColor)
				fifoActionList.append([maxPoint,newTriedColors])
				data = copy.copy(self.emptyData)
		return "No errors"
	def controlledPrint(self,toPrint,thisEnd="\n"):
		#print(toPrint,end = thisEnd)
		file = open('test.txt','a')
		file.write(toPrint.__str__()+thisEnd)
		file.close()
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
			lowestPossibleColor = 10
			for point in listOfPointsWithMaxSaturation:
				pointLowestColor = self.getLowestPossibleColorFromSaturationSet(saturationDictionary[point])
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

data = int(input('please input sudoku base: '))
s = Sudoku(data)
s.printColors()
file = open('test.txt','w')
file.close()
while True:
	print("1 to exit, 2 to solve, 3 to generate new one, 4 else for step")
	#key = ord(getch())
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
		file = open('test.txt','w')
		file.close()
		data = int(input("Enter a number of solved points: "))
		s.generateRandomMaybeSolvable(data)
		s.printColors()
		print('Graph generated')
	elif key == 4:
		print(s.colorGraphOneStepNew())
		s.printColors()
	else:
		print('unsupported integer')