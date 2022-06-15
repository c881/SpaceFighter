from pathlib import Path
import pygame as pg
from spaceship import Spaceship
p = Path(__file__).parent
# Window
WIDTH, HEIGHT = 600, 400
WIN = pg.display.set_mode((WIDTH, HEIGHT))
BORDER = pg.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
pg.font.init()
pg.mixer.init()
pg.display.set_caption("RPG with Nimrod")
HEALTH_FONT = pg.font.SysFont('arial', 40)
WINNER_FONT = pg.font.SysFont('comicsans', 100)
# Game speed
FPS = 60

# Spaceship
VEL = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Bullets
BULLET_VEL = 10
MAX_BULLETS = 5
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
BULLET_FIRE_SOUND = pg.mixer.Sound('Assets/game-gun-shot.mp3')
BULLET_HIT_SOUND = pg.mixer.Sound('Assets/explosion-01.mp3')

# Colors
WHITE = (200, 200, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# We can use os.path.join because of different os use different writing
# We use pathlib, because we are only dealing with Paths
# YELLOW_SPACESHIP = pg.image.load(os.path.join('Assets', 'spaceship_yellow.png'))


yellow = Spaceship(p.joinpath('Assets', 'spaceship_yellow.png'), WIDTH * 0.25, HEIGHT * 0.5,
                   SPACESHIP_WIDTH, SPACESHIP_HEIGHT, 90, 10, YELLOW, BULLET_VEL, (pg.K_a, pg.K_d, pg.K_w, pg.K_s))
red = Spaceship(p.joinpath('Assets', 'spaceship_red.png'), WIDTH * 0.75, HEIGHT * 0.5,
                SPACESHIP_WIDTH, SPACESHIP_HEIGHT, -90, 10, RED, -1 * BULLET_VEL,
                (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN))

SPACE = pg.transform.scale(
    pg.image.load(p.joinpath('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow):
    WIN.blit(SPACE, (0, 0))
    pg.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render(f'Health:{red.health}', 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f'Health:{yellow.health}', 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(yellow.image, (yellow.rect.x, yellow.rect.y))
    WIN.blit(red.image, (red.rect.x, red.rect.d))
    for bullet in red.bullets:
        pg.draw.rect(WIN, RED, bullet)
    for bullet in yellow.bullets:
        pg.draw.rect(WIN, YELLOW, bullet)
    pg.display.update()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pg.display.update()
    pg.time.delay(5000)


# Dealing with the logic of the game
def main():
    run = True
    winner_text = ""

    # Set the pace of the game
    clock = pg.time.Clock()

    while run:
        # The game will run at FPS time per seconds
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL and len(yellow.bullets) < MAX_BULLETS:
                    bullet = pg.Rect(yellow.rect.x + 5 + SPACESHIP_WIDTH, yellow.rect.y + SPACESHIP_HEIGHT // 2,
                                     BULLET_WIDTH, BULLET_HEIGHT)
                    yellow.bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pg.K_RCTRL and len(red.bullets) < MAX_BULLETS:
                    bullet = pg.Rect(red.rect.x + 5, red.rect.d + SPACESHIP_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT)
                    red.bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

        if red.health < 1:
            winner_text = "Yellow Wins!"
        if yellow.health < 1:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        key_pressed = pg.key.get_pressed()
        yellow.handle_movement(key_pressed)
        red.handle_movement(key_pressed)
        yellow.handle_bullets(red)
        red.handle_bullets(yellow)

        draw_window(red, yellow)
    main()


if __name__ == "__main__":
    main()
