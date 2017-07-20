from pygame import Color

cache = [[[Color(r*17, g*17, b*17) for b in xrange(16)] for g in xrange(16)] for r in xrange(16)]

def hex(str):
    r = int(str[0],16)
    g = int(str[1],16)
    b = int(str[2],16)
    return cache[r][g][b]

def darker(col):
    return Color(col.r/2, col.g/2, col.b/2)

def lighter(col):
    return Color(127, 127, 127)+darker(col)
