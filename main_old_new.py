# import pygame library
import pygame

# initialize pygame
pygame.init()

# get screen resolution
display_info = pygame.display.Info()
screen_width = display_info.current_w
screen_height = display_info.current_h
screen_resolution = (screen_width, screen_height)

# display window
window = pygame.display.set_mode(screen_resolution)
pygame.display.set_caption('Game')

# create clock, set FPS to 60
clock = pygame.time.Clock()
FPS = 60

# if window is fullscreen
fullscreen = False

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            handle_key(event.key)

def handle_key(key):
    if key == pygame.K_F11:
        global fullscreen
        fullscreen = not fullscreen
        if fullscreen:
            window = pygame.display.set_mode(screen_resolution, pygame.FULLSCREEN)
        else:
            window = pygame.display.set_mode(screen_resolution)

levels = []
            
# game loop
while True:

    # event handler
    handle_inputs()


    # cap FPS, then update screen
    clock.tick(FPS)
    pygame.display.update()
