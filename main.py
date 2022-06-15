from pathlib import Path
import pygame as pg

# Window
WIDTH, HEIGHT = 600, 400
WIN = pg.display.set_mode((WIDTH, HEIGHT))
BORDER = pg.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
pg.font.init()
pg.mixer.init()
pg.display.set_caption("RPG with Nimrod")
HEALTH_FONT = pg.font.SysFont('arial', 40)
# Game speed
FPS = 60

# Spaceship
VEL = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Bullets
BULLET_VEL = 10
MAX_BULLETS = 5
BULLET_WIDTH, BULLET_HEIGHT = 5, 10

YELLOW_HIT = pg.USEREVENT + 1
RED_HIT = pg.USEREVENT + 2

# Colors
WHITE = (200, 200, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
YELLOW = (255,255,0)

p = Path(__file__).parent

# We can use os.path.join because of different os use different writing
# We use pathlib, because we are only dealing with Paths
# YELLOW_SPACESHIP = pg.image.load(os.path.join('Assets', 'spaceship_yellow.png'))

class Spaceship:
    def __init__(image_path, width, height, direction, health, bullets=None):
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(image_path),(width, height)),direction)
        self.width = width
        self.height = height
        self.health = health
        self.bullets = bullets
            

YELLOW_SPACESHIP = pg.transform.rotate(pg.transform.scale(
    pg.image.load(p.joinpath('Assets', 'spaceship_yellow.png')), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP = pg.transform.rotate(pg.transform.scale(
    pg.image.load(p.joinpath('Assets', 'spaceship_red.png')), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

SPACE = pg.transform.scale(
    pg.image.load(p.joinpath('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.fill(WHITE)
    WIN.blit(SPACE,(0,0))
    pg.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render(f'Health:{red_health}',1,WHITE)
    yellow_health_text = HEALTH_FONT.render(f'Health:{yellow_health}',1,WHITE)
    WIN.blit(red_health_text, (WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in red_bullets:
        pg.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pg.draw.rect(WIN, YELLOW, bullet)
    pg.display.update()


def yellow_handle_movement(key_pressed, yellow):
    if key_pressed[pg.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if key_pressed[pg.K_d] and yellow.x + VEL + SPACESHIP_WIDTH < BORDER.x:
        yellow.x += VEL
    if key_pressed[pg.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if key_pressed[pg.K_s] and yellow.y + 3 * VEL + SPACESHIP_HEIGHT < HEIGHT:
        yellow.y += VEL


def red_handle_movement(key_pressed, red):
    if key_pressed[pg.K_LEFT] and red.x - VEL > BORDER.x + 10:
        red.x -= VEL
    if key_pressed[pg.K_RIGHT] and red.x + VEL + SPACESHIP_WIDTH < WIDTH:
        red.x += VEL
    if key_pressed[pg.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if key_pressed[pg.K_DOWN] and red.y + 3 * VEL + SPACESHIP_HEIGHT < HEIGHT:
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pg.event.post(pg.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pg.event.post(pg.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


# Dealing with the logic of the game
def main():
    run = True
    red_health = 10
    yellow_health = 10
    winner_text = ""

    # Set the pace of the game
    clock = pg.time.Clock()

    # red = pg.Rect(x,y,width, height)
    red = pg.Rect(WIDTH*0.75, HEIGHT*0.5, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pg.Rect(WIDTH*0.25, HEIGHT*0.5, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets = []
    red_bullets = []

    while run:
        # The game will run at FPS time per seconds
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pg.Rect(yellow.x + 5 + SPACESHIP_WIDTH, yellow.y + SPACESHIP_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                if event.key == pg.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pg.Rect(red.x + 5, red.y + SPACESHIP_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1
        if red_health < 1:
            winner_text = "Yellow Wins!"
        if yellow_health < 1:
            winner_text = "Red Wins!"
        if winner_text != "":
            run = False
        

        key_pressed = pg.key.get_pressed()
        yellow_handle_movement(key_pressed, yellow)
        red_handle_movement(key_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)


if __name__ == "__main__":
    main()
