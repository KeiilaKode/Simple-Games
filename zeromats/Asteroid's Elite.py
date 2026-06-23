# Imports
import pygame
from pygame import mixer
from random import randint
from time import time as timer
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Game Constants
WIDTH = 900
HEIGHT = 750
FPS = 65
GOAL = 20
MAX_LOSS = 10
BULLET_LIMIT = 10
RELOAD_TIME = 3


# Text Font
FONT_LARGE = pygame.font.Font(None, 36)
FONT_MEDIUM = pygame.font.Font(None, 36)
WIN_TEXT = FONT_LARGE.render("You Win!", True, (255, 255, 255))
LOSE_TEXT = FONT_LARGE.render("You lose!", True, (220, 30, 30))

# Game Music
pygame.mixer.music.load("soong.wav")
pygame.mixer.music.play()

# Shooting sound
FIRE_SOUND = pygame.mixer.Sound("gunshot.mp3")

# Game Settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Elite")
clock = pygame.time.Clock()

# Load background and Fit to screen
bg = pygame.image.load("skysky.jpg")
background = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Load bullet, player, and enemy images
IMG_BULLET = pygame.image.load("player bullet beam 1.png").convert_alpha()
IMG_PLAYER = pygame.image.load("Fireflyfly.png").convert_alpha()

# Enemies
IMG_ALIEN1 = pygame.image.load("alien ship 1.png").convert_alpha()
IMG_ALIEN2 = pygame.image.load("alien ship 2.png").convert_alpha()
IMG_ALIEN3 = pygame.image.load("alien ship 3.png").convert_alpha()
IMG_ALIEN4 = pygame.image.load("alien ship 4.png").convert_alpha()
IMG_ALIEN5 = pygame.image.load("alien ship 5.png").convert_alpha()
IMG_ALIEN6 = pygame.image.load("alien ship 6.png").convert_alpha()
IMG_ALIEN7 = pygame.image.load("alien ship 7.png").convert_alpha()
IMG_ALIEN8 = pygame.image.load("alien ship 8.png").convert_alpha()

# Asteroids
IMG_ASTEROID1 = pygame.image.load("asteroid 1.png").convert_alpha()
IMG_ASTEROID2 = pygame.image.load("asteroid 2.png").convert_alpha()

# Game Classes
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, img, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.transform.scale(img, (width, height))
                                                                       #self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def reset(self):
        screen.blit(self.image, self.rect.topleft)

class Player(GameSprite):

    # Function to move player
    def controls(self):
        keys = pygame.key.get_pressed()
        # Left
        if keys[pygame.K_a] and self.rect.left > 5:
            self.rect.x -= self.speed
        # Right
        if keys[pygame.K_d] and self.rect.right < WIDTH - 5:
            self.rect.x += self.speed
        # Up
        if keys[pygame.K_w] and self.rect.bottom > 50:
            self.rect.y -= self.speed
        # Down
        if keys[pygame.K_s] and self.rect.top < HEIGHT - 50:
            self.rect.y += self.speed

    # Function to shoot
    def shoot(self):
        pass


# Enemy Class
class Alien(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = randint(80, WIDTH - 80)
            self.rect.y = -40

# Helper Function

def spawn_enemies():
    for _ in range(2):
        monsters.add(Alien(IMG_ALIEN5, randint(80, WIDTH - 80), -40, 90, 60, randint(1, 5)))
    for _ in range(2):
        monsters.add(Alien(IMG_ALIEN1, randint(80, WIDTH - 80), -40, 90, 60, randint(1, 5)))
    for _ in range(2):
        monsters.add(Alien(IMG_ALIEN2, randint(80, WIDTH - 80), -40, 90, 60, randint(1, 5)))
    for _ in range(2):
        monsters.add(Alien(IMG_ALIEN3, randint(80, WIDTH - 80), -40, 90, 60, randint(1, 5)))
    for _ in range(2):
        monsters.add(Alien(IMG_ALIEN4, randint(80, WIDTH - 80), -40, 90, 60, randint(1, 5)))
    for _ in range(2):
        asteroids.add(Alien(IMG_ASTEROID1, randint(80, WIDTH - 80), -40, 60, 30, randint(1, 5)))


# TEST LOADING CHARACTERS
player = Player(IMG_PLAYER, 200, 200, 150, 180, 8) # 200, 200, 150, 180, 8)
monsters = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
spawn_enemies()

# While loop
bob = True
while bob:

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            bob = False

    screen.blit(background, (0, 0))
    player.reset()
    monsters.draw(screen)
    asteroids.draw(screen)

    player.controls()
    monsters.update()
    asteroids.update()

    pygame.display.update()
    clock.tick(FPS)


