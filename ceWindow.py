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
            ceText.drawText(surf, line, self.x+16, self.y+16+16*nLine)

        sheet.draw(surf, self.x, self.y, 'ic00')
        sheet.draw(surf, self.x+8*self.dx-8, self.y, 'ic02')
        sheet.draw(surf, self.x, self.y+8*self.dy-8, 'ic11')
        sheet.draw(surf, self.x+8*self.dx-8, self.y+8*self.dy-8, 'ic13')

        for xo in range(1, self.dx-1):
            sheet.draw(surf, self.x+8*xo, self.y, 'ic01')
            sheet.draw(surf, self.x+8*xo, self.y+8*self.dy-8, 'ic12')

        for yo in range(1, self.dy-1):
            sheet.draw(surf, self.x, self.y+8*yo, 'ic10')
            sheet.draw(surf, self.x+8*self.dx-8, self.y+8*yo, 'ic03')


def main():
  clock = pygame.time.Clock()

  scr = ceGame.init()

  flat = CEFill(ceColor.hex('008'))
  grad = CEFillGradient(ceColor.hex('33C'), ceColor.hex('003'))

  lines = [
    ''.join(chr(x) for x in range(32))+'\n'+
    ''.join(chr(x) for x in range(128,160))
  ]

  window = CEWindow(0, grad, '\n'.join(lines), 0, 0, 32, 11)

  while ceGame.running:
    flat.render(scr, 0, 0, ceGame.XSIZE, ceGame.YSIZE)
    window.render(scr)

    mils = clock.tick(60)

    ceGame.update()

    ceGame.render(scr)

if __name__=='__main__':
    main()
