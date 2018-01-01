import pygame
from ceWorld import CEWorld

running = True

XSIZE = 256
YSIZE = 224

#FS = True
FS = False

camera = (0, 0) # top left corner of screen in world coords
scale = 2

screen = None
back = None
world = None
timer = 0

windows = []

def debug(st):
    # add logging?
    print('[DEBUG] '+st)

def hasWindow():
    return len(windows) > 0

def addWindow(win):
    windows.append(win)

def delWindow(win):
    global windows
    windows = [w for w in windows if w is not win]

def popWindow():
    global windows
    windows = windows[:-1]

def getCamera():
    return camera

def quit():
    global running
    running = False

def rescale(sc):
    global scale
    scale = sc
    init()

def init():
    global screen, back, world
    pygame.init()
    screen = pygame.display.set_mode((XSIZE*scale, YSIZE*scale), pygame.FULLSCREEN if FS else 0)
    back = pygame.Surface((XSIZE, YSIZE))
    world = CEWorld()
    return back

def update():
    global timer
    timer += 1
    # TODO: make this use the abstraction instead
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT or (ev.type == pygame.KEYUP and ev.key == pygame.K_ESCAPE):
            quit()
        if ev.type == pygame.KEYDOWN and hasWindow():
            windows[-1].update(ev.key)

def render(surf):
    global screen, windows
    
    for win in windows:
        win.render(surf)

    pygame.transform.scale(surf, (XSIZE*scale, YSIZE*scale), screen)
    pygame.display.flip()

if __name__=='__main__':
    surf = init()
    while running:
        update()
        render(surf)
