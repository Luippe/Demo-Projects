import numpy as np
import time

def matprint(mat, fmt="g"):
    col_maxes = [max([len(("{:"+fmt+"}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:"+str(col_maxes[i])+fmt+"}").format(y), end="")
        print("")


# Class for finding the closest path to where the player wants to move
class PlayerPathFinding:
    def __init__(self, goal_pos, current_pos, view_mat):
        self.current_pos = current_pos
        self.goal_pos = goal_pos
        self.view_mat = view_mat
        self.curr_start_val = 0
        self.sorted_index = 0
        self.path_pos = [1,1]
        self.checked_pos = []
        self.priority_queue = []
        self.direc_path = []
        self.next_path = []
        self.sol_tiles = [goal_pos]
        self.sol_path = []
        self.scale = 10
        self.priority_queue.append([1000,0])
        self.checked_pos.append(current_pos)
        self.next_path.append(current_pos)
        self.direc_path.append(current_pos)
        self.max_step = 20
        self.start = time.time()

    # Find the closest path
    def update(self):
        start = True         
        self.path_pos.append(self.current_pos)
        x_curr = self.current_pos[0]
        y_curr = self.current_pos[1]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                next_pos = [x_curr+i, y_curr+j]
                if (next_pos in self.path_pos) == False and (self.view_mat[y_curr+j,x_curr+i] != 0):
                    goal_dist = self.scale*np.linalg.norm([a_i - b_i for a_i, b_i in zip(next_pos, self.goal_pos)])
                    start_dist = np.linalg.norm([a_i - b_i for a_i, b_i in zip(next_pos, self.current_pos)]) + self.curr_start_val
                    if (next_pos in self.checked_pos) == False:
                        self.checked_pos.append(next_pos)
                        self.priority_queue.append([goal_dist + start_dist,start_dist])
                        self.direc_path.append(self.current_pos)
                        self.next_path.append(next_pos)
                    else:
                        comparing_index = self.checked_pos.index(next_pos)
                        if self.priority_queue[comparing_index][0] > goal_dist + start_dist:
                            self.priority_queue[comparing_index] = [goal_dist + start_dist,start_dist]
                            path_index = self.next_path.index(next_pos)
                            self.direc_path[path_index] = self.current_pos
                            self.next_path[path_index] = next_pos
        self.checked_pos.remove(self.current_pos)
        self.priority_queue.remove(self.priority_queue[self.sorted_index])
        try:
            self.sorted_index = self.priority_queue.index(min(self.priority_queue, key = lambda x: x[0]))
        except:
            return False,[]
        self.curr_start_val = self.priority_queue[self.sorted_index][1]
        self.current_pos = self.checked_pos[self.sorted_index]
        if self.current_pos == self.goal_pos:
            end = time.time()
            print(end-self.start)
            next_loc = self.goal_pos
            for num in range(self.max_step):
                place = self.next_path.index(next_loc)
                next_loc = self.direc_path[place]
                self.sol_tiles.append(next_loc)
                if self.sol_tiles[-1] == [6,5]:
                    start = False
                    break
            self.sol_tiles = np.array(self.sol_tiles)
            for num in range(len(self.sol_tiles)-1):
                self.sol_path.append(tuple(self.sol_tiles[num]-self.sol_tiles[num+1]))
        return start, self.sol_path