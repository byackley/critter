import json
import pygame
from ceEntity import CEEntity
from ceSprite import CESprite
import ceColor
import ceText
import ceGame

def rowToInts(row):
    return [int(s) for s in row.split()]

def clamp(val, mn, mx):
    if val<mn:
        return mn
    elif val>mx:
        return mx
    else:
        return val

class CEStage(CEEntity):

    def __init__(self, fn):
        super(CEStage, self).__init__()
        data = json.load( open('rsrc/stage/'+fn+'.json') )

        self.tileset = pygame.image.load( 'rsrc/sprite/tiles/' + data['tileset']+'.png' )
        self.tiledata = json.load( open('rsrc/sprite/tiles/' + data['tileset'] + '.json'))
        self.tiledata['walls'] = set(self.tiledata['walls'])


        print self.tiledata['walls']

        self.tileWidth = self.tileset.get_width()/16

        self.tiles = [[rowToInts(row) for row in layer] for layer in data['tiles']]
        self.name = data['name']
        self.music = data['music']
        self.animations = data['animations']

        self.timer = 0
        self.aspeed = data['anim-speed']
        self.aframe = 0

    def update(self, mils):
        self.timer += mils
        if self.timer > self.aspeed:
            self.aframe += 1
            self.timer -= self.aspeed

    def isWall(self, layer, x, y):
        return self.tiles[layer][y][x] in self.tiledata.walls

    def render(self, surf, camSprite):

        camx = clamp(
            camSprite.get('x') - ceGame.XSIZE/2, 0, 16*len(self.tiles[0][0]) - ceGame.XSIZE)
        camy = clamp(
            camSprite.get('y') - ceGame.YSIZE/2, 0, 16*len(self.tiles[0]) - ceGame.YSIZE)

        tilex = int(camx/16)+1
        ox = 16-camx%16
        tiley = int(camy/16)+1
        oy = 16-camy%16

        for layer in xrange(len(self.tiles)):
            for xpos in xrange(-1,16):
                for ypos in xrange(-1,14):
                    try:
                        tNum = self.tiles[layer][ypos+tiley][xpos+tilex]
                        if tNum<0:
                            # this is an animation
                            frames = self.animations[-tNum-1]['frames']
                            tNum = frames[self.aframe % len(frames)]

                    except IndexError:
                        continue
                    surf.blit(self.tileset,
                        (ox+xpos*16, oy+ypos*16),
                        (16*(tNum%self.tileWidth), 16*int(tNum/self.tileWidth), 16, 16))

        return (camx, camy)


    def _drawTile(self, surf, n, x, y):
        tileX = 16*(n % self.tileWidth)
        tileY = 16*(n / self.tileWidth)
        surf.blit(self.tileset, (x, y), (tileX, tileY, 16, 16))

def main():
  clock = pygame.time.Clock()

  scr = ceGame.init()
  sprites = []

  sprites.append( CESprite('iris', 'player-grid16') )
  sprites[-1].setState('stand-n')
  sprites[-1].moveTo( (12*16, 24*16) )

  sprites[-1].set('collideWall', True)
  sprites[-1].set('collideOther', False)

  stage = CEStage('temple')

  frames = 0

  while ceGame.running:
    frames += 1
    scr.fill(ceColor.hex('008'))

    mils = clock.tick(60)

    ceGame.update()
    # TODO: Game should keep track of sprites and propagate update/render to all
    stage.update(mils)

    sprites.sort(key=(lambda s:s.get('y')))

    (camx, camy) = stage.render(scr, sprites[-1])

    for sprite in sprites:
        sprite.update(mils)
        sprite.render(scr, camx, camy)

    ceGame.render(scr)

if __name__=='__main__':
    main()
