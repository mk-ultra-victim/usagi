import pygame

pygame.init()

display_info = pygame.display.Info()
screen_width = display_info.current_w
screen_height = display_info.current_h
screen_resolution = (screen_width, screen_height)

window = pygame.display.set_mode(screen_resolution)
pygame.display.set_caption("Game")

clock = pygame.time.Clock()
FPS = 60

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

game = Usagi_Game()

while True:
    handle_inputs()

    game.update()

    clock.tick(FPS)
    pygame.display.update()
