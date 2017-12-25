import ceGame
import ceWindow
import ceSheet
import pygame
import ceColor

verbs = ['attack', 'magic', 'items', 'tact', 'act']
cursor = 0
cTimer = 0

if __name__=='__main__':

    scr = ceGame.init()
        
    enemy = ceSheet.CESheet('battle/001')
    actions = ceSheet.CESheet('battle/actions')
    
    enemy.register(0, '00f', '66f')
    enemy.register(1, '3f9', 'f93')
    enemy.register(2, '93f', '777')
    enemy.register(3, '222', 'f00')

    clock = pygame.time.Clock()

    windows = [
        ceWindow.CEWindow(0, None, ' Zero \n`#b7`#b7`#b7`#b7`#b7`#b7\n`i80904/\n   999\n`i8125/47 ', 0, 176, 8, 8),
        ceWindow.CEWindow(0, None, ' Juli \n`#b7`#b7`#b7`#b7`#b7`#b7\n`i80557/\n   600\n`i8132/53 ', 64, 176, 8, 8),
        ceWindow.CEWindow(0, None, 'Claire\n`#b7`#b7`#b7`#b7`#b7`#b7\n`i80420/\n   420\n`i81 5/90 ', 128, 176, 8, 8),
        ceWindow.CEWindow(0, None, 'Bri`#e8le\n`#b7`#b7`#b7`#b7`#b7`#b7\n`i80 11/\n   999\n`i81 1/99 ', 192, 176, 8, 8),
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

'''
