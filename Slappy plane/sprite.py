import pygame
from setting import *
from random import choice, randint

class background(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        background_image = pygame.image.load('Graphics/back_ground.png').convert()

        full_h = background_image.get_height() * scale_factor
        full_w = background_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(background_image, (full_w, full_h))

        self.image = pygame.Surface((full_w * 2,full_h))
        self.image.blit(full_sized_image,(0,0))
        self.image.blit(full_sized_image,(full_w,0))

        #animation I think
        self.rect = self.image.get_rect(topleft=(0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 300 * dt

        if self.rect.centerx <= 0:
            self.pos.x = 0
        
        self.rect.x = round(self.pos.x)

class ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'

        #image
        ground_graphic = pygame.image.load('Graphics/ground_pixel_perfect.png').convert_alpha()
        self.image = pygame.transform.scale(ground_graphic, pygame.math.Vector2(ground_graphic.get_size()) * scale_factor)

        #position
        self.rect = self.image.get_rect(bottomleft = (0, WIN_H))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #mask I guess
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        self.pos.x -= 300 * delta_time

        if self.rect.centerx <= 0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)

class Boxxer_boye(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        #image stuff I think
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frame[self.frame_index]

        #rect
        self.rect = self.image.get_rect(midleft = (WIN_W / 20,WIN_H / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #movement
        self.gravity = 600
        self.direction = 0

        #mask I guess
        self.mask = pygame.mask.from_surface(self.image)

        #sound
        self.jump_sound_super_effect = pygame.mixer.Sound('Graphics/JUMP_UP_RIGHT_NOW_PLEASE_HELP_ITS_22;14!!!!!!!!!!!!!!!!!!!!!!!!!!!!_AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH.wav')
        self.jump_sound_super_effect.set_volume(0.2)

    def import_frames(self,scale_factor):
        self.frame = []

        for animate in range(1,4):
            surface = pygame.image.load(f'Graphics/Boxxer_Boye_{animate}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surface, pygame.math.Vector2(surface.get_size()) * scale_factor)
            self.frame.append(scaled_surface)

    def unreal_physical_gravity(self, delta_time):
        self.direction += self.gravity * delta_time
        self.pos.y += self.direction * delta_time
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.direction = - 400
        self.jump_sound_super_effect.play()

    def animation(self, delta_time):
        self.frame_index += 6 * delta_time
        if self.frame_index >= len(self.frame):
            self.frame_index = 0

        self.image = self.frame[int(self.frame_index)]

    def rotation(self):
        rotating_boxxer_boye = pygame.transform.rotozoom(self.image, -self.direction * 0.34 , 1)
        self.image = rotating_boxxer_boye
        
        #mask again I guess
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        self.unreal_physical_gravity(delta_time)
        self.animation(delta_time)
        self.rotation()

class obscle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'obscle'

        orientation = choice(('up', 'down'))
        surface = pygame.image.load(f'Graphics/obscle_{choice((1,2))}.png').convert_alpha()
        
        
        self.image = pygame.transform.scale(surface, pygame.math.Vector2(surface.get_size()) * scale_factor)
        
        x = WIN_W + randint(40,100)

        if orientation == 'up':
            y = WIN_H + randint(10,50)
            self.rect = self.image.get_rect(midbottom = (x,y))
        
        else:
            y = randint(-50, -10)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop = (x,y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        #mask I guess
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        self.pos.x -= 400 * delta_time
        self.rect.x = round(self.pos.x)

        if self.rect.right <= -100:
            self.kill()
            
