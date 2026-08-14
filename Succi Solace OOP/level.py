# --- level.py ---#
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


def trim_transparent_borders(surface):
    w, h = surface.get_size()
    left, right, top, bottom = w, 0, h, 0

    for y in range(h):
        for x in range(w):
            if surface.get_at((x, y)).a > 0:
                if x < left: left = x
                if x > right: right = x
                if y < top: top = y
                if y > bottom: bottom = y

    if right >= left and bottom >= top:
        return surface.subsurface((left, top, (right - left) + 1, (bottom - top) + 1)).copy()
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

        self.max_backgrounds = 17

        # Only default to 0.0 if a subclass (like Level 2) hasn't already set it
        if not hasattr(self, 'platform_offset_ratio'):
            self.platform_offset_ratio = 0.0

        self.platform_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.demon_group = pygame.sprite.Group()
        self.skeleton_group = pygame.sprite.Group()

        self.last_spawned_bg_index = -1
        self.load_assets()

        self.level_end_x = self.max_backgrounds * self.bg_w
        self.door_world_x = ((self.max_backgrounds - 1) * self.bg_w) + 900

        if not hasattr(self, 'platform_images') or not self.platform_images:
            self.platform_images = [self.platform_image]

        self.platform_group.add(
            Platform(200, 580, 180, random.choice(self.platform_images), self.platform_offset_ratio))
        self.platform_group.add(
            Platform(450, 380, 200, random.choice(self.platform_images), self.platform_offset_ratio))
        self.platform_group.add(
            Platform(800, 480, 160, random.choice(self.platform_images), self.platform_offset_ratio))

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
        self.platform_group.empty()
        self.enemy_group.empty()
        self.demon_group.empty()
        self.skeleton_group.empty()
        self.last_spawned_bg_index = -1

        self.platform_group.add(
            Platform(200, 580, 180, random.choice(self.platform_images), self.platform_offset_ratio))
        self.platform_group.add(
            Platform(450, 380, 200, random.choice(self.platform_images), self.platform_offset_ratio))
        self.platform_group.add(
            Platform(800, 480, 160, random.choice(self.platform_images), self.platform_offset_ratio))

    def update(self, dt, camera_x, player_x, player_y):
        for platform in list(self.platform_group):
            if platform.rect.right < camera_x - 4000: platform.kill()

        if camera_x + self.screen_width < self.level_end_x - 500:
            if len(self.platform_group) < 40:
                last_p = max(self.platform_group, key=lambda p: p.rect.x, default=None)
                p_x = (last_p.rect.right + random.randint(120, 290)) if last_p else (camera_x + self.screen_width + 100)

                chosen_plat_img = random.choice(self.platform_images)
                self.platform_group.add(
                    Platform(p_x, random.randint(320, 625), random.randint(90, 200), chosen_plat_img,
                             self.platform_offset_ratio))

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
        self.platform_offset_ratio = 0.22  # Adjust this if needed based on our last step!
        super().__init__(screen_width, screen_height)

    def load_assets(self):
        # Create the base sequence for Level 2
        base_bg_filenames = [
            "backgrounds/lvl_2_bgs/bg1.png",
            "backgrounds/lvl_2_bgs/bg2.png",
            "backgrounds/lvl_2_bgs/bg3.png",
            "backgrounds/lvl_2_bgs/bg4.png",
            "backgrounds/lvl_2_bgs/bg5.png",
            "backgrounds/lvl_2_bgs/bg6.png",
            "backgrounds/lvl_2_bgs/bg7.png",
            "backgrounds/lvl_2_bgs/bg8.png"
        ]

        # Loop it twice (16 backgrounds) and append the final one
        full_bg_filenames = base_bg_filenames * 2
        full_bg_filenames.append("backgrounds/lvl_2_bgs/bg9.png")

        # Load and scale them seamlessly
        first_raw = pygame.image.load(full_bg_filenames[0]).convert()
        first_trimmed = trim_black_side_borders(first_raw)
        bg_scale_ratio = self.screen_height / first_trimmed.get_height()
        self.bg_w = int(first_trimmed.get_width() * bg_scale_ratio) - 1

        self.bg_list = [pygame.transform.smoothscale(trim_black_side_borders(pygame.image.load(f).convert()),
                                                     (self.bg_w, self.screen_height)) for f in full_bg_filenames]

        # Ensure max backgrounds syncs up with our list length (17)
        self.max_backgrounds = len(full_bg_filenames)

        # Floor Setup
        floor_img = pygame.image.load("mats/floor2.PNG").convert()
        floor_img.set_colorkey((0, 0, 0))
        self.target_floor_h = 200
        floor_scale_ratio = self.target_floor_h / floor_img.get_height()
        self.floor_w = int(floor_img.get_width() * floor_scale_ratio) - 1
        self.floor_img = pygame.transform.smoothscale(floor_img, (self.floor_w, self.target_floor_h))
        self.floor_flip_img = pygame.transform.flip(self.floor_img, True, False)

        self.platform_image = pygame.image.load("mats/plat31c.png").convert_alpha()

        # Load Level 2 platforms
        try:
            plat2_raw = pygame.image.load("mats/platforms/lvl2_p2.png").convert_alpha()
            plat3_raw = pygame.image.load("mats/platforms/lvl2_p3.PNG").convert_alpha()

            self.platform_images = [
                trim_transparent_borders(plat2_raw),
                trim_transparent_borders(plat3_raw)
            ]
        except pygame.error as e:
            print(f"Error loading Level 2 platforms: {e}")
            self.platform_images = [self.platform_image]

        # Enemies Setup
        self.bird_sheet_img = pygame.image.load("spritsheets/enemies/flyer_SS_NB.png").convert_alpha()
        self.demon_walk_r, self.demon_walk_l = load_enemy_frames("spritsheets/enemies/D_WALK_SSNB.png", 7, 0.35)
        self.demon_attack_r, self.demon_attack_l = load_enemy_frames("spritsheets/enemies/D_attack_SSNB.png", 12, 0.35)
        self.skel_walk_r, self.skel_walk_l = load_enemy_frames("spritsheets/enemies/skelly_walk_NB.png", 8, 0.7)
        self.skel_idle_r, self.skel_idle_l = load_enemy_frames("spritsheets/enemies/skelly_idle_NB.png", 10, 0.7)
        self.skel_attack_r, self.skel_attack_l = load_enemy_frames("spritsheets/enemies/skelly_attack_NB.png", 10, 0.7)