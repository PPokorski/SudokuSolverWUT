import math
import random
from msvcrt import getch

class Sudoku:
	def __init__(self,number,colorsList=None):
		self.n:int = number	#stopien sudoku	Tablica sudoku jest n^n x n^n
		self.N:int = int(math.pow(self.n,2))
		self.colors:list
		if not isinstance(colorsList,list):
			self.colors = [0 for x in range(int(self.N*self.N))]
		else:
			self.colors = colorsList
		self.matrix:list = [0 for x in range(int(math.pow(len(self.colors),2)))]
		amountOfPoints:int = int(len(self.colors))
		for a in range(amountOfPoints):
			for x in range(amountOfPoints):
				if a!=x:
					if (a%self.N) == (x%self.N) or (a//self.N) == (x//self.N):
						self.matrix[a+x*amountOfPoints] = 1
					elif ((a//self.N)//self.n)== ((x//self.N)//self.n) and ((a%self.N)//self.n)==((x%self.N)//self.n):
						self.matrix[a+x*amountOfPoints] = 1
	def printColors(self):
		toPrint:str = " "
		unitWidth:int = 2+self.N//10
		bar:str = '-'*int(unitWidth*(self.N)+2*(self.n-1)-1)
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
		toPrint:str = " "
		matrixWidth:int = (self.N*self.N)
		for i in range(int(matrixWidth*matrixWidth)):
			if i%(matrixWidth) == 0:
				toPrint+='\n'
			toPrint+=str(int(self.matrix[i]))
		print(toPrint)	
	def getSaturation(self,point):
		neighbourColors = {0}
		amountOfPoints:int = int(len(self.colors))
		for i in range(amountOfPoints):
			if self.matrix[point+i*amountOfPoints] == 1:
				neighbourColors.add(self.colors[i])
		return neighbourColors
	def isUncolored(self):
		amountOfPoints:int = int(len(self.colors))
		for i in range(amountOfPoints):
			if self.colors[i] == 0:
				return True
		return False
	def colorGraph(self):
		if not self.isUncolored():
			return "The graph is solved"
		amountOfPoints:int = int(len(self.colors))
		saturationDictionary:dict = {}
		setOfAllColors:set = {x+1 for x in range(self.N)}
		setOfUncoloredPoints: set = set()
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
		amountOfPoints:int = int(len(self.colors))
		saturationDictionary:dict = {}
		setOfAllColors:set = {x+1 for x in range(self.N)}
		setOfUncoloredPoints: set = set()
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
		setOfAllColors:set = {x+1 for x in range(self.N)}
		amountOfPoints:int = int(len(self.colors))
		setOfUncoloredPoints: set = {x for x in range(amountOfPoints)}
		self.colors = [0 for x in range(int(self.N*self.N))]
		if toColor>amountOfPoints:
			toColor = amountOfPoints
		for n in range(toColor):
			newColor = random.sample(setOfAllColors,1)[0]
			newPoint = random.sample(setOfUncoloredPoints,1)[0]
			setOfUncoloredPoints.remove(newPoint)
			self.colors[newPoint] = newColor
	
data = int(input('please input sudoku base: '))
s = Sudoku(data)
s.printColors()
while True:
	print("ESC to exit, enter to solve, q to generate new one, everything else for step")
	key = ord(getch())
	print("pressed key: "+str(key),end="\t")
	if key == 27: #ESC
		print('Good Bye')
		break
	elif key == 13:	#solve
		print(s.colorGraph())
		s.printColors()
	elif key == 113:	#q
		data = int(input("Enter a number of solved points: "))
		s.generateRandomMaybeSolvable(data)
		s.printColors()
		print('Graph generated')
	else:
		print(s.colorGraphOneStep())
		s.printColors()