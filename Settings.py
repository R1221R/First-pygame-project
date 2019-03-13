import pygame, random

pygame.mixer.init()

from os import path

# Screen settings
WIDTH = 500
HEIGHT = 600
FPS = 60
TITLE = "TEST"
# Useful Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# Func


def draw_Text(surf, text, size, color, x, y):
    font = pygame.font.SysFont('spantaran', size)
    text_surface = font.render(text, False, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)


def draw_bar(surf, length, height, f_color, s_color, x, y, pct):
    if pct < 0:
        pct = 0
    Bar_Length = length
    Bar_height = height
    fill = pct
    outline_rect = pygame.Rect(x, y, Bar_Length, Bar_height)
    fill_rect = pygame.Rect(x, y, fill, Bar_height)
    pygame.draw.rect(surf, f_color, fill_rect)
    pygame.draw.rect(surf, s_color, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 15 * i
        img_rect.y = y
        surf.blit(img, img_rect)


# Code & Files
mob_num = 8
enemy_num = 2
Pshield = 100
Pdefence = 1
Pstrength = 1
BulletDelay = 15
PowerupTime = 10 * FPS
# Pics
img_dir = path.join(path.dirname(__file__), 'img')
BG = pygame.image.load(path.join(img_dir, "BG.png"))
BG2 = pygame.image.load(path.join(img_dir, "BG2.png"))
PShip = pygame.image.load(path.join(img_dir, "Pship.png"))
Plife = pygame.image.load(path.join(img_dir, "playerLife.png"))
Cursor = pygame.image.load(path.join(img_dir, "cursor.png"))

Meteors = [pygame.image.load(path.join(img_dir, "Meteors\\MB_1.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\MB_2.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\MB_3.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\MB_4.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\MM_1.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\MM_2.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\MS_1.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\MS_2.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\MS_3.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\MS_4.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\GB_1.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\GB_2.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\GB_3.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\GB_4.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\GM_1.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\GM_2.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\GS_1.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\GS_2.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\GS_3.png")),
           pygame.image.load(path.join(img_dir, "Meteors\\GS_4.png"))]

Laser = {
    "player": [pygame.image.load(path.join(img_dir, "Laser\\laserRed01.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserRed02.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserRed03.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserRed04.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserRed05.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserRed06.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserRed07.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserRed07.png"))],
    "enemy": [pygame.image.load(path.join(img_dir, "Laser\\laserBlue01.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserBlue02.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserBlue03.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserBlue04.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserBlue05.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserBlue06.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserBlue07.png")),
         pygame.image.load(path.join(img_dir, "Laser\\laserBlue07.png"))]}

Explosion_ani = {
                "sm": [pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion00.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion01.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion02.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion03.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion04.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion05.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion06.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion07.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion08.png"))],
                "lg": [pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion00.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion01.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion02.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion03.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion04.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion05.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion06.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion07.png")),
                       pygame.image.load(path.join(img_dir, "Explosion\\regularExplosion08.png"))],
                "player": [pygame.image.load(path.join(img_dir, "Explosion\\sonicExplosion00.png")),
                           pygame.image.load(path.join(img_dir, "Explosion\\sonicExplosion01.png")),
                           pygame.image.load(path.join(img_dir, "Explosion\\sonicExplosion02.png")),
                           pygame.image.load(path.join(img_dir, "Explosion\\sonicExplosion03.png")),
                           pygame.image.load(path.join(img_dir, "Explosion\\sonicExplosion04.png")),
                           pygame.image.load(path.join(img_dir, "Explosion\\sonicExplosion05.png")),
                           pygame.image.load(path.join(img_dir, "Explosion\\sonicExplosion06.png")),
                           pygame.image.load(path.join(img_dir, "Explosion\\sonicExplosion07.png")),
                           pygame.image.load(path.join(img_dir, "Explosion\\sonicExplosion08.png"))]}

Enemies = [pygame.image.load(path.join(img_dir, "Enemies\\enemyBlue1.png")),
           pygame.image.load(path.join(img_dir, "Enemies\\enemyBlue2.png")),
           pygame.image.load(path.join(img_dir, "Enemies\\enemyBlue3.png")),
           pygame.image.load(path.join(img_dir, "Enemies\\enemyBlue4.png")),
           pygame.image.load(path.join(img_dir, "Enemies\\enemyBlue5.png"))]

Button = {
    "play": [pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000001.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000002.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000003.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000004.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000005.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000006.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000007.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000008.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000009.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000010.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000011.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000012.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000013.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000014.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000015.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000016.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000017.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000018.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000019.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000020.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000021.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000022.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000023.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000024.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000025.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000026.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000027.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000028.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000029.png")),
             pygame.image.load(path.join(img_dir, "play button 300x80 hover\\Play button 300x80 hover000030.png"))],
    "quit": [pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000001.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000002.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000003.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000004.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000005.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000006.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000007.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000008.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000009.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000010.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000011.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000012.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000013.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000014.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000015.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000016.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000017.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000018.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000019.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000020.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000021.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000022.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000023.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000024.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000025.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000026.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000027.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000028.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000029.png")),
             pygame.image.load(path.join(img_dir, "Quit button 300x80 hover\\Quit button 300x80 hover000030.png"))],
    "level select": [pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000001.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000002.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000003.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000004.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000005.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000006.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000007.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000008.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000009.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000010.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000011.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000012.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000013.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000014.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000015.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000016.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000017.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000018.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000019.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000020.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000021.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000022.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000023.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000024.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000025.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000026.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000027.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000028.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000029.png")),
             pygame.image.load(path.join(img_dir, "level select button 300x80 hover\\level select button 300x80 hover000030.png"))]}

Power_ups = {"shield": pygame.image.load(path.join(img_dir, "Pow\\shield.png")),
             "gun": pygame.image.load(path.join(img_dir, "Pow\\speed.png")),
             "another life": pygame.image.load(path.join(img_dir, "Pow\\life.png"))}

for i in range(len(Explosion_ani["lg"])):
    Explosion_ani["lg"][i] = pygame.transform.scale(Explosion_ani["lg"][i], (75, 75))
for i in range(len(Explosion_ani["sm"])):
    Explosion_ani["sm"][i] = pygame.transform.scale(Explosion_ani["sm"][i], (25, 25))

# Sounds
snd_dir = path.join(path.dirname(__file__), 'snd')
pygame.mixer_music.load(path.join(snd_dir, 'mp3.mp3'))
pygame.mixer_music.set_volume(0.4)
Laser_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
Laser_sound.set_volume(0.5)
Shield = pygame.mixer.Sound(path.join(snd_dir, 'shield.wav'))
Gun = pygame.mixer.Sound(path.join(snd_dir, 'gun.wav'))
another_life = pygame.mixer.Sound(path.join(snd_dir, 'another life.wav'))
Hit = pygame.mixer.Sound(path.join(snd_dir, 'hit.wav'))
death = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
Expl_snd = []
for i in range(4):
    expl = pygame.mixer.Sound(path.join(snd_dir, 'Explosion%s.wav' %i))
    Expl_snd.append(expl)

