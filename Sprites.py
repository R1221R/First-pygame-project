from Settings import *
import random


class Bg(pygame.sprite.Sprite):
    def __init__(self, bg, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bg
        self.rect = self.image.get_rect()
        self.rect.bottom = pos

    def update(self):
        self.rect.bottom += 5
        if self.rect.top > WIDTH:
            self.rect.bottom = 0


class bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, owner, facing):
        pygame.sprite.Sprite.__init__(self)
        self.image = Laser[owner][0]
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.facing = facing
        self.owner = owner
        self.rect.centerx = x
        self.speedY = 0 * self.facing
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frameCount = 10

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frameCount:
            self.last_update = now
            self.frame += 1
            if self.frame == 4:
                self.speedY = -20 * self.facing
                self.frameCount = 50
            if self.frame >= 5:
                self.speedY -= 10 * self.facing
            if self.frame == len(Laser[self.owner]):
                self.frameCount = 500000000
            else:
                center = self.rect.center
                self.image = Laser[self.owner][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
        self.rect.y += self.speedY
        if self.rect.bottom < -50 or self.rect.top > HEIGHT + 50:
            self.kill()


class player(pygame.sprite.Sprite):
    def __init__(self, surf):
        self.surface = surf
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(PShip, (50, 30))
        self.rect = self.image.get_rect()
        self.radius = 17
        self.delay = BulletDelay
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedX = 0
        self.vel = 10
        self.shield = Pshield
        self.lives = 1
        self.hidden = False
        self.power = 1
        self.power_time = 1

    def update(self):
        # PowerUP time update
        if self.power >= 2 and self.power_time >= 1:
            self.power_time -= 1
        elif self.power_time == 0:
            self.power_time = 1
            self.power -= 1
        # Moving
        self.speedX = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.speedX = self.vel
        elif keys[pygame.K_LEFT]:
            self.speedX = -self.vel
        self.rect.centerx += self.speedX
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        keys = pygame.key.get_pressed()
        if not self.hidden:
            if keys[pygame.K_SPACE]:
                if self.power < 1:
                    self.power = 1
                if self.power == 1:
                    self.b = bullet(self.rect.centerx, self.rect.top, "player", 1)
                    Laser_sound.play()
                if self.power == 2:
                    self.b = bullet(self.rect.left, self.rect.centery, "player", 1)
                    self.b1 = bullet(self.rect.right, self.rect.centery, "player", 1)
                    Laser_sound.play()
                if self.power >= 3:
                    self.b = bullet(self.rect.left, self.rect.centery, "player", 1)
                    self.b1 = bullet(self.rect.right, self.rect.centery, "player", 1)
                    self.b2 = bullet(self.rect.centerx, self.rect.top, "player", 1)
                    Laser_sound.play()
                    self.power = 3
                return True

    def powerup(self):
        self.power += 1
        self.power_time = PowerupTime


class mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = random.choice(Meteors)
        self.image = self.image_origin.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(4, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-12, 12)
        self.last_update = pygame.time.get_ticks()
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_origin, self.rot)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 50 or self.rect.right < -50 or self.rect.left > WIDTH + 65:
            self.new()

    def new(self):
        self.image = random.choice(Meteors)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(4, 8)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = Explosion_ani[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frameCount = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frameCount:
            self.last_update = now
            self.frame += 1
            if self.frame == len(Explosion_ani[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = Explosion_ani[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        t = random.random()
        if t > 0.97:
            self.type = "another life"
        elif 0.97 > t > 0.3:
            self.type = "gun"
        elif t < 0.3:
            self.type = "shield"
        self.image = Power_ups[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedY = 7

    def update(self):
        self.rect.y += self.speedY
        # kill
        if self.rect.top > HEIGHT + 20:
            self.kill()


class enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(Enemies), (50, 30))
        self.rect = self.image.get_rect()
        self.radius = 17
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = random.randrange(100, 500)
        self.rect.top = -100
        self.speedX = 0
        self.speedY = 0
        self.ini_delay = 70
        self.delay = self.ini_delay
        self.shield = Pshield
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.speedY = 0
        now = pygame.time.get_ticks()
        if now - self.last_update > 300:
            self.last_update = now
            self.speedX = random.choice([-6, 6])
        if self.rect.centery < 100:
            self.speedY = 3
            self.speedX = 0
        self.rect.centerx += self.speedX
        self.rect.top += self.speedY
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedX = -6
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedX = 6
        if self.shield < 0:
            self.kill()


    def shoot(self, x, y):
        if self.delay == self.ini_delay:
            self.b = bullet(x, y, "enemy", -1)
            self.delay = 0
            Laser_sound.play()
            return True


class cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Cursor
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pygame.mouse.get_pos()

    def update(self):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class button(pygame.sprite.Sprite):
    def __init__(self, center, btn):
        pygame.sprite.Sprite.__init__(self)
        self.init_image = Button[btn][0]
        self.btn = btn
        self.image = self.init_image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frameCount = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frameCount:
            self.last_update = now
            self.frame += 1
            if self.frame == len(Button[self.btn]):
                self.frame = 0
                self.init_image = Button[self.btn][0]
            else:
                center = self.rect.center
                self.init_image = Button[self.btn][self.frame]
                self.rect = self.init_image.get_rect()
                self.rect.center = center
        old_center = self.rect.center
        self.image = self.init_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center
