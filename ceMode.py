import json
import pygame
from ceEntity import CEEntity
from ceSprite import CESprite
import ceColor
import ceText
import ceGame
import ceStage

sprites = []
clock = pygame.time.Clock()
stage = None

def update():
    global sprites, stage

    mils = clock.tick(60)

    ceGame.update()
    if stage != None:
        stage.update(mils)

    sprites.sort(key=(lambda s:s.get('y')))

    for sprite in sprites:
        sprite.update(mils)

def render(scr):
    global stage, sprites

    if stage == None:
        return

    (camx, camy) = stage.render(scr, sprites[-1])

    for sprite in sprites:
        sprite.update(mils)
        sprite.render(scr, camx, camy)

    ceGame.render(scr)

def main():
    global sprites

    scr = ceGame.init()

    iris = CESprite('iris', 'player-grid16')
    iris.setState('stand-n')
    iris.moveTo( (12*16, 24*16) )

    iris.set('collideWall', True)
    iris.set('collideOther', False)

    stage = ceStage.CEStage('temple')

    iris.stage = stage

    sprites.append( iris )

    while ceGame.running:
        update()
        render(scr)

if __name__=='__main__':
    main()
