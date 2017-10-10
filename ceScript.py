import re
import pygame
import ceGame
import ceColor
from ceControl import *
from ceSprite import *
import ceText

def parseStateDef(cmds):
    out = ([],[])
    for cmd in cmds:
        if ':' in cmd:
            out[1].append(tuple(map(lambda x:x.strip(), cmd.split(':', 1))))
        else:
            out[0].append(cmd.strip().split(' '))
    return out

re_num = re.compile('\d+')

def getValue(val, sprite):
    if val[0]=='@':
        return sprite.get(val[1:])
    elif re_num.match(val):
        return int(val)
    else:
        return 0

keymap = {
    '^': c_UP,
    'v': c_DOWN,
    '<': c_LEFT,
    '>': c_RIGHT,
    'A': c_A,
    'B': c_B,
    'X': c_X,
    'Y': c_Y,
    'L': c_L,
    'R': c_R,
    'S': c_START,
    '[': c_PREV,
    ']': c_NEXT
}

def checkCondition(conds, spr):
    out = True

    for cond in conds.split():
        if cond[0]=='+': # check for keydown
            if cond[1] in keymap:
                out = out and isDown(keymap[cond[1]])
        elif cond[0]=='-': # check for keyup
            if cond[1] in keymap:
                out = out and isUp(keymap[cond[1]])
        elif cond[0]=='%': # check for mod-16==0
            #print spr.get(cond[1:])
            out = out and (spr.get(cond[1:]) % 16 == 0)
    return out

class CEScript(object):
    def __init__(self, fn):
        self.states = {} # map of state name to (instructions, transitions)
        script = open('rsrc/script/'+fn+'.sct').read().strip()
        stateDefs = map(lambda x: x.strip().split('\n'), script.split('//'))

        for stateDef in stateDefs:
            if stateDef[0] == '*':
                common = parseStateDef(stateDef[1:])
                for state in self.states.keys():
                    self.states[state][0].extend(common[0])
                    self.states[state][1].extend(common[1])
            else:
                self.states[stateDef[0]] = parseStateDef(stateDef[1:])

    def init(self, sprite):
        self.runState('init', sprite)

    def run(self, sprite):
        self.runState(sprite.state, sprite)

    def runState(self, state, sprite):
        sdef = self.states[state]
        for cmd in sdef[0]:
            if cmd[0]=='set':
                sprite.set(cmd[1], int(cmd[2]))
            elif cmd[0]=='inc':
                sprite.set(cmd[1], sprite.get(cmd[1]) + getValue(cmd[2], sprite))
            elif cmd[0]=='dec':
                sprite.set(cmd[1], sprite.get(cmd[1]) - getValue(cmd[2], sprite))
            elif cmd[0]=='mvx':
                sprite.move(int(cmd[1]), 0)
            elif cmd[0]=='mvy':
                sprite.move(0, int(cmd[1]))
            elif cmd[0]=='mvxy':
                sprite.move(int(cmd[1]), int(cmd[2]))
        for trig in sdef[1]:
            cond, dest = trig
            if checkCondition(cond, sprite):
                sprite.setState(dest)
                break

def main():
  clock = pygame.time.Clock()

  scr = ceGame.init()
  sprites = []

  sprites.append( CESprite('iris', 'player') )
  sprites[-1].setState('stand-w')
  sprites[-1].moveTo( (random.randint(0, ceGame.XSIZE), random.randint(0, ceGame.YSIZE)))

  frames = 0

  while ceGame.running:
    frames += 1
    scr.fill(ceColor.hex('008'))

    mils = clock.tick(60)

    ceGame.update()
    # TODO: Game should keep track of sprites and propagate update/render to all

    sprites.sort(key=(lambda s:s.get('y')))

    for sprite in sprites:
        sprite.update(mils)
        sprite.render(scr, ceGame.getCamera())

    ceText.drawText(scr, sprite.state, 0, 0)
    ceText.drawText(scr, 'fps=%5.1f' % clock.get_fps(), 0, 8)

    ceGame.render(scr)

if __name__=='__main__':
    main()
