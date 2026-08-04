import pygame
import sys
import random
import os
from pygame import mixer

# Initialize mixer and pygame
mixer.init()
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Succi Slipped")

# Sets Frame Rate
clock = pygame.time.Clock()
FPS = 60

# Load Music and Sounds
try:
    pygame.mixer.music.load("Satie_Gnossienne_1.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1, 0.0)
    jump_fx = pygame.mixer.Sound("Swoosh.mp3")
    jump_fx.set_volume(0.3)
    death_fx = pygame.mixer.Sound("Pause.mp3")
    death_fx.set_volume(0.6)
except pygame.error:
    pass

# Game Variables
gravity = 1500.0
max_platforms = 40
game_over = False
score = 0

# High score loading
if os.path.exists("score.txt"):
    with open("score.txt", "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

# Define colors & fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (253, 117, 234)
font_small = pygame.font.SysFont("Lucida Sans", 20)
font_big = pygame.font.SysFont("Lucida Sans", 24)

# Load Images with Correct Extensions
try:
    bg_img = pygame.image.load("cross_bg.png").convert()
    bg_flip_img = pygame.image.load("cross_bg_flip.png").convert()
    floor_img = pygame.image.load("floor2.PNG").convert()
    platform_image = pygame.image.load("plat31c.png").convert_alpha()
    bird_sheet_img = pygame.image.load("demon_sprite_sheet_3.png").convert_alpha()
except pygame.error as e:
    print(f"Error loading image assets: {e}")
    pygame.quit()
    sys.exit()

# Scale Backgrounds and Floor
bg_scale_ratio = SCREEN_HEIGHT / bg_img.get_height()
bg_w = int(bg_img.get_width() * bg_scale_ratio)
bg_img = pygame.transform.smoothscale(bg_img, (bg_w, SCREEN_HEIGHT))
bg_flip_img = pygame.transform.smoothscale(bg_flip_img, (bg_w, SCREEN_HEIGHT))

floor_img.set_colorkey((0, 0, 0))
target_floor_h = 200
floor_scale_ratio = target_floor_h / floor_img.get_height()
floor_w = int(floor_img.get_width() * floor_scale_ratio)
floor_img = pygame.transform.smoothscale(floor_img, (floor_w, target_floor_h))
floor_flip_img = pygame.transform.flip(floor_img, True, False)


# SpriteSheet Class
class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        image.set_colorkey(colour)
        return image


bird_sheet = SpriteSheet(bird_sheet_img)


# Enemy (Bat) Class supporting multi-directional spawns and pixel masks
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_pos, y, sprite_sheet, scale, forced_direction=None):
        super().__init__()
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # Allow forced direction from left or right, or choose randomly
        self.direction = forced_direction if forced_direction is not None else random.choice([-1, 1])
        self.flip = (self.direction == 1)

        animation_steps = 3
        frame_width = bird_sheet_img.get_width() // animation_steps
        frame_height = bird_sheet_img.get_height()

        for animation in range(animation_steps):
            image = sprite_sheet.get_image(animation, frame_width, frame_height, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False)
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)

        self.image = self.animation_list[self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y

    def update(self, camera_x):
        animation_cooldown = 125
        self.image = self.animation_list[self.frame_index]

        # Update mask as frames animate
        self.mask = pygame.mask.from_surface(self.image)

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        self.rect.x += self.direction * 4

        # Remove if off screen relative to camera view
        if self.rect.right < camera_x - 400 or self.rect.left > camera_x + SCREEN_WIDTH + 400:
            self.kill()


# Platform Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.transform.scale(platform_image, (width, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        pass


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_panel():
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, PINK, (0, 30), (SCREEN_WIDTH, 30), 2)
    draw_text("SCORE: " + str(score), font_small, WHITE, 10, 5)


def get_sprites_from_sheet(filename, approx_width=810, target_h=1080):
    try:
        sheet = pygame.image.load(filename).convert_alpha()
    except pygame.error as e:
        print(f"Unable to load sprite sheet image: {filename}")
        raise SystemExit(e)

    sheet_width, sheet_height = sheet.get_size()
    if sheet_height == target_h - 1:
        padded = pygame.Surface((sheet_width, target_h), pygame.SRCALPHA)
        padded.fill((0, 0, 0, 0))
        padded.blit(sheet, (0, 0))
        sheet = padded
        sheet_width, sheet_height = sheet.get_size()

    num_frames = round(sheet_width / approx_width)
    if num_frames < 1:
        num_frames = 1
    exact_sprite_width = sheet_width // num_frames

    sprites = []
    for i in range(num_frames):
        sprite = pygame.Surface((exact_sprite_width, sheet_height), pygame.SRCALPHA).convert_alpha()
        rect_to_copy = (i * exact_sprite_width, 0, exact_sprite_width, sheet_height)
        sprite.blit(sheet, (0, 0), rect_to_copy)
        if sheet_height != target_h:
            sprite = pygame.transform.smoothscale(sprite, (exact_sprite_width, target_h))
        sprites.append(sprite)
    return sprites


# Load character animations
animations = {
    "idle": get_sprites_from_sheet("S_IDLE_NB.png"),
    "walk": get_sprites_from_sheet("S_WALK_NB.png"),
    "run": get_sprites_from_sheet("S_RUN_NB.png"),
    "jump": get_sprites_from_sheet("S_JUMP_NB.png"),
    "run_jump": get_sprites_from_sheet("S_RUN_JUMP_NB.png"),
    "duck": get_sprites_from_sheet("S_DUCK_NB.png")
}

animation_speeds = {"idle": 175, "walk": 130, "run": 75, "jump": 80, "run_jump": 50, "duck": 50}
animation_loops = {"idle": True, "walk": True, "run": True, "jump": False, "run_jump": False, "duck": False}
animation_scale_corrections = {"idle": 1.0, "walk": 1.08, "run": 1.08, "jump": 1.0, "run_jump": 1.08, "duck": 1.0}

# Game world states & physics variables
x = 400.0
y_ground = 730.0
y = y_ground
vx = 0.0
vy = 0.0
speed_walk = 180.0
speed_run = 320.0
jump_impulse = -800.0
on_ground = True
facing_right = True

camera_x = 0.0
LEFT_DEAD_ZONE = SCREEN_WIDTH * 0.25
RIGHT_DEAD_ZONE = SCREEN_WIDTH * 0.75

current_anim = "idle"
current_frame = 0
animation_timer = 0
playing = True

platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

starting_platform = Platform(200, 580, 180)
platform_group.add(starting_platform)
platform_group.add(Platform(550, 480, 200))
platform_group.add(Platform(900, 380, 160))

# Main Game Loop
run = True
while run:
    dt_ms = clock.tick(FPS)
    dt = dt_ms / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not game_over:
        keys = pygame.key.get_pressed()
        moving = False
        run_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        duck_pressed = keys[pygame.K_DOWN]

        recovering_duck = (current_anim == "duck" and not duck_pressed and playing)

        if recovering_duck or (duck_pressed and on_ground):
            vx = 0
        elif keys[pygame.K_LEFT]:
            facing_right = False
            moving = True
            vx = - (speed_run if run_pressed else speed_walk)
        elif keys[pygame.K_RIGHT]:
            facing_right = True
            moving = True
            vx = (speed_run if run_pressed else speed_walk)
        else:
            vx = 0

        if keys[pygame.K_SPACE] and on_ground and not duck_pressed and not recovering_duck:
            if moving and "run_jump" in animations:
                current_anim = "run_jump"
            else:
                current_anim = "jump"
            current_frame = 0
            animation_timer = 0
            playing = True
            vy = jump_impulse
            on_ground = False
            try:
                jump_fx.play()
            except:
                pass

        x += vx * dt

        if not on_ground:
            vy += gravity * dt
            y += vy * dt

            for platform in platform_group:
                if vy > 0 and platform.rect.colliderect(x - 20, y - 5, 40, 10):
                    if y - vy * dt <= platform.rect.top + 10:
                        y = platform.rect.top
                        vy = 0
                        on_ground = True
                        break

            if y >= y_ground:
                y = y_ground
                vy = 0
                on_ground = True
        else:
            on_platform = False
            for platform in platform_group:
                if platform.rect.colliderect(x - 20, y, 40, 5):
                    on_platform = True
                    break
            if not on_platform and y < y_ground:
                on_ground = False

        if not on_ground:
            pass
        elif recovering_duck:
            pass
        elif duck_pressed:
            if current_anim != "duck":
                current_anim = "duck"
                current_frame = 0
                animation_timer = 0
                playing = True
        elif moving:
            if run_pressed and "run" in animations:
                if current_anim != "run":
                    current_anim = "run"
                    current_frame = 0
                    animation_timer = 0
                    playing = True
            else:
                if "walk" in animations and current_anim != "walk":
                    current_anim = "walk"
                    current_frame = 0
                    animation_timer = 0
                    playing = True
        else:
            if "idle" in animations and current_anim != "idle":
                current_anim = "idle"
                current_frame = 0
                animation_timer = 0
                playing = True

        screen_x = x - camera_x
        if screen_x > RIGHT_DEAD_ZONE:
            camera_x += (screen_x - RIGHT_DEAD_ZONE)
        elif screen_x < LEFT_DEAD_ZONE:
            camera_x -= (LEFT_DEAD_ZONE - screen_x)

        # Clear platforms that have scrolled off-screen to the left so generation never stops
        for platform in list(platform_group):
            if platform.rect.right < camera_x - 4000:
                platform.kill()

        # Continuously generate platforms ahead of the camera
        if len(platform_group) < max_platforms:
            last_platform = max(platform_group, key=lambda p: p.rect.x, default=None)
            if last_platform:
                p_x = last_platform.rect.x + random.randint(250, 400)
            else:
                p_x = camera_x + SCREEN_WIDTH + 100
            p_w = random.randint(140, 220)
            p_y = random.randint(320, 620)
            platform_group.add(Platform(p_x, p_y, p_w))

        # Increase max bats on screen to 5 and randomize spawn side (left or right)
        if len(enemy_group) < 5 and random.randint(1, 60) == 1:
            spawn_side = random.choice(["left", "right"])
            enemy_y = random.randint(200, 550)
            if spawn_side == "left":
                # Spawn off-screen to the left, moving right
                spawn_x = camera_x - 150
                enemy = Enemy(spawn_x, enemy_y, bird_sheet, 1.5, forced_direction=1)
            else:
                # Spawn off-screen to the right, moving left
                spawn_x = camera_x + SCREEN_WIDTH + 150
                enemy = Enemy(spawn_x, enemy_y, bird_sheet, 1.5, forced_direction=-1)
            enemy_group.add(enemy)

        enemy_group.update(camera_x)
        score = int(x)

        anim_frames = animations[current_anim]
        delay = animation_speeds.get(current_anim, 120)
        loop = animation_loops.get(current_anim, True)
        animation_timer += dt_ms

        if current_anim == "duck" and duck_pressed:
            if current_frame >= 6:
                current_frame = 6
                animation_timer = 0

        if current_anim == "jump" and not on_ground:
            if current_frame >= 5:
                current_frame = 5
                animation_timer = 0

        if current_anim == "run_jump" and not on_ground:
            if current_frame >= 9:
                current_frame = 9
                animation_timer = 0

        if loop:
            if animation_timer >= delay:
                steps = animation_timer // delay
                animation_timer = animation_timer % delay
                current_frame = (current_frame + int(steps)) % max(1, len(anim_frames))
        else:
            if animation_timer >= delay and playing:
                steps = animation_timer // delay
                animation_timer = animation_timer % delay
                current_frame += int(steps)
                if current_frame >= len(anim_frames) - 1:
                    current_frame = len(anim_frames) - 1
                    playing = False

        # --- DRAWING PHASE ---
        start_bg_index = int(camera_x // bg_w)
        num_bgs_to_draw = (SCREEN_WIDTH // bg_w) + 2
        for i in range(start_bg_index, start_bg_index + num_bgs_to_draw):
            current_bg = bg_img if i % 2 == 0 else bg_flip_img
            bg_screen_x = (i * bg_w) - camera_x
            screen.blit(current_bg, (bg_screen_x, 0))

        start_floor_index = int(camera_x // floor_w)
        num_floors_to_draw = (SCREEN_WIDTH // floor_w) + 2
        floor_draw_y = SCREEN_HEIGHT - target_floor_h + 30
        for i in range(start_floor_index, start_floor_index + num_floors_to_draw):
            current_floor = floor_img if i % 2 == 0 else floor_flip_img
            floor_screen_x = (i * floor_w) - camera_x
            screen.blit(current_floor, (floor_screen_x, floor_draw_y))

        for platform in platform_group:
            plat_screen_x = platform.rect.x - camera_x
            if -200 < plat_screen_x < SCREEN_WIDTH + 200:
                screen.blit(platform.image, (plat_screen_x, platform.rect.y))

        frame_surf = anim_frames[current_frame]
        display_w, display_h = frame_surf.get_size()
        base_scale_factor = 0.25
        correction = animation_scale_corrections.get(current_anim, 1.0)
        final_scale = base_scale_factor * correction

        frame_to_draw = pygame.transform.smoothscale(frame_surf,
                                                     (int(display_w * final_scale), int(display_h * final_scale)))
        if not facing_right:
            frame_to_draw = pygame.transform.flip(frame_to_draw, True, False)

        fw, fh = frame_to_draw.get_size()
        blit_x = int(screen_x - fw // 2)
        blit_y = int(y - fh)
        screen.blit(frame_to_draw, (blit_x, blit_y))

        # Create precise pixel mask for the player from the currently drawn surface
        player_mask = pygame.mask.from_surface(frame_to_draw)

        for enemy in enemy_group:
            enemy_screen_x = enemy.rect.x - camera_x
            screen.blit(enemy.image, (enemy_screen_x, enemy.rect.y))

            # True pixel-perfect collision check using masks
            offset = (blit_x - enemy_screen_x, blit_y - enemy.rect.y)
            if enemy.mask.overlap(player_mask, offset):
                game_over = True
                try:
                    death_fx.play()
                except:
                    pass

        draw_panel()

    else:
        screen.fill(BLACK)
        draw_text("YOUR SOUL HAS BEEN LOST!!", font_big, WHITE, SCREEN_WIDTH // 2 - 180, 250)
        draw_text("SCORE: " + str(score), font_big, WHITE, SCREEN_WIDTH // 2 - 80, 300)
        draw_text("PRESS SPACE TO TRY AGAIN", font_big, WHITE, SCREEN_WIDTH // 2 - 150, 350)

        if score > high_score:
            high_score = score
            with open("score.txt", "w") as file:
                file.write(str(high_score))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_over = False
            score = 0
            x = 400.0
            y = y_ground
            camera_x = 0.0
            enemy_group.empty()
            platform_group.empty()

            starting_platform = Platform(200, 580, 180)
            platform_group.add(starting_platform)
            platform_group.add(Platform(550, 480, 300))
            platform_group.add(Platform(900, 380, 260))

    pygame.display.update()

pygame.quit()
sys.exit()