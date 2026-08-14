import pygame
import sys
import os
from pygame import mixer, Color

# OOP Imports
from player import Player
from entities import Projectile, Merchant
from level import Level_01, Merchant_Room

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# ==========================================
# INITIALIZATION & AUDIO
# ==========================================
mixer.init()
pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Succi Solace")

try:
    game_icon = pygame.image.load("mats/pink design.png").convert_alpha()
    pygame.display.set_icon(game_icon)
except pygame.error:
    pass

clock = pygame.time.Clock()
FPS = 60

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

    # Merchant Voice Line
    merchant_voice_fx = pygame.mixer.Sound("mats/merchant entrance.mp3")
    merchant_voice_fx.set_volume(0.6)
except pygame.error as e:
    print(f"Audio Load Warning: {e}")

# ==========================================
# UI & PLAYER ASSET LOADING
# ==========================================
WHITE, BLACK, PINK, LIGHT_GRAY = (255, 255, 255), (0, 0, 0), (253, 117, 234), (180, 180, 180)
font_small = pygame.font.SysFont("Lucida Sans", 20)
font_big = pygame.font.SysFont("Lucida Sans", 48)

if os.path.exists("score.txt"):
    with open("score.txt", "r") as file:
        high_score = int(file.read())
else:
    high_score = 0


def get_sprites_from_sheet(filename, approx_width=810, target_h=1080):
    sheet = pygame.image.load(filename).convert_alpha()
    sw, sh = sheet.get_size()
    if sh == target_h - 1:
        padded = pygame.Surface((sw, target_h), pygame.SRCALPHA)
        padded.fill((0, 0, 0, 0))
        padded.blit(sheet, (0, 0))
        sheet, sh = padded, target_h
    num_frames = max(1, round(sw / approx_width))
    fw = sw // num_frames
    return [pygame.transform.smoothscale(sheet.subsurface((i * fw, 0, fw, sh)), (fw, target_h)) for i in
            range(num_frames)]


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
animation_speeds = {"idle": 175, "walk": 130, "run": 75, "jump": 80, "run_jump": 50, "duck": 50, "attack": 90,
                    "run_attack": 75}
animation_loops = {"idle": True, "walk": True, "run": True, "jump": False, "run_jump": False, "duck": False,
                   "attack": False, "run_attack": False}
animation_scale_corrections = {"idle": 1.0, "walk": 1.08, "run": 1.08, "jump": 1.0, "run_jump": 1.08, "duck": 1.0,
                               "attack": 2.8, "run_attack": 1.08}

fireball_img = pygame.image.load("spritsheets/fireball.png").convert_alpha()
explode_img = pygame.image.load("spritsheets/explode_NB.png").convert_alpha()
end_image = pygame.transform.smoothscale(pygame.image.load("backgrounds/death_screen.png").convert_alpha(),
                                         (SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_text(text, font, text_col, x, y): screen.blit(font.render(text, True, text_col), (x, y))


def draw_panel(score, rem):
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, PINK, (0, 30), (SCREEN_WIDTH, 30), 3)
    draw_text(f"SCORE: {score}     REM: {rem}", font_small, WHITE, 10, 5)
    draw_text(f"HIGH SCORE: {high_score}", font_small, WHITE, SCREEN_WIDTH // 2 - 80, 5)


# ==========================================
# GAME STATE SETUP
# ==========================================
current_state = "LEVEL_1"
game_over, paused = False, False
camera_x = 0.0
rem = 0  # Currency Tracker

current_level = Level_01(SCREEN_WIDTH, SCREEN_HEIGHT)
merchant_room = Merchant_Room(SCREEN_WIDTH, SCREEN_HEIGHT)
merchant_npc = None  # Loaded on demand when entering the room

succi = Player(400.0, current_level.y_ground, animations, animation_speeds, animation_scale_corrections, jump_fx,
               cast_fx)
projectile_group = pygame.sprite.Group()

# ==========================================
# MAIN GAME LOOP
# ==========================================
run = True
while run:
    dt_ms = clock.tick(FPS)
    dt = dt_ms / 1000.0
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                if not game_over: paused = not paused
            # DEBUG SHORTCUT: Press 'M' to instantly teleport to the merchant door screen
            elif event.key == pygame.K_m and current_state == "LEVEL_1":
                succi.x = current_level.level_end_x - 300
                camera_x = current_level.level_end_x - SCREEN_WIDTH

    if not game_over and not paused:

        if current_state == "LEVEL_1":
            succi.update(keys, dt, dt_ms, current_level.platform_group, animation_loops)

            # Prevent Succi from walking past the end of the level
            if succi.x > current_level.level_end_x - 100:
                succi.x = current_level.level_end_x - 100

            if (succi.attacking and
                    succi.current_frame == (8 if succi.current_anim == "attack" else 4) and
                    not succi.fireball_spawned):
                spawn_x = succi.x + (90 if succi.facing_right else -90)
                projectile_group.add(
                    Projectile(spawn_x, succi.y - 180, 1 if succi.facing_right else -1, fireball_img, explode_img,
                               0.28))
                succi.fireball_spawned = True
                try:
                    cast_fx.play()
                except NameError:
                    pass

            screen_x = succi.x - camera_x
            if screen_x > SCREEN_WIDTH * 0.75:
                camera_x += (screen_x - SCREEN_WIDTH * 0.75)
            elif screen_x < SCREEN_WIDTH * 0.25:
                camera_x -= (SCREEN_WIDTH * 0.25 - screen_x)

            # Stop Camera at the end of the level
            if camera_x > current_level.level_end_x - SCREEN_WIDTH:
                camera_x = current_level.level_end_x - SCREEN_WIDTH
            if camera_x < 0: camera_x = 0

            current_level.update(dt, camera_x, succi.x, succi.y)
            projectile_group.update(dt, camera_x, SCREEN_WIDTH)

            # Projectile Hits & REM Collection
            for proj in projectile_group:
                if proj.state == "fly":
                    for group in [current_level.enemy_group, current_level.demon_group, current_level.skeleton_group]:
                        for target in group:
                            ty = target.rect.top if hasattr(target, 'state') else target.rect.y
                            if proj.mask.overlap(target.mask, (target.rect.x - proj.rect.x, ty - proj.rect.y)):
                                proj.explode()
                                rem += target.rem_value  # Collect REM
                                target.kill()
                                try:
                                    explode_fx.play()
                                except NameError:
                                    pass
                                break
                        if proj.state != "fly": break

            score = int(succi.x)

        elif current_state == "MERCHANT":
            # Update the merchant's cutscene/animation frames and sync audio
            if merchant_npc:
                merchant_npc.update(dt_ms, merchant_voice_fx)

    # ==========================================
    # DRAWING PHASE
    # ==========================================
    if not game_over:
        if current_state == "LEVEL_1":
            current_level.draw(screen, camera_x)

            succi_blit_x, succi_blit_y = succi.draw(screen, camera_x)

            for proj in projectile_group:
                if -200 < (px := proj.rect.x - camera_x) < SCREEN_WIDTH + 200: screen.blit(proj.image,
                                                                                           (px, proj.rect.y))

            for group in [current_level.enemy_group, current_level.demon_group, current_level.skeleton_group]:
                for target in group:
                    tx = target.rect.x - camera_x
                    if -200 < tx < SCREEN_WIDTH + 200:
                        ty = target.rect.top if hasattr(target, 'state') else target.rect.y
                        if target.mask.overlap(succi.mask, (succi_blit_x - tx, succi_blit_y - ty)):
                            game_over = True
                            try:
                                death_fx.play()
                            except NameError:
                                pass

            # DOOR INTERACTION LOGIC (Triggers anywhere on the final background screen)
            current_bg_index = int(succi.x // current_level.bg_w)
            if current_bg_index >= current_level.max_backgrounds - 1:
                if keys[pygame.K_e]:
                    current_state = "MERCHANT"
                    pygame.mixer.music.stop()  # Stop level background music

                    if merchant_npc is None:
                        merchant_npc = Merchant(SCREEN_WIDTH, SCREEN_HEIGHT, "spritsheets/merchant_SS.png",
                                                columns=7, rows=4)

                    succi.x = 400.0  # Reset position safely inside merchant room

        elif current_state == "MERCHANT":
            # Draw the merchant room background
            merchant_room.draw(screen, 0)

            # Draw the cutscene animation frames playing
            if merchant_npc:
                merchant_npc.draw(screen)

        draw_panel(score, rem)

        if paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            draw_text("GAME PAUSED", font_big, Color("turquoise1"), SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 50)
            draw_text("Press 'P' or 'ESC' to Resume", font_small, LIGHT_GRAY, SCREEN_WIDTH // 2 - 140,
                      SCREEN_HEIGHT // 2 + 20)
            ctrl_x = SCREEN_WIDTH - 280
            draw_text("CONTROLS:", font_small, PINK, ctrl_x, 50)
            draw_text("Arrow Keys : Move / Duck", font_small, Color("blue1"), ctrl_x, 80)
            draw_text("Shift      : Run", font_small, Color("blue1"), ctrl_x, 105)
            draw_text("Space      : Jump", font_small, Color("blue1"), ctrl_x, 130)
            draw_text("F Key      : Cast Fireball", font_small, Color("blue1"), ctrl_x, 155)
            draw_text("E Key      : To Enter", font_small, Color("blue1"), ctrl_x, 180)
            draw_text("P / ESC    : Pause", font_small, PINK, ctrl_x, 205)


    else:
        screen.blit(end_image, (0, 0))
        pygame.draw.line(screen, Color("plum1"), (350, 245), (870, 245), 6)
        draw_text("YOUR SOUL HAS BEEN LOST!!", font_big, Color("blue1"), SCREEN_WIDTH // 2 - 350, 250)
        pygame.draw.line(screen, Color("plum1"), (350, 315), (870, 315), 6)
        draw_text(f"SCORE: {score}", font_big, Color("turquoise1"), SCREEN_WIDTH // 2 - 150, 320)
        pygame.draw.line(screen, Color("plum1"), (350, 400), (870, 400), 6)
        draw_text("PRESS SPACE TO TRY AGAIN", font_big, Color("blue1"), SCREEN_WIDTH // 2 - 330, 400)
        pygame.draw.line(screen, Color("plum1"), (350, 475), (SCREEN_WIDTH // 2 + 330, 475), 6)

        if score > high_score:
            high_score = score
            with open("score.txt", "w") as file: file.write(str(high_score))

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            game_over, paused, camera_x, rem = False, False, 0.0, 0
            current_state = "LEVEL_1"
            current_level.reset()  # <--- Fast reset using already-loaded assets!
            merchant_npc = None
            succi = Player(400.0, current_level.y_ground, animations, animation_speeds, animation_scale_corrections,
                           jump_fx, cast_fx)
            projectile_group.empty()

            # Restart background music if it was stopped in the merchant room
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1, 0.0)

    pygame.display.update()

mixer.quit()
pygame.quit()
sys.exit()