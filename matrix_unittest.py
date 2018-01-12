import unittest
import matrix
import matrix_database

class TestMatrix(unittest.TestCase):
	def test_dummy(self):
		self.assertEqual(0,0)

def create_test(n,diagram,solution):
	def check_solution(self):
		sudoku = matrix.Sudoku(n)
		diagram_1 = matrix_database.Diagram(n,diagram)
		sudoku.setColorsFromDiagram(diagram_1)
		sudoku.colorGraphNew()
		resultDiagram = sudoku.getColorsAsDiagram()
		self.assertEqual(solution,resultDiagram.colors)		
	return check_solution
	
def stringToLine(str):
	list = []
	for c in str:
		if c == '.':
			list.append(0)
		elif c.isdigit():
			list.append(int(c))
		elif ord(c)>=ord('a'):
			list.append(ord(c) - ord('a') + 10)
	return list
	
if __name__ == '__main__':
	diagramList2 = []
	solutionList2 = []
	diagramList3 = []
	solutionList3 = []
	id = 0
	with open('sudoku_4x4_solution.csv','r') as file:
		file.readline()
		for line in file:
			lines = line.split(',')
			diagramList2 = stringToLine(lines[0])
			solutionList2 = stringToLine(lines[1])
			test_method = create_test(2,diagramList2,solutionList2)
			test_method.__name__ = "test_method_{0}_{1}".format('4x4',id)
			setattr(TestMatrix,test_method.__name__,test_method)
			id+=1
	id = 0
	with open('sudoku_9x9_solution.csv','r') as file:
		file.readline()
		for line in file:
			lines = line.split(',')
			diagramList3 = stringToLine(lines[0])
			solutionList3 = stringToLine(lines[1])
			test_method = create_test(3,diagramList3,solutionList3)
			test_method.__name__ = "test_method_{0}_{1}".format('9x9',id)
			setattr(TestMatrix,test_method.__name__,test_method)
			id+=1
	unittest.main()
