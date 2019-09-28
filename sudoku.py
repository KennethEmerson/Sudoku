
##############################################################################################################
# Sudoku class
# K. Emerson 2017
# class that contains a sudoku and the methods to solve the sudoku and check the solution

# input requisites:
#   input must be an numpy array containing only integers
#   input must be squared array (4x4,9x9,16x16)
#   input array must contain squared blocks
##############################################################################################################

import numpy as np
import math
import sys

# classes for exceptions
class Error(Exception):
   pass
class NoNumpyArrayError(Error):
   pass
class ArraySizeError(Error):
   pass
class ArrayContentError(Error):
    pass

class Sudoku:
    def __init__(self,input):   
        
        # first check the input
        try:
            if not isinstance(input,np.ndarray):                # is input an numpy array
                raise NoNumpyArrayError
            if (len(input)!=len(input[0])):                     # is input a squared array
                raise ArraySizeError
            if not math.sqrt(len(input)).is_integer():          # does input contain square boxes
                raise ArraySizeError
            if not np.all(input >= 0):                          # all inputs must be zero or higher
                raise ArrayContentError
            if not np.all(input <= len(input)):                 # all inputs must be lower than max value
                raise ArrayContentError
            if not issubclass(input.dtype.type, np.integer):    #
                raise ArrayContentError

        except NoNumpyArrayError:
            sys.exit("error: Input is not an numpy array")
        except ArraySizeError:
            sys.exit("error: Input is not correct size")
        except ArrayContentError:
            sys.exit("error: Elements in iput are negative or non-integer") 
        
        # various variables for the sudoku
        self.original = input                                       # stores the original sudoku                              
        self.original_mask = (self.original != 0)                   # stores the mask for the original sudoku
        self.values = input                                         # stores the actual sudoku (solution)
        self.total_rows = len(self.values)                          # stores the total amount of rows
        self.total_columns = len(self.values[0])                    # stores the total amount of columns
        self.total_cells = np.size(input)                           # stores the total amount of cells
        self.box_size = int(math.sqrt(self.total_rows))             # stores the size of one box
        self.total_hor_boxes = self.total_rows//self.box_size       # stores the total amount of horizontal boxes
        self.total_vert_boxes = self.total_columns//self.box_size   # stores the total amount of vertical boxes
        self.actual_index = 0                                       # stores the actual index in the sudoku 
        self.potential_values = tuple([n for n                      # stores all potential values for the cells
                in range(1,self.total_rows+1)])
        self.max_value = self.potential_values[-1]

    # returns the corresponding row for the actual index
    def actual_row(self):
        return self.actual_index // self.total_columns
    
    # returns the corresponding column for the actual index
    def actual_column(self):
        return self.actual_index % self.total_columns
    
    # prints the sudoku (with missing values if attempt was made to solve the sudoku)
    def print_values(self):
        print("*"*40)
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in self.values]))

    # prints the original sudoku
    def print_original(self):
        print("*"*40)
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in self.original]))

    # checks if every row contains every digit only once (zeros are ignored)
    def check_rows(self):
        is_row_correct = True
        for row in self.values:
            checklist = list(self.potential_values)
            for i in range(0,self.total_columns):
                if row[i] !=0:
                    if checklist[row[i]-1]!=0:
                        checklist[row[i]-1] = 0
                    else:
                        is_row_correct = False
        return is_row_correct

    # checks if every column contains every digit only once (zeros are ignored)
    def check_columns(self):
        is_column_correct = True
        for column in self.values.T:
            checklist = list(self.potential_values)
            for i in range(0,self.total_rows):
                if column[i] !=0:
                    if checklist[column[i]-1]!=0:
                        checklist[column[i]-1] = 0
                    else:
                        is_column_correct = False
        return is_column_correct
    
    # checks if the given bow contains every digit only once (zeros are ignored)
    def check_one_box(self,matr):
        is_box_correct = True
        checklist = list(self.potential_values)
        for i in range(0,self.box_size):
            for j in range(0,self.box_size):
                item = matr[i][j]
                if item !=0:
                    if checklist[item-1]!=0:
                        checklist[item-1] = 0
                    else:
                        is_box_correct = False
        return is_box_correct
    
    # checks if every box contains every digit only once (zeros are ignored)
    def check_all_box(self):
        are_boxes_correct = True
        nr_rows = self.total_rows    
        nr_columns = self.total_columns
        b_size = self.box_size
        for i in range(0,self.total_hor_boxes):
            for j in range(0,self.total_vert_boxes):
                if not self.check_one_box(self.values[(b_size*i):((b_size*i)+b_size),(b_size*j):(b_size*j)+b_size]):
                    are_boxes_correct = False
        return are_boxes_correct
    
    # checks if all blanks (zeros) are filled in with a value
    def check_all_filled(self):
        return (np.count_nonzero(self.values) == self.total_cells)
   
    # checks if the sudoku rules are met
    def check_solution(self):
        if self.check_rows() and self.check_columns() and self.check_all_box():
            return True
        else:
            return False  
     
    
    # we attempt to fill the sudoku until it is completely filled or until we reach the max amount of attempts allowed.
    # we will follow the sudoku's actual index, if it is not a part of the original sudoku we will try to fill it with 
    # a valid number starting from 1 to the maximum value
    # if maximum value is not valid we will backtrack to the previous number and try to increase it's value 
    # with one and then repeat 
    # the trial for the actual number all over again
    # the backtrack will continue if no solution was found
    
    def find_solution(self,max_attempts=200):
        backtrack_counter = 0       # counts the amount of backtracks executed
        self.actual_index = 0       # sets the actual index of the sudoku to zero
        index_direction = 1         # two possible values 1 for the next cell, -1 to go to the previous cell 
        
        
       # This outer while loop continues until we have reached:
       #  - the final cell
       #  - all cells are filled
       #  - the max of attempts/backtracks is reached
        while (self.check_all_filled()== False and 
               self.actual_index <= self.total_cells and
               backtrack_counter < max_attempts):
            
            # checks if cell is not part of the original sudoku
            if not(self.original_mask[self.actual_row(),self.actual_column()]):                                   
                
                #If nine is not already reached incease by one
                # else reset value to zero and 
                if self.values[self.actual_row(),self.actual_column()] != self.max_value:
                    self.values[self.actual_row(),self.actual_column()] += 1
                    nine_reached = False
                else:
                    self.values[self.actual_row(),self.actual_column()] = 0
                    nine_reached = True
                
                # keeps increasing the value until the value is valid or maximum value is reached
                # or the value is set back to zero ()
                while (self.check_solution() == False and
                       (self.values[self.actual_row(),self.actual_column()]<self.max_value) and
                      self.values[self.actual_row(),self.actual_column()]!=0):
                        self.values[self.actual_row(),self.actual_column()] += 1                      # increase the number
                
                # after the while loop check if no solution was found,
                # if so set the index_direction to negative to start backtrack
                if self.check_solution() == False or nine_reached :
                    self.values[self.actual_row(),self.actual_column()]=0 # zet terug op nul
                    index_direction = -1 
                    backtrack_counter += 1
                

                if (self.check_solution()==True and not nine_reached and
                    self.values[self.actual_row(),self.actual_column()] in range(1,self.max_value+1)):
                    index_direction = 1
    
            self.actual_index=self.actual_index+index_direction
      
        self.actual_index = 0
        print("All cells filled: {0}".format(self.check_all_filled()))
        print("Solution found: {0}".format(self.check_solution()))
        print("number of backtracks: {0}".format(backtrack_counter))
        self.print_values()


###################################################################################
#  test of 2 sudokus
###################################################################################

sudoku9x9 = np.array([[0,0,3,1,8,0,7,0,9],
                      [4,0,7,0,3,0,0,6,8],
                      [0,0,0,2,0,4,0,0,3],
                      [1,0,0,7,0,0,0,0,5],
                      [8,0,0,0,2,0,0,0,7],
                      [7,0,0,0,0,8,0,0,4],
                      [2,0,0,5,0,3,0,0,0],
                      [3,8,0,0,4,0,9,0,2],
                      [9,0,5,0,1,2,3,0,0]])

sudoku4x4 = np.array([[0,0,1,0],
                      [1,0,0,4],
                      [3,0,0,2],
                      [0,2,0,0]])

test = Sudoku(sudoku9x9)
test.find_solution(200)
test2 = Sudoku(sudoku4x4)
test2.find_solution(50)
