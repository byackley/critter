import pygame
import ceSheet
import ceGame
import math
import random

sheet = None
icons = None

colors = [
    ('FFF', '888', '444'),
    ('00F', '008', '004'),
    ('2F2', '181', '040'),
    ('0FF', '088', '044'),
    ('F00', '800', '400'),
    ('F0F', '808', '404'),
    ('FF0', '880', '440'),
    ('F80', '840', '420'),
    ('F08', '804', '402'),
    ('08F', '048', '024'),
    ('0F8', '084', '042'),
    ('80F', '408', '204'),
    ('8F0', '480', '240'),
]

def drawText(surf, text, x, y, c1='FFF', c2='444'):
    global sheet, icons, colors
    
    if icons is None:
        icons = ceSheet.CESheet('font/icons')
        
    if sheet is None:
        sheet = ceSheet.CESheet('font/8x8-00')
        for n, col in enumerate(colors):
            sheet.register(n, col[0], col[2])
            sheet.register(n+16, col[1], col[2])

    pos = 0
    color = 0
    baseColor = 0
    state = 0
    cmd = ''
    arg = 0
    
    flash = False
    wobble = False
    wave = False
    
    for ch in text:  
        
        xo = 0
        yo = 0
              
        if wobble:        
            xo += random.randint(-1, 2)
            yo += random.randint(-1, 2)
        if wave:
            yo += int(2.5*math.sin(pos + ceGame.timer / 5.0))
        if flash and ceGame.timer % 40 > 20:
            color = baseColor ^ 16
        else:
            color = baseColor
            
        if state == 1:
            cmd = ch
            arg = 0
            state = 2
        elif state == 2:
            arg += 16*int(ch,16)
            state = 3
        elif state == 3:
            arg += int(ch,16)
            state = 0
            if cmd == 'c': # color
                baseColor = arg
            elif cmd == 'i': # icon
                pos += 1
                icons.draw(surf, x+8*pos+xo, y+yo, 'ic%02x' % arg)
            elif cmd == '#': # character by position
                pos += 1
                sheet.draw(surf, x+8*pos+xo, y+yo, 'ch%02x' % arg, color)
            elif cmd == 'w': # wobble
                wobble = not wobble
            elif cmd == 'v': # wave
                wave = not wave
            elif cmd == 'f': # flash
                flash = not flash
        else:
            if ch=='`':
                state = 1 # wait for 3-character command
            else:
                pos += 1
                sheet.draw(surf, x+8*pos+xo, y+yo, 'ch%02x' % ord(ch), color)

if __name__=='__main__':
    ceGame.init()

    out = file('rsrc/sprite/font/8x8-00.txt', 'w')
    for x in xrange(256):
        out.write('ch%02x %d %d 8 8\n' % (x, 8*(x%16), 8*(x//16)))

    out = file('rsrc/sprite/font/icons.txt', 'w')
    for x in xrange(256):
        out.write('ic%02x %d %d 8 8\n' % (x, 8*(x%16), 8*(x//16)))
