import pygame
import sys
import random
import os
from pygame import mixer, Color

# ==========================================
# INITIALIZATION
# ==========================================
mixer.init()
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Succi Solace")

# Set Window Icon
try:
    game_icon = pygame.image.load("mats/pink design.png").convert_alpha()
    pygame.display.set_icon(game_icon)
except pygame.error:
    pass

# Sets Frame Rate
clock = pygame.time.Clock()
FPS = 60

# ==========================================
# ASSET LOADING: AUDIO
# ==========================================
try:
    pygame.mixer.music.load("mats/Phaneroza-_No-Umbra-No-Penumbra.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1, 0.0)

    jump_fx = pygame.mixer.Sound("mats/Swoosh.mp3")
    jump_fx.set_volume(0.3)
    death_fx = pygame.mixer.Sound("mats/Pause.mp3")
    death_fx.set_volume(0.6)

    cast_fx = pygame.mixer.Sound("mats/cast.mp3")
    cast_fx.set_volume(0.4)
    explode_fx = pygame.mixer.Sound("mats/explode.mp3")
    explode_fx.set_volume(0.2)
except pygame.error as e:
    print(f"Audio Load Warning: {e}")

# ==========================================
# GAME VARIABLES
# ==========================================
gravity = 1500.0
max_platforms = 40
game_over = False
paused = False
score = 0

if os.path.exists("score.txt"):
    with open("score.txt", "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

# UI Colors & Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (253, 117, 234)
CYAN = (0, 255, 255)
LIGHT_GRAY = (180, 180, 180)
font_small = pygame.font.SysFont("Lucida Sans", 20)
font_big = pygame.font.SysFont("Lucida Sans", 48)

# ==========================================
# ASSET LOADING: IMAGES & BACKGROUNDS
# ==========================================
def trim_black_side_borders(surface, threshold=15):
    w, h = surface.get_size()
    left, right = 0, w
    for x in range(w // 4):
        has_content = False
        for y in range(0, h, 10):
            color = surface.get_at((x, y))
            if color.r > threshold or color.g > threshold or color.b > threshold:
                has_content = True
                break
        if has_content:
            left = x
            break
    for x in range(w - 1, w - 1 - (w // 4), -1):
        has_content = False
        for y in range(0, h, 10):
            color = surface.get_at((x, y))
            if color.r > threshold or color.g > threshold or color.b > threshold:
                has_content = True
                break
        if has_content:
            right = x + 1
            break
    if right > left:
        return surface.subsurface((left, 0, right - left, h)).copy()
    return surface

try:
    bg_filenames = [
        "backgrounds/cross_bg.png",
        "backgrounds/cross_bg_flip.png",
        "backgrounds/cross_bg_3.png",
        "backgrounds/cross_bg_door_flip.PNG",
        "backgrounds/cross_bg_3_flip.PNG",
        "backgrounds/cross_bg_2.png",
        "backgrounds/cross_bg_4.png",
        "backgrounds/cross_bg_4_flip.PNG"
    ]

    first_raw = pygame.image.load(bg_filenames[0]).convert()
    first_trimmed = trim_black_side_borders(first_raw)
    bg_scale_ratio = SCREEN_HEIGHT / first_trimmed.get_height()
    bg_w = int(first_trimmed.get_width() * bg_scale_ratio) - 1

    bg_list = []
    for filename in bg_filenames:
        raw_img = pygame.image.load(filename).convert()
        trimmed_img = trim_black_side_borders(raw_img)
        scaled_img = pygame.transform.smoothscale(trimmed_img, (bg_w, SCREEN_HEIGHT))
        bg_list.append(scaled_img)

    floor_img = pygame.image.load("mats/floor2.PNG").convert()
    floor_img.set_colorkey((0, 0, 0))
    target_floor_h = 200
    floor_scale_ratio = target_floor_h / floor_img.get_height()
    floor_w = int(floor_img.get_width() * floor_scale_ratio) - 1
    floor_img = pygame.transform.smoothscale(floor_img, (floor_w, target_floor_h))
    floor_flip_img = pygame.transform.flip(floor_img, True, False)

    platform_image = pygame.image.load("mats/plat31c.png").convert_alpha()
    bird_sheet_img = pygame.image.load("spritsheets/enemies/flyer_SS_NB.png").convert_alpha()
    end_image = pygame.image.load("backgrounds/death_screen.png").convert_alpha()
    end_image = pygame.transform.smoothscale(end_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    fireball_img = pygame.image.load("spritsheets/fireball.png").convert_alpha()
    explode_img = pygame.image.load("spritsheets/explode_NB.png").convert_alpha()

except pygame.error as e:
    print(f"Error loading image assets: {e}")
    pygame.quit()
    sys.exit()

# ==========================================
# PRE-LOAD ENEMY FRAMES (ELIMINATES LAG SPIKES)
# ==========================================
def load_enemy_frames(filename, num_frames, scale):
    try:
        sheet = pygame.image.load(filename).convert_alpha()
    except pygame.error as e:
        print(f"Unable to load enemy sprite sheet: {filename} - {e}")
        sys.exit()

    frames_r = []
    frames_l = []
    fw = sheet.get_width() // num_frames
    fh = sheet.get_height()
    for i in range(num_frames):
        frame = pygame.Surface((fw, fh), pygame.SRCALPHA).convert_alpha()
        frame.blit(sheet, (0, 0), (i * fw, 0, fw, fh))
        frame_r = pygame.transform.smoothscale(frame, (int(fw * scale), int(fh * scale)))
        frame_l = pygame.transform.flip(frame_r, True, False)
        frames_r.append(frame_r)
        frames_l.append(frame_l)
    return frames_r, frames_l

# 1. Load Demon Arrays
demon_walk_r, demon_walk_l = load_enemy_frames("spritsheets/enemies/D_WALK_SSNB.png", 7, 0.35)
demon_attack_r, demon_attack_l = load_enemy_frames("spritsheets/enemies/D_attack_SSNB.png", 12, 0.35)

# 2. Load Skeleton Arrays
skel_walk_r, skel_walk_l = load_enemy_frames("spritsheets/enemies/skelly_walk_NB.png", 8, 0.7)
skel_idle_r, skel_idle_l = load_enemy_frames("spritsheets/enemies/skelly_idle_NB.png", 10, 0.7)
skel_attack_r, skel_attack_l = load_enemy_frames("spritsheets/enemies/skelly_attack_NB.png", 10, 0.7)


# ==========================================
# CLASSES
# ==========================================
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_pos, y, sprite_sheet, scale, forced_direction=None):
        super().__init__()
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.direction = forced_direction if forced_direction is not None else random.choice([-1, 1])
        self.flip = (self.direction == 1)

        animation_steps = 8
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
        self.mask = pygame.mask.from_surface(self.image)

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        self.rect.x += self.direction * 4
        if self.rect.right < camera_x - 400 or self.rect.left > camera_x + SCREEN_WIDTH + 400:
            self.kill()

class Demon(pygame.sprite.Sprite):
    def __init__(self, spawn_x, y_pos, patrol_start_x, patrol_end_x):
        super().__init__()
        # Grab the globally loaded arrays
        self.walk_frames_right = demon_walk_r
        self.walk_frames_left = demon_walk_l
        self.attack_frames_right = demon_attack_r
        self.attack_frames_left = demon_attack_l

        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.anim_speed = 100

        self.patrol_start_x = patrol_start_x
        self.patrol_end_x = patrol_end_x
        self.speed = 2.0
        self.direction = 1
        self.state = "walk"

        self.image = self.walk_frames_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = spawn_x
        self.rect.bottom = y_pos + 85
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, camera_x, player_x=None, player_y=None):
        if player_x is not None and player_y is not None:
            if abs(player_y - self.rect.centery) < 150:
                dist_to_player = abs(player_x - self.rect.centerx)
                if dist_to_player < 180 and self.state != "attack":
                    self.state = "attack"
                    self.frame_index = 0
                    self.update_time = pygame.time.get_ticks()
                    self.direction = 1 if player_x > self.rect.centerx else -1

        if self.state == "walk":
            self.rect.x += self.direction * self.speed
            if self.rect.x >= self.patrol_end_x:
                self.rect.x = self.patrol_end_x
                self.direction = -1
            elif self.rect.x <= self.patrol_start_x:
                self.rect.x = self.patrol_start_x
                self.direction = 1

            if pygame.time.get_ticks() - self.update_time > self.anim_speed:
                self.update_time = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames_right)
            self.image = self.walk_frames_right[self.frame_index] if self.direction == 1 else self.walk_frames_left[self.frame_index]

        elif self.state == "attack":
            attack_speed = 70
            if pygame.time.get_ticks() - self.update_time > attack_speed:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1

                if self.frame_index >= len(self.attack_frames_right):
                    self.state = "walk"
                    self.frame_index = 0
            if self.state == "attack":
                self.image = self.attack_frames_right[self.frame_index] if self.direction == 1 else self.attack_frames_left[self.frame_index]

        old_bottom = self.rect.bottom
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.bottom = old_bottom
        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.right < camera_x - 1000:
            self.kill()

class Skeleton(pygame.sprite.Sprite):
    def __init__(self, spawn_x, y_pos, patrol_start_x, patrol_end_x):
        super().__init__()
        # Grab the globally loaded arrays
        self.walk_frames_right = skel_walk_r
        self.walk_frames_left = skel_walk_l
        self.idle_frames_right = skel_idle_r
        self.idle_frames_left = skel_idle_l
        self.attack_frames_right = skel_attack_r
        self.attack_frames_left = skel_attack_l

        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.anim_speed = 100

        self.patrol_start_x = patrol_start_x
        self.patrol_end_x = patrol_end_x
        self.speed = 1.8
        self.direction = 1
        self.state = "walk"

        self.image = self.walk_frames_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = spawn_x

        self.rect.bottom = y_pos + 240
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, camera_x, player_x=None, player_y=None):
        if player_x is not None and player_y is not None:
            if abs(player_y - self.rect.centery) < 250:
                dist_to_player = abs(player_x - self.rect.centerx)
                if dist_to_player < 180 and self.state != "attack":
                    self.state = "attack"
                    self.frame_index = 0
                    self.update_time = pygame.time.get_ticks()
                    self.direction = 1 if player_x > self.rect.centerx else -1

        if self.state == "walk":
            self.rect.x += self.direction * self.speed
            if self.rect.x >= self.patrol_end_x:
                self.rect.x = self.patrol_end_x
                self.direction = -1
                self.state = "idle"
                self.frame_index = 0
            elif self.rect.x <= self.patrol_start_x:
                self.rect.x = self.patrol_start_x
                self.direction = 1
                self.state = "idle"
                self.frame_index = 0

            if self.state == "walk":
                if pygame.time.get_ticks() - self.update_time > self.anim_speed:
                    self.update_time = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.walk_frames_right)
                self.image = self.walk_frames_right[self.frame_index] if self.direction == 1 else self.walk_frames_left[self.frame_index]

        if self.state == "idle":
            idle_speed = 120
            if pygame.time.get_ticks() - self.update_time > idle_speed:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                if self.frame_index >= len(self.idle_frames_right):
                    self.state = "walk"
                    self.frame_index = 0
            if self.state == "idle":
                self.image = self.idle_frames_right[self.frame_index] if self.direction == 1 else self.idle_frames_left[self.frame_index]

        if self.state == "attack":
            attack_speed = 80
            if pygame.time.get_ticks() - self.update_time > attack_speed:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                if self.frame_index >= len(self.attack_frames_right):
                    self.state = "walk"
                    self.frame_index = 0
            if self.state == "attack":
                self.image = self.attack_frames_right[self.frame_index] if self.direction == 1 else self.attack_frames_left[self.frame_index]

        old_bottom = self.rect.bottom
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.bottom = old_bottom
        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.right < camera_x - 1000:
            self.kill()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, scale=0.45):
        super().__init__()
        self.direction = direction
        self.speed = 800.0
        self.state = "fly"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.fly_frames = []
        num_fly = 6
        fw = fireball_img.get_width() // num_fly
        fh = fireball_img.get_height()
        for i in range(num_fly):
            frame = pygame.Surface((fw, fh), pygame.SRCALPHA).convert_alpha()
            frame.blit(fireball_img, (0, 0), (i * fw, 0, fw, fh))
            frame = pygame.transform.smoothscale(frame, (int(fw * scale), int(fh * scale)))
            if direction == -1:
                frame = pygame.transform.flip(frame, True, False)
            self.fly_frames.append(frame)

        self.exp_frames = []
        num_exp = 8
        ew = explode_img.get_width() // num_exp
        eh = explode_img.get_height()
        for i in range(num_exp):
            frame = pygame.Surface((ew, eh), pygame.SRCALPHA).convert_alpha()
            frame.blit(explode_img, (0, 0), (i * ew, 0, ew, eh))
            frame = pygame.transform.smoothscale(frame, (int(ew * scale), int(eh * scale)))
            if direction == -1:
                frame = pygame.transform.flip(frame, True, False)
            self.exp_frames.append(frame)

        self.image = self.fly_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt, camera_x):
        cooldown = 50 if self.state == "fly" else 40
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            if self.state == "fly":
                if self.frame_index >= len(self.fly_frames):
                    self.frame_index = 0
                self.image = self.fly_frames[self.frame_index]
            else:
                if self.frame_index >= len(self.exp_frames):
                    self.kill()
                    return
                else:
                    self.image = self.exp_frames[self.frame_index]

        if self.state == "fly":
            self.rect.x += self.direction * self.speed * dt
            self.mask = pygame.mask.from_surface(self.image)

            if self.rect.right < camera_x - 500 or self.rect.left > camera_x + SCREEN_WIDTH + 500:
                self.kill()

    def explode(self):
        if self.state != "explode":
            self.state = "explode"
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


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
    pygame.draw.line(screen, PINK, (0, 30), (SCREEN_WIDTH, 30), 3)
    draw_text("SCORE: " + str(score), font_small, WHITE, 10, 5)
    draw_text("HIGH SCORE: " + str(high_score), font_small, WHITE, SCREEN_WIDTH // 2 - 80, 5)


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

animations = {
    "idle": get_sprites_from_sheet("spritsheets/S_IDLE_NB.png"),
    "walk": get_sprites_from_sheet("spritsheets/S_WALK_NB.png"),
    "run": get_sprites_from_sheet("spritsheets/S_RUN_NB.png"),
    "jump": get_sprites_from_sheet("spritsheets/S_JUMP_NB.png"),
    "run_jump": get_sprites_from_sheet("spritsheets/S_RUN_JUMP_NB.png"),
    "duck": get_sprites_from_sheet("spritsheets/S_DUCK_NB.png"),
    "attack": get_sprites_from_sheet("spritsheets/S_ATTACK_NB.png"),
    "run_attack": get_sprites_from_sheet("spritsheets/S_RUNSHOT_NB.png")
}

animation_speeds = {"idle": 175, "walk": 130, "run": 75, "jump": 80, "run_jump": 50, "duck": 50, "attack": 90, "run_attack": 75}
animation_loops = {"idle": True, "walk": True, "run": True, "jump": False, "run_jump": False, "duck": False, "attack": False, "run_attack": False}
animation_scale_corrections = {"idle": 1.0, "walk": 1.08, "run": 1.08, "jump": 1.0, "run_jump": 1.08, "duck": 1.0, "attack": 2.8, "run_attack": 1.08}

# ==========================================
# PLAYER PHYSICS & CAMERA STATE
# ==========================================
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
fireball_spawned = False

# ==========================================
# WORLD GENERATION SETUP
# ==========================================
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
demon_group = pygame.sprite.Group()
skeleton_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()

last_spawned_bg_index = -1

starting_platform = Platform(200, 580, 180)
platform_group.add(starting_platform)
platform_group.add(Platform(450, 380, 200))
platform_group.add(Platform(800, 480, 160))

# ==========================================
# MAIN GAME LOOP
# ==========================================
run = True
while run:
    dt_ms = clock.tick(FPS)
    dt = dt_ms / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                if not game_over:
                    paused = not paused

    if not game_over and not paused:

        keys = pygame.key.get_pressed()
        moving = False
        run_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        duck_pressed = keys[pygame.K_DOWN]
        attack_pressed = keys[pygame.K_f]

        recovering_duck = (current_anim == "duck" and not duck_pressed and playing)
        attacking = (current_anim in ["attack", "run_attack"] and playing)

        if attack_pressed and not duck_pressed and not recovering_duck:
            if not attacking:
                is_moving_keys = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]
                if (is_moving_keys and run_pressed) or not on_ground:
                    current_anim = "run_attack"
                else:
                    current_anim = "attack"

                current_frame = 0
                animation_timer = 0
                playing = True
                fireball_spawned = False
                attacking = True

        if attacking:
            target_frame = 8 if current_anim == "attack" else 4
            if current_frame == target_frame and not fireball_spawned:
                spawn_x = x + (90 if facing_right else -90)
                spawn_y = y - 180
                fireball = Projectile(spawn_x, spawn_y, 1 if facing_right else -1, scale=0.28)
                projectile_group.add(fireball)
                fireball_spawned = True
                try: cast_fx.play()
                except NameError: pass

        if current_anim == "attack":
            vx = 0
        elif recovering_duck or (duck_pressed and on_ground):
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

        if keys[pygame.K_SPACE] and on_ground and not duck_pressed and not recovering_duck and not attacking:
            if moving and "run_jump" in animations:
                current_anim = "run_jump"
            else:
                current_anim = "jump"
            current_frame = 0
            animation_timer = 0
            playing = True
            vy = jump_impulse
            on_ground = False
            try: jump_fx.play()
            except NameError: pass

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

        if attacking: pass
        elif not on_ground: pass
        elif recovering_duck: pass
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
        if screen_x > RIGHT_DEAD_ZONE: camera_x += (screen_x - RIGHT_DEAD_ZONE)
        elif screen_x < LEFT_DEAD_ZONE: camera_x -= (LEFT_DEAD_ZONE - screen_x)

        for platform in list(platform_group):
            if platform.rect.right < camera_x - 4000:
                platform.kill()

        if len(platform_group) < max_platforms:
            last_platform = max(platform_group, key=lambda p: p.rect.x, default=None)
            if last_platform:
                gap = random.randint(120, 290)
                p_x = last_platform.rect.right + gap
            else:
                p_x = camera_x + SCREEN_WIDTH + 100
            p_w = random.randint(90, 200)
            p_y = random.randint(320, 625)
            platform_group.add(Platform(p_x, p_y, p_w))

        if len(enemy_group) < 3 and random.randint(1, 60) == 1:
            spawn_side = random.choice(["left", "right"])
            enemy_y = random.randint(200, 550)
            if spawn_side == "left":
                spawn_x = camera_x - 150
                enemy = Enemy(spawn_x, enemy_y, bird_sheet, .15, forced_direction=1)
            else:
                spawn_x = camera_x + SCREEN_WIDTH + 150
                enemy = Enemy(spawn_x, enemy_y, bird_sheet, .15, forced_direction=-1)
            enemy_group.add(enemy)

        # ==================================================
        # THE FIX: Perfect Spawning Isolation (No Overlapping)
        # ==================================================
        current_bg_index = int(x // bg_w)
        if current_bg_index > last_spawned_bg_index:
            target_bg_index = current_bg_index + 1
            patrol_start = target_bg_index * bg_w
            patrol_end = (target_bg_index + 1) * bg_w - 100

            # It cycles cleanly: 1: Skeleton, 2: Skeleton, 3: Demon.
            # This ensures Skeletons spawn twice as often, but they never share a screen with a Demon.
            if target_bg_index % 3 == 0:
                spawn_x_demon = patrol_start + 100
                demon = Demon(spawn_x_demon, y_ground, patrol_start, patrol_end)
                demon_group.add(demon)
            else:
                spawn_x_skel = patrol_start + 100
                skeleton = Skeleton(spawn_x_skel, y_ground, patrol_start, patrol_end)
                skeleton_group.add(skeleton)

            last_spawned_bg_index = current_bg_index

        enemy_group.update(camera_x)
        demon_group.update(camera_x, x, y)
        skeleton_group.update(camera_x, x, y)
        projectile_group.update(dt, camera_x)

        for proj in projectile_group:
            if proj.state == "fly":
                for enemy in enemy_group:
                    offset = (enemy.rect.x - proj.rect.x, enemy.rect.y - proj.rect.y)
                    if proj.mask.overlap(enemy.mask, offset):
                        proj.explode()
                        enemy.kill()
                        try: explode_fx.play()
                        except NameError: pass
                        break
                if proj.state == "fly":
                    for demon in demon_group:
                        offset = (demon.rect.x - proj.rect.x, demon.rect.y - proj.rect.y)
                        if proj.mask.overlap(demon.mask, offset):
                            proj.explode()
                            demon.kill()
                            try: explode_fx.play()
                            except NameError: pass
                            break
                if proj.state == "fly":
                    for skel in skeleton_group:
                        offset = (skel.rect.x - proj.rect.x, skel.rect.top - proj.rect.y)
                        if proj.mask.overlap(skel.mask, offset):
                            proj.explode()
                            skel.kill()
                            try: explode_fx.play()
                            except NameError: pass
                            break

        score = int(x)

        anim_frames = animations[current_anim]
        delay = animation_speeds.get(current_anim, 120)
        loop = animation_loops.get(current_anim, True)
        animation_timer += dt_ms

        if current_anim == "duck" and duck_pressed:
            if current_frame >= 6: current_frame = 6; animation_timer = 0
        if current_anim == "jump" and not on_ground:
            if current_frame >= 5: current_frame = 5; animation_timer = 0
        if current_anim == "run_jump" and not on_ground:
            if current_frame >= 9: current_frame = 9; animation_timer = 0

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

    if not game_over:
        start_bg_index = int(camera_x // bg_w)
        num_bgs_to_draw = (SCREEN_WIDTH // bg_w) + 2
        for i in range(start_bg_index, start_bg_index + num_bgs_to_draw):
            current_bg = bg_list[i % len(bg_list)]
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

        frame_to_draw = pygame.transform.smoothscale(frame_surf, (int(display_w * final_scale), int(display_h * final_scale)))
        if not facing_right: frame_to_draw = pygame.transform.flip(frame_to_draw, True, False)

        fw, fh = frame_to_draw.get_size()
        blit_x = int(screen_x - fw // 2)

        y_offset = 0
        x_offset = 0
        if current_anim == "attack":
            y_offset = 230
            shift_amount = 200
            if facing_right: x_offset = shift_amount
            else: x_offset = -shift_amount

        blit_x += x_offset
        blit_y = int(y - fh) + y_offset

        screen.blit(frame_to_draw, (blit_x, blit_y))

        player_mask = pygame.mask.from_surface(frame_to_draw)

        for enemy in enemy_group:
            enemy_screen_x = enemy.rect.x - camera_x
            screen.blit(enemy.image, (enemy_screen_x, enemy.rect.y))
            offset = (blit_x - enemy_screen_x, blit_y - enemy.rect.y)
            if enemy.mask.overlap(player_mask, offset):
                game_over = True
                try: death_fx.play()
                except NameError: pass

        for demon in demon_group:
            demon_screen_x = demon.rect.x - camera_x
            if -200 < demon_screen_x < SCREEN_WIDTH + 200:
                screen.blit(demon.image, (demon_screen_x, demon.rect.top))
                offset = (blit_x - demon_screen_x, blit_y - demon.rect.top)
                if demon.mask.overlap(player_mask, offset):
                    game_over = True
                    try: death_fx.play()
                    except NameError: pass

        for skel in skeleton_group:
            skel_screen_x = skel.rect.x - camera_x
            if -200 < skel_screen_x < SCREEN_WIDTH + 200:
                screen.blit(skel.image, (skel_screen_x, skel.rect.top))
                offset = (blit_x - skel_screen_x, blit_y - skel.rect.top)
                if skel.mask.overlap(player_mask, offset):
                    game_over = True
                    try: death_fx.play()
                    except NameError: pass

        for proj in projectile_group:
            proj_screen_x = proj.rect.x - camera_x
            if -200 < proj_screen_x < SCREEN_WIDTH + 200:
                screen.blit(proj.image, (proj_screen_x, proj.rect.y))

        draw_panel()

        if paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            draw_text("GAME PAUSED", font_big, Color("turquoise1"), SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 50)
            draw_text("Press 'P' or 'ESC' to Resume", font_small, LIGHT_GRAY, SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 20)
            ctrl_x = SCREEN_WIDTH - 280
            draw_text("CONTROLS:", font_small, PINK, ctrl_x, 50)
            draw_text("Arrow Keys : Move / Duck", font_small, Color("blue1"), ctrl_x, 80)
            draw_text("Shift      : Run", font_small, Color("blue1"), ctrl_x, 105)
            draw_text("Space      : Jump", font_small, Color("blue1"), ctrl_x, 130)
            draw_text("F Key      : Cast Fireball", font_small, Color("blue1"), ctrl_x, 155)
            draw_text("P / ESC    : Pause", font_small, PINK, ctrl_x, 180)

    else:
        screen.blit(end_image, (0, 0))
        pygame.draw.line(screen, Color("plum1"), (350, 245), (500 + 520, 245), 6)
        draw_text("YOUR SOUL HAS BEEN LOST!!", font_big, Color("blue1"), SCREEN_WIDTH // 2 - 350, 250)
        pygame.draw.line(screen, Color("plum1"), (350, 315), (500 + 520, 315), 6)
        draw_text("SCORE: " + str(score), font_big, Color("turquoise1"), SCREEN_WIDTH // 2 - 150, 320)
        pygame.draw.line(screen, Color("plum1"), (350, 400), (500 + 520, 400), 6)
        draw_text("PRESS SPACE TO TRY AGAIN", font_big, Color("blue1"), SCREEN_WIDTH // 2 - 330, 400)
        pygame.draw.line(screen, Color("plum1"), (350, 475), (SCREEN_WIDTH // 2 + 330, 475), 6)

        if score > high_score:
            high_score = score
            with open("score.txt", "w") as file: file.write(str(high_score))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_over = False
            paused = False
            score = 0
            x = 400.0
            y = y_ground
            camera_x = 0.0
            enemy_group.empty()
            platform_group.empty()
            demon_group.empty()
            skeleton_group.empty()
            projectile_group.empty()
            last_spawned_bg_index = -1
            starting_platform = Platform(200, 580, 180)
            platform_group.add(starting_platform)
            platform_group.add(Platform(550, 480, 300))
            platform_group.add(Platform(900, 380, 260))

    pygame.display.update()

mixer.quit()
pygame.quit()
sys.exit()