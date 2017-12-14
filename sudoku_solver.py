import copy

import networkx
import matplotlib.pyplot

import sudoku


class SudokuSolver:
    def __init__(self, sudoku_state):

        if not isinstance(sudoku_state, sudoku.Sudoku):
            raise ValueError("Sudoku state must be an object of Sudoku class!")

        self.sudoku = copy.copy(sudoku_state)
        self.sudoku_graph = networkx.Graph()

        self.create_sudoku_graph_from_board()

    def create_sudoku_graph_from_board(self):
        rank = self.sudoku.sudoku_rank
        size = self.sudoku.sudoku_size
        for x_1 in range(1, size + 1):
            for y_1 in range(1, size + 1):
                for x_2 in range(1, size + 1):
                    for y_2 in range(1, size + 1):
                        if x_1 is x_2 or y_1 is y_2 or\
                                (((x_1 - 1) // rank is (x_2 - 1) // rank) and ((y_1 - 1) // rank is (y_2 - 1) // rank)):
                            self.sudoku_graph.add_edge((x_1, y_1), (x_2, y_2))


sudoku_board = [
    [4, 1, 1, 2],
    [2, 3, 1, 1],
    [3, 1, 2, 1],
    [2, 1, 1, 3]
]

sudoku_game = sudoku.Sudoku(2, sudoku_board)

sudoku_solver = SudokuSolver(sudoku_game)

sudoku_game.print_board()

matplotlib.pyplot.subplot(121)
pos_graph = networkx.spring_layout(sudoku_solver.sudoku_graph)
networkx.draw(sudoku_solver.sudoku_graph, pos=pos_graph)
networkx.draw_networkx_labels(sudoku_solver.sudoku_graph, pos=pos_graph)
matplotlib.pyplot.show()
