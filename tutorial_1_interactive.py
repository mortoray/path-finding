#!/usr/bin/python3
import mortoray_path_finding as mpf
import math

def fill_shortest_path(board, start, end, max_distance = math.inf):
	""" Creates a duplicate of the board with shortest path counts from start-end recorded in each cell. """
	nboard = board.clone()
	nboard.clear_count(math.inf)

	# mark the start and end for the UI
	nboard.at( start ).mark = mpf.maze.CellMark.Start
	nboard.at( end ).mark = mpf.maze.CellMark.End

	# we start here, thus a distance of 0
	open_list = [ start ]
	nboard.at( start ).count = 0
	
	# (x,y) offsets from current cell
	neighbours = [ [-1,0], [1,0], [0,-1], [0,1] ]
	while open_list:
		cur_pos = open_list.pop(0)
		cur_cell = nboard.at( cur_pos )
		
		for neighbour in neighbours:
			ncell_pos = mpf.maze.add_point(cur_pos, neighbour)
			if not nboard.is_valid_point(ncell_pos):
				continue
				
			cell = nboard.at( ncell_pos )
			
			if cell.type != mpf.maze.CellType.Empty:
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
	""" Returns the path to the end, assuming the board has been filled in via fill_shortest_path """
	cell = board.at( end )
	path = []
	while cell != None:
		path.append(cell)
		cell = cell.path_from
		
	return path
	
	
class MyFinder(mpf.draw.Finder):
	"""Integrate into the simple UI	"""
	def __init__(self):
		self.reset()
	
	def step(self, frames):
		self.max_distance = max( 0, self.max_distance + frames )
		self.result = fill_shortest_path(self.game.board, self.game.start, self.game.end, max_distance = self.max_distance)
		self.set_board(self.result)
		self.set_path(get_path_to(self.result, self.game.end))
	
	def reset(self):
		self.game = mpf.maze.create_wall_maze(20,10)
		self.max_distance = 18
		self.step(0)
	
	

finder = MyFinder()
finder.run()
