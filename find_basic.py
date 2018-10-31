#!/usr/bin/python3
import mortoray_path_finding as mpf
import copy, math

def clear_count(board, value):
	for o in board:
		for i in o:
			i.count = value
			i.path_from = None
			
def fill_shortest_path(board, start, end, max_distance = math.inf):
	nboard = copy.deepcopy(board)
	clear_count(nboard, math.inf)
	nboard[start[0]][start[1]].mark = mpf.CellMark.Start
	nboard[end[0]][end[1]].mark = mpf.CellMark.End
	nboard[start[0]][start[1]].count = 0
	
	open_list = [ start ]
	
	neighbours = [ [-1,0], [1,0], [0,-1], [0,1] ]
	while open_list:
		cur_pos = open_list.pop(0)
		cur_cell = nboard[cur_pos[0]][cur_pos[1]]
		
		for neighbour in neighbours:
			ncell_pos = mpf.add_point(cur_pos, neighbour)
			if not mpf.is_valid_point(ncell_pos, nboard):
				continue
				
			cell = nboard[ncell_pos[0]][ncell_pos[1]]
			
			if cell.type != mpf.CellType.Empty:
				continue
				
			dist = cur_cell.count + 1
			if dist > max_distance:
				continue
				
			if cell.count > dist:
				cell.count = dist
				cell.path_from = cur_cell
				open_list.append(ncell_pos)

	return nboard

def get_path_to(board, end):
	cell = board[end[0]][end[1]]
	path = []
	while cell != None:
		path.append(cell)
		cell = cell.path_from
		
	return path
	
class MyFinder(mpf.Finder):
	def __init__(self):
		self.board = mpf.create_wall_board(20,10)
		self.max_distance = 18
		self.step(0)
	
	def step(self, frames):
		end = [17,3]
		start = [4,8]
		
		self.max_distance = max( 0, self.max_distance + frames )
		self.result = fill_shortest_path(self.board, start, end, max_distance = self.max_distance)
		self.set_board(self.result)
		self.set_path(get_path_to(self.result, end))
	

finder = MyFinder()
finder.run()
