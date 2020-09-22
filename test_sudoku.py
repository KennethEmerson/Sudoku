import numpy as np
import pytest
from sudoku import Sudoku, ArraySizeError, NoNumpyArrayError

correct_input = np.array([[0,0,1,0], 
                          [1,0,0,4],
                          [3,0,0,2],
                          [0,2,0,0]])
correct_sudoku = Sudoku(correct_input)

solution = np.array([[2,4,1,3],
                    [1,3,2,4],
                    [3,1,4,2],
                    [4,2,3,1]])
solved_sudoku = Sudoku(solution)


wrong_input_1 = np.array([[0,0,1,0], 
                          [1,0,0,1],
                          [3,0,0,2],
                          [1,2,0,0]])
wrong_sudoku_1 = Sudoku(wrong_input_1)

def test_actual_row():
    assert correct_sudoku.actual_row() == 0

def test_actual_column():
    assert correct_sudoku.actual_column() == 0

def test_check_rows():
    assert correct_sudoku.check_rows() == True
    assert wrong_sudoku_1.check_rows() == False

def test_check_columns():
    assert correct_sudoku.check_columns() == True
    assert wrong_sudoku_1.check_columns() == False

def test_check_one_box():
    assert correct_sudoku.check_one_box(np.array([[0,1],[0,2]])) == True
    assert wrong_sudoku_1.check_one_box(np.array([[0,1],[1,0]])) == False

def test_check_all_box():
  assert correct_sudoku.check_all_box() == True
  assert wrong_sudoku_1.check_all_box() == False

def test_check_all_filled():
  assert solved_sudoku.check_all_filled() == True

def test_check_solution():
  assert solved_sudoku.check_solution() == True

def test_find_solution():
  correct_sudoku.find_solution(200)
  assert np.array_equal(correct_sudoku.values, solution)