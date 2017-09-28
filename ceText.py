import pygame
import ceSheet
import ceGame

sheet = None
# icons = (load icon/gfx sheet)

def drawText(surf, text, x, y, c1='FFF', c2='444'):
    global sheet
    if sheet==None:
        sheet = ceSheet.CESheet('font/8x8-00')
        sheet.register(0, 'FFF', '444')
    for n,ch in enumerate(text):
        sheet.draw(surf, x+8*n, y, 'ch%02x' % ord(ch), 0)

if __name__=='__main__':
    ceGame.init()

    out = file('rsrc/sprite/font/8x8-00.txt', 'w')
    for x in xrange(256):
        out.write('ch%02x %d %d 8 8\n' % (x, 8*(x%16), 8*(x//16)))

    out = file('rsrc/sprite/font/icons.txt', 'w')
    for x in xrange(256):
        out.write('ic%02x %d %d 8 8\n' % (x, 8*(x%16), 8*(x//16)))
