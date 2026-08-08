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

    screen = pygame.display.set_mode((1400, 800))
    pygame.display.set_caption("Sprite Sheet Viewer - Air Physics & Ducking Fixes")
    clock = pygame.time.Clock()

    # Load animations
    animations = {
        "idle": get_sprites_from_sheet("spritsheets/S_IDLE_NB.png"),
        "walk": get_sprites_from_sheet("spritsheets/S_WALK_NB.png"),
        "run": get_sprites_from_sheet("spritsheets/S_RUN_NB.png"),
        "jump": get_sprites_from_sheet("spritsheets/S_JUMP_NB.png"),
        "run_jump": get_sprites_from_sheet("spritsheets/S_RUN_JUMP_NB.png"),
        "duck": get_sprites_from_sheet("spritsheets/S_DUCK_NB.png")
    }

    # Per-animation timing (ms per frame)
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


    # 1.0 is default size. 1.2 means 20% larger. Tweak these numbers until they match the idle!
    animation_scale_corrections = {
        "idle": 1.0,
        "walk": 1.08,  # Boost walk size
        "run": 1.08,  # Boost run size (she looked smallest here)
        "jump": 1.0,
        "run_jump": 1.08,
        "duck": 1.0
    }

    # Character physics/state
    x = 600.0
    y_ground = 700.0
    y = y_ground
    vx = 0.0
    vy = 0.0
    speed_walk = 180.0
    speed_run = 320.0
    gravity = 1500.0
    jump_impulse = -700.0
    on_ground = True
    facing_right = True

    # Animation playback state
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

        # Check if she is currently in the second half of the duck animation (standing back up)
        # This occurs when she is in the duck anim, the button is released, and it hasn't reached the last frame yet
        recovering_duck = (current_anim == "duck" and not duck_pressed and playing)

        # Input logic
        if recovering_duck:
            vx = 0  # Lock movement while she stands back up
        elif duck_pressed and on_ground:
            vx = 0  # Cannot walk while ducking
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

        # Jump logic (Prevent jumping if she is ducking or recovering from a duck)
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

        # ==========================================
        # PHYSICS OVERHAUL
        # ==========================================

        # Apply horizontal movement globally so running jumps keep their forward momentum!
        x += vx * dt

        if not on_ground:
            vy += gravity * dt
            y += vy * dt
            # landing detection
            if y >= y_ground:
                y = y_ground
                vy = 0
                on_ground = True

                # Choose landing fallback animation
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
            # Handle ground animation state changes
            if recovering_duck:
                # Do nothing, let the animation block below advance her frames until she is fully standing
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
        # ANIMATION TIMING & CLAMPING
        # ==========================================
        anim_frames = animations[current_anim]
        delay = animation_speeds.get(current_anim, 120)
        loop = animation_loops.get(current_anim, True)
        animation_timer += dt_ms

        # --- NEW CUSTOM FRAME CLAMPS ---

        # 1. Duck Hold: Pause on 7th frame (index 6) as long as DOWN is held
        if current_anim == "duck" and duck_pressed:
            if current_frame >= 6:
                current_frame = 6
                animation_timer = 0  # Prevent the timer from advancing

        # 2. Jump Hangtime: Pause on the "falling" frame so she doesn't play landing frames in mid-air
        if current_anim == "jump" and not on_ground:
            if current_frame >= 5:  # Index 5 is the peak/fall frame in your 9-frame sheet
                current_frame = 5
                animation_timer = 0

        # 3. Running Jump Hangtime
        if current_anim == "run_jump" and not on_ground:
            if current_frame >= 9:  # Index 9 is the fall loop in your 13-frame sheet
                current_frame = 9
                animation_timer = 0

        # Standard playback logic
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

                # Check if animation is finished
                if current_frame >= len(anim_frames) - 1:
                    current_frame = len(anim_frames) - 1
                    playing = False  # Setting playing to False signals that 'recovering_duck' is finished next loop

        # Draw
        screen.fill((50, 150, 200))

        # draw ground line for reference
        pygame.draw.line(screen, (80, 80, 80), (0, y_ground + 1), (1400, y_ground + 1), 2)

        # get current frame surface and scale for display
        frame_surf = anim_frames[current_frame]
        display_w, display_h = frame_surf.get_size()

        # Base scale down character for screen
        base_scale_factor = 0.65

        # Apply the custom correction multiplier for the current animation
        correction = animation_scale_corrections.get(current_anim, 1.0)
        final_scale = base_scale_factor * correction

        frame_to_draw = pygame.transform.smoothscale(frame_surf,
                                                     (int(display_w * final_scale), int(display_h * final_scale)))

        if not facing_right:
            frame_to_draw = pygame.transform.flip(frame_to_draw, True, False)

        # draw using bottom anchor: place so feet sit on y
        fw, fh = frame_to_draw.get_size()
        blit_x = int(x - fw // 2)
        blit_y = int(y - fh)
        screen.blit(frame_to_draw, (blit_x, blit_y))

        # debug text
        font = pygame.font.SysFont(None, 20)
        txt = f"Anim: {current_anim}  Frame: {current_frame}/{len(anim_frames) - 1}  Pos: ({int(x)},{int(y)}) on_ground:{on_ground}"
        screen.blit(font.render(txt, True, (255, 255, 255)), (8, 8))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()