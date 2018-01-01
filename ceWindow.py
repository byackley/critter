import pygame
from ceFill import CEFillGradient, CEFill
from ceEntity import CEEntity
import ceSheet
import ceText
import ceGame
import ceColor
from ceControl import *
import ceScript

sheet = None

MAIN_BG = CEFillGradient(ceColor.hex('77c'), ceColor.hex('003'))

class CEWidget(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.win = None
        self.neighbors = [None, None, None, None] # up left down right
        self.do = None
        
    def __repr__(self):
        return '[Widget]'
        
    def onAdd(self, win):
        return

class CEWTextEntry(CEWidget):
    pass

class CEWCloseButton(CEWidget):
    '''
    NOTE: adding a Close Button to a window will trap focus on the close
    button itself. This is meant for 'click arrow to advance box' sort of
    text boxes.
    '''
    def __init__(self, x, y):
        super(CEWCloseButton,self).__init__(x,y)
        self.do = [['close']]
        self.neighbors=[self, self, self, self]
        
    def onAdd(self, win):
        win.selected = self
        
    def render(self, surf):
        if ceGame.timer % 30 > 15: # flash
            ceText.drawText(surf, '`i60', self.win.x+self.x, self.win.y+self.y)

class CEWMenuItem(CEWidget):
    def __init__(self, x, y, text, do=None):
        super(CEWMenuItem,self).__init__(x,y)
        self.text = text
        self.do = do

    def render(self, surf):
        selected = self.win.selected is self
        ceText.drawText(surf,
            '`c00`v00'+self.text if selected else '`c10'+self.text,
            self.win.x+self.x,
            self.win.y+self.y)
    
    def __repr__(self):
        return '[Menu Item %s]' % self.text

def linkVertical(items):
    for n,item in enumerate(items):
        item.neighbors[0] = items[n-1] 
        item.neighbors[2] = items[(n+1)%(len(items))]

def linkHorizontal(items):
    for n,item in enumerate(items):
        item.neighbors[1] = items[n-1] 
        item.neighbors[3] = items[(n+1)%(len(items))]

class CEWText(CEWidget):
    def __init__(self, x, y, text):
        super(CEWText,self).__init__(x,y)
        self.text = text

    def render(self, surf):
        ceText.drawText(surf, self.text, self.win.x+self.x, self.win.y+self.y)
        
    def __repr__(self):
        return '[Text %s]' % self.text

class CEWindow(CEEntity):
    def __init__(self, frame=0, bg=None, x=0, y=0, dx=32, dy=6):
        global sheet

        if sheet == None:
            sheet = ceSheet.CESheet('font/icons')

        self.frame = frame
        self.bg = bg
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        
        self.widgets = []
        self.selected = None
        
    def __repr__(self):
        return '[Window at %d,%d containing %s]' % (self.x, self.y, ','.join(str(w) for w in self.widgets))
        
    def add(self, widget):
        self.widgets.append(widget)
        widget.win = self
        widget.onAdd(self)
        
    def update(self, key=None):
        sel = self.selected
        if key is None:
            return
        if key==c_UP and sel.neighbors[0] is not None:
            self.selected = sel.neighbors[0]
        if key==c_LEFT and sel.neighbors[1] is not None:
            self.selected = sel.neighbors[1]
        if key==c_DOWN and sel.neighbors[2] is not None:
            self.selected = sel.neighbors[2]
        if key==c_RIGHT and sel.neighbors[3] is not None:
            self.selected = sel.neighbors[3]
        if key==c_A and self.selected.do is not None:
            for cmd in self.selected.do:
                ceScript.runCmd(cmd)
            
    def render(self, surf):
        
        # background    
        if self.bg:
            self.bg.render(surf, self.x, self.y, self.dx*8, self.dy*8)
            
        # frame border
        if self.frame is not None:
            fp = 4*self.frame

            sheet.draw(surf, self.x, self.y, 'ic0%1x' % fp)
            sheet.draw(surf, self.x+8, self.y, 'ic0%1x' % (fp+1) )
            sheet.draw(surf, self.x, self.y+8, 'ic1%1x' % fp)
            
            sheet.draw(surf, self.x+8*self.dx-8, self.y, 'ic3%1x' % fp)
            sheet.draw(surf, self.x+8*self.dx-8, self.y+8, 'ic1%1x' % (fp+3))
            sheet.draw(surf, self.x+8*self.dx-16, self.y, 'ic0%1x' % (fp+2))
            
            sheet.draw(surf, self.x, self.y+8*self.dy-8, 'ic0%1x' % (fp+3))
            sheet.draw(surf, self.x+8, self.y+8*self.dy-8, 'ic3%1x' % (fp+1))
            sheet.draw(surf, self.x, self.y+8*self.dy-16, 'ic2%1x' % fp)

            sheet.draw(surf, self.x+8*self.dx-8, self.y+8*self.dy-8, 'ic3%1x' % (fp+3))
            sheet.draw(surf, self.x+8*self.dx-8, self.y+8*self.dy-16, 'ic2%1x' % (fp+3))        
            sheet.draw(surf, self.x+8*self.dx-16, self.y+8*self.dy-8, 'ic3%1x' % (fp+2))

            for xo in range(2, self.dx-2):
                sheet.draw(surf, self.x+8*xo, self.y, 'ic1%1x' % (fp+1)) # top
                sheet.draw(surf, self.x+8*xo, self.y+8*self.dy-8, 'ic2%1x' % (fp+2)) #bottom

            for yo in range(2, self.dy-2):
                sheet.draw(surf, self.x, self.y+8*yo, 'ic2%1x' % (fp+1)) # left
                sheet.draw(surf, self.x+8*self.dx-8, self.y+8*yo, 'ic1%1x' % (fp+2)) # right
            
        # contents
        
        for widget in self.widgets:
            widget.render(surf)
            
def makeDemoCmd(n):
    if n==0:
        return [['text', 'This is a series\nof text boxes.', 'You can dismiss them...', '...and the next will show up\nin order!']]
    else:
        return [['debug', 'Selected Item [%d]' % n]]

def main():
  clock = pygame.time.Clock()

  scr = ceGame.init()

  flat = CEFill(ceColor.hex('000'))

  window = CEWindow(None, None, 0, 0, 32, 11)
  ceGame.addWindow(window)

  for y in range(0,15):
    window.add( CEWMenuItem( int(y/5)*64, 8+(y%5)*16, 'Item %d'%y, makeDemoCmd(y)) )

  linkVertical(window.widgets[0:5])
  linkVertical(window.widgets[5:10])
  linkVertical(window.widgets[10:15])

  linkHorizontal(window.widgets[0:15:5])
  linkHorizontal(window.widgets[1:15:5])
  linkHorizontal(window.widgets[2:15:5])
  linkHorizontal(window.widgets[3:15:5])
  linkHorizontal(window.widgets[4:15:5])
    
  window.selected = window.widgets[0]

  while ceGame.running:
    flat.render(scr, 0, 0, ceGame.XSIZE, ceGame.YSIZE)

    mils = clock.tick(60)

    ceGame.update()
    window.update()

    ceGame.render(scr)
    
if __name__=='__main__':
    main()
