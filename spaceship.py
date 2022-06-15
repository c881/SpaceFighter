class Spaceship:
    def __init__(self, image_path, x, y, width, height, direction, health, colour, bullet_vel, keys=None, bullets=None):
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(image_path),
                                                            (width, height)), direction)
        self.health = health
        self.rect = pg.Rect(x, y,width, height)
        self.colour = colour
        self.bullets = bullets
        self.bullet_vel = bullet_vel
        self.Keys = keys

    def handle_movement(self, key_pressed):
        if key_pressed in self.keys:
            if key_pressed[pg.K_a] and self.rect.x - VEL > 0 or \
                    key_pressed[pg.K_LEFT] and self.rect.x - VEL > BORDER.x + 10:
                self.rect.x -= VEL
            if key_pressed[pg.K_d] and self.rect.x + VEL + self.rect.width < BORDER.x or \
                    key_pressed[pg.K_RIGHT] and self.rect.x + VEL + self.rect.height < WIDTH:
                self.rect.x += VEL
            if key_pressed[pg.K_w] and self.rect.y - VEL > 0 or \
                    key_pressed[pg.K_UP] and self.rect.y - VEL > 0:
                self.rect.y -= VEL
            if key_pressed[pg.K_s] and self.rect.y + 3 * VEL + self.rect.height < HEIGHT or \
                    key_pressed[pg.K_DOWN] and red.rect.y + 3 * VEL + self.rect.height < HEIGHT:
                self.rect.y += VEL

    def handle_bullets(self, target):
        for bullet in self.bullets:
            bullet.x += self.bullet_vel
            if target.rect.colliderect(bullet):
                BULLET_HIT_SOUND.play()
                target.health -= 1
                self.bullets.remove(bullet)
            elif 0 > bullet.x > WIDTH:
                self.bullets.remove(bullet)
