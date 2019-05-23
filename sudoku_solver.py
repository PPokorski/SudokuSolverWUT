import copy
import itertools

import networkx.classes
import networkx.algorithms

import matplotlib.pyplot

import sudoku


class SudokuSolver:
    def __init__(self, sudoku_state):

        if not isinstance(sudoku_state, sudoku.Sudoku):
            raise ValueError("Sudoku state must be an object of Sudoku class!")

        self.sudoku = copy.copy(sudoku_state)
        # The actual graph representing sudoku state
        self.sudoku_graph = networkx.Graph()
        # The action list containing decision made so far during coloring
        self.fifo_action_list = []
        # The dictionary mapping cells to colors
        self.graph_colors = {}
        # The dictionary mapping set of colours that can't be used for given cell
        # E.g. for each cell it contains colours used in adjacent cells.
        self.neighbouring_colors = {}
        # The dictionary mapping cells to minimum color that can be assigned to them.
        # It's used when stepping back along fifo_action_list to ensure that different decision path is taken
        self.min_graph_colors = {}
        # The last popped item from fifo_action_list. Used for resetting min_graph_colors.
        self.last_list_pop = ()

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
                            # For each pair of adjacent cells create an edge between them.
                            self.sudoku_graph.add_edge((x_1, y_1), (x_2, y_2))

                # For each cell, if it's not empty, make a new entry in self.graph_colors
                if self.sudoku.sudoku_board[x_1 - 1][y_1 - 1] != self.sudoku.sudoku_empty_cell:
                    self.graph_colors[(x_1, y_1)] = self.sudoku.sudoku_board[x_1 - 1][y_1 - 1]
                self.min_graph_colors[(x_1, y_1)] = 1

        # To each cell assign all the colors neighbouring with it.
        self.neighbouring_colors = {v: set() for v in self.sudoku_graph}
        for node, color in self.graph_colors.items():
            for v in self.sudoku_graph[node]:
                self.neighbouring_colors[v].add(color)

    def solve_sudoku_step(self):

        # Compute the maximum saturation and the set of nodes that
        # achieve that saturation. Choose among uncolored nodes.
        saturation = {v: len(c) for v, c in self.neighbouring_colors.items()
                      if v not in self.graph_colors}
        # Choose the node with the highest saturation.
        node = max(saturation, key=lambda v: saturation[v])

        # Set to keep track of colors of neighbours
        neighbour_colors = {self.graph_colors[v] for v in self.sudoku_graph[node] if v in self.graph_colors}
        # Find the first unused color.
        is_available_color = False
        for color in self.sudoku.sudoku_numbers:
            if (color not in neighbour_colors) and (color >= self.min_graph_colors[node]):
                is_available_color = True
                break

        # If any color is available then use it
        if is_available_color:
            # Assign the new color to the current node.
            self.graph_colors[node] = color
            self.fifo_action_list.append([node, color])
            for v in self.sudoku_graph[node]:
                self.neighbouring_colors[v].add(color)
        # If not, then go back one step.
        else:
            if len(self.fifo_action_list) == 0:
                return 'Sudoku unsolvable!'

            [previous_node, previous_color] = copy.copy(self.fifo_action_list.pop())
            # Delete the entry from graph_colors
            del self.graph_colors[previous_node]
            # Increase the minimum number that can be used for this node, so that we can choose another path
            # in next iteration
            self.min_graph_colors[previous_node] = previous_color + 1
            # If we popped before, then reset its min_graph_colors for that previous node.
            # The min_graph_colors was only valid at the time it was popped.
            if len(self.last_list_pop) != 0:
                self.min_graph_colors[self.last_list_pop] = 1

            self.last_list_pop = copy.copy(previous_node)

            # Check for each node adjacent to previous_node if it's adjacent to another node
            # with the same color as previous_node
            for v in self.sudoku_graph[previous_node]:
                neighbours = self.sudoku_graph[v]
                value_remains = False
                for neighbour in neighbours:
                    if neighbour in self.graph_colors.keys() and self.graph_colors[neighbour] == previous_color:
                        value_remains = True

                # If no, then it this node is no longer adjacent to color of previous_node.
                if not value_remains:
                    self.neighbouring_colors[v].remove(previous_color)

                    # Assign colors from graph_colors to the board.

    def solve_sudoku(self):

        while len(self.sudoku_graph) != len(self.graph_colors):
            self.solve_sudoku_step()


        for i in range(self.sudoku.sudoku_size):
            for j in range(self.sudoku.sudoku_size):
                self.sudoku.sudoku_board[i][j] = self.graph_colors[(i + 1, j + 1)]

        return 'Sudoku solved!'



[r, q_board, a_board] = sudoku.get_question_board_from_file('/home/pokor/PycharmProjects/SudokuSolverWUT/sudoku/easy_0.csv')


sudoku_game = sudoku.Sudoku(r, q_board, a_board)

sudoku_solver = SudokuSolver(sudoku_game)

print('Current board')
sudoku_solver.sudoku.print_board()

print(sudoku_solver.solve_sudoku())

print('Solved board')
sudoku_solver.sudoku.print_board()

matplotlib.pyplot.subplot(121)
pos_graph = networkx.spring_layout(sudoku_solver.sudoku_graph)
networkx.draw(sudoku_solver.sudoku_graph, pos=pos_graph)
networkx.draw_networkx_labels(sudoku_solver.sudoku_graph, pos=pos_graph)
# matplotlib.pyplot.show()
