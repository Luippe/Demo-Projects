import pyaudio
import pygame
import struct
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import ListedColormap
from os import path
from pygame.locals import *
from scipy.fftpack import fft, ifft, fft2, fftshift
from scipy import signal
import wave
import scipy.io.wavfile as wv
from scipy.spatial.transform import Rotation as R
from pprint import pprint
import time
import cv2

# When bundled by PyInstaller (--onefile), data files (fonts, PNGs, WAVs) are
# unpacked to a temp dir exposed as sys._MEIPASS, but the process working
# directory is NOT that dir. Switch to it when frozen so the bare-relative asset
# loads below resolve. No effect when running from source (sys.frozen is unset).
if getattr(sys, 'frozen', False):
    import os
    os.chdir(sys._MEIPASS)

flags = FULLSCREEN | DOUBLEBUF
pygame.init()
clock = pygame.time.Clock()
# Fixed 1920x1080 logical resolution; SCALED scales it to any window size and remaps mouse input.
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE | pygame.SCALED)
screen_width, screen_height = pygame.display.get_surface().get_size()
# print(pygame.display.Info())
wf2 = 'wav_test2.wav'
wf3 = 'wobble.wav'
CHUNK = 1024*2
FORMAT = pyaudio.paInt16
FORMAT24 = pyaudio.paInt24

RATE = 48000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (72, 72, 72)
LIGHT_GREY = (107, 107, 107)
RED = (217, 33, 33)
BLUE = (30, 144, 255)
GREEN = (26, 148, 49)
YELLOW = (255, 243, 128)
p = pyaudio.PyAudio()
cmap = matplotlib.colormaps['turbo']

# define input and output devices here
p = pyaudio.PyAudio()

input_info = p.get_default_input_device_info()
output_info = p.get_default_output_device_info()
CHANNELS_INPUT = input_info['maxInputChannels']
CHANNELS_OUTPUT = output_info['maxOutputChannels']
player = p.open(format=FORMAT, channels=CHANNELS_OUTPUT, rate=RATE, output=True, frames_per_buffer=CHUNK, output_device_index=output_info['index'])
stream = p.open(format=FORMAT, channels=CHANNELS_INPUT, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=input_info['index'])

run = True
wf_data2 = wave.open(wf2,'rb')
n2_samples = wf_data2.getnframes()
cut_frames = int(n2_samples/3)
data2 = wf_data2.readframes(cut_frames)
signal_array2 = np.frombuffer(data2, dtype=np.int16)
size_conv = len(signal_array2)
signal_array2 = np.pad(signal_array2,(0,2*CHUNK),'constant')
y_fft2 = fft(signal_array2)*2/size_conv
next_chunk = np.zeros_like(np.real(y_fft2))

def round_to_multiple(base,mult):
    return mult*round(base/mult)

add_echo = False
change_pitch = False
auto_tune = False
visuals = True
discord = False

counter = 0
d = 500
bar_list = []
bar_row = []
y_init = 600
x_init = 850
x_vec = 0
y_vec = 0
z_vec = 0
num_rows = 15
spec_timer = 0
row_len = num_rows*10
timer = 0
loc = []
color_list = []
color_row = []
color_col = []
key_pressed = False
is_held = False
is_pressed = False
hide_button = False

ang_accum = np.pi/60
bar_side = 20
half_size = bar_side/2
z_limit = bar_side
timer_accum = bar_side
arrow_move = [0, 0, timer_accum]
divisor_const = 2*bar_side
ang = 0
left_side = -480
right_side = left_side+bar_side
tot_quat = np.eye(3)
option_names_page0 = ['Amplitude', 'Frequency']
option_names_page1 = ['Slice', 'Sphere','Spectrogram','Full Screen']
x_tot = 0
y_tot = 0
z_tot = 0
scroll_num = 5
img_counter = 0
record_timer = 0
timer_reset = 50
counter_list = [0,-screen_width]
blit_order = [1, 0]
data_record = []
surface_num = 1
pixel_screen1 = pygame.Surface((screen_width, screen_height))
pixel_screen2 = pygame.Surface((screen_width, screen_height))
surface_list = [pixel_screen1, pixel_screen2]



#function for calculating quaternion values and matrix
def quat_mat(angs,vec):
    x_vec,y_vec,z_vec = vec
    q0 = np.sin(angs/2)*x_vec
    q1 = np.sin(angs/2)*y_vec
    q2 = np.sin(angs/2)*z_vec
    q3 = np.cos(angs/2)
    r = R.from_quat([q0,q1,q2,q3])
    return r.as_matrix()

#function for outputting text onto the screen
font = pygame.font.Font('editundo.ttf', 20)
def draw_text(text, font, text_col, pos):
    img = font.render(text, True, text_col)
    screen.blit(img, pos)

#Create pages
class Pages():
    def __init__(self):
        self.page = 1
        self.page_timer = 10
        self.page_x = 0
        self.run = False
        self.freq = True
        self.amp = False
        self.click_allow = True
        self.slice = False
        self.circle_marker = False
        self.full_spectrogram = True
        self.font = pygame.font.Font('editundo.ttf', 60)
        self.check_mark = []
        self.check_rect = []
        self.num_options_page0 = 2
        self.num_options_page1 = 4
        self.top_color = True
        self.send_image = False
        for num in range(2):
            img = pygame.image.load(f'checkmark{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (60, 60))
            self.check_mark.append(img)
        for i in range(self.num_options_page1):
            check_rect = pygame.Rect(1515, 160 + 80*i, 60, 60)
            self.check_rect.append([check_rect,0])

        self.check_rect = np.array(self.check_rect, dtype = object)
        self.check_rect[3][1] = 1
        self.check_rect[2][1] = 1
        self.image_spec = pygame.Rect(1540, 500, 330, 60)

    def update(self):
        if self.run == True:
            pos = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(pos[0],pos[1],5,5)
            if pos[0] <= 1454 and pygame.mouse.get_pressed()[0] == 1:
                self.run = False
                self.page_timer = 10
                self.page_x = 0
                pygame.mouse.get_rel()
            if pygame.mouse.get_pressed()[0] == 0:
                self.click_allow = True
            self.page_timer -= 1
            if self.page_timer <= 0:
                self.page_timer = 0
            self.page_x += self.page_timer**2
            pygame.draw.rect(screen, GREY, (1739 - self.page_x, 0, 700, screen_height))
            pygame.draw.rect(screen, WHITE, (1739 - self.page_x, 0, 700, screen_height),15)
            if self.page == 0:
                draw_text("Options", self.font, BLACK, (1800 - self.page_x, 50))
                for i in range(self.num_options_page0):
                    draw_text(option_names_page0[i], self.font, BLACK, (1900 - self.page_x, 160 + 80*i))
                    screen.blit(self.check_mark[self.check_rect[i][1]], (1800 - self.page_x, 160 + 80*i))
                    if mouse_rect.colliderect(self.check_rect[i][0]) and pygame.mouse.get_pressed()[0] == 1 and self.click_allow == True:
                        self.click_allow = False
                        if self.check_rect[i][1] == 0:
                            self.check_rect[:,1] = 0
                            self.check_rect[i][1] = 1
                        elif self.check_rect[i][1] == 1:
                            self.check_rect[i][1] = 0
            elif self.page == 1:
                draw_text("Options", self.font, BLACK, (1800 - self.page_x, 50))
                for i in range(self.num_options_page1):
                    draw_text(option_names_page1[i], self.font, BLACK, (1900 - self.page_x, 160 + 80*i))
                    screen.blit(self.check_mark[self.check_rect[i][1]], (1800 - self.page_x, 160 + 80*i))
                    if mouse_rect.colliderect(self.check_rect[i][0]) and pygame.mouse.get_pressed()[0] == 1 and self.click_allow == True:
                        self.click_allow = False
                        if i == 0:
                            self.slice = not self.slice
                        elif i == 1:
                            self.circle_marker = not self.circle_marker
                        elif i == 2:
                            self.top_color = not self.top_color
                            self.full_spectrogram = False
                            self.check_rect[3][1] = 0
                        elif i == 3 and self.top_color == True:
                            self.full_spectrogram = not self.full_spectrogram
                            self.image_spec = pygame.Rect(1515, 500, 60, 60)
                        if self.check_rect[i][1] == 0:
                            self.check_rect[i][1] = 1
                        elif self.check_rect[i][1] == 1:
                            self.check_rect[i][1] = 0
            # sends image to spectrogram and plays it. does not work.
            # if self.full_spectrogram == True and self.page == 1:
            #     draw_text("Send Image", self.font, BLACK, (1835 - self.page_x, 500))
            #     pygame.draw.rect(screen, RED, self.image_spec,width=3)
            #     if mouse_rect.colliderect(self.image_spec) and pygame.mouse.get_pressed()[0] == 1 and self.click_allow == True:
            #         self.click_allow = False
            #         self.send_image = True
            #         self.img = pygame.image.load('test_audio.jpg').convert_alpha()
            #         self.img_grayscale = pygame.transform.grayscale(self.img)
            #         self.px_grayscale = pygame.surfarray.array3d(self.img_grayscale)
            #         self.img_grayscale = self.px_grayscale[:,:,1].transpose()
            #         # self.img_fft = fft2(self.img_grayscale)*2/CHUNK
            #         # self.img_fft = fftshift(self.img_fft)
            #         # plt.imshow(self.mag_spec,cmap='gray')
            #         # plt.show()
            #         # self.y_fft_abs = abs(self.img_fft/20)
            #         self.y_fft_abs = self.img_grayscale

                
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.page = 1
        elif key[pygame.K_RIGHT]:
            self.page = 0

#Create Timestep for discord audio
class Slider():
    def __init__(self):
        self.slider_x = round(screen_width - timer_reset)/2
        self.slider_length = timer_reset
    def update(self, timer_record):
        pygame.draw.rect(screen, WHITE, (self.slider_x, 500, self.slider_length, 10))
        pygame.draw.rect(screen, RED, (self.slider_x + timer_record, 480, 10, 50))
        pygame.draw.rect(screen, WHITE, (self.slider_x, 480, 10, 50))
        pygame.draw.rect(screen, WHITE, (self.slider_x+self.slider_length, 480, 10, 50))


slider_class = Slider()
page_class = Pages()
# Start loop
while run == True:
    pygame.display.update()
    screen.fill(BLACK)

    if add_echo == True:
        data = stream.read(CHUNK)
        # print(sys.getsizeof(data))
        data_int = np.array(struct.unpack(str(2*CHUNK) + 'h',data))
        data_modified = np.pad(data_int,(0,size_conv),'constant')
        y_fft = (fft(data_modified)*2/CHUNK)
        y_fft_abs = abs(y_fft[0:CHUNK])
        y_conv = y_fft2*y_fft
        y_ifft = np.real(ifft(y_conv*size_conv/12))
        y_fft_filtered = np.zeros_like(y_fft)
        y_res = np.add(y_ifft, next_chunk)
        next_chunk = y_res[2*CHUNK::]
        next_chunk = np.pad(next_chunk,(0,2*CHUNK),'constant')
        y_res = y_res[0:2*CHUNK]
        y_res = [round(x) for x in y_res]
        try:
            data_send = struct.pack(str(len(y_res)) + 'h',*y_res)
        except:
            print('limit value for short reached')
        player.write(data_send,CHUNK)

    counter += 1
    if change_pitch == True:
        val = int(0.8*CHUNK)
        data = stream.read(val, exception_on_overflow = False)
        data_int = np.array(struct.unpack(str(2*val) + 'h',data))
        data_int = 10*data_int
        data_resampled = signal.resample(data_int,2*CHUNK)
        # print(data_int[1],data_resampled[1])
        y_res = data_resampled
        y_res = y_res[0:2*CHUNK]
        y_res = [round(x) for x in y_res]
        try:
            data_send = struct.pack(str(len(y_res)) + 'h',*y_res)
        except:
            print('limit value for short reached')
        player.write(data_send)
    
    if auto_tune == True:
        data = stream.read(CHUNK)
        data_int = np.array(struct.unpack(str(2*CHUNK) + 'h',data))
        data_int = 10*data_int
        y_tuned = np.zeros_like(data_int)
        tune_const = 10
        tune_window = 5
        y_fft = (fft(data_int)*2/CHUNK)
        for i in range(1,int(len(y_fft)/tune_const)):
            y_val = np.mean(y_fft[i*tune_const - tune_window:i*tune_const + tune_window])
            y_tuned[i*tune_const] = y_val
        y_ifft = np.real(ifft(y_tuned*CHUNK*10/2))
        y_res = [int(x) for x in y_ifft]
        data_send = struct.pack(str(len(y_res)) + 'h',*y_res)
        player.write(data_send)
    
    if visuals == True:
        if page_class.send_image == False:
            data = stream.read(CHUNK)
            data_int = np.array(struct.unpack(str(CHANNELS_INPUT*CHUNK) + 'h',data))
            data_int = 5*data_int
            y_fft = (fft(data_int)*2/CHUNK)
            y_fft_abs = abs(y_fft[0:CHUNK]/20)
        else:
            img_counter += 1
            y_fft_abs = page_class.y_fft_abs[:,img_counter]
            width_fft,height_fft = np.shape(page_class.y_fft_abs)
            if img_counter == np.shape(y_fft_abs):
                img_counter = 0
                page_class.send_image = False

        y_fit = y_fft_abs[0:int(screen_width/divisor_const)]
        if [x_vec,y_vec,z_vec] != [0, 0, 0]:
            norm_val = np.linalg.norm([x_vec, y_vec, z_vec])
            norm_vec = [x_vec,y_vec,z_vec]/norm_val
        else:
            norm_vec = [0, 0, 0]


        if page_class.full_spectrogram == False:
            timer += timer_accum
            if key_pressed == True:
                r = quat_mat(ang_accum,norm_vec)
                arrow_move = r@arrow_move
                tot_quat = r@tot_quat
                for row in range(len(bar_list)):
                    for index in range(int(screen_width/divisor_const)):
                        bar_list[row][index] = r@bar_list[row][index]

            #add in bars with the correct rotation and height
            if timer == z_limit:
                bar_row = []
                color_row = []
                timer += bar_side*num_rows
                for index in range(int(screen_width/divisor_const)):   #48 rects per row
                    y_height = y_fit[index]
                    points = np.array([[left_side+bar_side*index,half_size,-row_len+bar_side+timer],[left_side+bar_side*index,-half_size-y_height,-row_len+bar_side+timer],[right_side+bar_side*index,-half_size-y_height,-row_len+bar_side+timer],[right_side+bar_side*index,half_size,-row_len+bar_side+timer],
                                    [right_side+bar_side*index,half_size,-row_len+bar_side+bar_side+timer],[right_side+bar_side*index,-half_size-y_height,-row_len+bar_side+bar_side+timer],[left_side+bar_side*index,-half_size-y_height,-row_len+bar_side+bar_side+timer],[left_side+bar_side*index,half_size,-row_len+bar_side+bar_side+timer]])
                    points = points.transpose()
                    new_points = tot_quat@points
                    bar_row.append(new_points)
                    color_height = cmap(abs(y_height)/50)[0:3]
                    rgb_rect = [255*x for x in color_height]
                    color_row.append(rgb_rect)
                    for row in range(len(bar_list)):
                        bar_list[row][index][:] -= [[arrow_move[0]], [arrow_move[1]], [arrow_move[2]]]
                color_list.append(color_row)
                bar_list.append(bar_row)
                color_loc = np.array(color_list)
                timer = 0
            if page_class.slice == True and len(bar_list) >= 5:
                bar_list = []
                num_rows = 1
                row_len = num_rows*10
            elif page_class.slice == False:
                num_rows = 30
                row_len = num_rows*10
            if len(bar_list) == num_rows+1:
                bar_list.pop(0)
                color_list.pop(0)
            if len(bar_list) > 0:
                loc = np.array(bar_list)
                loc = np.swapaxes(loc, 2,3)
                loc[:,:,:,0] += x_init
                loc[:,:,:,1] += y_init
                loc = loc[:,:,:,0:2]
            if y_tot < 0:
                loc = np.flip(loc,1)
                color_loc = np.flip(color_loc, 1)
            if arrow_move[2] > 0:
                loc = np.flip(loc,0)
                color_loc = np.flip(color_loc, 0)
            arrow_norm_val = np.linalg.norm(arrow_move)
            arrow_norm_vec = arrow_move/arrow_norm_val
            start_time = time.time()
            for row in range(len(loc)):
                for index in range(int(screen_width/divisor_const)):
                    pos = loc[row][index]
                    top_face = np.concatenate((pos[1:3], pos[5:7]))
                    left_face = np.concatenate((pos[0:2],pos[6:8]))
                    right_face = pos[2:6]
                    back_face = pos[4:8]
                    front_face = pos[0:4]
                    if page_class.circle_marker == True:
                        left,height = pos[2][0:2]
                        if page_class.top_color == True:
                            color_val =  color_loc[row][index]
                            pygame.draw.circle(screen, color_val, (left,height), 10)
                        else:
                            pygame.draw.circle(screen, WHITE, (left,height), 10)
                    else:
                        if y_tot < 0:
                            if arrow_move[2] < 0:
                                pygame.draw.polygon(screen, WHITE, (back_face))
                                pygame.draw.polygon(screen, LIGHT_GREY, (left_face))
                            else:
                                pygame.draw.polygon(screen, WHITE, (front_face))
                                pygame.draw.polygon(screen, LIGHT_GREY, (left_face))
                            if page_class.top_color == True:
                                color_val =  color_loc[row][index]
                                pygame.draw.polygon(screen, color_val, (top_face))
                            else:
                                pygame.draw.polygon(screen, GREY, (top_face))
                        else:
                            if arrow_move[2] < 0:
                                pygame.draw.polygon(screen, WHITE, (back_face))
                                pygame.draw.polygon(screen, LIGHT_GREY, (right_face))
                            else:
                                pygame.draw.polygon(screen, WHITE, (front_face))
                                pygame.draw.polygon(screen, LIGHT_GREY, (right_face))
                            if page_class.top_color == True:
                                color_val =  color_loc[row][index]
                                pygame.draw.polygon(screen, color_val, (top_face))
                            else:
                                pygame.draw.polygon(screen, GREY, (top_face))
        start_time = time.time()
        if page_class.full_spectrogram == True:
            pxarray  = pygame.PixelArray(surface_list[surface_num])
            #Make semilog plot. turn frequency into log form

            color_col = []
            spec_timer += 1
            #transpose pxarray so indexing becomes (rows,columns)
            pxarray = pxarray.transpose()
            if page_class.send_image == False:
                y_log = np.round(1200-169.25*np.log(np.arange(1,screen_height)))
                y_log = y_log.astype(int)
                y_log = list(set(y_log))
                y_log = np.flip(y_log)
                data_size = len(y_log)
                data_height = y_fft_abs[0:data_size]
                color_height = cmap(abs(data_height)/100)
                color_height = 255*color_height[:,0:3]
                color_height = list(map(tuple,color_height))
                for i in range(len(y_log)-1):
                    pxarray[y_log[i+1]:y_log[i],(-counter_list[surface_num]-scroll_num):-counter_list[surface_num]] = color_height[i]
            else:
                color_height = cmap(abs(data_height)/100)
                color_height = 255*color_height[:,0:3]
                color_height = list(map(tuple,color_height))
                pxarray[0:width_fft,(-counter_list[surface_num]-scroll_num):-counter_list[surface_num]] = color_height
            pxarray.close()
            counter_list = [x+scroll_num for x in counter_list]
            if counter_list[0] ==  screen_width:
                counter_list[0] = -screen_width
                surface_num = 0
                surface_list[surface_num].fill((0,0,0,0))
            elif counter_list[1] == screen_width:
                counter_list[1] = -screen_width
                surface_num = 1
                surface_list[surface_num].fill((0,0,0,0))
            for i in range(2):
                screen.blit(surface_list[i], (counter_list[i],0))
            # data_send = struct.pack(str(len(y_res)) + 'h',*y_res)
            # player.write(data_send)
        # end_time = time.time()
        # print(end_time - start_time)
        # print(z_tot,y_tot, arrow_norm_vec)
        # pygame.draw.line(screen, RED, (x_init,y_init),(x_init+500*arrow_norm_vec[0],y_init+500*arrow_norm_vec[1]))
        # for i in range(len(y_fit)):
        #     y_val = round_to_multiple(y_fit[i],10)
        #     pygame.draw.rect(screen, WHITE, (20*i, screen_height - y_val, 20, y_val))

    if discord == True:
        record_timer += 1
        data = stream.read(CHUNK)
        data_int = list(struct.unpack(str(CHANNELS_INPUT*CHUNK) + 'h',data))
        data_record = data_record + data_int
        slider_class.update(record_timer)
        if record_timer >= timer_reset:
            record_timer = 0
            data_record = [round(x) for x in data_record]
            data_send = struct.pack(str(len(data_record)) + 'h',*data_record)
            obj = wave.open('temp_audio.wav','wb')
            obj.setnchannels(CHANNELS_INPUT)
            obj.setsampwidth(2)
            obj.setframerate(RATE)
            obj.writeframesraw(data_send)
            data_record = []


    pos = pygame.mouse.get_pos()
    mouse_rect = pygame.Rect(pos[0],pos[1],5,5)
    if hide_button == False:
        pygame.draw.rect(screen,WHITE, (1800,0,100,100),0,5)
        open_page_rect = pygame.Rect((1800, 0), (100, 100))
        if open_page_rect.colliderect(mouse_rect) and pygame.mouse.get_pressed()[0] == 1 and page_class.run == False:
            page_class.run = True
        elif page_class.run == True:
            page_class.update()

    x_vec = 0
    y_vec = 0
    z_vec = 0

    key = pygame.key.get_pressed()
    key_pressed = False
    if pygame.mouse.get_pressed()[0] == 1 and is_pressed == False and page_class.run == False:
        is_pressed = True
        [x_moved,y_moved] = pygame.mouse.get_rel()
    elif is_pressed == True and page_class.run == False:
        is_held = True
        if pygame.mouse.get_pressed()[0] == 0:
            is_pressed = False
            is_held = False
        [x_moved,y_moved] = pygame.mouse.get_rel()
        if y_moved > 0:
            x_vec = 1
            x_tot += 1
            key_pressed = True
        elif y_moved < 0:
            x_vec = -1
            x_tot -= 1
            key_pressed = True
        if x_moved > 0:
            y_vec = -1
            y_tot -= 1
            key_pressed = True
        elif x_moved < 0:
            y_vec = 1
            y_tot += 1
            key_pressed = True

    if key[pygame.K_UP]:
        x_vec = 1
        x_tot += 1
        key_pressed = True
    elif key[pygame.K_DOWN]:
        x_vec = -1
        x_tot -= 1
        key_pressed = True
    if key[pygame.K_LEFT]:
        y_vec = 1
        y_tot += 1
        key_pressed = True
    elif key[pygame.K_RIGHT]:
        y_vec = -1
        y_tot -= 1
        key_pressed = True
    if key[pygame.K_a]:
        z_vec = 1
        z_tot += 1
        key_pressed = True
    elif key[pygame.K_d]:
        z_vec = -1
        z_tot -= 1
        key_pressed = True

        
        
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_h:
                hide_button = not hide_button
pygame.quit()