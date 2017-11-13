import ceGame
import ceColor
import pygame
import random
import datetime
import urllib.request, urllib.error, urllib.parse

class Cell:
    def __init__(self, ch=0, fg=0, bg=0, gfx=False, flash=False, double=False):
        self.ch = ch
        self.fg = fg
        self.bg = bg
        self.flash = flash
        self.double = double
        self.hide = False
        self.gfx =gfx

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
            if double and y<24:
                cells[y+1][x+n].double = False
            cells[y][x+n].ch = ord(ch)
            cells[y][x+n].gfx = False
        except IndexError:
            pass

def putGfx(num, x, y, fg=7, bg=0, flash=False):
    cells[y][x].ch = num
    cells[y][x].gfx = True
    cells[y][x].flash = flash
    cells[y][x].fg = fg
    cells[y][x].bg = bg

def recolor(base, col):
    out = base.copy()
    out.fill(col, None, pygame.BLEND_MULT)
    return out

def render(surf, timer):
    for nRow,row in enumerate(cells):
        for nCol,cell in enumerate(row):
            if nRow > 0 and cells[nRow-1][nCol].double:
                continue
            chRow = int(cell.ch/16)
            chCol = cell.ch % 16
            surf.blit(sheets['gfx'][cell.bg], (8+nCol*6, nRow*9), (15*6, 3*9, 6, 9))
            if cell.double:
                surf.blit(sheets['gfx'][cell.bg], (8+nCol*6, (nRow+1)*9), (15*6, 3*9, 6, 9))
            if not cell.flash or timer % 60 < 30:
                which = 'gfx' if cell.gfx else 'text'
                if cell.double:
                    surf.blit(sheets['tall'][cell.fg], (8+nCol*6, nRow*9), (chCol*6, chRow*18, 6, 18))
                else:
                    surf.blit(sheets[which][cell.fg], (8+nCol*6, nRow*9), (chCol*6, chRow*9, 6, 9))

TIME_ADJUST = datetime.timedelta(days=10227)

def drawLogo(x, y, fg, bg):
    logo = [ 0,  0, 20,  0,  0,  0,
            32, 32,  6, 57, 18, 41,
            37, 18, 39, 24,  1,  1,
             0,  0,  0, 10,  0,  0]

    for n,ch in enumerate(logo):
        putGfx(ch, x + n%6, y + int(n/6), fg, bg)

def drawNews(main, sub, y):
    putText(main, 0, y, 3, 0)
    putText(sub, 1+len(main), y, 7, 0)

def load(url=None):
    global cells
    if url is None:
        # render the sample 'page 0'
        putText('    Welcome to the City of Elseways     ', 0, 1, 7, 9, False, True)
        putText('   - a service of the Cosmos Corps -    ', 0, 3, 7, 10)

        drawLogo(0, 5, 14, 4)

        putText('Today:   54\xb0', 7, 5)
        putGfx(0x80, 14, 5, 3)

        putText('Tonight:   31\xb0', 21, 5)
        putGfx(0x83, 30, 5, 8)

        putGfx(0x91, 7, 7, 15)
        putText('Writers wanted!', 9, 7, 2)
        putText('This won\'t be', 25, 7)
        putText('the last edition of the news!', 7, 8)

        drawNews('WRITER STUMPED', 'Headlines are really hard', 10)
        drawNews('STUFF HAPPENS', 'You won\'t believe it', 12)
        drawNews('FREE', 'Slightly used scientific equipment', 14)
        drawNews('FOR SALE', 'Spatial distortion analyzer', 15)
        drawNews('NEW RECORD!', 'Runner X defends title again', 17)
        drawNews('RECIPES', 'Too much cheese? No such thing!', 19)
        drawNews('INTERVIEW', 'M.H. Nostrils and her new book', 20)
        drawNews('HOME TIPS', 'Care for your loyal Anthrobots', 22)
    else:
        with urllib.request.urlopen(url) as response:
            line = response.read().decode('utf-8')
            print('recd', line)

            for b in line:
                count = 0
                for code in line.split(' '):
                    x = count%40
                    y = int(count/40)+1

                    cells[y][x].ch = int(code[:2],16)
                    cells[y][x].fg = int(code[2],16)
                    cells[y][x].bg = int(code[3],16)
                    flags = int(code[4])
                    cells[y][x].flash = flags & 8 > 0
                    cells[y][x].double = flags & 4 > 0
                    cells[y][x].hide = flags & 2 > 0
                    cells[y][x].gfx = flags & 1 > 0

                    count += 1

def dump():
    for nRow,row in enumerate(cells[1:-1]):
        for nCol,cell in enumerate(row):
            flags = 8 if cell.flash else 0 \
                + 4 if cell.double else 0 \
                + 2 if cell.hide else 0 \
                + 1 if cell.gfx else 0
            print('%02x%x%x%x' % (cell.ch, cell.fg, cell.bg, flags), end=' ')

def update():
        # header row
    dt = datetime.datetime.now() - TIME_ADJUST
    header = 'CREEFRAX '+dt.strftime('%y %b %d')
    timeStr = dt.strftime('%I:%M:%S %p')

    putText(' '*40, 0, 0)
    putText(header, 0, 0)
    putText(timeStr, 29, 0, 3)

    putText('  \x7F Red ', 0, 24, 1, 0)
    putText('\x7F Org ', 8, 24, 15, 0)
    putText('\x7F Ylw ', 14, 24, 3, 0)
    putText('\x7F Grn ', 20, 24, 2, 0)
    putText('\x7F Blu ', 26, 24, 4, 0)
    putText('\x7F Pur   ', 32, 24, 10, 0)

URL = 'http://gull.us/~bj/cf/000.txt'

if __name__=='__main__':
    surf = ceGame.init()
    timer = 0

    baseText = pygame.image.load('rsrc/cf-text.png')
    baseTall = pygame.image.load('rsrc/cf-text-tall.png')
    baseGfx = pygame.image.load('rsrc/cf-gfx.png')

    sheets = {
        'text': [recolor(baseText, c) for c in COLORS],
        'tall': [recolor(baseTall, c) for c in COLORS],
        'gfx': [recolor(baseGfx, c) for c in COLORS]
    }

    load(URL)

    while ceGame.running:
        timer += 1

        update()
        ceGame.update()

        render(surf, timer)
        ceGame.render(surf)
    if URL is None:
        dump()
