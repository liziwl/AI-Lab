import numpy as np
import os, sys
try:
    from tkinter import *
except ImportError:  #Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    from tkMessageBox import *
    import tkFileDialog
else:  #Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *

# tags for file
file_tag='train' #train/test

# The board size of go game
BOARD_SIZE = 9
COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
POINT_STATE_CHECKED=100
POINT_STATE_UNCHECKED=101
POINT_STATE_NOT_ALIVE=102
POINT_STATE_ALIVE=103
POINT_STATE_EMPYT=104

def read_go(file_name):
  # read from txt file and save as a matrix
  go_arr = np.zeros((BOARD_SIZE, BOARD_SIZE))
  for line in open(file_name):
    line = line.strip()
    lst = line.split()
    row = int(lst[0])
    col = int(lst[1])
    val = int(lst[2])
    go_arr[row, col] = val
  return go_arr


def plot_go(go_arr, txt='Default'):
  # Visualization of a go matrix
  # First draw a canvas with 9*9 grid
  root = Tk()
  cv = Canvas(root, width=50*(BOARD_SIZE+1), height=50*(BOARD_SIZE+1), bg='#F7DCB4')
  cv.create_text(250,10,text=txt,fill='blue')
  cv.pack(side=LEFT)
  size = 50
  for x in range(BOARD_SIZE):
    cv.create_line(size+x*size, size, size+x*size, size+(BOARD_SIZE-1)*size)
  for y in range(BOARD_SIZE):
    cv.create_line(size, size+y*size, size+(BOARD_SIZE-1)*size, size+size*y)
  # Second draw white and black circles on cross points
  offset = 20
  idx_black = np.argwhere(go_arr == COLOR_BLACK)
  idx_white = np.argwhere(go_arr == COLOR_WHITE)
  len_black = idx_black.shape[0]
  len_white = idx_white.shape[0]
  for i in range(len_black):
    if idx_black[i,0] >= BOARD_SIZE or idx_black[i,1] >= BOARD_SIZE:
      print ('IndexError: index out of range')
      sys.exit(0)
    else:
      new_x = 50*(idx_black[i,1]+1)
      new_y = 50*(idx_black[i,0]+1)
      cv.create_oval(new_x-offset, new_y-offset, new_x+offset, new_y+offset, width=1, fill='black', outline='black')
  for i in range(len_white):
    if idx_white[i,0] >= BOARD_SIZE or idx_white[i,1] >= BOARD_SIZE:
      print ('IndexError: index out of range')
      sys.exit(0)
    else:
      new_x = 50*(idx_white[i,1]+1)
      new_y = 50*(idx_white[i,0]+1)
      cv.create_oval(new_x-offset, new_y-offset, new_x+offset, new_y+offset, width=1, fill='white', outline='white')
  root.mainloop()

#-------------------------------------------------------
# Rule judgement  *need finish
#-------------------------------------------------------
def is_alive(check_state, go_arr, i, j, color_type):
  # 判断(i, j)位置是否存活
  '''
  This function checks whether the point (i,j) and its connected points with the same color are alive, it can only be used for white/black chess only
  Depth-first searching.
  :param check_state: The guard array to verify whether a point is checked
  :param go_arr: chess board
  :param i: x-index of the start point of searching
  :param j: y-index of the start point of searching
  :return: POINT_STATE_CHECKED/POINT_STATE_ALIVE/POINT_STATE_NOT_ALIVE, POINT_STATE_CHECKED=> the start point (i,j) is checked, POINT_STATE_ALIVE=> the point and its linked points with the same color are alive, POINT_STATE_NOT_ALIVE=>the point and its linked points with the same color are dead
  '''
  pass

def go_judege(go_arr):
  # 判断是否符合规则
  '''
  :param go_arr: the numpy array contains the chess board
  :return: whether this chess board fit the go rules in the document
           False => unfit rule
           True => ok
  '''
  is_fit_go_rule = True
  check_state = np.zeros(go_arr.shape)
  check_state[:] = POINT_STATE_EMPYT
  tmp_indx = np.where(go_arr != 0)
  check_state[tmp_indx] = POINT_STATE_UNCHECKED
  for i in range(go_arr.shape[0]):
    for j in range(go_arr.shape[1]):
      if check_state[i, j] == POINT_STATE_UNCHECKED:
        tmp_alive = is_alive(check_state, go_arr,i,j, go_arr[i,j])
        if tmp_alive == POINT_STATE_NOT_ALIVE: # once the go rule is broken, stop the searching and return the state
          is_fit_go_rule = False
          break
      else:
        pass # pass if the point and its lined points are checked
  return is_fit_go_rule

#-------------------------------------------------------
# User strategy  *need finish
#-------------------------------------------------------
def user_step_eat(go_arr):
  # 吃子
  '''
  :param go_arr: chessboard
  :return: ans=>where to put one step forward for white chess pieces so that some black chess pieces will be killed; user_arr=> the result chessboard after the step
  '''
  pass

def user_setp_possible(go_arr):
  # 输出所有白棋的下一步
  '''
  :param go_arr: chessboard
  :return: ans=> all the possible locations to put one step forward for white chess pieces
  '''
  pass

if __name__ == "__main__":
  chess_rule_monitor = True
  problem_tag="Default"
  ans=[]
  user_arr=np.zeros([0,0])

  # The first problem: rule checking
  problem_tag = "Problem 0: rule checking"
  go_arr = read_go('{}_0.txt'.format(file_tag))
  plot_go(go_arr, problem_tag)
  chess_rule_monitor=go_judege(go_arr)
  print ("{}:{}".format(problem_tag, chess_rule_monitor))
  plot_go(go_arr, '{}=>{}'.format(problem_tag, chess_rule_monitor))

  problem_tag = "Problem 00: rule checking"
  go_arr = read_go('{}_00.txt'.format(file_tag))
  plot_go(go_arr, problem_tag)
  chess_rule_monitor = go_judege(go_arr)
  print ("{}:{}".format(problem_tag, chess_rule_monitor))
  plot_go(go_arr, '{}=>{}'.format(problem_tag, chess_rule_monitor))

  # The second~fifth prolbem: forward one step and eat the adverse points on the chessboard
  for i in range(1,5):
    problem_tag = "Problem {}: forward on step".format(i)
    go_arr = read_go('{}_{}.txt'.format(file_tag, i))
    plot_go(go_arr, problem_tag)
    chess_rule_monitor = go_judege(go_arr)
    #ans, user_arr = user_step_eat(go_arr) # need finish
    print ("{}:{}".format(problem_tag, ans))
    plot_go(user_arr, '{}=>{}'.format(problem_tag, chess_rule_monitor))

  # The sixth problem: find all the postion which can place a white chess pieces
  problem_tag = "Problem {}: all possible position".format(5)
  go_arr = read_go('{}_{}.txt'.format(file_tag,5))
  plot_go(go_arr, problem_tag)
  chess_rule_monitor = go_judege(go_arr)
  #ans = user_setp_possible(go_arr) # need finish
  print ("{}:{}".format(problem_tag, ans))
  plot_go(go_arr, '{}=>{}'.format(problem_tag, chess_rule_monitor))