from Settings import *
import sys
from Sprites import *



class Game:
    def __init__(self):
        # Initialize win, game, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        # Start New Game
        pygame.mixer_music.play(-1)
        pygame.mouse.set_visible(False)
        self.bg = Bg(BG2, WIDTH + 100)
        self.bg1 = Bg(BG, 100)
        self.bg2 = Bg(BG2, - WIDTH + 90)
        self.bgs = pygame.sprite.Group(self.bg, self.bg1, self.bg2)
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemies_bullets = pygame.sprite.Group()

        self.player = player(self.screen)
        self.all_sprites.add(self.player)
        self.score = 0
        self.death_delay = 0
        self.start_time = pygame.time.get_ticks()

        for _ in range(mob_num + 1):
            self.m = mob()
            self.mobs.add(self.m)
            self.all_sprites.add(self.m)
        self.run()

    def run(self):
        # Game Loop
        self.go = False
        while not self.go:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop.Update
        self.bgs.update()
        self.player_bullet_delay()
        self.enemy_bullet_delay()
        self.player_collisions()
        self.death()
        self.bullet_collisions()
        self.powerups()
        self.mobs_counter()
        self.all_sprites.update()
    # Update Functions

    def player_bullet_delay(self):
        if self.player.delay == BulletDelay:
            if self.player.shoot():
                if self.player.power == 1:
                    self.all_sprites.add(self.player.b)
                    self.bullets.add(self.player.b)
                    self.player.delay = 0
                if self.player.power >= 2:
                    self.all_sprites.add(self.player.b, self.player.b1)
                    self.bullets.add(self.player.b, self.player.b1)
                    self.player.delay = 0
                if self.player.power >= 3:
                    self.all_sprites.add(self.player.b, self.player.b1, self.player.b2)
                    self.bullets.add(self.player.b, self.player.b1, self.player.b2)
                    self.player.delay = 0
        else:
            self.player.delay += 1

    def enemy_bullet_delay(self):
         for Enemy in self.enemies:
            if Enemy.delay == Enemy.ini_delay:
                if Enemy.shoot(Enemy.rect.centerx, Enemy.rect.bottom + 30):
                    self.all_sprites.add(Enemy.b)
                    self.enemies_bullets.add(Enemy.b)
            else:
                Enemy.delay += 1

    def player_collisions(self):
        # P & M Collision
        self.hits = pygame.sprite.spritecollide(self.player, self.mobs,
                                                True, pygame.sprite.collide_circle)
        for hit in self.hits:
            Hit.play()
            self.player.shield -= hit.radius / Pdefence
            self.exp = Explosion(self.player.rect.centerx, self.player.rect.centery - 5, "sm")
            self.all_sprites.add(self.exp)
            hit.kill()
            if self.player.shield <= 0:
                exp = Explosion(self.player.rect.centerx, self.player.rect.centery, "player")
                self.all_sprites.add(exp)
                death.play()
        # P & E Collision
        hits = pygame.sprite.spritecollide(self.player, self.enemies_bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            self.player.shield -= 10 / Pdefence
            exp = Explosion(self.player.rect.centerx, self.player.rect.top, "sm")
            self.all_sprites.add(exp)
            if self.player.shield < 0:
                exp = Explosion(self.player.rect.centerx, self.player.rect.centery, "player")
                self.all_sprites.add(exp)
                death.play()

    def death(self):
        if self.player.shield <= 0:
            death.play()
            self.player.hidden = True
            self.player.rect.centerx = -500
            self.player.rect.centery = -500
            self.death_delay += 1
            for m in self.mobs:
                exp = Explosion(m.rect.centerx, m.rect.centery, "lg")
                self.all_sprites.add(exp)
                m.kill()
            for e in self.enemies:
                exp = Explosion(e.rect.centerx, e.rect.centery, "lg")
                self.all_sprites.add(exp)
                e.kill()
            if self.death_delay == 70:
                self.player.hidden = False
                self.player.rect.centerx = WIDTH / 2
                self.player.rect.bottom = HEIGHT - 10
                self.player.lives -= 1
                self.player.shield = Pshield
                self.player.power = 1
                self.death_delay = 0
                self.start_time = pygame.time.get_ticks()
        if self.player.lives == 0:
            self.death_delay += 1
            self.player.kill()
            if self.death_delay == 35:
                self.go = True
                self.show_go_screen()

    def bullet_collisions(self):
        # B & M Collision
        self.atts = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for att in self.atts:
            self.exp = Explosion(att.rect.centerx, att.rect.centery, "lg")
            self.all_sprites.add(self.exp)
            random.choice(Expl_snd).play()
            self.score += int((100 - self.m.radius) / 10)
            if pygame.time.get_ticks() - self.start_time > 15000:
                if random.random() <= 0.3 and len(self.enemies) < enemy_num:
                    Enemy = enemy()
                    self.all_sprites.add(Enemy)
                    self.enemies.add(Enemy)

            if pygame.time.get_ticks() - self.start_time > 10000:
                if random.random() <= 0.1:
                    pow = Pow(att.rect.center)
                    if pow.type == "shield":
                        Shield.play()
                    elif pow.type == "gun":
                        Gun.play()
                    elif pow.type == "another life":
                        another_life.play()
                    self.all_sprites.add(pow)
                    self.power_ups.add(pow)
        # B & E Collision
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for hit in hits:
            hit.shield -= 20 * Pstrength
            Hit.play()
            exp = Explosion(hit.rect.centerx, hit.rect.bottom, "sm")
            self.all_sprites.add(exp)
            if hit.shield < 0:
                self.score += 500
                exp = Explosion(hit.rect.centerx, hit.rect.centery, "lg")
                self.all_sprites.add(exp)
                hit.kill()

    def mobs_counter(self):
        if len(self.mobs) < mob_num + 1:
            self.m = mob()
            self.mobs.add(self.m)
            self.all_sprites.add(self.m)

    def powerups(self):
        self.pows = pygame.sprite.spritecollide(self.player, self.power_ups, True)
        for pow in self.pows:
            if pow.type == "shield":
                self.player.shield += random.randrange(10, 40)
                if self.player.shield > Pshield:
                    self.player.shield = Pshield
            if pow.type == "gun":
                self.player.powerup()
            if pow.type == "another life":
                self.player.lives += 1
                if self.player.lives > 5:
                    self.player.lives = 5
            pass

    # Game Parts
    def events(self):
        # Game Loop.Events
        for event in pygame.event.get():
            # QUIT
            if event.type == pygame.QUIT:
                sys.exit(0)

    def draw(self):
        # Game Loop.Draw
        self.bgs.draw(self.screen)
        self.all_sprites.draw(self.screen)
        draw_Text(self.screen, str(self.score), 18, WHITE, WIDTH / 2, 20)
        draw_bar(self.screen, Pshield, 10, GREEN, WHITE, 20, 40, self.player.shield)
        if self.player.power >= 2:
            draw_bar(self.screen, 100, 10, BLUE, WHITE, 20, 60, self.player.power_time / 6)
        for Enemy in self.enemies:
            draw_bar(self.screen, 50, 5, RED, RED, Enemy.rect.left, Enemy.rect.top - 5, Enemy.shield / 4)
        draw_lives(self.screen, WIDTH - 90, 40, self.player.lives, Plife)
        # Flipping After Drawing
        pygame.display.flip()

    def levelSelect(self):
        self.bg = Bg(BG2, WIDTH + 100)
        self.bg1 = Bg(BG, 100)
        self.bg2 = Bg(BG2, - WIDTH + 90)
        self.bgs = pygame.sprite.Group(self.bg, self.bg1, self.bg2)
            # Stuff
        self.btns = pygame.sprite.Group()
        self.play = button((WIDTH / 2, HEIGHT / 6 * 3), "play")
        self.quit = button((WIDTH / 2, HEIGHT / 6 * 5), "quit")
        self.level_select = button((WIDTH / 2, HEIGHT / 6 * 4), "level select")
        self.cursor = cursor()
        self.btns.add(self.play, self.quit, self.level_select)
        self.sprites = pygame.sprite.Group(self.btns, self.cursor)
        pygame.mouse.set_visible(False)

        self.waiting = True
        while self.waiting:
            self.bgs.update()
            self.bgs.draw(self.screen)
            click = pygame.sprite.spritecollideany(self.cursor, self.btns)
            self.sprites.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cursor.image = pygame.transform.scale(Cursor, (25, 27))
                    self.cursor.rect = self.cursor.image.get_rect()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.cursor.image = Cursor
                    self.cursor.rect = self.cursor.image.get_rect()
                if click and event.type == pygame.MOUSEBUTTONUP:
                    if click.btn == "play":
                        self.waiting = False
                        self.new()
                    if click.btn == "quit":
                        sys.exit(0)
                    if click.btn == "select level":
                        self.levelSelect()

            self.sprites.update()
            if click:
                init_center = click.rect.center
                click.image = pygame.transform.scale(click.image, (click.rect.width - 7, click.rect.height - 7))
                click.rect = click.image.get_rect()
                click.rect.center = init_center

    def show_start_screen(self):
        # Game Splash/Start
            # BG
        self.bg = Bg(BG2, WIDTH + 100)
        self.bg1 = Bg(BG, 100)
        self.bg2 = Bg(BG2, - WIDTH + 90)
        self.bgs = pygame.sprite.Group(self.bg, self.bg1, self.bg2)
            # Stuff
        self.btns = pygame.sprite.Group()
        self.play = button((WIDTH / 2, HEIGHT / 6 * 3), "play")
        self.quit = button((WIDTH / 2, HEIGHT / 6 * 5), "quit")
        # self.level_select = button((WIDTH / 2, HEIGHT / 6 * 4), "level select")
        self.cursor = cursor()
        self.btns.add(self.play, self.quit, )#self.level_select)
        self.sprites = pygame.sprite.Group(self.btns, self.cursor)
        pygame.mouse.set_visible(False)

        self.waiting = True
        while self.waiting:
            self.bgs.update()
            self.bgs.draw(self.screen)
            click = pygame.sprite.spritecollideany(self.cursor, self.btns)
            draw_Text(self.screen, "Shoot Them UP", 64, WHITE, WIDTH / 2, HEIGHT / 6)
            draw_Text(self.screen, "Arrow keys to move",
                      35, WHITE, WIDTH / 2, HEIGHT / 6 + 50)
            draw_Text(self.screen, "Space to Shoot", 35, WHITE, WIDTH / 2, HEIGHT / 6 + 80)
            self.sprites.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cursor.image = pygame.transform.scale(Cursor, (25, 27))
                    self.cursor.rect = self.cursor.image.get_rect()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.cursor.image = Cursor
                    self.cursor.rect = self.cursor.image.get_rect()
                if click and event.type == pygame.MOUSEBUTTONUP:
                    if click.btn == "play":
                        self.waiting = False
                        self.new()
                    if click.btn == "quit":
                        sys.exit(0)
                    if click.btn == "level select":
                        self.waiting = False
                        self.levelSelect()

            self.sprites.update()
            if click:
                init_center = click.rect.center
                click.image = pygame.transform.scale(click.image, (click.rect.width - 7, click.rect.height - 7))
                click.rect = click.image.get_rect()
                click.rect.center = init_center

    def show_go_screen(self):
        # Game Over/Continue
        # Game Splash/Start
            # BG
        self.bg = Bg(BG2, WIDTH + 100)
        self.bg1 = Bg(BG, 100)
        self.bg2 = Bg(BG2, - WIDTH + 90)
        self.bgs = pygame.sprite.Group(self.bg, self.bg1, self.bg2)
            # Stuff
        self.btns = pygame.sprite.Group()
        self.play = button((WIDTH / 2, HEIGHT / 6 * 3), "play")
        self.quit = button((WIDTH / 2, HEIGHT / 6 * 5), "quit")
        # self.level_select = button((WIDTH / 2, HEIGHT / 6 * 4), "level select")
        self.cursor = cursor()
        self.btns.add(self.play, self.quit, )#self.level_select)
        self.sprites = pygame.sprite.Group(self.btns, self.cursor)
        pygame.mouse.set_visible(False)

        self.waiting = True
        while self.waiting:
            self.bgs.update()
            self.bgs.draw(self.screen)
            click = pygame.sprite.spritecollideany(self.cursor, self.btns)
            draw_Text(self.screen, "Shoot Them UP", 64, WHITE, WIDTH / 2, HEIGHT / 6)
            draw_Text(self.screen, str(self.score),
                      35, WHITE, WIDTH / 2, HEIGHT / 3)
            self.sprites.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cursor.image = pygame.transform.scale(Cursor, (25, 27))
                    self.cursor.rect = self.cursor.image.get_rect()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.cursor.image = Cursor
                    self.cursor.rect = self.cursor.image.get_rect()
                if click and event.type == pygame.MOUSEBUTTONUP:
                    if click.btn == "play":
                        self.waiting = False
                        self.new()
                    if click.btn == "quit":
                        sys.exit(0)
                    if click.btn == "level select":
                        self.waiting = False
                        self.levelSelect()

            self.sprites.update()
            if click:
                init_center = click.rect.center
                click.image = pygame.transform.scale(click.image, (click.rect.width - 7, click.rect.height - 7))
                click.rect = click.image.get_rect()
                click.rect.center = init_center



g = Game()
g.show_start_screen()
while g.running:
    g.new()
    if g.go:
        g.show_go_screen()

pygame.quit()
