import pygame, math, random, types, copy
from enum import Enum

pygame.init()
pygame.display.set_caption("Path Finding Demo")
cell_font = pygame.font.SysFont(pygame.font.get_default_font(), 25)

class CellType(Enum):
	Empty = 1
	Block = 2
	
class CellMark(Enum):
	No = 0
	Start = 1
	End = 2
	
class Cell:
	def __init__(self, type = CellType.Empty, pos = None):
		self.type = type
		self.count = 0
		self.mark = CellMark.No
		self.path_from = None
		self.pos = pos

		
class CellGrid:
	def __init__(self, board):
		self.board = board
		
	def get_size(self):
		return [len(self.board), len(self.board[0])]
		
	def at(self, pos):
		return self.board[pos[0]][pos[1]]
		
	def clone(self):
		return CellGrid( copy.deepcopy(self.board) )
		
	def clear_count(self, count):
		for o in self.board:
			for i in o:
				i.count = count
				i.path_from = None

	def is_valid_point(self, pos):
		sz = self.get_size()
		return pos[0] >= 0 and pos[1] >= 0 and pos[0] < sz[0] and pos[1] < sz[1]
				
	
def create_empty_maze( x, y ):
	return types.SimpleNamespace( 
		board = CellGrid( [[Cell(type = CellType.Empty, pos=[ix,iy]) for iy in range(y)] for ix in range(x)] ),
		start = [random.randrange(0,x), random.randrange(0,y)],
		end = [random.randrange(0,x), random.randrange(0,y)])
	
def create_wall_maze( x, y ):
	board = [[Cell(type = CellType.Empty, pos=[ix,iy]) for iy in range(y)] for ix in range(x)]
	for i in range(0,x):
		board[i][int(y/2)].type = CellType.Block
	for i in range(0,y):
		board[int(x/2)][i].type = CellType.Block
		
	board[random.randint(0,x/2-1)][int(y/2)].type = CellType.Empty
	board[random.randint(x/2+1,x-1)][int(y/2)].type = CellType.Empty
	board[int(x/2)][random.randint(0,y/2-1)].type = CellType.Empty
	board[int(x/2)][random.randint(y/2+1,y-1)].type = CellType.Empty
	
	return types.SimpleNamespace( board = CellGrid(board),
		start = [random.randrange(0,x/2), random.randrange(y/2+1,y)],
		end = [random.randrange(x/2+1,x), random.randrange(0,y/2)] )
	
def trans_rect( r, off ):
	return [r[0] + off[0], r[1] + off[1], r[2], r[3]]
	
def main_loop(ui):
	screen = pygame.display.set_mode((1000,800))

	clock = pygame.time.Clock()
	clock.tick()
	i = 0
	while True:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			break
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				break
			if event.key == pygame.K_RIGHT:
				ui.step(1)
			if event.key == pygame.K_LEFT:
				ui.step(-1)
			if event.key == pygame.K_r:
				ui.reset()
		
		ui.draw(screen)
		
		pygame.display.update()
		clock.tick(60)
		
		
		
	pygame.quit()
	
	
class Finder:
	def __init__(self):
		pass
		
	def set_board(self, board):
		self.board = board
		
	def set_path(self, path):
		self.path = path
		
	def run(self):
		main_loop(self)
		
	def draw(self, surface):
		if self.board == None:
			return
			
		draw_board(surface, surface.get_rect(), self.board)
		if self.path != None:
			draw_path(surface, surface.get_rect(), self.board, self.path)
		
		
	def step(self, steps):
		pass
		
	def reset(self):
		pass


class BoardMetrics:
	def __init__(self, area, board):
		self.area = area
		self.spacing = 3
		self.left = area[0] + self.spacing
		self.top = area[1] + self.spacing
		self.width = area[2] - area[0] - 2 * self.spacing
		self.height = area[3] - area[1] - 2 * self.spacing
		self.num_y = board.get_size()[1]
		self.num_x = board.get_size()[0]
		self.cy = self.height / self.num_y
		self.cx = self.width / self.num_x
		
	def cell_rect(self, pos):
		return [self.left + pos[0] * self.cx, self.top + pos[1] * self.cy, self.cx - self.spacing, self.cy - self.spacing]
		
	def cell_center(self, pos):
		rct = self.cell_rect(pos)
		return [rct[0]+rct[2]/2, rct[1] + rct[3]/2]

def draw_board(surface, area, board):
	pygame.draw.rect(surface, (0,0,0), area)
	metrics = BoardMetrics(area, board)

	colors = {
		CellType.Empty: (40,40,40),
		CellType.Block: (128,100,0),
	}
	marks = {
		CellMark.Start: (110,110,0),
		CellMark.End: (0,110,0),
	}
	for y in range(0,metrics.num_y):
		for x in range(0,metrics.num_x):
			cell = board.at([x,y])
			clr = colors.get(cell.type, (100,100,0))
			cell_rect = metrics.cell_rect( [x, y] )
			
			pygame.draw.rect(surface, clr, cell_rect)
			
			if cell.count != math.inf:
				number = cell_font.render( "{}".format(cell.count), True, (255,255,255))
				surface.blit(number, trans_rect(number.get_rect(), 
					[cell_rect[0] + (cell_rect[2] - number.get_rect()[2])/2, 
					cell_rect[1] + (cell_rect[3] -number.get_rect()[3])/2]
				))
			
			mark = marks.get(cell.mark, None)
			if mark != None:
				pygame.draw.rect(surface, mark, cell_rect, metrics.spacing)

				
def draw_path(surface, area, board, path):
	metrics = BoardMetrics(area, board)
	for i in range(0,len(path)-1):
		ctr_a = metrics.cell_center( path[i].pos )
		ctr_b = metrics.cell_center( path[i+1].pos )
		pygame.draw.line(surface, (120,220,0),  ctr_a, ctr_b, metrics.spacing )
		
	
def add_point(a,b):
	return [a[0] + b[0], a[1] + b[1]]

