from pygame import Color

cache = [[[Color(r*17, g*17, b*17) for b in range(16)] for g in range(16)] for r in range(16)]

def hex(str):
    r = int(str[0],16)
    g = int(str[1],16)
    b = int(str[2],16)
    return cache[r][g][b]

def darker(col):
    return Color(int(col.r/2), int(col.g/2), int(col.b/2))

def lighter(col):
    return Color(127, 127, 127)+darker(col)
