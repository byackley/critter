import pygame

running = True

XSIZE = 320
YSIZE = 240

FS = False

camera = (0, 0) # top left corner of screen in world coords

scale = 3

screen = None
back = None

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
    global screen, back
    pygame.init()
    screen = pygame.display.set_mode((XSIZE*scale, YSIZE*scale), pygame.FULLSCREEN if FS else 0)
    back = pygame.Surface((XSIZE, YSIZE))
    return back

def update():
    # TODO: make this use the abstraction instead
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT or (ev.type == pygame.KEYUP and ev.key == pygame.K_ESCAPE):
            quit()

def render(surf):
    global screen

    pygame.transform.scale(surf, (XSIZE*scale, YSIZE*scale), screen)
    pygame.display.flip()

if __name__=='__main__':
    surf = init()
    while running:
        update()
        render(surf)
