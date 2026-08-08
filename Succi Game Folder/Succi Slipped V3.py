import pygame
import sys
import random
import os
from pygame import mixer, Color

# ==========================================
# INITIALIZATION (OOP NOTE: This would go in a Game class __init__)
# ==========================================
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

# ==========================================
# ASSET LOADING: AUDIO
# ==========================================
try:
    pygame.mixer.music.load("mats/Satie_Gnossienne_1.mp3")  #
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1, 0.0)
    jump_fx = pygame.mixer.Sound("mats/Swoosh.mp3")  #
    jump_fx.set_volume(0.3)
    death_fx = pygame.mixer.Sound("mats/Pause.mp3")  #
    death_fx.set_volume(0.6)
except pygame.error:
    pass  # Fails silently if audio files are missing

# ==========================================
# GAME VARIABLES
# ==========================================
gravity = 1500.0
max_platforms = 40
game_over = False
score = 0

# High score loading (Reads from local file or creates it)
if os.path.exists("score.txt"):
    with open("score.txt", "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

# Define colors & fonts for the UI
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (253, 117, 234)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
MAROON = (128, 0, 0)
PURPLE = (128, 0, 128)
NAVY = (0, 0, 128)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
font_small = pygame.font.SysFont("Lucida Sans", 20)
font_big = pygame.font.SysFont("Lucida Sans", 48)


# ==========================================
# ASSET LOADING: IMAGES & BACKGROUNDS
# ==========================================
def trim_black_side_borders(surface, threshold=15):
    """Scans the left and right edges of an image and trims off solid black borders."""
    w, h = surface.get_size()
    left = 0
    right = w

    # Scan from left edge inward to find where real image content starts
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

    # Scan from right edge inward
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


# ==========================================
# ASSET LOADING: IMAGES & BACKGROUNDS
# ==========================================
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

    # Trim and load the first image to calculate master target width
    first_raw = pygame.image.load(bg_filenames[0]).convert()
    first_trimmed = trim_black_side_borders(first_raw)
    bg_scale_ratio = SCREEN_HEIGHT / first_trimmed.get_height()
    bg_w = int(first_trimmed.get_width() * bg_scale_ratio) - 1

    bg_list = []
    for filename in bg_filenames:
        raw_img = pygame.image.load(filename).convert()
        # Automatically crop off any black side pillars baked into the image
        trimmed_img = trim_black_side_borders(raw_img)
        # Scale to standard game dimensions
        scaled_img = pygame.transform.smoothscale(trimmed_img, (bg_w, SCREEN_HEIGHT))
        bg_list.append(scaled_img)

    # Load Floor
    floor_img = pygame.image.load("mats/floor2.PNG").convert()
    floor_img.set_colorkey((0, 0, 0))
    target_floor_h = 200
    floor_scale_ratio = target_floor_h / floor_img.get_height()
    floor_w = int(floor_img.get_width() * floor_scale_ratio) - 1
    floor_img = pygame.transform.smoothscale(floor_img, (floor_w, target_floor_h))
    floor_flip_img = pygame.transform.flip(floor_img, True, False)

    # Load Platforms and Enemy Sprite Sheet and death screen BG
    platform_image = pygame.image.load("mats/plat31c.png").convert_alpha()
    bird_sheet_img = pygame.image.load("spritsheets/enemies/flyer_SS_NB.png").convert_alpha()
    end_image = pygame.image.load("backgrounds/death_screen.png").convert_alpha()
    end_image = pygame.transform.smoothscale(end_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

except pygame.error as e:
    print(f"Error loading image assets: {e}")
    pygame.quit()
    sys.exit()


# ==========================================
# CLASSES (OOP Components)
# ==========================================

class SpriteSheet:
    """Utility class to extract individual frames from a large sprite sheet image."""

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
    """Handles the flying bat enemies. Contains its own update logic."""

    def __init__(self, x_pos, y, sprite_sheet, scale, forced_direction=None):
        super().__init__()
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # Allow forced direction from left (1) or right (-1), or choose randomly
        self.direction = forced_direction if forced_direction is not None else random.choice([-1, 1])
        # If flying right (1), flip the image so it faces right.
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
        # OOP NOTE: This handles the bat's internal state (animation & movement) every frame
        animation_cooldown = 125
        self.image = self.animation_list[self.frame_index]

        # Update pixel-perfect mask as frames animate
        self.mask = pygame.mask.from_surface(self.image)

        # Frame timer logic
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        # Move Enemy horizontally across world
        self.rect.x += self.direction * 4

        # Memory Cleanup: Remove if it flies too far off screen relative to camera view
        if self.rect.right < camera_x - 400 or self.rect.left > camera_x + SCREEN_WIDTH + 400:
            self.kill()


# NEW: Ground-patrolling Demon class
# NEW: Ground-patrolling Demon class
class Demon(pygame.sprite.Sprite):
    def __init__(self, spawn_x, y_pos, patrol_start_x, patrol_end_x, scale=0.35):
        super().__init__()
        self.walk_frames_right = []
        self.walk_frames_left = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.anim_speed = 100  # milliseconds per frame

        # Patrol boundaries (based on the background width)
        self.patrol_start_x = patrol_start_x
        self.patrol_end_x = patrol_end_x

        self.speed = 2.0
        self.direction = 1  # 1 = moving right, -1 = moving left

        # Load and slice the walking sprite sheet
        try:
            walk_sheet = pygame.image.load("spritsheets/enemies/D_WALK_SSNB.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading Demon sprite sheet: {e}")
            pygame.quit()
            sys.exit()

        # CHANGED FROM 8 TO 7 (5670 pixels / 810 pixels = exactly 7 frames)
        num_frames = 7
        frame_w = walk_sheet.get_width() // num_frames
        frame_h = walk_sheet.get_height()

        for i in range(num_frames):
            frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA).convert_alpha()
            frame.blit(walk_sheet, (0, 0), (i * frame_w, 0, frame_w, frame_h))

            # Scale frame down to match game scale
            scaled_w = int(frame_w * scale)
            scaled_h = int(frame_h * scale)
            frame_right = pygame.transform.smoothscale(frame, (scaled_w, scaled_h))
            frame_left = pygame.transform.flip(frame_right, True, False)

            self.walk_frames_right.append(frame_right)
            self.walk_frames_left.append(frame_left)

        # Set initial image and collision rect
        self.image = self.walk_frames_right[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = spawn_x
        self.rect.bottom = y_pos + 80  # Align feet with ground/platform level
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, camera_x):
        # 1. Patrol Movement Logic
        self.rect.x += self.direction * self.speed

        # Reverse direction at patrol boundaries
        if self.rect.x >= self.patrol_end_x:
            self.rect.x = self.patrol_end_x
            self.direction = -1
        elif self.rect.x <= self.patrol_start_x:
            self.rect.x = self.patrol_start_x
            self.direction = 1

        # 2. Animation Timer
        if pygame.time.get_ticks() - self.update_time > self.anim_speed:
            self.update_time = pygame.time.get_ticks()
            self.frame_index = (self.frame_index + 1) % len(self.walk_frames_right)

        # 3. Update current frame & collision mask based on facing direction
        if self.direction == 1:
            self.image = self.walk_frames_right[self.frame_index]
        else:
            self.image = self.walk_frames_left[self.frame_index]

        self.mask = pygame.mask.from_surface(self.image)

        # Despawn him quicker so he doesn't block the next spawn point
        if self.rect.right < camera_x - 1000:
            self.kill()


class Platform(pygame.sprite.Sprite):
    """Handles the static skull platforms in the world."""

    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.transform.scale(platform_image, (width, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        pass  # Currently static, but you could add moving logic here later


# ==========================================
# UI HELPER FUNCTIONS (OOP NOTE: Could go into a UIManager class)
# ==========================================
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_panel():
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, PINK, (0, 30), (SCREEN_WIDTH, 30), 3)
    draw_text("SCORE: " + str(score), font_small, WHITE, 10, 5)
    draw_text("HIGH SCORE: " + str(high_score), font_small, WHITE, SCREEN_WIDTH // 2 - 80, 5)


# ==========================================
# CHARACTER ANIMATION SETUP
# ==========================================
def get_sprites_from_sheet(filename, approx_width=810, target_h=1080):
    """Slices a massive character sprite sheet into individual frames."""
    try:
        sheet = pygame.image.load(filename).convert_alpha()
    except pygame.error as e:
        print(f"Unable to load sprite sheet image: {filename}")
        raise SystemExit(e)

    sheet_width, sheet_height = sheet.get_size()

    # Prevents vertical drift if the image height is missing a single pixel
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


# Load character animations (OOP NOTE: This block would belong in a Player class __init__)
animations = {
    "idle": get_sprites_from_sheet("spritsheets/S_IDLE_NB.png"),  #
    "walk": get_sprites_from_sheet("spritsheets/S_WALK_NB.png"),  #
    "run": get_sprites_from_sheet("spritsheets/S_RUN_NB.png"),  #
    "jump": get_sprites_from_sheet("spritsheets/S_JUMP_NB.png"),  #
    "run_jump": get_sprites_from_sheet("spritsheets/S_RUN_JUMP_NB.png"),  #
    "duck": get_sprites_from_sheet("spritsheets/S_DUCK_NB.png")  #
}

# Animation configuration data
animation_speeds = {"idle": 175, "walk": 130, "run": 75, "jump": 80, "run_jump": 50, "duck": 50}
animation_loops = {"idle": True, "walk": True, "run": True, "jump": False, "run_jump": False, "duck": False}
animation_scale_corrections = {"idle": 1.0, "walk": 1.08, "run": 1.08, "jump": 1.0, "run_jump": 1.08, "duck": 1.0}

# ==========================================
# PLAYER PHYSICS & CAMERA STATE
# ==========================================
# OOP NOTE: The x, y, vx, vy variables would become self.x, self.y, etc., in a Player class
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

# OOP NOTE: Camera could be its own class managing what part of the world is visible
camera_x = 0.0
LEFT_DEAD_ZONE = SCREEN_WIDTH * 0.25
RIGHT_DEAD_ZONE = SCREEN_WIDTH * 0.75

current_anim = "idle"
current_frame = 0
animation_timer = 0
playing = True

# ==========================================
# WORLD GENERATION SETUP
# ==========================================
# Groups to hold all active entities
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
demon_group = pygame.sprite.Group()  # NEW: Tracks patrolling demons
last_spawned_bg_index = 0  # NEW: Tracks which background panel we are on

# Create Initial Starting Platforms
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

    # 1. EVENT HANDLING (OOP NOTE: Could be Game.handle_events())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not game_over:

        # 2. INPUT GATHERING (OOP NOTE: Could be Player.handle_input())
        keys = pygame.key.get_pressed()
        moving = False
        run_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        duck_pressed = keys[pygame.K_DOWN]

        # Check if she is standing back up from a duck
        recovering_duck = (current_anim == "duck" and not duck_pressed and playing)

        # Apply movement intent based on keys
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

        # Apply jump intent
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

        # 3. PHYSICS & COLLISIONS (OOP NOTE: Could be Player.update_physics())
        x += vx * dt  # Move horizontally

        if not on_ground:
            vy += gravity * dt
            y += vy * dt  # Move vertically

            # Check Platform Collisions while falling
            for platform in platform_group:
                # If falling (vy > 0) AND player rect intersects platform rect
                if vy > 0 and platform.rect.colliderect(x - 20, y - 5, 40, 10):
                    # Snap feet to the top of the platform
                    if y - vy * dt <= platform.rect.top + 10:
                        y = platform.rect.top
                        vy = 0
                        on_ground = True
                        break

            # Check Ground Floor Collision
            if y >= y_ground:
                y = y_ground
                vy = 0
                on_ground = True
        else:
            # If on ground, verify we haven't walked off the edge of a platform
            on_platform = False
            for platform in platform_group:
                if platform.rect.colliderect(x - 20, y, 40, 5):
                    on_platform = True
                    break
            if not on_platform and y < y_ground:
                on_ground = False  # Start falling!

        # 4. ANIMATION STATE MACHINE (OOP NOTE: Could be Player.update_animation_state())
        if not on_ground:
            pass  # Keep playing air animation
        elif recovering_duck:
            pass  # Keep playing standing-up animation
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

        # 5. CAMERA LOGIC (OOP NOTE: Could be Camera.update(player.x))
        screen_x = x - camera_x
        if screen_x > RIGHT_DEAD_ZONE:
            camera_x += (screen_x - RIGHT_DEAD_ZONE)
        elif screen_x < LEFT_DEAD_ZONE:
            camera_x -= (LEFT_DEAD_ZONE - screen_x)

        # 6. WORLD GENERATION & CLEANUP (OOP NOTE: Could be LevelManager.update())

        # Clear platforms that are way behind the camera (Allows generous backtracking)
        for platform in list(platform_group):
            if platform.rect.right < camera_x - 4000:
                platform.kill()

        # Continuously generate platforms ahead of the camera
        if len(platform_group) < max_platforms:
            last_platform = max(platform_group, key=lambda p: p.rect.x, default=None)
            if last_platform:
                # Measure the GAP directly from the right end of the previous platform
                gap = random.randint(120, 290)
                p_x = last_platform.rect.right + gap
            else:
                p_x = camera_x + SCREEN_WIDTH + 100

            # Narrower platforms (100px - 180px) demand cleaner landing precision
            p_w = random.randint(90, 200)

            # Vertical height range (320px - 620px)
            p_y = random.randint(320, 625)

            platform_group.add(Platform(p_x, p_y, p_w))

        # Generate Bats (max 3 on screen)
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

        # NEW: Spawn Demon on every 3rd background panel
        current_bg_index = int(x // bg_w)

        # Check if you have crossed into a new background panel
        if current_bg_index > last_spawned_bg_index:
            # If the NEXT background is a multiple of 3 (e.g., bg 3, 6, 9...)
            if (current_bg_index + 1) % 2 == 0:
                if len(demon_group) == 0:
                    target_bg_index = current_bg_index + 1

                    # Set patrol bounds to the exact width of that 3rd background panel
                    patrol_start = target_bg_index * bg_w
                    patrol_end = (target_bg_index + 1) * bg_w - 100

                    # Spawn him slightly inside the left edge of that background
                    spawn_x = patrol_start + 50

                    # Create demon aligned to the floor height
                    demon = Demon(spawn_x, y_ground, patrol_start, patrol_end, scale=0.35)
                    demon_group.add(demon)

            # Update the tracker so we don't spawn multiple times per panel
            last_spawned_bg_index = current_bg_index

        # Update Enemy positions
        enemy_group.update(camera_x)
        demon_group.update(camera_x)

        # Track distance traveled as score
        score = int(x)

        # 7. ADVANCE FRAME TIMERS
        anim_frames = animations[current_anim]
        delay = animation_speeds.get(current_anim, 120)
        loop = animation_loops.get(current_anim, True)
        animation_timer += dt_ms

        # Custom logic to freeze frames on specific poses (Ducking / Mid-air)
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

        # Step frames forward based on time elapsed
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

        # ==========================================
        # 8. DRAWING PHASE (OOP NOTE: Could be Game.draw())
        # ==========================================

        # A. Draw Looping Wall Backgrounds
        start_bg_index = int(camera_x // bg_w)
        num_bgs_to_draw = (SCREEN_WIDTH // bg_w) + 2
        for i in range(start_bg_index, start_bg_index + num_bgs_to_draw):
            current_bg = bg_list[i % len(bg_list)]
            bg_screen_x = (i * bg_w) - camera_x
            screen.blit(current_bg, (bg_screen_x, 0))

        # B. Draw Floor Backgrounds
        start_floor_index = int(camera_x // floor_w)
        num_floors_to_draw = (SCREEN_WIDTH // floor_w) + 2
        floor_draw_y = SCREEN_HEIGHT - target_floor_h + 30
        for i in range(start_floor_index, start_floor_index + num_floors_to_draw):
            current_floor = floor_img if i % 2 == 0 else floor_flip_img
            floor_screen_x = (i * floor_w) - camera_x
            screen.blit(current_floor, (floor_screen_x, floor_draw_y))

        # C. Draw Platforms relative to camera view
        for platform in platform_group:
            plat_screen_x = platform.rect.x - camera_x
            if -200 < plat_screen_x < SCREEN_WIDTH + 200:
                screen.blit(platform.image, (plat_screen_x, platform.rect.y))

        # D. Draw Player
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

        # E. Draw Bats and Check True Pixel-Perfect Collision
        for enemy in enemy_group:
            enemy_screen_x = enemy.rect.x - camera_x
            screen.blit(enemy.image, (enemy_screen_x, enemy.rect.y))

            # If the visible pixels of the bat overlap the visible pixels of the player...
            offset = (blit_x - enemy_screen_x, blit_y - enemy.rect.y)
            if enemy.mask.overlap(player_mask, offset):
                game_over = True
                try:
                    death_fx.play()
                except:
                    pass

        # NEW: Draw Demon relative to camera view & check collision
        for demon in demon_group:
            demon_screen_x = demon.rect.x - camera_x

            # Only draw if near visible screen
            if -200 < demon_screen_x < SCREEN_WIDTH + 200:
                screen.blit(demon.image, (demon_screen_x, demon.rect.y))

                # Pixel-perfect collision check
                offset = (blit_x - demon_screen_x, blit_y - demon.rect.y)
                if demon.mask.overlap(player_mask, offset):
                    game_over = True
                    try:
                        death_fx.play()
                    except:
                        pass

        # F. Draw UI Overlay
        draw_panel()

    else:
        # ==========================================
        # GAME OVER STATE
        # ==========================================
        # Draw the death screen background starting at top-left (0, 0)
        screen.blit(end_image, (0, 0))
        # pygame.draw.line(surface, color, start_pos, end_pos, width)
        pygame.draw.line(screen, Color("plum1"), (350, 245), (500 + 520, 245), 6)
        draw_text("YOUR SOUL HAS BEEN LOST!!", font_big, Color("blue1"), SCREEN_WIDTH // 2 - 350, 250)
        pygame.draw.line(screen, Color("plum1"), (350, 315), (500 + 520, 315), 6)
        draw_text("SCORE: " + str(score), font_big, Color("turquoise1"), SCREEN_WIDTH // 2 - 150, 320)
        pygame.draw.line(screen, Color("plum1"), (350, 400), (500 + 520, 400), 6)
        draw_text("PRESS SPACE TO TRY AGAIN", font_big, Color("blue1"), SCREEN_WIDTH // 2 - 330, 400)
        pygame.draw.line(screen, Color("plum1"), (350, 475), (SCREEN_WIDTH // 2 + 330, 475), 6)

        if score > high_score:
            high_score = score
            with open("score.txt", "w") as file:
                file.write(str(high_score))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # Reset Game Variables
            game_over = False
            score = 0
            x = 400.0
            y = y_ground
            camera_x = 0.0
            enemy_group.empty()
            platform_group.empty()

            # NEW: Clear demon state
            demon_group.empty()
            last_spawned_bg_index = 0

            # Generate fresh starting platforms
            starting_platform = Platform(200, 580, 180)
            platform_group.add(starting_platform)
            platform_group.add(Platform(550, 480, 300))
            platform_group.add(Platform(900, 380, 260))

    pygame.display.update()

mixer.quit()
pygame.quit()
sys.exit()