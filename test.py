from Settings import *
from Sprites import *




pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
running = True
sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemies_bullets = pygame.sprite.Group()


class mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = random.choice(Meteors)
        self.image = self.image_origin.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = WIDTH / 2
        self.rect.y = random.randrange(-150, -100)
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
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 50 or self.rect.right < -50 or self.rect.left > WIDTH + 65:
            self.new()

    def new(self):
        self.image = random.choice(Meteors)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)


class player(pygame.sprite.Sprite):
    def __init__(self):
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
        self.shield = 100

    def update(self):
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

    def shoot(self, x, y):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.b = bullet(x, y, "player", 1)
            Laser_sound.play()
            return True


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
        self.shield = 100
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




player = player()
sprites.add(player)


for i in range(3):
    Enemy = enemy()
    sprites.add(Enemy)
    enemies.add(Enemy)

while running:
        clock.tick(FPS)
        # Game Loop.Events
        for event in pygame.event.get():
            # QUIT
            if event.type == pygame.QUIT:
                running = False
        if player.delay == BulletDelay:
            if player.shoot(player.rect.centerx, player.rect.top):
                sprites.add(player.b)
                bullets.add(player.b)
                player.delay = 0
        else:
            player.delay += 1
        for Enemy in enemies:
            if Enemy.delay == Enemy.ini_delay:
                if Enemy.shoot(Enemy.rect.centerx, Enemy.rect.bottom + 30):
                    sprites.add(Enemy.b)
                    enemies_bullets.add(Enemy.b)
            else:
                Enemy.delay += 1
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for hit in hits:
            hit.shield -= 20
            Hit.play()
            exp = Explosion(hit.rect.centerx, hit.rect.bottom, "sm")
            sprites.add(exp)
            if hit.shield < 0:
                exp = Explosion(hit.rect.centerx, hit.rect.centery, "lg")
                sprites.add(exp)
                hit.kill()
        hits = pygame.sprite.spritecollide(player, enemies_bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= 20
            exp = Explosion(player.rect.centerx, player.rect.top, "sm")
            sprites.add(exp)
            if player.shield < 0:
                exp = Explosion(player.rect.centerx, player.rect.centery, "player")
                sprites.add(exp)

        sprites.update()
        screen.fill(BLACK)
        sprites.draw(screen)
        for Enemy in enemies:
            draw_bar(screen, 50, 5, RED, RED, Enemy.rect.left, Enemy.rect.top - 5, Enemy.shield / 4)
        pygame.display.flip()
