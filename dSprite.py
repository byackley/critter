import pygame
from dSheet import DSheet
from dScript import DScript
import dGame
import dColor
import random # TODO: write own RNG library

class DSprite:
    '''This is a particular instance of a sprite, including position/state data.'''

    def __init__(self, sheetFile, scriptFile):
        self.sheet = DSheet(sheetFile)
        self.timer = 0
        self.vars = {}

        self.currentAnim = ''
        self.currentFrame = 0

        self.script = DScript(scriptFile)
        self.script.init(self)

    def setState(self, name):
        self.state = name
        self.currentAnim = name
        self.currentFrame = 0

    def set(self, name, val):
        self.vars[name] = val

    def get(self, name, default=None):
        if name in self.vars:
            return self.vars[name]
        return default

    def moveTo(self, pos):
        self.set('x', pos[0])
        self.set('y', pos[1])

    def advance(self):
        self.currentFrame = (1+self.currentFrame) % (self.getAnimLength())

    def getAnimLength(self):
        return len(self.sheet.getAnim(self.state))

    def getFramedef(self):
        if (self.currentFrame > self.getAnimLength()):
            print self.currentFrame, self.sheet.getAnim(self.currentAnim)
            return ('', 1000)
        return self.sheet.getAnim(self.currentAnim)[self.currentFrame]

    def update(self, mils):
        self.timer += mils
        frameName, frameTime = self.getFramedef()
        if self.timer > frameTime:
            self.timer -= frameTime
            self.advance()
        self.script.run(self)

    def render(self, surf, camera):
        self.sheet.draw(surf,
            self.get('x')-camera[0], self.get('y')-camera[1], self.getFramedef()[0])

if __name__=='__main__':
  clock = pygame.time.Clock()

  scr = dGame.init()
  sprites = []
  for i in range(256):
      sprites.append( DSprite('iris', 'player') )
      sprites[-1].setState('walk-'+random.choice('nswe'))
      sprites[-1].moveTo( (random.randint(0, 256), random.randint(0, 224)))

  frames = 0

  while dGame.running:
    frames += 1
    scr.fill(dColor.hex('008'))

    mils = clock.tick(60)

    dGame.update()
    # TODO: Game should keep track of sprites and propagate update/render to all

    for sprite in sprites:
        sprite.update(mils)
        sprite.render(scr, dGame.getCamera())

        if sprite.get('x')<-16:
            sprite.set('x',dGame.XSIZE)
        elif sprite.get('x')>dGame.XSIZE:
            sprite.set('x',-16)

        if sprite.get('y')<-16:
            sprite.set('y',dGame.YSIZE)
        elif sprite.get('y')>dGame.YSIZE:
            sprite.set('y',-16)

    dGame.render(scr)

    if frames%100==0:
        print clock.get_fps()
