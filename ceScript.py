import re
import pygame
import ceGame
import ceColor
from ceControl import *
from ceSprite import *
import ceText
import ceStage
import ceWindow

def parseStateDef(cmds):
    out = ([],[])
    for cmd in cmds:
        if ':' in cmd:
            out[1].append(tuple([x.strip() for x in cmd.split(':', 1)]))
        else:
            out[0].append(cmd.strip().split(' '))
    return out

re_num = re.compile('\d+')

def getValue(val, sprite):
    if val[0]=='@':
        return sprite.get(val[1:])
    elif val[0]=='-':
        return -getValue(val[1:], sprite)
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
    ']': c_NEXT,
    '0': c_0,
    '1': c_1,
    '2': c_2,
    '3': c_3,
    '4': c_4,
    '5': c_5,
    '6': c_6,
    '7': c_7,
    '8': c_8,
    '9': c_9,
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

def runCmd(cmd, sprite=None):
    if cmd is None or len(cmd)==0:
        return
        
    if cmd[0]=='set':
        sprite.set(cmd[1], int(cmd[2]))
    elif cmd[0]=='inc':
        sprite.set(cmd[1], sprite.get(cmd[1]) + getValue(cmd[2], sprite))
    elif cmd[0]=='dec':
        sprite.set(cmd[1], sprite.get(cmd[1]) - getValue(cmd[2], sprite))
    elif cmd[0]=='mv': # move, checking physics
        sprite.move(getValue(cmd[1], sprite), getValue(cmd[2], sprite))
    elif cmd[0]=='map': # place sprite on new map
        sprite.stage = ceStage.CEStage(cmd[1])
        sprite.moveTo( ( int(cmd[2])*16, int(cmd[3])*16 ) )
    elif cmd[0]=='sfx': # play sound effect
        pass
    elif cmd[0]=='music': # switch music
        pass
    elif cmd[0]=='close': # close current window
        ceGame.popWindow()
    elif cmd[0]=='text': # add sequence of text boxes
        for box in cmd[-1:0:-1]: # backwards from the end, for correct order
            window = ceWindow.CEWindow(1, ceWindow.MAIN_BG, 0, 0, 32, 11)
            for n,line in enumerate(box.split('\n')):
                window.add(ceWindow.CEWText(0, 8+16*n, line))
            window.add(ceWindow.CEWCloseButton(232, 72))
            print(window)
            ceGame.addWindow(window)
    elif cmd[0]=='debug':
        ceGame.debug(','.join(cmd[1:]))
    else:
        ceGame.debug('Unknown command: '+cmd)
        
class CEScript(object):
    def __init__(self, fn=None):
        self.states = {} # map of state name to (instructions, transitions)
        if fn is None:
            return
        script = open('rsrc/script/'+fn+'.sct').read().strip()
        stateDefs = [x.strip().split('\n') for x in script.split('//')]

        for stateDef in stateDefs:
            if stateDef[0] == '*':
                common = parseStateDef(stateDef[1:])
                for state in list(self.states.keys()):
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
            runCmd(cmd, sprite)
        for trig in sdef[1]:
            cond, dest = trig
            if checkCondition(cond, sprite):
                if dest == '!': # special notation for 'run map trigger'
                    coord = '%s %s' % (int(sprite.get('x')/16), int(sprite.get('y')/16))
                    if coord in sprite.stage.scripts:
                        script = sprite.stage.scripts[coord].split(' ')
                        runCmd(script, sprite)
                else:
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
