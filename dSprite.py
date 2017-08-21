import pygame
from dSheet import DSheet
from dScript import DScript
import dGame
import dColor

class DSprite:
    '''This is a particular instance of a sprite, including position/state data.'''

    def __init__(self, sheetFile, scriptFile):
        self.sheet = DSheet(sheetFile)
        self.timer = 0

        self.currentAnim = ''
        self.currentFrame = 0

        self.currentState = ''
        self.script = DScript(scriptFile)

    def setAnimation(self, name):
        self.currentAnim = name
        self.currentFrame = 0

    def moveTo(self, pos):
        self.x, self.y = pos

    def advance(self):
        self.currentFrame = (1+self.currentFrame) % (self.getAnimLength())

    def getAnimLength(self):
        return len(self.sheet.getAnim(self.currentAnim))

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

    def render(self, surf, camera):
        self.sheet.draw(surf, self.x-camera[0], self.y-camera[1], self.getFramedef()[0])

if __name__=='__main__':
  clock = pygame.time.Clock()

  scr = dGame.init()
  sprites = []
  for i in range(4):
      sprites.append( DSprite('iris', 'player') )

  sprites[0].setAnimation('walk-n')
  sprites[1].setAnimation('walk-s')
  sprites[2].setAnimation('walk-w')
  sprites[3].setAnimation('walk-e')

  sprites[0].moveTo( (100, 80) )
  sprites[1].moveTo( (100, 120) )
  sprites[2].moveTo( (80, 100) )
  sprites[3].moveTo( (120, 100) )

  while dGame.running:
    scr.fill(dColor.hex('008'))

    mils = clock.tick(60)

    dGame.update()
    # TODO: Game should keep track of sprites and propagate update/render to all

    for i in range(4):
        sprites[i].update(mils)
        sprites[i].render(scr, dGame.getCamera())

    dGame.render(scr)

    print clock.get_fps()
