import pygame
from os import path
from pygame.locals import *
import images as im
import random
import display_manager as display

run = True
BLACK = (0,0,0)
WHITE = (255, 255, 255)


def draw_text(text, font, text_col, x, y, surface, alpha_val):
    img = font.render(text, True, text_col)
    img.set_alpha(alpha_val)
    surface.blit(img, (x, y))


class Game_Over():
    def __init__(self, screen_width, screen_height, x, y, direction):
        self.right_hurt = im.right_hurt
        self.left_hurt = im.left_hurt
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_x = x
        self.player_y = y
        self.direction = direction
        self.font = pygame.font.SysFont('Futura', 50)
        self.disappear = 0
        self.fading_particle_list = []
        self.delay = 0
        self.timer = 0

    def update(self, primary_surface, surface):
        while run:
            self.delay += 1
            primary_surface.fill((150,150,150))
            if self.direction == -1:
                primary_surface.blit(self.right_hurt[0], (self.player_x, self.player_y))
            elif self.direction == 1:
                primary_surface.blit(self.left_hurt[0], (self.player_x, self.player_y))
            if self.delay > 400 and self.disappear < 100:
                self.fading_particle_list.append([[self.player_x + 25 + random.randint(-15,15), self.player_y + self.disappear], self.direction * random.randint(2, 4),random.randint(2, 4), random.randint(5,20)])
                self.disappear += 0.05

            pygame.draw.rect(primary_surface, (150, 150, 150), (self.player_x, self.player_y, 60, self.disappear))
            for particle in self.fading_particle_list:
                particle[0][0] += 0.05 * particle[1]
                particle[0][1] -= 0.05 * particle[2]
                particle[3] -= 0.03
                pygame.draw.rect(primary_surface, BLACK, [int(particle[0][0]), int(particle[0][1]), 4, 4])
                if particle[3] <= 1:
                    self.fading_particle_list.remove(particle)
            if self.disappear > 100:
                self.timer += 0.1
                draw_text('GAME OVER', self.font, BLACK, self.screen_width / 2 - 100, self.screen_height / 2, primary_surface, self.timer)
                if self.timer > 255:
                    self.timer = 255
            for event in pygame.event.get():
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    pygame.quit()
            display.present(primary_surface)
