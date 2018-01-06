import copy	# dla operacji które wymagają kopiowania struktur
import math #dla operacji matematycznych
import random	# dla generowania losowych plansz i losowego wybierania
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

class Database:
	def __init__(self):
		self.EasyList3 = []
		self.fillEasy3(self.EasyList3)
	def getEasy(self,n):
		return random.choice(self.EasyList3)
	def fillEasy3(self,list):
		ListOfLists = []
		ListOfLists.append([9,0,1,0,0,2,7,0,8,0,4,0,8,9,0,0,1,0,8,7,0,5,0,3,0,0,9,5,6,7,0,0,0,0,0,0,0,0,9,0,0,0,8,0,0,0,0,0,0,0,0,1,7,2,7,0,0,6,0,8,0,2,3,0,3,0,0,2,9,0,5,0,2,0,4,3,0,0,6,0,1])
		file = open('sudokuDiagrams.txt','r')
		for line in file:
			newList = []
			for letter in line:
				if letter == '.':
					newList.append(0)
				if letter.isdigit():
					newList.append(int(letter))
			ListOfLists.append(copy.copy(newList))
		for l in ListOfLists:
			if len(l) == 81:
				list.append(Diagram(3,l))
			else:
				print("list {} is wrong!".format(l.__str__()))