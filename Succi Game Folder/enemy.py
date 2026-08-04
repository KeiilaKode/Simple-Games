import pygame
import random
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, y, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self)
        # Define Variables
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False



        # Load images from sprite sheet
        animation_steps = 2
        for animation in range (animation_steps):
            image = sprite_sheet.get_image(animation, 54.2, 62, scale,(0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False)
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)


        # Select starting image and create rectangle from it
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()

        if self.direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = screen_width
        self.rect.y = y

    def update(self, scroll, screen_width):
        # Update animation
        animation_cooldown = 175
        # Update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # If the animation has run out, reset back to the start
        if self.frame_index >=  len(self.animation_list):
            self.frame_index = 0



        # Move Enemy
        self.rect.x += self.direction * 2
        self.rect.y += scroll

        # Check if gone off screen
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()






