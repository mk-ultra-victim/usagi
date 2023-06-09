import pygame
from pygame import mixer
from fighter import Fighter

pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colors
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
# player scores [p1, p2]
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# define fighter variables
USAGI_SIZE = 1620
USAGI_SCALE = 0.4
USAGI_OFFSET = [720, 560]
USAGI_DATA = [USAGI_SIZE, USAGI_SCALE, USAGI_OFFSET]

# load music and sounds
pygame.mixer.music.load("assets/audio/musicloop01.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)

# load background image
bg_image = pygame.image.load("assets/images/background/bg_1_px.png").convert_alpha()

# load spritesheets
usagi_sheet = pygame.image.load("assets/images/usagi_spritesheet.png").convert_alpha()

# load victory image
victory_img = pygame.image.load("assets/images/ui/victory.png").convert_alpha()

# define number of steps in each animation
USAGI_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]

# define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# load health bar images
health_bar_red = pygame.image.load("assets/images/ui/health_bar_red.png").convert_alpha()
health_bar_bg = pygame.image.load("assets/images/ui/health_bar_bg.png").convert_alpha()

# function for drawing fighter health bars
def draw_health_bar(health, x, y):
    barx = 400
    bary = 30

    pygame.draw.rect(screen, BLACK, (x - 5, y - 5, barx + 10, bary + 10))
    
    ratio = health / 100
    scaled_health_bar_bg = pygame.transform.scale(health_bar_bg, (barx, bary))
    screen.blit(scaled_health_bar_bg, (x, y))
    
    scaled_health_bar_red = pygame.transform.scale(health_bar_red, (barx * ratio, bary))
    screen.blit(scaled_health_bar_red, (x, y))
    

# create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, USAGI_DATA, usagi_sheet, USAGI_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, USAGI_DATA, usagi_sheet, USAGI_ANIMATION_STEPS, sword_fx)

# game loop
run = True
while run:

    clock.tick(FPS)

    # draw background
    draw_bg()

    # show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    if intro_count <= 0:
        # move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_1, round_over)
    else:
        # display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        # update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # update fighters
    fighter_1.update()
    fighter_2.update()
    
    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # display victory image
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 310, False, USAGI_DATA, usagi_sheet, USAGI_ANIMATION_STEPS, sword_fx)
            fighter_2 = Fighter(2, 700, 310, True, USAGI_DATA, usagi_sheet, USAGI_ANIMATION_STEPS, sword_fx)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display
    pygame.display.update()

# exit pygame
pygame.quit()
