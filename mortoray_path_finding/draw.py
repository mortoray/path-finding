import pygame, math, random, types, copy
from enum import Enum
from . import maze

pygame.init()
pygame.display.set_caption("Path Finding Demo")
cell_font = pygame.font.SysFont(pygame.font.get_default_font(), 25)

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
		self.path = None
		self.board = None
		
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
		return [rct[0]+rct[2]//2, rct[1] + rct[3]//2]

def draw_board(surface, area, board):
	pygame.draw.rect(surface, (0,0,0), area)
	metrics = BoardMetrics(area, board)

	colors = {
		maze.CellType.Empty: (40,40,40),
		maze.CellType.Block: (128,100,0),
	}
	marks = {
		maze.CellMark.Start: (110,110,0),
		maze.CellMark.End: (0,110,0),
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
					[cell_rect[0] + (cell_rect[2] - number.get_rect()[2])//2, 
					cell_rect[1] + (cell_rect[3] -number.get_rect()[3])//2]
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
		

