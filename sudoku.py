
class Sudoku:
    def __init__(self, rank, initial_board):
        # What is the base rank of sudoku.
        # Size of the board is rank * rank
        self.sudoku_rank = rank
        # Size of the sudoku board, number of cells in rows and columns
        self.sudoku_size = rank ** 2
        # Actual sudoku board
        self.sudoku_board = initial_board
        # Numbers that can go into sudoku board
        self.sudoku_numbers = [i + 1 for i in range(self.sudoku_size)]
        # Value of the empty (not filled yet) cell
        self.sudoku_empty_cell = None

        self.check_initial_board_validity(rank, initial_board)

    def check_initial_board_validity(self, rank, initial_board):
        if not isinstance(initial_board, list):
            raise ValueError("The initial_board should be a list of lists!")

        size = rank**2
        if size != len(initial_board):
            raise ValueError("initial_board size is {0} while sudoku size is {1}. They should be equal!".format(
                len(initial_board), size
            ))

        for i in range(size):
            if not isinstance(initial_board[i], list):
                raise ValueError("initial_board[{0}] is not a list!".format(i))

            if size != len(initial_board[i]):
                raise ValueError("initial_board[{0}] size is {1} while sudoku size is {2}".format(
                    i, len(initial_board[i]), size
                ))

            for j in range(size):
                if initial_board[i][j] not in self.sudoku_numbers:
                    if initial_board[i][j] is not self.sudoku_empty_cell:
                        raise ValueError("initial_board should only contain integers from 1 to {0} or {1} for empty cell".format(
                            size, self.sudoku_empty_cell
                        ))

    def is_solved(self):
        return not any(self.sudoku_empty_cell in row for row in self.sudoku_board)

    def print_board(self):
        for i in range(self.sudoku_size):
            for j in range(self.sudoku_size):
                if self.sudoku_board[i][j] is self.sudoku_empty_cell:
                    print("-", end="")
                else:
                    print(self.sudoku_board[i][j], end="")
            print()


sudoku_board = [
    [4, 1, 1, 2],
    [2, 3, 1, 1],
    [3, 1, 2, 1],
    [2, 1, 1, 3]
]

# sudoku = Sudoku(2, sudoku_board)
#
# sudoku.print_board()
#
# if sudoku.is_solved():
#     print("Sudoku is solved!")
# else:
#     print("Sudoku is not solved :(!")