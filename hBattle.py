import ceGame
import ceWindow
import ceSheet
import pygame
import ceColor

verbs = ['attack', 'magic', 'items', 'tact', 'act']
cursor = 0
cTimer = 0

def makeStatusString(bits):
    return '`#b7' * 6

def battleWindow(pName, x):
    return ceWindow.CEWindow(0, None,
        '%6s\n%6s\n`i80%3d/\n   %3d\n`i81%2d/%2d' % (
            ceGame.world.get('players/%s/name' % pName),
            makeStatusString(ceGame.world.get('players/%s/status' % pName)),
            ceGame.world.get('players/%s/hp' % pName),
            ceGame.world.get('players/%s/hpmax' % pName),
            ceGame.world.get('players/%s/cp' % pName),
            ceGame.world.get('players/%s/cp' % pName),
        ), x, 176, 8, 8)

def setBattleStats(pName, name, hp, hpmax, cp, cpmax):
    ceGame.world.set('players/%s/name' % pName, name)
    ceGame.world.set('players/%s/hp' % pName, hp)
    ceGame.world.set('players/%s/hpmax' % pName, hpmax)
    ceGame.world.set('players/%s/cp' % pName, cp)
    ceGame.world.set('players/%s/cpmax' % pName, cpmax)

if __name__=='__main__':

    scr = ceGame.init()
    
    enemy = ceSheet.CESheet('battle/001')
    actions = ceSheet.CESheet('battle/actions')
    
    enemy.register(0, '00f', '66f')
    enemy.register(1, '3f9', 'f93')
    enemy.register(2, '93f', '777')
    enemy.register(3, '222', 'f00')
    
    setBattleStats('p1', 'Foo', 100, 120, 90, 99)
    setBattleStats('p2', 'Bar', 4, 4, 10, 20)
    setBattleStats('p3', 'Whomp', 922, 923, 0, 0)
    setBattleStats('p4', 'Abcdefghi', 100, 200, 30, 40)

    clock = pygame.time.Clock()

    windows = [
        battleWindow('p1', 0), battleWindow('p2', 64), 
        battleWindow('p3', 128), battleWindow('p4', 192),
        ceWindow.CEWindow(0, None, ' 1234567890 1234567890 1234567890\n'+' Text goes here', -16, 96, 36, 8)
    ]

    while ceGame.running:
        scr.fill(ceColor.hex('000'))

        enemy.draw(scr, 32, 32, None, 0)
        enemy.draw(scr, 80, 32, None, 1)
        enemy.draw(scr, 128, 32, None, 2)
        enemy.draw(scr, 176, 32, None, 3)
        
        for n, verb in enumerate(verbs):
            actions.draw(scr, n*48, 160, verb+('1' if cursor==n else '0'))
        
        for window in windows:
            window.render(scr)

        clock.tick(60)

        cTimer += 1
        if cTimer % 60 == 0:
            cursor = (1+cursor)%5

        ceGame.update()
        ceGame.render(scr)
        
'''
NOTES:

stats are Attack, Defense, Magic, and Flair (need new names)

Use the Priority Queue idea for turn order
current turn = queue[0]
entity at queue[0] chooses an action, is requeued at now+time(action)

'''
