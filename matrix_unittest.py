import unittest
import matrix
import matrix_database

class TestMatrix(unittest.TestCase):
	pass

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
	
def create_battery_of_tests(n):
	diagramList = []
	solutionList = []
	id = 0
	with open('sudoku_{0}x{0}_solution.csv'.format(n*n),'r') as file:
		file.readline()
		for line in file:
			lines = line.split(',')
			diagramList = stringToLine(lines[0])
			solutionList = stringToLine(lines[1])
			test_method = create_test(n,diagramList,solutionList)
			test_method.__name__ = "test_method_{0}x{0}_{1}".format(n*n,id)
			setattr(TestMatrix,test_method.__name__,test_method)
			id+=1
if __name__ == '__main__':
	create_battery_of_tests(2)
	create_battery_of_tests(3)
	unittest.main()
