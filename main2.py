from pathlib import Path
import pygame as pg

p = Path(__file__).parent
# Window
WIDTH, HEIGHT = 600, 400
WIN = pg.display.set_mode((WIDTH, HEIGHT))
SPACE = pg.transform.scale(pg.image.load(p.joinpath('Assets', 'space.png')),
                           (WIDTH, HEIGHT))
BORDER = pg.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
pg.font.init()
pg.mixer.init()
pg.display.set_caption("RPG with Nimrod")
HEALTH_FONT = pg.font.SysFont('arial', 40)
WINNER_FONT = pg.font.SysFont('comicsans', 100)
ASDW_KEYS = (pg.K_a, pg.K_d, pg.K_w, pg.K_s)
ARROWS_KEYS = (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN)
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

YELLOW_HIT = pg.USEREVENT + 1
RED_HIT = pg.USEREVENT + 2

# Colors
WHITE = (200, 200, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# We can use os.path.join because of different os use different writing
# We use pathlib, because we are only dealing with Paths
# YELLOW_SPACESHIP = pg.image.load(os.path.join('Assets', 'spaceship_yellow.png'))

class Spaceship:
    def __init__(self, image_path, x, y, direction, vel, health, colour, bullet_vel, event, keys=None,
                 bullets=None, text=''):
        
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(image_path),
                (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), direction)
        self.rect = pg.Rect(x, y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.vel = vel
        self.colour = colour
        self.health = health
        self.bullets = bullets
        self.bullet_vel = bullet_vel
        self.event = event
        self.keys = keys
        self.text = text

    def handle_movement(self, key_pressed):
        if key_pressed in self.keys:
            if key_pressed[pg.K_a] and self.rect.x - self.vel > 0 or \
                 key_pressed[pg.K_LEFT] and self.rect.x - self.vel > BORDER.x + 10:
                self.rect.x -= self.vel
            if key_pressed[pg.K_d] and self.rect.x + self.vel + self.rect.width < BORDER.x or \
                 key_pressed[pg.K_RIGHT] and self.rect.x + self.vel + self.rect.height < WIDTH:
                self.rect.x += self.vel
            if key_pressed[pg.K_w] and self.rect.y - self.vel > 0 or \
                 key_pressed[pg.K_UP] and self.rect.y - self.vel > 0:
                self.rect.y -= self.vel
            if key_pressed[pg.K_s] and self.rect.y + 3 * self.vel + self.rect.height < HEIGHT or \
                 key_pressed[pg.K_DOWN] and self.rect.y + 3 * self.vel + self.rect.height < HEIGHT:
                self.rect.y += self.vel

    def handle_bullets(self, target):
        for bullet in self.bullets:
            bullet.x += self.bullet_vel
            if target.rect.colliderect(bullet):
                BULLET_HIT_SOUND.play()
                target.health -= 1
                self.bullets.remove(bullet)
            elif 0 < bullet.x > WIDTH:
                self.bullets.remove(bullet)

    def fire(self, key):
        if key in (pg.K_LCTRL, pg.K_RCTRL) and len(self.bullets) < MAX_BULLETS:
            if self.colour == YELLOW:
                bullet = pg.Rect(self.rect.x + 5 + self.rect.width, self.rect.y + self.rect.height // 2,
                             BULLET_WIDTH, BULLET_HEIGHT)
            else:
                bullet = pg.Rect(self.rect.x + 5, self.rect.y + self.rect.height // 2, BULLET_WIDTH, BULLET_HEIGHT)

            self.bullets.append(bullet)
            BULLET_FIRE_SOUND.play()


def draw_window(red, yellow):
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pg.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render(f'Health:{red.health}', 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f'Health:{yellow.health}', 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(yellow.image, (yellow.rect.x, yellow.rect.y))
    WIN.blit(red.image, (red.rect.x, red.rect.y))
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
    yellow = Spaceship(p.joinpath('Assets', 'spaceship_yellow.png'), x=WIDTH * 0.25, y=HEIGHT * 0.5,
                       direction=90, vel=VEL, health=10, colour=YELLOW, bullet_vel=BULLET_VEL, event=YELLOW_HIT,
                       keys=ASDW_KEYS, bullets=[],text="Yellow Wins!")
    red = Spaceship(p.joinpath('Assets', 'spaceship_red.png'), WIDTH * 0.75, HEIGHT * 0.5,
                    -90, VEL, 10, RED, -1 * BULLET_VEL, RED_HIT, ARROWS_KEYS, [], "Red Wins!")

    SPACE = pg.transform.scale(
        pg.image.load(p.joinpath('Assets', 'space.png')), (WIDTH, HEIGHT))

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
                if event.key == pg.K_LCTRL:
                    yellow.fire(event.key)
                if event.key == pg.K_RCTRL:
                    red.fire(event.key)

        if red.health < 1:
            draw_winner(yellow.text)
            break
        if yellow.health < 1:
            draw_winner(red.text)
            break

        key_pressed = pg.key.get_pressed()
        yellow.handle_movement(key_pressed)
        red.handle_movement(key_pressed)
        yellow.handle_bullets(red)
        red.handle_bullets(yellow)

        draw_window(red, yellow)
    event.key =''
    main()


if __name__ == "__main__":
    main()
