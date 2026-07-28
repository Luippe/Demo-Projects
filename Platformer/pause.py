import pygame
import images as im
from os import path
from pygame.locals import *
import display_manager as display

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (169, 169, 169)

#function to draw text onto screen
def draw_text(text, text_col, x, y, surface, size, alpha):
    font = pygame.font.Font(im.FONT_PATH, size)
    img = font.render(text, True, text_col)
    img.set_alpha(alpha)
    surface.blit(img, (x, y))


#class for pausing the game
class Pause():
    def __init__(self, screen, key_list):
        self.run = True
        self.key_list = key_list
        self.rect_list= []
        self.movement_list = ["Up", "Left", "Down", "Right", "Jump", "Interact"]
        self.pause_images = im.images_pause
        for num in range(5):
            key_rect = pygame.Rect((1200, 400 + 100*num), (300, 80))
            self.rect_list.append(key_rect)
        screen_width, screen_height = display.LOGICAL_SIZE
        self.screen = screen
        self.screen_copy = self.screen.copy()
        self.transparent_surface = pygame.Surface((screen_width, screen_height), SRCALPHA)
        self.transparent_surface.fill((0,0,0,200))
        self.screen.blit(self.transparent_surface, (0,0))
        self.choose_allow = False
        self.binding_error = False
        self.choose_key = 0
        self.fade_timer = 80


    #let player customize and bind keys
    def update(self):
        while self.run:
            self.screen.blit(self.screen_copy, (0,0))
            self.screen.blit(self.transparent_surface, (0,0))
            draw_text('KEY BINDING', BLACK, 1100, 180, self.screen, 50, self.fade_timer)
            if self.fade_timer < 255:
                self.fade_timer += 5
            pygame.draw.rect(self.transparent_surface, (100, 100, 100, self.fade_timer), (150, 100, 1620, 880), 0, 20)
            pygame.draw.rect(self.transparent_surface, (169, 169, 169, self.fade_timer), (700, 180, 1020, 720), 0, 20)
            pygame.draw.rect(self.transparent_surface, (169, 169, 169, self.fade_timer), (200, 180, 400, 720), 0, 20)
            pygame.draw.rect(self.transparent_surface, (0, 0, 0, self.fade_timer), (200, 180, 400, 720), 10, 20)
            pygame.draw.rect(self.transparent_surface, (0, 0, 0, self.fade_timer), (700, 180, 1020, 720), 10, 20)
            pygame.draw.rect(self.transparent_surface, (0, 0, 0, self.fade_timer), (150, 100, 1620, 880), 10, 20)
            pygame.draw.rect(self.transparent_surface, (169, 169, 169, self.fade_timer), (1000, 150, 400, 100), 0, 20)
            pygame.draw.rect(self.transparent_surface, (0, 0, 0, self.fade_timer), (1000, 150, 400, 100), 10, 20)
            pos = display.get_mouse_pos()
            mouse_rect = pygame.Rect((pos[0],pos[1]), (5,5))
            for num, tile in enumerate(self.rect_list):
                pygame.draw.rect(self.transparent_surface, (97, 47, 11, self.fade_timer), tile, 0, 20)
                pygame.draw.rect(self.transparent_surface, (145, 82, 33, self.fade_timer), tile, 10, 20)
                draw_text(f'{self.movement_list[num]}', BLACK, 1000, 410 + 100*num, self.screen, 50, self.fade_timer)
                draw_text(f'{pygame.key.name(self.key_list[num])}', BLACK, 1300, 410 + 100*num, self.screen, 50, self.fade_timer)
                if tile.colliderect(mouse_rect) and pygame.mouse.get_pressed()[0] == 1 and self.choose_allow == False:
                    self.choose_key = num
                    self.choose_allow = True
                    self.binding_error = False

            if self.choose_allow == True:
                draw_text('Press a key to bind', BLACK, 1060, 300, self.screen, 50, self.fade_timer)
            if self.binding_error == True:
                draw_text('That key is already in use!', BLACK, 1000, 300, self.screen, 50, 255)

            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                    elif self.choose_allow == True:
                        if event.key in self.key_list:
                            self.binding_error = True
                        else:
                            self.key_list[self.choose_key] = event.key
                        self.choose_allow = False
            display.present(self.screen)
        return self.key_list
