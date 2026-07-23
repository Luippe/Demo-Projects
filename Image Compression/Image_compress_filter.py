'''
Note:
In the simulation, you can drag the moving bar inside the rectangle to change
the compression and circle scale
Changing the compression scale will remove all low pass filters
Press ESC to exit simulation
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft2, ifft2, fftshift, ifftshift
import pygame
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode((800,800))
screen_width, screen_height = pygame.display.get_surface().get_size()
img = plt.imread('pupp_gray.jpg').astype(float)

pixel_size = 2
remove_row_col = 1
x_previous = 640
x_previous2 = 640
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (217, 33, 33)
compress_ratio = 0
fraction = 0
run = True
compressed_img = img
filtered_img = img

#draw original image when starting simulation
for row in range(np.shape(img)[0]):
    for col in range(np.shape(img)[1]):
        pygame.draw.rect(screen, (img[row][col], img[row][col], img[row][col]), (screen_width/2 - 332 + col*pixel_size, 50 + row*pixel_size, pixel_size, pixel_size))

def get_distance(i,j,m,n):
    return ((i-m)**2 + (j-n)**2)**0.5

font = pygame.font.SysFont('Futura', 40)
def draw_text(text, font, text_col, x, y):
    txtbox = font.render(text, True, text_col)
    screen.blit(txtbox, (x, y))

#main loop
while run:
    pos = pygame.mouse.get_pos()
    x_mouse = pos[0]
    y_mouse = pos[1]

    #calculation for when changing the compression scale
    if (150 < x_mouse < 650) and (700 < y_mouse < 730):
        if pygame.mouse.get_pressed()[0] == 1:
            screen.fill(BLACK)
            compress_ratio = (x_mouse - 150)/1500
            if compress_ratio != 0:
                remove_row_col = int(np.sqrt(1/compress_ratio))
                compressed_img = img[::remove_row_col, ::remove_row_col]
                pixel_size = (300/(np.shape(compressed_img)[0]))*2
                img_row, img_col = np.shape(compressed_img)
                for row in range(img_row):
                    for col in range(img_col):
                        pygame.draw.rect(screen, (compressed_img[row][col], compressed_img[row][col], compressed_img[row][col]), (screen_width/2 - 332 + col*pixel_size, 50 + row*pixel_size, pixel_size, pixel_size))
            x_previous = x_mouse

    #calculation for when changing the circle scale
    elif (150 < x_mouse < 650) and (750 < y_mouse < 780):
        if pygame.mouse.get_pressed()[0] == 1:
            screen.fill(BLACK)
            fraction = (x_mouse - 150)/1500
            f_img = fftshift(fft2(compressed_img))
            row, col = f_img.shape
            radius = min(row, col) * fraction
            for i in range(row):
                for j in range(col):
                    if get_distance(i, j, row//2, col//2) > radius:
                        f_img[i][j] = 0
            filtered_img = abs(ifft2(ifftshift(f_img)))
            img_row, img_col = np.shape(compressed_img)
            for row in range(img_row):
                for col in range(img_col):
                    filtered_img[row][col] = sorted((0, filtered_img[row][col], 255))[1]
                    pygame.draw.rect(screen, (filtered_img[row][col], filtered_img[row][col], filtered_img[row][col]), (screen_width/2 - 332 + col*pixel_size, 50 + row*pixel_size, pixel_size, pixel_size))
            x_previous2 = x_mouse

    #draw boxes, lines, and measurements
    pygame.draw.line(screen, RED, (x_previous, 700), (x_previous, 730), 5)
    pygame.draw.line(screen, RED, (x_previous2, 750), (x_previous2, 780), 5)
    pygame.draw.rect(screen, WHITE, (150, 700, 500, 30), 5)
    pygame.draw.rect(screen, WHITE, (150, 750, 500, 30), 5)
    draw_text(f'Compression Scale: {"{:.3f}".format(compress_ratio)}', font, WHITE, 50, 10)
    draw_text(f'Circle Scale: {"{:.3f}".format(fraction)}', font, WHITE, 500, 10)


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        elif event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()