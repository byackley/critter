import pygame
import random

import ceGame
import ceColor

cache = {}
frames = {} # filename -> {frame name -> (x, y, dx, dy)}

WHITE = ceColor.hex('FFF')

def parseFrame(st):
    spl = st.split(',')
    return (spl[0], int(spl[1]))

class CESheet:
    def __init__(self, fn):
        self.image = pygame.image.load('rsrc/sprite/'+fn+'.png').convert()
        self.name = fn
        self.image.set_colorkey(ceColor.hex('000'))
        self.frames = {}
        self.anims = {}

        mode = 0
        for line in open('rsrc/sprite/'+fn+'.txt'):
            if line[0]=='#':
                mode += 1
                continue

            spl = line.split()
            if mode == 0:
                if len(spl)>1:
                    self.frames[spl[0]] = map(int, spl[1:])
            elif mode == 1:
                self.anims[ spl[0] ] = map(parseFrame, spl[1:])

    def getAnim(self, name):
        if name in self.anims:
            return self.anims[name]
        else:
            return []

    def draw(self, surf, drawX, drawY, frame=None, col=-1):
        if frame:
            x, y, dx, dy = self.frames[frame]
        else:
            x, y, dx, dy = 0, 0, self.image.get_width(), self.image.get_height()
        if col==-1:
            surf.blit(self.image, (drawX, drawY), (x, y, dx, dy))
        else:
            surf.blit(cache[(self.name, col)], (drawX, drawY), (x, y, dx, dy))

    def isFrame(self, name):
        return name in self.frames

    def frameNames(self):
        return self.frames.keys()

    def register(self, n, c1, c2):
        pixArray = pygame.PixelArray(self.image.copy())
        pixArray.replace( ceColor.hex('F00'), c1, 0.05 )
        pixArray.replace( ceColor.hex('0F0'), c2, 0.05 )

        pixArray.replace( ceColor.hex('800'), ceColor.darker(c1), 0.05 )
        pixArray.replace( ceColor.hex('080'), ceColor.darker(c2), 0.05 )

        pixArray.replace( ceColor.hex('F88'), ceColor.lighter(c1), 0.05 )
        pixArray.replace( ceColor.hex('8F8'), ceColor.lighter(c2), 0.05 )

        newSurf = pixArray.make_surface()
        newSurf.set_colorkey(ceColor.hex('000'))

        cache[(self.name, n)] = newSurf

if __name__=='__main__':
    clock = pygame.time.Clock()

    scr = ceGame.init()
    sprite = CESheet('iris')

    while ceGame.running:
        scr.fill(ceColor.hex('008'))
        for i in xrange(1,800):
            sprite.draw(scr,
                random.random()*ceGame.XSIZE,
                random.random()*ceGame.YSIZE,
                random.choice(sprite.frameNames()))
        clock.tick(60)

        ceGame.update()
        ceGame.render(scr)

        print clock.get_fps()
