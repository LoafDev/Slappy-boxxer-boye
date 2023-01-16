import pygame, sys, time
from setting import *
from sprite import background, ground, Boxxer_boye, obscle

class game:
    def __init__(self):

        global boxxer_boye, obscle_timer, all_sprite, collision_sprite, scale_factor, active, start_offset

        #True or False thing I will rename it later, ok?
        active = True

        #sprite groups
        all_sprite = pygame.sprite.Group()
        collision_sprite = pygame.sprite.Group()

        #scale factor
        background_height = pygame.image.load('Graphics/back_ground.png').get_height()
        scale_factor = WIN_H / background_height

        #sprite setups
        background(all_sprite, scale_factor)
        ground([all_sprite, collision_sprite], scale_factor)
        boxxer_boye = Boxxer_boye(all_sprite, scale_factor / 1.5)

        #timer
        obscle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obscle_timer, 1400)

        #text
        self.font = pygame.font.Font('Graphics/prstart.ttf', 24)
        self.score = 0
        start_offset = 0

        #menu
        self.menu_surface = pygame.image.load('Graphics/menu (I think).png').convert_alpha()
        self.menu_image = pygame.transform.scale(self.menu_surface, pygame.math.Vector2(self.menu_surface.get_size()) * (scale_factor/1.6))
        self.menu_rect = self.menu_image.get_rect(center = (WIN_W / 2, WIN_H / 2))

        #music
        self.epic_music = pygame.mixer.Sound('Graphics/by_David_Renda.wav')
        self.epic_music.set_volume(0.1)
        self.epic_music.play(loops=-1)

    def collisions(self):
        if pygame.sprite.spritecollide(boxxer_boye, collision_sprite, False, pygame.sprite.collide_mask) or boxxer_boye.rect.top <= 0:
            global active
            
            active = False
            boxxer_boye.kill()

            for sprite in collision_sprite.sprites():
                if sprite.sprite_type == 'obscle':
                    sprite.kill()

    def display_text(self):
        if active:
            self.score = (pygame.time.get_ticks() - start_offset) // 1000
            y = WIN_H / 10
        else:
            y = WIN_H / 2 + (self.menu_rect.height / 1.4)

        score_surface = self.font.render(str(self.score), True, 'white')
        score_rect = score_surface.get_rect(midtop = (WIN_W / 2, y))
        screen.blit(score_surface, score_rect)

    def update(self, delta_time):
        all_sprite.update(delta_time)
        all_sprite.draw(screen)
        self.display_text()

        if active:
            self.collisions()
        else:
            screen.blit(self.menu_image, self.menu_rect)

if __name__ == '__main__':
    pygame.init()
    last_time = time.time()

    screen = pygame.display.set_mode((WIN_W,WIN_H))
    caption = pygame.display.set_caption('Slapping da bird')
    clock = pygame.time.Clock()
    game = game()

    while True:
            delta_time = time.time() - last_time
            last_time = time.time()
            game.update(delta_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if active:
                        boxxer_boye.jump()
                    else:
                        boxxer_boye = Boxxer_boye(all_sprite, scale_factor / 1.5)
                        active = True
                        start_offset = pygame.time.get_ticks()
                
                if event.type == obscle_timer and active:
                    obscle([all_sprite, collision_sprite], scale_factor * 1.7)

            pygame.display.update()
            clock.tick(FRAMERATE)