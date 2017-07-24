import pygame
import random

import dGame
import dColor

cache = {}
frames = {} # filename -> {frame name -> (x, y, dx, dy)}

WHITE = dColor.hex('FFF')

class DSheet:
    def __init__(self, fn):
        self.image = pygame.image.load('rsrc/sprite/'+fn+'.png').convert()
        self.name = fn
        self.image.set_colorkey(dColor.hex('000'))
        frames[fn] = {}

        for line in open('rsrc/sprite/'+fn+'.txt'):
            spl = line.split()
            if len(spl)>1:
                frames[fn][spl[0]] = map(int, spl[1:])

        print frames[fn]

    def draw(self, surf, drawX, drawY, frame=None, col=-1):
        if frame:
            x, y, dx, dy = frames[self.name][frame]
        else:
            x, y, dx, dy = 0, 0, self.image.get_width(), self.image.get_height()
        if col==-1:
            surf.blit(self.image, (drawX, drawY), (x, y, dx, dy))
        else:
            surf.blit(cache[(self.name, col)], (drawX, drawY), (x, y, dx, dy))

    def register(self, n, c1, c2):
        pixArray = pygame.PixelArray(self.image.copy())
        pixArray.replace( dColor.hex('F00'), c1, 0.05 )
        pixArray.replace( dColor.hex('0F0'), c2, 0.05 )

        pixArray.replace( dColor.hex('800'), dColor.darker(c1), 0.05 )
        pixArray.replace( dColor.hex('080'), dColor.darker(c2), 0.05 )

        pixArray.replace( dColor.hex('F88'), dColor.lighter(c1), 0.05 )
        pixArray.replace( dColor.hex('8F8'), dColor.lighter(c2), 0.05 )

        newSurf = pixArray.make_surface()
        newSurf.set_colorkey(dColor.hex('000'))

        cache[(self.name, n)] = newSurf

if __name__=='__main__':
    clock = pygame.time.Clock()

    scr = dGame.init()
    sprite = DSheet('iris')

    while dGame.running:
        scr.fill(dColor.hex('008'))
        for i in xrange(1,800):
            sprite.draw(scr,
                random.random()*dGame.XSIZE,
                random.random()*dGame.YSIZE,
                'walk-s1')
        clock.tick(60)

        dGame.update()
        dGame.render(scr)

        print clock.get_fps()
