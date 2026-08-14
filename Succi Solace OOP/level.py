import pygame
import random
from entities import Enemy, Demon, Skeleton, Platform


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
        if has_content: left = x; break
    for x in range(w - 1, w - 1 - (w // 4), -1):
        has_content = False
        for y in range(0, h, 10):
            color = surface.get_at((x, y))
            if color.r > threshold or color.g > threshold or color.b > threshold:
                has_content = True
                break
        if has_content: right = x + 1; break
    if right > left: return surface.subsurface((left, 0, right - left, h)).copy()
    return surface


def load_enemy_frames(filename, num_frames, scale):
    sheet = pygame.image.load(filename).convert_alpha()
    frames_r, frames_l = [], []
    fw, fh = sheet.get_width() // num_frames, sheet.get_height()
    for i in range(num_frames):
        frame = pygame.Surface((fw, fh), pygame.SRCALPHA).convert_alpha()
        frame.blit(sheet, (0, 0), (i * fw, 0, fw, fh))
        frame_r = pygame.transform.smoothscale(frame, (int(fw * scale), int(fh * scale)))
        frames_r.append(frame_r)
        frames_l.append(pygame.transform.flip(frame_r, True, False))
    return frames_r, frames_l


class Level_01:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.y_ground = 730.0

        # 8 backgrounds * 2 loops = 16 + 1 Merchant Door = 17 Total
        self.max_backgrounds = 17

        self.platform_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.demon_group = pygame.sprite.Group()
        self.skeleton_group = pygame.sprite.Group()

        self.last_spawned_bg_index = -1
        self.load_assets()

        self.level_end_x = self.max_backgrounds * self.bg_w

        # Exact world X coordinate where the merchant door sits on the 17th background
        self.door_world_x = ((self.max_backgrounds - 1) * self.bg_w) + 900

        self.platform_group.add(Platform(200, 580, 180, self.platform_image))
        self.platform_group.add(Platform(450, 380, 200, self.platform_image))
        self.platform_group.add(Platform(800, 480, 160, self.platform_image))

    def load_assets(self):
        base_bg_filenames = [
            "backgrounds/cross_bg.png", "backgrounds/cross_bg_flip.png",
            "backgrounds/cross_bg_3.png", "backgrounds/cross_bg_door_flip.PNG",
            "backgrounds/cross_bg_3_flip.PNG", "backgrounds/cross_bg_2.png",
            "backgrounds/cross_bg_4.png", "backgrounds/cross_bg_4_flip.PNG"
        ]

        full_bg_filenames = base_bg_filenames * 2
        full_bg_filenames.append("backgrounds/lvl_1_merchant_bg.png")

        first_raw = pygame.image.load(base_bg_filenames[0]).convert()
        first_trimmed = trim_black_side_borders(first_raw)
        bg_scale_ratio = self.screen_height / first_trimmed.get_height()
        self.bg_w = int(first_trimmed.get_width() * bg_scale_ratio) - 1

        self.bg_list = [pygame.transform.smoothscale(trim_black_side_borders(pygame.image.load(f).convert()),
                                                     (self.bg_w, self.screen_height)) for f in full_bg_filenames]

        floor_img = pygame.image.load("mats/floor2.PNG").convert()
        floor_img.set_colorkey((0, 0, 0))
        self.target_floor_h = 200
        floor_scale_ratio = self.target_floor_h / floor_img.get_height()
        self.floor_w = int(floor_img.get_width() * floor_scale_ratio) - 1
        self.floor_img = pygame.transform.smoothscale(floor_img, (self.floor_w, self.target_floor_h))
        self.floor_flip_img = pygame.transform.flip(self.floor_img, True, False)

        self.platform_image = pygame.image.load("mats/plat31c.png").convert_alpha()
        self.bird_sheet_img = pygame.image.load("spritsheets/enemies/flyer_SS_NB.png").convert_alpha()

        self.demon_walk_r, self.demon_walk_l = load_enemy_frames("spritsheets/enemies/D_WALK_SSNB.png", 7, 0.35)
        self.demon_attack_r, self.demon_attack_l = load_enemy_frames("spritsheets/enemies/D_attack_SSNB.png", 12, 0.35)
        self.skel_walk_r, self.skel_walk_l = load_enemy_frames("spritsheets/enemies/skelly_walk_NB.png", 8, 0.7)
        self.skel_idle_r, self.skel_idle_l = load_enemy_frames("spritsheets/enemies/skelly_idle_NB.png", 10, 0.7)
        self.skel_attack_r, self.skel_attack_l = load_enemy_frames("spritsheets/enemies/skelly_attack_NB.png", 10, 0.7)

    def reset(self):
        """Resets level entities without re-loading images from disk."""
        self.platform_group.empty()
        self.enemy_group.empty()
        self.demon_group.empty()
        self.skeleton_group.empty()
        self.last_spawned_bg_index = -1

        # Re-add starting platforms
        self.platform_group.add(Platform(200, 580, 180, self.platform_image))
        self.platform_group.add(Platform(450, 380, 200, self.platform_image))
        self.platform_group.add(Platform(800, 480, 160, self.platform_image))

    def update(self, dt, camera_x, player_x, player_y):
        for platform in list(self.platform_group):
            if platform.rect.right < camera_x - 4000: platform.kill()

        if camera_x + self.screen_width < self.level_end_x - 500:
            if len(self.platform_group) < 40:
                last_p = max(self.platform_group, key=lambda p: p.rect.x, default=None)
                p_x = (last_p.rect.right + random.randint(120, 290)) if last_p else (camera_x + self.screen_width + 100)
                self.platform_group.add(
                    Platform(p_x, random.randint(320, 625), random.randint(90, 200), self.platform_image))

            if len(self.enemy_group) < 3 and random.randint(1, 60) == 1:
                side = random.choice(["left", "right"])
                ex = (camera_x - 150) if side == "left" else (camera_x + self.screen_width + 150)
                self.enemy_group.add(Enemy(ex, random.randint(200, 550), self.bird_sheet_img, .15,
                                           forced_direction=1 if side == "left" else -1))

        current_bg_index = int(player_x // self.bg_w)

        if current_bg_index > self.last_spawned_bg_index and current_bg_index < self.max_backgrounds - 1:
            t_bg = current_bg_index + 1
            p_start, p_end = t_bg * self.bg_w, (t_bg + 1) * self.bg_w - 100

            if t_bg % 3 == 0:
                self.demon_group.add(
                    Demon(p_start + 100, self.y_ground, p_start, p_end, self.demon_walk_r, self.demon_walk_l,
                          self.demon_attack_r, self.demon_attack_l))
            else:
                self.skeleton_group.add(
                    Skeleton(p_start + 100, self.y_ground, p_start, p_end, self.skel_walk_r, self.skel_walk_l,
                             self.skel_idle_r, self.skel_idle_l, self.skel_attack_r, self.skel_attack_l))

            self.last_spawned_bg_index = current_bg_index

        self.enemy_group.update(camera_x, self.screen_width)
        self.demon_group.update(camera_x, player_x, player_y)
        self.skeleton_group.update(camera_x, player_x, player_y)

    def draw(self, screen, camera_x):
        s_bg = int(camera_x // self.bg_w)
        for i in range(s_bg, s_bg + (self.screen_width // self.bg_w) + 2):
            if i < self.max_backgrounds:
                screen.blit(self.bg_list[i], ((i * self.bg_w) - camera_x, 0))

        s_floor = int(camera_x // self.floor_w)
        for i in range(s_floor, s_floor + (self.screen_width // self.floor_w) + 2):
            if (i * self.floor_w) < self.level_end_x:
                screen.blit(self.floor_img if i % 2 == 0 else self.floor_flip_img,
                            ((i * self.floor_w) - camera_x, self.screen_height - self.target_floor_h + 30))

        for p in self.platform_group:
            if -200 < (px := p.rect.x - camera_x) < self.screen_width + 200: screen.blit(p.image, (px, p.rect.y))

        for enemy in self.enemy_group:
            if -200 < (ex := enemy.rect.x - camera_x) < self.screen_width + 200: screen.blit(enemy.image,
                                                                                             (ex, enemy.rect.y))
        for demon in self.demon_group:
            if -200 < (dx := demon.rect.x - camera_x) < self.screen_width + 200: screen.blit(demon.image,
                                                                                             (dx, demon.rect.top))
        for skel in self.skeleton_group:
            if -200 < (sx := skel.rect.x - camera_x) < self.screen_width + 200: screen.blit(skel.image,
                                                                                            (sx, skel.rect.top))


class Merchant_Room:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.y_ground = 730.0

        try:
            raw_bg = pygame.image.load("backgrounds/lvl_1_merchant_bg.png").convert()
            trimmed_bg = trim_black_side_borders(raw_bg)
            scale_ratio = self.screen_height / trimmed_bg.get_height()
            self.bg_w = int(trimmed_bg.get_width() * scale_ratio)
            self.bg_image = pygame.transform.smoothscale(trimmed_bg, (self.bg_w, self.screen_height))

            floor_img = pygame.image.load("mats/floor2.PNG").convert()
            floor_img.set_colorkey((0, 0, 0))
            self.target_floor_h = 200
            floor_scale_ratio = self.target_floor_h / floor_img.get_height()
            self.floor_w = int(floor_img.get_width() * floor_scale_ratio) - 1
            self.floor_img = pygame.transform.smoothscale(floor_img, (self.floor_w, self.target_floor_h))
        except pygame.error as e:
            print(f"Error loading Merchant Room assets: {e}")
            sys.exit()

    def draw(self, screen, camera_x):
        screen.blit(self.bg_image, (0 - camera_x, 0))
        s_floor = int(camera_x // self.floor_w)
        for i in range(s_floor, s_floor + (self.screen_width // self.floor_w) + 2):
            screen.blit(self.floor_img, ((i * self.floor_w) - camera_x, self.screen_height - self.target_floor_h + 30))


class Level_02(Level_01):
    def __init__(self, screen_width, screen_height):
        # Initialize exactly like Level 1, but we override the asset loading
        super().__init__(screen_width, screen_height)

    def load_assets(self):
        # Override Level 1 assets to use the new purple forest background
        raw_bg = pygame.image.load("backgrounds/lvl_2_bgs/level_2bg.png").convert()
        trimmed_bg = trim_black_side_borders(raw_bg)
        bg_scale_ratio = self.screen_height / trimmed_bg.get_height()
        self.bg_w = int(trimmed_bg.get_width() * bg_scale_ratio) - 1

        scaled_bg = pygame.transform.smoothscale(trimmed_bg, (self.bg_w, self.screen_height))

        # Make Level 2 longer (e.g., 25 backgrounds)
        self.max_backgrounds = 25
        self.bg_list = [scaled_bg for _ in range(self.max_backgrounds)]

        # Load floor and enemy assets
        floor_img = pygame.image.load("mats/floor2.PNG").convert()
        floor_img.set_colorkey((0, 0, 0))
        self.target_floor_h = 200
        floor_scale_ratio = self.target_floor_h / floor_img.get_height()
        self.floor_w = int(floor_img.get_width() * floor_scale_ratio) - 1
        self.floor_img = pygame.transform.smoothscale(floor_img, (self.floor_w, self.target_floor_h))
        self.floor_flip_img = pygame.transform.flip(self.floor_img, True, False)

        self.platform_image = pygame.image.load("mats/plat31c.png").convert_alpha()
        self.bird_sheet_img = pygame.image.load("spritsheets/enemies/flyer_SS_NB.png").convert_alpha()

        self.demon_walk_r, self.demon_walk_l = load_enemy_frames("spritsheets/enemies/D_WALK_SSNB.png", 7, 0.35)
        self.demon_attack_r, self.demon_attack_l = load_enemy_frames("spritsheets/enemies/D_attack_SSNB.png", 12, 0.35)
        self.skel_walk_r, self.skel_walk_l = load_enemy_frames("spritsheets/enemies/skelly_walk_NB.png", 8, 0.7)
        self.skel_idle_r, self.skel_idle_l = load_enemy_frames("spritsheets/enemies/skelly_idle_NB.png", 10, 0.7)
        self.skel_attack_r, self.skel_attack_l = load_enemy_frames("spritsheets/enemies/skelly_attack_NB.png", 10, 0.7)