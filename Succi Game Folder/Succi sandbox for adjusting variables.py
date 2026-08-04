import pygame
import sys


def get_sprites_from_sheet(filename, approx_width=810, target_h=1080):
    """
    Extracts individual sprites using fixed-width slicing.
    Pads 1 pixel if height == target_h - 1 to avoid vertical drift.
    """
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

    print(
        f"Loaded '{filename}' -> sheet {sheet_width}x{sheet_height}, frames: {num_frames}, frame_w: {exact_sprite_width}")
    return sprites


# ==========================================
# Main Game Loop
# ==========================================
def main():
    pygame.init()

    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sprite Sheet Viewer - Scrolling Camera & Floor")
    clock = pygame.time.Clock()

    # ==========================================
    # LOAD BACKGROUNDS & FLOOR
    # ==========================================
    try:
        # Load Wall Background
        bg_img = pygame.image.load("cross_bg.png").convert()
        bg_flip_img = pygame.image.load("cross_bg_flip.png").convert()

        bg_scale_ratio = SCREEN_HEIGHT / bg_img.get_height()
        bg_w = int(bg_img.get_width() * bg_scale_ratio)

        bg_img = pygame.transform.smoothscale(bg_img, (bg_w, SCREEN_HEIGHT))
        bg_flip_img = pygame.transform.smoothscale(bg_flip_img, (bg_w, SCREEN_HEIGHT))

        # Load Floor
        floor_img = pygame.image.load("floor2.PNG").convert()
        # Make the solid black area at the top of the floor image transparent
        floor_img.set_colorkey((0, 0, 0))

        # Scale the floor (adjust target_floor_h if you want the floor taller/shorter)
        target_floor_h = 225
        floor_scale_ratio = target_floor_h / floor_img.get_height()
        floor_w = int(floor_img.get_width() * floor_scale_ratio)
        floor_img = pygame.transform.smoothscale(floor_img, (floor_w, target_floor_h))

        # Auto-generate a flipped floor image for perfect seamless tiling
        floor_flip_img = pygame.transform.flip(floor_img, True, False)

    except pygame.error as e:
        print("Could not load background or floor images. Check filenames!")
        raise SystemExit(e)

    # ==========================================
    # LOAD ANIMATIONS
    # ==========================================
    animations = {
        "idle": get_sprites_from_sheet("S_IDLE_NB.png"),
        "walk": get_sprites_from_sheet("S_WALK_NB.png"),
        "run": get_sprites_from_sheet("S_RUN_NB.png"),
        "jump": get_sprites_from_sheet("S_JUMP_NB.png"),
        "run_jump": get_sprites_from_sheet("S_RUN_JUMP_NB.png"),
        "duck": get_sprites_from_sheet("S_DUCK_NB.png")
    }

    animation_speeds = {
        "idle": 175,
        "walk": 130,
        "run": 75,
        "jump": 80,
        "run_jump": 50,
        "duck": 50
    }

    animation_loops = {
        "idle": True,
        "walk": True,
        "run": True,
        "jump": False,
        "run_jump": False,
        "duck": False
    }

    animation_scale_corrections = {
        "idle": 1.0,
        "walk": 1.08,
        "run": 1.08,
        "jump": 1.0,
        "run_jump": 1.08,
        "duck": 1.0
    }

    # ==========================================
    # PHYSICS & STATE
    # ==========================================
    x = 600.0
    y_ground = 730.0  # Slightly adjusted so her feet sit perfectly on the stone edge
    y = y_ground
    vx = 0.0
    vy = 0.0
    speed_walk = 180.0
    speed_run = 320.0
    gravity = 1500.0
    jump_impulse = -700.0
    on_ground = True
    facing_right = True

    camera_x = 0.0

    LEFT_DEAD_ZONE = SCREEN_WIDTH * 0.25
    RIGHT_DEAD_ZONE = SCREEN_WIDTH * 0.75

    current_anim = "idle" if "idle" in animations else next(iter(animations))
    current_frame = 0
    animation_timer = 0
    playing = True

    running = True
    while running:
        dt_ms = clock.tick(60)
        dt = dt_ms / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        moving = False
        run_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        duck_pressed = keys[pygame.K_DOWN]

        recovering_duck = (current_anim == "duck" and not duck_pressed and playing)

        # Input logic
        if recovering_duck:
            vx = 0
        elif duck_pressed and on_ground:
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

        # Jump logic
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

        # Apply global horizontal movement
        x += vx * dt

        if not on_ground:
            vy += gravity * dt
            y += vy * dt
            if y >= y_ground:
                y = y_ground
                vy = 0
                on_ground = True
                if recovering_duck:
                    pass
                elif duck_pressed:
                    current_anim = "duck"
                elif moving:
                    current_anim = "run" if run_pressed and "run" in animations else "walk" if "walk" in animations else "idle"
                else:
                    current_anim = "idle" if "idle" in animations else current_anim
                current_frame = 0
                animation_timer = 0
                playing = True
        else:
            if recovering_duck:
                pass
            elif duck_pressed:
                if current_anim != "duck":
                    current_anim = "duck";
                    current_frame = 0;
                    animation_timer = 0;
                    playing = True
            elif moving:
                if run_pressed and "run" in animations:
                    if current_anim != "run":
                        current_anim = "run";
                        current_frame = 0;
                        animation_timer = 0;
                        playing = True
                else:
                    if "walk" in animations and current_anim != "walk":
                        current_anim = "walk";
                        current_frame = 0;
                        animation_timer = 0;
                        playing = True
            else:
                if "idle" in animations and current_anim != "idle":
                    current_anim = "idle";
                    current_frame = 0;
                    animation_timer = 0;
                    playing = True

        # ==========================================
        # CAMERA DEAD ZONE LOGIC
        # ==========================================
        screen_x = x - camera_x

        if screen_x > RIGHT_DEAD_ZONE:
            camera_x += (screen_x - RIGHT_DEAD_ZONE)
        elif screen_x < LEFT_DEAD_ZONE:
            camera_x -= (LEFT_DEAD_ZONE - screen_x)

        # ==========================================
        # ANIMATION TIMING
        # ==========================================
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

                    # ==========================================
        # DRAWING & RENDERING
        # ==========================================

        # 1. DRAW WALL BACKGROUND
        start_bg_index = int(camera_x // bg_w)
        num_bgs_to_draw = (SCREEN_WIDTH // bg_w) + 2

        for i in range(start_bg_index, start_bg_index + num_bgs_to_draw):
            current_bg = bg_img if i % 2 == 0 else bg_flip_img
            bg_screen_x = (i * bg_w) - camera_x
            screen.blit(current_bg, (bg_screen_x, 0))

        # 2. DRAW FLOOR
        start_floor_index = int(camera_x // floor_w)
        num_floors_to_draw = (SCREEN_WIDTH // floor_w) + 2

        # Calculate where the floor should be drawn so the stone surface lines up with y_ground
        floor_draw_y = SCREEN_HEIGHT - target_floor_h + 30

        for i in range(start_floor_index, start_floor_index + num_floors_to_draw):
            current_floor = floor_img if i % 2 == 0 else floor_flip_img
            floor_screen_x = (i * floor_w) - camera_x
            screen.blit(current_floor, (floor_screen_x, floor_draw_y))

        # 3. DRAW CHARACTER
        frame_surf = anim_frames[current_frame]
        display_w, display_h = frame_surf.get_size()
        base_scale_factor = 0.35

        correction = animation_scale_corrections.get(current_anim, 1.0)
        final_scale = base_scale_factor * correction

        frame_to_draw = pygame.transform.smoothscale(frame_surf,
                                                     (int(display_w * final_scale), int(display_h * final_scale)))

        if not facing_right:
            frame_to_draw = pygame.transform.flip(frame_to_draw, True, False)

        fw, fh = frame_to_draw.get_size()

        blit_x = int((x - camera_x) - fw // 2)
        blit_y = int(y - fh)
        screen.blit(frame_to_draw, (blit_x, blit_y))

        # 4. DEBUG TEXT
        font = pygame.font.SysFont(None, 20)
        txt = f"Anim: {current_anim} | World X: {int(x)} | Camera X: {int(camera_x)} | Screen X: {int(screen_x)}"
        screen.blit(font.render(txt, True, (255, 255, 255)), (8, 8))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()