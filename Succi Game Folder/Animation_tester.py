import pygame
import sys


def get_sprites_from_sheet(filename, approx_width=860):
    """
    Extracts individual sprites using fixed-width slicing.
    No auto-cropping, so the center axis remains as stable as the original image allows.
    """
    try:
        sheet = pygame.image.load(filename).convert_alpha()
    except pygame.error as e:
        print(f"Unable to load sprite sheet image: {filename}")
        raise SystemExit(e)

    sheet_width, sheet_height = sheet.get_size()
    num_frames = round(sheet_width / approx_width)
    exact_sprite_width = sheet_width // num_frames

    sprites = []
    for i in range(num_frames):
        # Create a surface with explicit alpha transparency
        sprite = pygame.Surface((exact_sprite_width, sheet_height), pygame.SRCALPHA).convert_alpha()
        rect_to_copy = (i * exact_sprite_width, 0, exact_sprite_width, sheet_height)

        # Blit the exact fixed slice
        sprite.blit(sheet, (0, 0), rect_to_copy)
        sprites.append(sprite)

    return sprites


# ==========================================
# Example Usage Setup
# ==========================================

def main():
    pygame.init()

    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Sprite Sheet Viewer - Stable Slices")
    clock = pygame.time.Clock()

    # Load animations
    animations = {
        "idle": get_sprites_from_sheet("idle_sheet2.png"),
        "walk": get_sprites_from_sheet("walk_sheet.png"),
        "run": get_sprites_from_sheet("run_sheet.png"),
        "jump": get_sprites_from_sheet("jump_sheet.png"),
        "run_jump": get_sprites_from_sheet("run_jump_sheet.png")
    }

    current_anim = "walk"
    current_frame = 0
    animation_timer = 0

    # Dictionary for independent animation speeds (milliseconds)
    animation_speeds = {
        "idle": 150,
        "walk": 100,
        "run": 50,
        "jump": 80,
        "run_jump": 60
    }

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: current_anim = "idle"
                if event.key == pygame.K_2: current_anim = "walk"
                if event.key == pygame.K_3: current_anim = "run"
                if event.key == pygame.K_4: current_anim = "jump"
                if event.key == pygame.K_5: current_anim = "run_jump"
                current_frame = 0

                # Timing logic
        animation_timer += dt
        current_delay = animation_speeds[current_anim]
        if animation_timer >= current_delay:
            current_frame = (current_frame + 1) % len(animations[current_anim])
            animation_timer = 0

        screen.fill((50, 150, 200))

        image_to_draw = animations[current_anim][current_frame]

        # Get original width/height and scale down by 50%
        orig_w, orig_h = image_to_draw.get_size()
        scaled_image = pygame.transform.smoothscale(image_to_draw, (orig_w // 2, orig_h // 2))

        # Draw the sprite at fixed coordinates to prevent any code-induced sliding
        screen.blit(scaled_image, (350, 100))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()