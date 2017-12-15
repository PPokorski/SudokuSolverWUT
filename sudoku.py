import copy
import math
import csv


def get_question_board_from_file(filename):
    question_board = []
    answer_board = []
    with open(filename, 'r') as open_file:
        reader = csv.reader(open_file)
        if (next(reader))[0] != 'Question':
            raise ValueError("The first line should be: Question")

        is_question = True
        for line in reader:
            if len(line) == 0:
                continue

            if line[0] == 'Answer':
                is_question = False
                continue

            if is_question:
                question_board.append([int(i) for i in line])
            else:
                answer_board.append([int(i) for i in line])

    rank = int(math.sqrt(len(question_board)))
    return [rank, question_board, answer_board]

def append_answer_board_to_file(filename, answer_board):
    with open(filename, 'a') as open_file:
        writer = csv.writer(open_file, delimiter=',')
        writer.writerow([' '])
        writer.writerow([' '])

        writer.writerow(['Answer'])
        for row in answer_board:
            writer.writerow(row)


def converter():
    all_lists = []
    with open('/home/pokor/Downloads/sudoku/sudokuDiagrams.txt', 'r') as open_file:
        no = 0
        for line in open_file:
            new_list = []
            i = 0
            tmp_list = []
            for letter in line:
                if letter == '.':
                    tmp_list.append(0)
                if letter.isdigit():
                    tmp_list.append(int(letter))

                i = i + 1
                if i % 9 == 0:
                    new_list.append(copy.copy(tmp_list))
                    tmp_list.clear()
                    i = 0
            all_lists.append(copy.copy(new_list))

            append_answer_board_to_file('/home/pokor/PycharmProjects/SudokuSolverWUT/sudoku/easy_' + str(no) + '.csv',new_list)
            no = no + 1


    return all_lists


class Sudoku:
    def __init__(self, rank, initial_board, answer_board):
        # What is the base rank of sudoku.
        # Size of the board is rank * rank
        self.sudoku_rank = rank
        # Size of the sudoku board, number of cells in rows and columns
        self.sudoku_size = rank ** 2
        # Actual sudoku board
        self.sudoku_board = copy.copy(initial_board)
        # The answer for sudoku board
        self.answer_board = copy.copy(answer_board)
        # Numbers that can go into sudoku board
        self.sudoku_numbers = [i + 1 for i in range(self.sudoku_size)]
        # Value of the empty (not filled yet) cell
        self.sudoku_empty_cell = 0

        self.check_initial_board_validity(rank, initial_board)
        if len(answer_board) != 0:
            self.check_initial_board_validity(rank, answer_board)

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
                    print("_", end=" ")
                else:
                    print(self.sudoku_board[i][j], end=" ")

                if ((j + 1) % self.sudoku_rank == 0) and ((j + 1) != self.sudoku_size):
                    print("|", end=" ")

            print()

            if ((i + 1) % self.sudoku_rank == 0) and ((i + 1) != self.sudoku_size):
                print("--" * (self.sudoku_size + 2), end="")
                print()



                # [r, q_board, a_board] = get_question_board_from_file('/home/pokor/PycharmProjects/SudokuSolverWUT/sudoku/easy_0.csv')
#
# sudoku = Sudoku(3, q_board, [])
#
# sudoku.print_board()

# if sudoku.is_solved():
#     print("Sudoku is solved!")
# else:
#     print("Sudoku is not solved :(!")