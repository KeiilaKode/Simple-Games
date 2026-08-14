import pygame
import random
import sys


class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        image.set_colorkey(colour)
        return image


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_pos, y, bird_sheet_img, scale, forced_direction=None):
        super().__init__()
        self.rem_value = 3  # REM value for Flyer
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.direction = forced_direction if forced_direction is not None else random.choice([-1, 1])

        sprite_sheet = SpriteSheet(bird_sheet_img)
        fw = bird_sheet_img.get_width() // 8
        fh = bird_sheet_img.get_height()

        for i in range(8):
            img = sprite_sheet.get_image(i, fw, fh, scale, (0, 0, 0))
            img = pygame.transform.flip(img, self.direction == 1, False)
            img.set_colorkey((0, 0, 0))
            self.animation_list.append(img)

        self.image = self.animation_list[self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x_pos, y))

    def update(self, camera_x, screen_width):
        if pygame.time.get_ticks() - self.update_time > 125:
            self.update_time = pygame.time.get_ticks()
            self.frame_index = (self.frame_index + 1) % len(self.animation_list)
        self.image = self.animation_list[self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x += self.direction * 4
        if self.rect.right < camera_x - 400 or self.rect.left > camera_x + screen_width + 400:
            self.kill()


class Demon(pygame.sprite.Sprite):
    def __init__(self, spawn_x, y_pos, patrol_start_x, patrol_end_x, walk_r, walk_l, attack_r, attack_l):
        super().__init__()
        self.rem_value = 5  # REM value for Demon
        self.walk_frames_right, self.walk_frames_left = walk_r, walk_l
        self.attack_frames_right, self.attack_frames_left = attack_r, attack_l
        self.frame_index, self.update_time, self.anim_speed = 0, pygame.time.get_ticks(), 100
        self.patrol_start_x, self.patrol_end_x, self.speed, self.direction, self.state = patrol_start_x, patrol_end_x, 2.0, 1, "walk"
        self.image = self.walk_frames_right[0]
        self.rect = self.image.get_rect(x=spawn_x)
        self.rect.bottom = y_pos + 85
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, camera_x, player_x=None, player_y=None):
        if player_x and player_y and abs(player_y - self.rect.centery) < 150:
            if abs(player_x - self.rect.centerx) < 180 and self.state != "attack":
                self.state, self.frame_index, self.update_time = "attack", 0, pygame.time.get_ticks()
                self.direction = 1 if player_x > self.rect.centerx else -1

        if self.state == "walk":
            self.rect.x += self.direction * self.speed
            if self.rect.x >= self.patrol_end_x:
                self.rect.x, self.direction = self.patrol_end_x, -1
            elif self.rect.x <= self.patrol_start_x:
                self.rect.x, self.direction = self.patrol_start_x, 1
            if pygame.time.get_ticks() - self.update_time > self.anim_speed:
                self.update_time = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames_right)
            self.image = self.walk_frames_right[self.frame_index] if self.direction == 1 else self.walk_frames_left[
                self.frame_index]

        elif self.state == "attack":
            if pygame.time.get_ticks() - self.update_time > 70:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                if self.frame_index >= len(self.attack_frames_right): self.state, self.frame_index = "walk", 0
            if self.state == "attack":
                self.image = self.attack_frames_right[self.frame_index] if self.direction == 1 else \
                    self.attack_frames_left[self.frame_index]

        old_bottom = self.rect.bottom
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.bottom = old_bottom
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.right < camera_x - 1000: self.kill()


class Skeleton(pygame.sprite.Sprite):
    def __init__(self, spawn_x, y_pos, patrol_start_x, patrol_end_x, walk_r, walk_l, idle_r, idle_l, attack_r,
                 attack_l):
        super().__init__()
        self.rem_value = 5  # REM value for Skeleton
        self.walk_frames_right, self.walk_frames_left = walk_r, walk_l
        self.idle_frames_right, self.idle_frames_left = idle_r, idle_l
        self.attack_frames_right, self.attack_frames_left = attack_r, attack_l
        self.frame_index, self.update_time, self.anim_speed = 0, pygame.time.get_ticks(), 100
        self.patrol_start_x, self.patrol_end_x, self.speed, self.direction, self.state = patrol_start_x, patrol_end_x, 1.8, 1, "walk"
        self.image = self.walk_frames_right[0]
        self.rect = self.image.get_rect(x=spawn_x)
        self.rect.bottom = y_pos + 240
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, camera_x, player_x=None, player_y=None):
        if player_x and player_y and abs(player_y - self.rect.centery) < 250:
            if abs(player_x - self.rect.centerx) < 180 and self.state != "attack":
                self.state, self.frame_index, self.update_time = "attack", 0, pygame.time.get_ticks()
                self.direction = 1 if player_x > self.rect.centerx else -1

        if self.state == "walk":
            self.rect.x += self.direction * self.speed
            if self.rect.x >= self.patrol_end_x or self.rect.x <= self.patrol_start_x:
                self.rect.x = self.patrol_end_x if self.direction == 1 else self.patrol_start_x
                self.direction *= -1
                self.state, self.frame_index = "idle", 0
            if self.state == "walk":
                if pygame.time.get_ticks() - self.update_time > self.anim_speed:
                    self.update_time, self.frame_index = pygame.time.get_ticks(), (self.frame_index + 1) % len(
                        self.walk_frames_right)
                self.image = self.walk_frames_right[self.frame_index] if self.direction == 1 else self.walk_frames_left[
                    self.frame_index]

        if self.state == "idle":
            if pygame.time.get_ticks() - self.update_time > 120:
                self.update_time, self.frame_index = pygame.time.get_ticks(), self.frame_index + 1
                if self.frame_index >= len(self.idle_frames_right): self.state, self.frame_index = "walk", 0
            if self.state == "idle": self.image = self.idle_frames_right[self.frame_index] if self.direction == 1 else \
                self.idle_frames_left[self.frame_index]

        if self.state == "attack":
            if pygame.time.get_ticks() - self.update_time > 80:
                self.update_time, self.frame_index = pygame.time.get_ticks(), self.frame_index + 1
                if self.frame_index >= len(self.attack_frames_right): self.state, self.frame_index = "walk", 0
            if self.state == "attack": self.image = self.attack_frames_right[
                self.frame_index] if self.direction == 1 else self.attack_frames_left[self.frame_index]

        old_bottom = self.rect.bottom
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.bottom = old_bottom
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.right < camera_x - 1000: self.kill()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, fireball_img, explode_img, scale=0.45):
        super().__init__()
        self.direction, self.speed, self.state = direction, 800.0, "fly"
        self.frame_index, self.update_time = 0, pygame.time.get_ticks()

        fw, fh = fireball_img.get_width() // 6, fireball_img.get_height()
        self.fly_frames = [pygame.transform.flip(
            pygame.transform.smoothscale(fireball_img.subsurface((i * fw, 0, fw, fh)),
                                         (int(fw * scale), int(fh * scale))), direction == -1, False) for i in range(6)]
        ew, eh = explode_img.get_width() // 8, explode_img.get_height()
        self.exp_frames = [pygame.transform.flip(
            pygame.transform.smoothscale(explode_img.subsurface((i * ew, 0, ew, eh)),
                                         (int(ew * scale), int(fh * scale) if False else int(eh * scale))),
            direction == -1, False) for i in range(8)]

        self.image = self.fly_frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt, camera_x, screen_width):
        if pygame.time.get_ticks() - self.update_time > (50 if self.state == "fly" else 40):
            self.update_time, self.frame_index = pygame.time.get_ticks(), self.frame_index + 1
            if self.state == "fly":
                self.frame_index %= len(self.fly_frames)
                self.image = self.fly_frames[self.frame_index]
            else:
                if self.frame_index >= len(self.exp_frames): self.kill(); return
                self.image = self.exp_frames[self.frame_index]

        if self.state == "fly":
            self.rect.x += self.direction * self.speed * dt
            self.mask = pygame.mask.from_surface(self.image)
            if self.rect.right < camera_x - 500 or self.rect.left > camera_x + screen_width + 500:
                self.kill()

    def explode(self):
        if self.state != "explode":
            self.state, self.frame_index, self.update_time = "explode", 0, pygame.time.get_ticks()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, platform_image, offset_ratio=0.0):
        super().__init__()
        orig_w, orig_h = platform_image.get_size()

        # Scale proportionally to preserve the chunky 3D floating island look
        scale = width / orig_w
        height = int(orig_h * scale)

        self.image = pygame.transform.smoothscale(platform_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        # Only apply a vertical offset if specified (e.g. for Level 2 3D islands)
        top_offset = int(height * offset_ratio)
        self.collision_rect = pygame.Rect(self.rect.x, self.rect.y + top_offset, self.rect.width, 10)


class Merchant(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, sheet_filename, columns=7, rows=4):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        try:
            sheet = pygame.image.load(sheet_filename).convert()
        except pygame.error as e:
            print(f"Unable to load merchant sprite sheet: {e}")
            sys.exit()

        sw, sh = sheet.get_size()
        fw = sw // columns
        fh = sh // rows

        self.intro_frames = []
        scale_factor = screen_width / fw
        new_h = int(fh * scale_factor)

        for row in range(rows):
            for col in range(columns):
                frame = pygame.Surface((fw, fh)).convert()
                frame.blit(sheet, (0, 0), (col * fw, row * fh, fw, fh))
                scaled_frame = pygame.transform.smoothscale(frame, (screen_width, new_h))
                self.intro_frames.append(scaled_frame)

        self.frame_index = 0
        self.animation_timer = 0
        self.anim_speed = 357
        self.state = "intro"

        self.image = self.intro_frames[0]
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))
        self.audio_played = False

    def update(self, dt_ms, voice_fx):
        if self.state == "intro":
            if not self.audio_played:
                voice_fx.play()
                self.audio_played = True

            self.animation_timer += dt_ms
            if self.animation_timer >= self.anim_speed:
                self.animation_timer = 0
                self.frame_index += 1

                if self.frame_index >= len(self.intro_frames):
                    self.frame_index = len(self.intro_frames) - 1
                    self.state = "idle"

            self.image = self.intro_frames[self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Merchant_UI:
    def __init__(self, screen_width, screen_height):
        try:
            raw_bg = pygame.image.load("backgrounds/M_inventory_empty.png").convert()
            self.bg = pygame.transform.smoothscale(raw_bg, (screen_width, screen_height))

            self.health_p = pygame.transform.smoothscale(pygame.image.load("mats/health_p.png").convert_alpha(),
                                                         (110, 150))
            self.mana_p = pygame.transform.smoothscale(pygame.image.load("mats/mana_p.png").convert_alpha(), (110, 150))
            self.purple_p = pygame.transform.smoothscale(pygame.image.load("mats/purple_p.png").convert_alpha(),
                                                         (110, 150))

            wings_raw = pygame.image.load("mats/wings_p_ss.png").convert_alpha()
            ww, wh = wings_raw.get_size()
            crop_h = int(wh * 0.70)
            y_offset = int(wh * 0.15)
            wings_cropped = wings_raw.subsurface((0, y_offset, ww, crop_h))
            self.wings_p = pygame.transform.smoothscale(wings_cropped, (110, 150))

        except pygame.error as e:
            print(f"Error loading UI: {e}")
            sys.exit()

        self.sold_out = {
            "Health Potion": False,
            "Mana Potion": False,
            "Wings Potion": False,
            "Purple Potion": False
        }

        self.slot_1_rect = pygame.Rect(680, 165, 130, 130)
        self.slot_2_rect = pygame.Rect(890, 165, 130, 130)
        self.slot_3_rect = pygame.Rect(1100, 165, 130, 130)
        self.slot_4_rect = pygame.Rect(680, 360, 130, 130)

        self.buy_rect = pygame.Rect(250, 650, 240, 65)

        self.selected_item = None
        self.font_title = pygame.font.SysFont("Lucida Sans", 36)
        self.font_desc = pygame.font.SysFont("Lucida Sans", 24)
        self.font_rem = pygame.font.SysFont("Lucida Sans", 30)

    def update(self, mouse_pos, mouse_click, rem):
        bought_item = None

        if self.slot_1_rect.collidepoint(mouse_pos) and not self.sold_out["Health Potion"]:
            if mouse_click: self.selected_item = "Health Potion"
        elif self.slot_2_rect.collidepoint(mouse_pos) and not self.sold_out["Mana Potion"]:
            if mouse_click: self.selected_item = "Mana Potion"
        elif self.slot_3_rect.collidepoint(mouse_pos) and not self.sold_out["Wings Potion"]:
            if mouse_click: self.selected_item = "Wings Potion"
        elif self.slot_4_rect.collidepoint(mouse_pos) and not self.sold_out["Purple Potion"]:
            if mouse_click: self.selected_item = "Purple Potion"

        if mouse_click and not (self.slot_1_rect.collidepoint(mouse_pos) or self.slot_2_rect.collidepoint(
                mouse_pos) or self.slot_3_rect.collidepoint(mouse_pos) or self.slot_4_rect.collidepoint(
                mouse_pos) or self.buy_rect.collidepoint(mouse_pos)):
            self.selected_item = None

        if mouse_click and self.buy_rect.collidepoint(mouse_pos):
            if self.selected_item == "Health Potion" and rem >= 50 and not self.sold_out["Health Potion"]:
                bought_item = "Health Potion"

        return bought_item

    def draw(self, screen, mouse_pos, rem):
        screen.blit(self.bg, (0, 0))

        if not self.sold_out["Health Potion"]:
            screen.blit(self.health_p, (self.slot_1_rect.x + 10, self.slot_1_rect.y - 10))
            if self.slot_1_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 255, 255), self.slot_1_rect, 3)

        if not self.sold_out["Mana Potion"]:
            screen.blit(self.mana_p, (self.slot_2_rect.x + 10, self.slot_2_rect.y - 10))
            if self.slot_2_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 255, 255), self.slot_2_rect, 3)

        if not self.sold_out["Wings Potion"]:
            screen.blit(self.wings_p, (self.slot_3_rect.x + 10, self.slot_3_rect.y - 10))
            if self.slot_3_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 255, 255), self.slot_3_rect, 3)

        if not self.sold_out["Purple Potion"]:
            screen.blit(self.purple_p, (self.slot_4_rect.x + 10, self.slot_4_rect.y - 10))
            if self.slot_4_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 255, 255), self.slot_4_rect, 3)

        if self.buy_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 50, 50), self.buy_rect, 3, border_radius=8)

        screen.blit(self.font_rem.render(str(rem), True, (253, 117, 234)), (280, 570))

        text_x = 270

        if self.selected_item == "Health Potion" and not self.sold_out["Health Potion"]:
            screen.blit(self.font_title.render("Health Potion", True, (50, 255, 50)), (text_x, 155))
            screen.blit(self.font_desc.render("Grants 3 Hits of Health.", True, (190, 200, 200)), (text_x, 205))
            screen.blit(self.font_title.render("COST: 50 REM", True, (253, 117, 234)), (text_x, 240))
        elif self.selected_item == "Mana Potion" and not self.sold_out["Mana Potion"]:
            screen.blit(self.font_title.render("Mana Potion", True, (50, 50, 255)), (text_x, 155))
            screen.blit(self.font_desc.render("Coming Soon...", True, (200, 200, 200)), (text_x, 205))
        elif self.selected_item == "Wings Potion" and not self.sold_out["Wings Potion"]:
            screen.blit(self.font_title.render("Wings Potion", True, (255, 200, 50)), (text_x, 155))
            screen.blit(self.font_desc.render("Coming Soon...", True, (200, 200, 200)), (text_x, 205))
        elif self.selected_item == "Purple Potion" and not self.sold_out["Purple Potion"]:
            screen.blit(self.font_title.render("Purple Potion", True, (180, 50, 255)), (text_x, 155))
            screen.blit(self.font_desc.render("Coming Soon...", True, (200, 200, 200)), (text_x, 205))


class Helldog(pygame.sprite.Sprite):
    def __init__(self, spawn_x, y_pos, patrol_start_x, patrol_end_x, walk_r, walk_l, attack_r, attack_l):
        super().__init__()
        self.health = 2
        self.rem_value = 10
        self.walk_frames_right, self.walk_frames_left = walk_r, walk_l
        self.attack_frames_right, self.attack_frames_left = attack_r, attack_l
        self.frame_index, self.update_time, self.anim_speed = 0, pygame.time.get_ticks(), 80
        self.patrol_start_x, self.patrol_end_x, self.speed, self.direction, self.state = patrol_start_x, patrol_end_x, 3.5, 1, "walk"
        self.image = self.walk_frames_right[0]

        self.rect = self.image.get_rect(x=spawn_x)
        # ADJUST THIS NUMBER to sink the feet through the transparent padding to touch the floor
        self.y_offset = 160
        self.rect.bottom = y_pos + self.y_offset
        self.mask = pygame.mask.from_surface(self.image)

    def take_damage(self):
        """Reduces health and returns True if the enemy dies."""
        self.health -= 1
        return self.health <= 0

    def update(self, camera_x, player_x=None, player_y=None):
        if player_x and player_y and abs(player_y - self.rect.centery) < 150:
            if abs(player_x - self.rect.centerx) < 220 and self.state != "attack":
                self.state, self.frame_index, self.update_time = "attack", 0, pygame.time.get_ticks()
                self.direction = 1 if player_x > self.rect.centerx else -1

        if self.state == "walk":
            self.rect.x += self.direction * self.speed
            if self.rect.x >= self.patrol_end_x:
                self.rect.x, self.direction = self.patrol_end_x, -1
            elif self.rect.x <= self.patrol_start_x:
                self.rect.x, self.direction = self.patrol_start_x, 1
            if pygame.time.get_ticks() - self.update_time > self.anim_speed:
                self.update_time = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames_right)
            self.image = self.walk_frames_right[self.frame_index] if self.direction == 1 else self.walk_frames_left[
                self.frame_index]

        elif self.state == "attack":
            if pygame.time.get_ticks() - self.update_time > 60:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                if self.frame_index >= len(self.attack_frames_right): self.state, self.frame_index = "walk", 0
            if self.state == "attack":
                self.image = self.attack_frames_right[self.frame_index] if self.direction == 1 else \
                self.attack_frames_left[self.frame_index]

        old_bottom = self.rect.bottom
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.bottom = old_bottom
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.right < camera_x - 1000: self.kill()


class Mau(pygame.sprite.Sprite):
    def __init__(self, spawn_x, y_pos, patrol_start_x, patrol_end_x, walk_r, walk_l, attack_r, attack_l):
        super().__init__()
        self.health = 2
        self.rem_value = 15
        self.walk_frames_right, self.walk_frames_left = walk_r, walk_l
        self.attack_frames_right, self.attack_frames_left = attack_r, attack_l
        self.frame_index, self.update_time, self.anim_speed = 0, pygame.time.get_ticks(), 100
        self.patrol_start_x, self.patrol_end_x, self.speed, self.direction, self.state = patrol_start_x, patrol_end_x, 2.0, 1, "walk"
        self.image = self.walk_frames_right[0]

        self.rect = self.image.get_rect(x=spawn_x)
        # ADJUST THIS NUMBER to sink the feet through the transparent padding to touch the floor
        self.y_offset = 160
        self.rect.bottom = y_pos + self.y_offset
        self.mask = pygame.mask.from_surface(self.image)

    def take_damage(self):
        self.health -= 1
        return self.health <= 0

    def update(self, camera_x, player_x=None, player_y=None):
        if player_x and player_y and abs(player_y - self.rect.centery) < 150:
            if abs(player_x - self.rect.centerx) < 160 and self.state != "attack":
                self.state, self.frame_index, self.update_time = "attack", 0, pygame.time.get_ticks()
                self.direction = 1 if player_x > self.rect.centerx else -1

        if self.state == "walk":
            self.rect.x += self.direction * self.speed
            if self.rect.x >= self.patrol_end_x:
                self.rect.x, self.direction = self.patrol_end_x, -1
            elif self.rect.x <= self.patrol_start_x:
                self.rect.x, self.direction = self.patrol_start_x, 1
            if pygame.time.get_ticks() - self.update_time > self.anim_speed:
                self.update_time = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames_right)
            self.image = self.walk_frames_right[self.frame_index] if self.direction == 1 else self.walk_frames_left[
                self.frame_index]

        elif self.state == "attack":
            if pygame.time.get_ticks() - self.update_time > 80:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                if self.frame_index >= len(self.attack_frames_right): self.state, self.frame_index = "walk", 0
            if self.state == "attack":
                self.image = self.attack_frames_right[self.frame_index] if self.direction == 1 else \
                self.attack_frames_left[self.frame_index]

        old_bottom = self.rect.bottom
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.bottom = old_bottom
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.right < camera_x - 1000: self.kill()


class Pkgrim(pygame.sprite.Sprite):
    def __init__(self, spawn_x, y_pos, patrol_start_x, patrol_end_x, walk_r, walk_l, attack_r, attack_l):
        super().__init__()
        self.health = 2
        self.rem_value = 8
        self.walk_frames_right, self.walk_frames_left = walk_r, walk_l
        self.attack_frames_right, self.attack_frames_left = attack_r, attack_l
        self.frame_index, self.update_time, self.anim_speed = 0, pygame.time.get_ticks(), 90
        self.patrol_start_x, self.patrol_end_x, self.speed, self.direction, self.state = patrol_start_x, patrol_end_x, 2.5, 1, "walk"
        self.image = self.walk_frames_right[0]

        self.rect = self.image.get_rect(x=spawn_x)
        # ADJUST THIS NUMBER to sink the feet through the transparent padding to touch the floor
        self.y_offset = 160
        self.rect.bottom = y_pos + self.y_offset
        self.mask = pygame.mask.from_surface(self.image)

    def take_damage(self):
        self.health -= 1
        return self.health <= 0

    def update(self, camera_x, player_x=None, player_y=None):
        if player_x and player_y and abs(player_y - self.rect.centery) < 150:
            if abs(player_x - self.rect.centerx) < 180 and self.state != "attack":
                self.state, self.frame_index, self.update_time = "attack", 0, pygame.time.get_ticks()
                self.direction = 1 if player_x > self.rect.centerx else -1

        if self.state == "walk":
            self.rect.x += self.direction * self.speed
            if self.rect.x >= self.patrol_end_x:
                self.rect.x, self.direction = self.patrol_end_x, -1
            elif self.rect.x <= self.patrol_start_x:
                self.rect.x, self.direction = self.patrol_start_x, 1
            if pygame.time.get_ticks() - self.update_time > self.anim_speed:
                self.update_time = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames_right)
            self.image = self.walk_frames_right[self.frame_index] if self.direction == 1 else self.walk_frames_left[
                self.frame_index]

        elif self.state == "attack":
            if pygame.time.get_ticks() - self.update_time > 70:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                if self.frame_index >= len(self.attack_frames_right): self.state, self.frame_index = "walk", 0
            if self.state == "attack":
                self.image = self.attack_frames_right[self.frame_index] if self.direction == 1 else \
                self.attack_frames_left[self.frame_index]

        old_bottom = self.rect.bottom
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.bottom = old_bottom
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.right < camera_x - 1000: self.kill()