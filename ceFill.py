import pygame
import ceGame
import ceColor

class CEFill(object):
    def __init__(self, color):
        self.color = color

    def render(self, surf, x, y, dx, dy):
        surf.fill(self.color, pygame.Rect(x, y, dx, dy))

GRADIENT_STEPS = 8

def quantize(n):
    return n - (n%17)

class CEFillGradient(CEFill):
    def __init__(self, c1, c2):
        dr = c2.r - c1.r
        dg = c2.g - c1.g
        db = c2.b - c1.b
        self.colors = [pygame.Color(
                        quantize(c1.r + (dr * n / GRADIENT_STEPS)),
                        quantize(c1.g + (dg * n / GRADIENT_STEPS)),
                        quantize(c1.b + (db * n / GRADIENT_STEPS))
                        ) for n in range(GRADIENT_STEPS)]

    def render(self, surf, x, y, dx, dy):
        height = dy/GRADIENT_STEPS
        for n in range(GRADIENT_STEPS):
            surf.fill( self.colors[n], pygame.Rect(x, y+n*height, dx, height))

def main():
  clock = pygame.time.Clock()

  scr = ceGame.init()

  flat = CEFill(ceColor.hex('147'))
  grad = CEFillGradient(ceColor.hex('55d'), ceColor.hex('002'))

  while ceGame.running:
    flat.render(scr, 0, 0, ceGame.XSIZE/2, ceGame.YSIZE/2)
    grad.render(scr, ceGame.XSIZE/2, ceGame.YSIZE/2, ceGame.XSIZE/2, ceGame.YSIZE/2)

    mils = clock.tick(60)

    ceGame.update()

    ceGame.render(scr)

if __name__=='__main__':
    main()
