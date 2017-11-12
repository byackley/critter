import ceGame
import ceColor
import pygame
import random
import datetime

class Cell:
	def __init__(self, ch=None, fg=None, bg=None, gfx=False, flash=False, double=False):
		self.ch = ch if ch else random.randint(0, 255)
		self.fg = fg if fg else random.randint(0, 15)
		self.bg = bg if bg else random.randint(0, 15)
		self.flash = random.random() < 0.1
		self.double = False
		self.gfx = random.random() < 0.5
		
	def __repr__(self):
		return '%c (%d %d)' % (self.ch, self.fg, self.bg)

cells = [[Cell() for x in range(40)] for y in range(25)]

SOLID = 0xBF

COLORS = [
	ceColor.hex('000'), # 0=black
	ceColor.hex('F00'), # 1=red
	ceColor.hex('0F0'), # 2=green
	ceColor.hex('FF0'), # 3=yellow
	ceColor.hex('00F'), # 4=blue
	ceColor.hex('F0F'), # 5=magenta
	ceColor.hex('0FF'), # 6=cyan
	ceColor.hex('FFF'), # 7=white
	ceColor.hex('888'), # 8=gray
	ceColor.hex('088'), # 9=dark cyan
	ceColor.hex('808'), #10=purple
	ceColor.hex('651'), #11=brown
	ceColor.hex('f88'), #12=pink
	ceColor.hex('afa'), #13=lt green
	ceColor.hex('88f'), #14=lt blue
	ceColor.hex('f80'), #15=orange	
]

def putText(st, x, y, fg=7, bg=0, flash=False, double=False):
	for n,ch in enumerate(st):
		try:
			cells[y][x+n].fg = fg
			cells[y][x+n].bg = bg
			cells[y][x+n].flash = flash
			cells[y][x+n].double = double
			cells[y][x+n].ch = ord(ch)
		except IndexError:
			pass

def recolor(base, col):
	out = base.copy()
	out.fill(col, None, pygame.BLEND_MULT)
	return out

def render(surf, timer):
	for nRow,row in enumerate(cells):
		for nCol,cell in enumerate(row):
			chRow = int(cell.ch/16)
			chCol = cell.ch % 16
			surf.blit(sheets[cell.bg], (8+nCol*6, nRow*9), (15*6, 11*9, 6, 9))
			if not cell.flash or timer % 60 < 30:
				surf.blit(sheets[cell.fg], (8+nCol*6, nRow*9), (chCol*6, chRow*9, 6, 9))

TIME_ADJUST = datetime.timedelta(days=10227)

def update():
	# header row
	dt = datetime.datetime.now() - TIME_ADJUST
	header = 'CREEFRAX '+dt.strftime('%y %b %d')
	timeStr = dt.strftime('%I:%M:%S %p')
	
	putText(header, 0, 0)
	putText(timeStr, 29, 0, 3)
	
	putText('Flashing Text!', 0, 4, 7, 1, True)

if __name__=='__main__':
	surf = ceGame.init()
	timer = 0

	baseSheet = pygame.image.load('rsrc/cf-text.png')
	
	sheets = [recolor(baseSheet, c) for c in COLORS]

	while ceGame.running:
		timer += 1
		
		update()
		ceGame.update()
		
		render(surf, timer)		
		ceGame.render(surf)
