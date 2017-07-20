import pygame
import random

import dGame
import dColor

cache = {}

WHITE = dColor.hex('FFF')

class DSheet:
    def __init__(self, fn):
        self.image = pygame.image.load('rsrc/'+fn+'.png').convert()
        self.name = fn
        self.image.set_colorkey(dColor.hex('000'))

    def draw(self, surf, x, y, n=-1):
        if n==-1:
            surf.blit(self.image, (x,y))
        else:
            surf.blit(cache[(self.name, n)], (x,y))

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
    sprite = DSheet('test-sprite')
    sprite.register(0, dColor.hex('00F'), dColor.hex('999'))
    sprite.register(1, dColor.hex('44F'), dColor.hex('0e0'))
    sprite.register(2, dColor.hex('123'), dColor.hex('ABC'))

    while dGame.running:
        scr.fill(dColor.hex('008'))
        for i in xrange(1,800):
            sprite.draw(scr,
                random.random()*dGame.XSIZE,
                random.random()*dGame.YSIZE,
                int(random.random()*3))
        clock.tick(60)

        dGame.update()
        dGame.render(scr)

        print clock.get_fps()
