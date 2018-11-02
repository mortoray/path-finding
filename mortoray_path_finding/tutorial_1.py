from . import maze
import math

def fill_shortest_path(board, start, end, max_distance = math.inf):
	""" Creates a duplicate of the board with shortest path counts from start-end recorded in each cell. """
	nboard = board.clone()
	nboard.clear_count(math.inf)

	# mark the start and end for the UI
	nboard.at( start ).mark = maze.CellMark.Start
	nboard.at( end ).mark = maze.CellMark.End

	# we start here, thus a distance of 0
	open_list = [ start ]
	nboard.at( start ).count = 0
	
	# (x,y) offsets from current cell
	neighbours = [ [-1,0], [1,0], [0,-1], [0,1] ]
	while open_list:
		cur_pos = open_list.pop(0)
		cur_cell = nboard.at( cur_pos )
		
		for neighbour in neighbours:
			ncell_pos = maze.add_point(cur_pos, neighbour)
			if not nboard.is_valid_point(ncell_pos):
				continue
				
			cell = nboard.at( ncell_pos )
			
			if cell.type != maze.CellType.Empty:
				continue
				
			dist = cur_cell.count + 1
			if dist > max_distance:
				continue
				
			if cell.count > dist:
				cell.count = dist
				cell.path_from = cur_cell
				open_list.append(ncell_pos)

	return nboard
