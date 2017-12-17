import pygame
from ceFill import CEFillGradient, CEFill
from ceEntity import CEEntity
import ceSheet
import ceText
import ceGame
import ceColor

sheet = None

class CEWindow(CEEntity):
    def __init__(self, frame=0, bg=None, text='', x=0, y=0, dx=32, dy=6, sfx=None):
        global sheet

        if sheet == None:
            sheet = ceSheet.CESheet('font/icons')

        self.frame = frame
        self.text = text
        self.bg = bg
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.sfx = None # TODO: make pitch-variable sound object

    def render(self, surf):
        if self.bg:
            self.bg.render(surf, self.x+8, self.y+8, (self.dx-2)*8, (self.dy-2)*8)
        for nLine, line in enumerate(self.text.split('\n')):
            ceText.drawText(surf, line, self.x, self.y+16+16*nLine)

        sheet.draw(surf, self.x, self.y, 'ic04')
        sheet.draw(surf, self.x+8, self.y, 'ic05')
        sheet.draw(surf, self.x, self.y+8, 'ic14')
        
        sheet.draw(surf, self.x+8*self.dx-8, self.y, 'ic34')
        sheet.draw(surf, self.x+8*self.dx-8, self.y+8, 'ic17')
        sheet.draw(surf, self.x+8*self.dx-16, self.y, 'ic06')
        
        sheet.draw(surf, self.x, self.y+8*self.dy-8, 'ic07')
        sheet.draw(surf, self.x+8, self.y+8*self.dy-8, 'ic35')
        sheet.draw(surf, self.x, self.y+8*self.dy-16, 'ic24')

        sheet.draw(surf, self.x+8*self.dx-8, self.y+8*self.dy-8, 'ic37')
        sheet.draw(surf, self.x+8*self.dx-8, self.y+8*self.dy-16, 'ic27')        
        sheet.draw(surf, self.x+8*self.dx-16, self.y+8*self.dy-8, 'ic36')

        for xo in range(2, self.dx-2):
            sheet.draw(surf, self.x+8*xo, self.y, 'ic15') # top
            sheet.draw(surf, self.x+8*xo, self.y+8*self.dy-8, 'ic26') #bottom

        for yo in range(2, self.dy-2):
            sheet.draw(surf, self.x, self.y+8*yo, 'ic25') # left
            sheet.draw(surf, self.x+8*self.dx-8, self.y+8*yo, 'ic16') # right


def main():
  clock = pygame.time.Clock()

  scr = ceGame.init()

  flat = CEFill(ceColor.hex('000'))
  grad = CEFillGradient(ceColor.hex('33C'), ceColor.hex('003'))

  lines = [
    'The beast codes frames with',
    '   text `c01inside`c00',
    'A decent size, but not that',
    '   `c01wide...`c00 `i74'
  ]

  window = CEWindow(0, flat, '\n'.join(lines), 0, 0, 32, 11)

  while ceGame.running:
    flat.render(scr, 0, 0, ceGame.XSIZE, ceGame.YSIZE)
    window.render(scr)

    mils = clock.tick(60)

    ceGame.update()

    ceGame.render(scr)

if __name__=='__main__':
    main()
