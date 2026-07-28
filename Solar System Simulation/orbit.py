'''
NOTES:

-The simulation will take a while to start because it needs to run the numerical algorithm to calculate thousands
of positions and velocity for each planet

-Yeah the code is pretty messy

Keys for Commands:
Space: Pauses the simulation
T: Shows the name of each planet
0~9: Moves the inertial frame to its respective planet
Q,W: Rotates the axis along x-axis
A,S: Rotates the axis along y-axis
Z,X: Rotates the axis along z-axis
Arrow UP: Increases the speed of simulation
Arrow DOWN: Decreases the speed of simulation
ESC: Exit simulation
'''

import pygame
import pickle
import numpy as np
from numpy.linalg import norm
import math as m
import os
import sys
from pygame.locals import *


def resource_path(relative_path):
    """Return an asset path that works from source and a PyInstaller bundle."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


pygame.init()
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode((1920, 1080), FULLSCREEN | SCALED)
screen_width, screen_height = pygame.display.get_surface().get_size()
#width: 1920 height: 1080
transparent_surface = pygame.Surface((screen_width, screen_height), SRCALPHA)

GREEN = (144, 201, 120)
LIGHT_BLUE = (147, 190, 255)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
BLACK = (0,0,0)
GREY = (169, 169, 169)
SUN = (200, 25, 25)
MERCURY = (122, 125, 41)
VENUS = (205, 100, 36)
EARTH = (255, 255, 255)
MARS = (181, 121, 86)
JUPITER = (202, 97, 36)
SATURN = (186, 191, 60)
URANUS = (147, 198, 210)
NEPTUNE = (55, 216, 255)
PLUTO = (16, 98, 118)
planet_colors = [SUN, MERCURY, VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE, PLUTO]
planet_names = ["SUN", "MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO"]
page2_text = ['Plane', 'Axis', 'Periapsis', 'Apoapsis', 'Time', 'Time Bar']
planet_radius = [6.955*10**5, 2.44*10**3, 6.0518*10**3, 6.37101*10**3, 3.3899*10**3, 6.9911*10**4, 5.8232*10**4, 2.5362*10**4, 2.4624*10**4, 1.195*10**3]
planet_mu = [1.326*10**11, 2.208*10**4, 3.248*10**5, 3.986*10**5, 4.282*10**4, 1.267*10**8, 3.795*10**7, 5.796*10**6, 6.87*10**6, 8.476*10**2]
masses = [1.98854*10**30, 3.302*10**23, 4.8685*10**24, 5.97219*10**24, 6.4185*10**23, 1.89813*10**27, 5.68319*10**26, 8.68103*10**25, 1.0241*10**26, 1.307*10**22]
basis_colors = [WHITE,LIGHT_BLUE,GREEN]
trail_particle = []
planet_images = []
basis_vec = np.array([[1,0,0],[0,1,0],[0,0,1]])
new_basis_vec = np.array([[1,0,0],[0,1,0],[0,0,1]])
basis_surf = np.array([[350,350,0],[-350,350,0],[-350, -350,0],[350,-350,0]])
new_basis_surf = np.array([[350,350,0],[-350,350,0],[-350, -350,0],[350,-350,0]])
keys_list = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]
ang_around_orbit = np.linspace(0,2*np.pi,1000)
zoom = 5
time_scale = 10
run = True
show_planet_name = False
is_pressed = False
show_trail = False
scale_radius = False
pause = False
real_planet = False
is_held = False
moving_bar = False
prev_x = 0
prev_y = 0
xtheta = 0
ytheta = 0
ztheta = 0
inertial_frame = 0
for num in range(10):
    img = pygame.image.load(resource_path(f'orbit_images/planet_{num}.png')).convert_alpha()
    img = pygame.transform.scale(img, (30, 30))
    planet_images.append(img)


#centers the coordinate system
def centers(pos):
    x = pos[0]
    y = pos[1]
    x = 960 + pos[0]
    y = 540 - pos[1]
    return [x,y]


#Calculation for orbital trajectory
def orbit(y, t):
    masses = [1.98854*10**30, 3.302*10**23, 4.8685*10**24, 5.97219*10**24, 6.4185*10**23, 1.89813*10**27, 5.68319*10**26, 8.68103*10**25, 1.0241*10**26, 1.307*10**22]
    x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,z1,z2,z3,z4,z5,z6,z7,z8,z9,z10,dx1,dx2,dx3,dx4,dx5,dx6,dx7,dx8,dx9,dx10,dy1,dy2,dy3,dy4,dy5,dy6,dy7,dy8,dy9,dy10,dz1,dz2,dz3,dz4,dz5,dz6,dz7,dz8,dz9,dz10 = y
    x_pos = [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10]
    y_pos = [y1,y2,y3,y4,y5,y6,y7,y8,y9,y10]
    z_pos = [z1,z2,z3,z4,z5,z6,z7,z8,z9,z10]
    accelx = np.zeros(10)
    accely = np.zeros(10)
    accelz = np.zeros(10)
    G = (6.6743*10**-20)*(60**4)
    for i in range(10):
        for j in range(10):
            if i != j:
                r = np.sqrt((x_pos[j] - x_pos[i])**2 + (y_pos[j] - y_pos[i])**2 + (z_pos[j] - z_pos[i])**2)
                Fm = G*masses[j]/r**3
                accelx[i] += Fm*(x_pos[j] - x_pos[i])
                accely[i] += Fm*(y_pos[j] - y_pos[i])
                accelz[i] += Fm*(z_pos[j] - z_pos[i])
    vel_output = np.array([dx1,dx2,dx3,dx4,dx5,dx6,dx7,dx8,dx9,dx10,dy1,dy2,dy3,dy4,dy5,dy6,dy7,dy8,dy9,dy10,dz1,dz2,dz3,dz4,dz5,dz6,dz7,dz8,dz9,dz10])
    dydt = np.concatenate((vel_output, accelx,accely,accelz),axis = 0)
    return dydt


#Apply rotation matrix so we can rotate around
def rotation(vec, theta,axis):
    basis_vec = np.eye(3)[axis]
    xvec = vec[0]
    yvec = vec[1]
    zvec = vec[2]
    new_x = xvec * m.cos(theta) + np.cross(basis_vec,xvec)*m.sin(theta) + basis_vec*np.dot(basis_vec,xvec)*(1 - m.cos(theta))
    new_y = yvec * m.cos(theta) + np.cross(basis_vec,yvec)*m.sin(theta) + basis_vec*np.dot(basis_vec,yvec)*(1 - m.cos(theta))
    new_z = zvec * m.cos(theta) + np.cross(basis_vec,zvec)*m.sin(theta) + basis_vec*np.dot(basis_vec,zvec)*(1 - m.cos(theta))
    new_vec = np.array([new_x,new_y,new_z])
    return new_vec


#function for outputting text onto the screen
font = pygame.font.Font(resource_path('editundo.ttf'), 20)
def draw_text(text, font, text_col, pos):
    img = font.render(text, True, text_col)
    screen.blit(img, pos)


#centers the coordinate system based on the selected planet
def center_planet(original, basis, planet_num):
    original_data = np.copy(original)
    new_basis = np.copy(basis)
    for i in range(10):
        new_basis[:,i] = original_data[:,i] - original_data[:,planet_num]
        new_basis[:,i+10] = original_data[:,i+10] - original_data[:,planet_num+10]
        new_basis[:,i+20] = original_data[:,i+20] - original_data[:,planet_num+20]
        new_basis[:,i+30] = original_data[:,i+30] - original_data[:,planet_num+30]
        new_basis[:,i+40] = original_data[:,i+40] - original_data[:,planet_num+40]
        new_basis[:,i+50] = original_data[:,i+50] - original_data[:,planet_num+50]
    return new_basis


tspace = np.linspace(0,10**5,10**5)
pos_init = np.array([[1.81899*10**5, 9.83630*10**5, -1.58778*10**4],
                    [-5.67576*10**7, -2.73592*10**7, 2.89173*10**6],
                    [4.28480*10**7, 1.00073*10**8, -1.11872*10**6],
                    [-1.43778*10**8, -4.00067*10**7, -1.38875*10**4],
                    [-1.14746*10**8, -1.96294*10**8, -1.32908*10**6],
                    [-5.66899*10**8, -5.77495*10**8, 1.50755*10**7],
                    [8.20513*10**7, -1.50241*10**9, 2.28565*10**7],
                    [2.62506*10**9, 1.40273*10**9, -2.87982*10**7],
                    [4.30300*10**9, -1.24223*10**9, -7.35857*10**7],
                    [1.65554*10**9, -4.73503*10**9, 2.77962*10**7]])
vel_init = np.array([[-1.12474*10**-2, 7.54876*10**-3, 2.68723*10**-4],
                    [1.16497*10, -4.14793*10, -4.45952],
                    [-3.22930*10, 1.36960*10, 2.05091],
                    [7.65151, -2.87514*10, 2.08354*10**-3],
                    [2.18369*10, -1.01132*10, -7.47957*10**-1],
                    [9.16793, -8.53244, -1.69767*10**-1],
                    [9.11312, 4.96372*10**-1, -3.71643*10**-1],
                    [-3.25937, 5.68878, 6.32569*10**-2],
                    [1.47132, 5.25363, -1.42701*10**-1],
                    [5.24541, 6.38510*10**-1, -1.60709]]) * 60**2

pos_init_vec = np.concatenate((pos_init[:,0], pos_init[:,1],pos_init[:,2]),axis = 0)
vel_init_vec = np.concatenate((vel_init[:,0], vel_init[:,1],vel_init[:,2]),axis = 0)

# Load the precomputed trajectories. Recalculating them on every launch is slow,
# and a bundled one-file executable should not need to write beside itself.
with open(resource_path('orbitdata_hours'), 'rb') as pickle_in:
    sol_basis = pickle.load(pickle_in)

t = 10
specific_energy = np.zeros(10)
semimajor = np.zeros(10)
semiminor = np.zeros(10)
ang_momentum = np.zeros(10)
eccentricity = np.zeros(10)
eccentricity_vec = []
inclination = np.zeros(10)
omega = np.zeros(10)
arg_peri = np.zeros(10)
true_anom = np.zeros(10)
periapsis = np.zeros(10)
apoapsis = np.zeros(10)
ellipse_vec_basis = []
semimajor_vec = []
semiminor_vec = []
periapsis_vec = []
apoapsis_vec = []
towards_center = []
normal_vec = []
planet_rect = [0,0,0,0,0,0,0,0,0,0]
planet_orbit_trace = []
ellipse_vec = [0,0]
sol_basis = center_planet(sol_basis,sol_basis, 0)

for i in range(10):
    velo_vec = sol_basis[0][i+30:i+51:10]/60**2
    radius_vec = sol_basis[0][i:i+21:10]
    k = [0,0,1]
    velo = np.linalg.norm(velo_vec)
    radius_var = np.linalg.norm(radius_vec)
    specific_energy[i] = 0.5*velo**2 - (planet_mu[0]/radius_var)
    ang_momentum_vec = np.cross(radius_vec,velo_vec)
    inclination[i] = np.arccos(ang_momentum_vec[2]/np.linalg.norm(ang_momentum_vec))
    ang_momentum[i] = np.linalg.norm(ang_momentum_vec)
    semimajor[i] = -planet_mu[0]/(2*specific_energy[i])
    normal_vec.append(np.cross(k,ang_momentum_vec))
    omega[i] = np.arccos(normal_vec[i][0]/np.linalg.norm(normal_vec[i]))
    if normal_vec[i][1] < 0:
        omega[i] = 2*np.pi - omega[i]
    eccentricity_vec.append(np.cross(velo_vec,ang_momentum_vec)/planet_mu[0] - radius_vec/np.linalg.norm(radius_vec))
    eccentricity[i] = norm(eccentricity_vec[i])
    periapsis[i] = semimajor[i]*(1-eccentricity[i])/10**7
    apoapsis[i] = semimajor[i]*(1+eccentricity[i])/10**7
    towards_center.append(-semimajor[i]*eccentricity_vec[i]/10**7)
    periapsis_vec.append(eccentricity_vec[i]*periapsis[i]/eccentricity[i])
    semimajor_vec.append(semimajor[i]*eccentricity_vec[i]/(eccentricity[i]*10**7))
    semiminor_direction = [-eccentricity_vec[i][1],eccentricity_vec[i][0],0]/(eccentricity[i]*10**7)

    semiminor_vec.append((semimajor[i])*np.sqrt(1 - eccentricity[i]**2)*semiminor_direction)
    apoapsis_vec.append(-eccentricity_vec[i]*apoapsis[i]/eccentricity[i])
    arg_peri[i] = np.arccos(np.dot(normal_vec[i],eccentricity_vec[i])/(np.linalg.norm(normal_vec[i])*eccentricity[i]))
    if eccentricity_vec[i][2] < 0:
        arg_peri[i] = 2*np.pi - arg_peri[i]
    semiminor[i] = semimajor[i]*np.sqrt(1-eccentricity[i]**2)
    true_anom[i] = np.arccos(np.dot(eccentricity_vec[i],radius_vec)/(eccentricity[i]*radius_var))
    if radius_vec[2] < 0:
        true_anom[i] = 2*np.pi - true_anom[i]

select_planet = 5
semiminor_vec_basis = np.copy(semiminor_vec)
semimajor_vec_basis = np.copy(semimajor_vec)
eccentricity_vec_basis = np.copy(eccentricity_vec)
towards_center_basis = np.copy(towards_center)
normal_vec_basis = np.copy(normal_vec)



ellipse_vec_basis = []
def calculate_ellipse():
    ellipse_vec_basis = []
    M_inc = [[1, 0, 0], [0, np.cos(inclination[select_planet]), np.sin(inclination[select_planet])], [0, -np.sin(inclination[select_planet]), np.cos(inclination[select_planet])]]
    M_omega = [[np.cos(omega[select_planet]), np.sin(omega[select_planet]), 0], [-np.sin(omega[select_planet]), np.cos(omega[select_planet]), 0], [0, 0, 1]]
    M_arg_peri = [[np.cos(arg_peri[select_planet]), np.sin(arg_peri[select_planet]), 0], [-np.sin(arg_peri[select_planet]), np.cos(arg_peri[select_planet]), 0], [0, 0, 1]]
    ellipse_rot_mat = np.matmul(np.matmul(M_arg_peri, M_inc), M_omega)
    #print(omega[select_planet], inclination[select_planet], arg_peri[select_planet],true_anom[select_planet])
    for ang in ang_around_orbit:
        ellipse_vec_basis.append(np.dot(np.transpose(ellipse_rot_mat),[semimajor[select_planet]*np.cos(ang)/10**7 + towards_center[select_planet][0], semiminor[select_planet]*np.sin(ang)/10**7 + towards_center[select_planet][1], 0]))
    return ellipse_vec_basis


for i in range(np.shape(sol_basis)[0]):
    sol_basis[i,:] = sol_basis[i,:]/10**7
sol_var = np.copy(sol_basis)
sol_original = np.copy(sol_basis)


#Create pages
class Pages():
    def __init__(self):
        self.page = 0
        self.page_timer = 10
        self.page_x = 0
        self.run = False
        self.click_allow = True
        self.font = pygame.font.Font(resource_path('editundo.ttf'), 60)
        self.check_mark = []
        self.check_rect = []
        self.check_rect2 = []
        self.show_axis = True
        self.show_plane = True
        self.show_periapsis = True
        self.show_apoapsis = True
        self.show_time = True
        self.show_time_bar = True
        for num in range(2):
            img = pygame.image.load(resource_path(f'orbit_images/checkmark{num}.png')).convert_alpha()
            img = pygame.transform.scale(img, (60, 60))
            self.check_mark.append(img)
        for i in range(10):
            check_rect = pygame.Rect(1515, 160 + 80*i, 60, 60)
            self.check_rect.append([check_rect,1])
        self.left = pygame.Rect(1615, screen_height - 90, 50, 50)
        self.right = pygame.Rect(1735, screen_height - 90, 50, 50)
        for i in range(6):
            check_rect = pygame.Rect(1515, 160 + 80*i, 60, 60)
            self.check_rect2.append([check_rect,1])

    def update(self):
        if self.run == True:
            pos = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(pos[0],pos[1],5,5)
            if pos[0] <= 1454 and pygame.mouse.get_pressed()[0] == 1:
                self.run = False
                self.page_timer = 10
                self.page_x = 0
                pygame.mouse.get_rel()
            elif mouse_rect.colliderect(self.left) and pygame.mouse.get_pressed()[0] == 1 and self.page == 1:
                self.page -= 1
            elif mouse_rect.colliderect(self.right) and pygame.mouse.get_pressed()[0] == 1 and self.page == 0:
                self.page += 1
            elif pygame.mouse.get_pressed()[0] == 0:
                self.click_allow = True
            self.page_timer -= 1
            if self.page_timer <= 0:
                self.page_timer = 0
            self.page_x += self.page_timer**2
            pygame.draw.rect(screen, GREY, (1739 - self.page_x, 0, 700, screen_height))
            pygame.draw.rect(screen, WHITE, (1739 - self.page_x, 0, 700, screen_height),15)
            pygame.draw.rect(screen, BLACK, (1900 - self.page_x, screen_height - 90, 50, 50))
            pygame.draw.rect(screen, BLACK, (2000 - self.page_x, screen_height - 90, 50, 50))
            draw_text("<", self.font, WHITE, (1910 - self.page_x, screen_height - 90))
            draw_text(">", self.font, WHITE, (2020 - self.page_x, screen_height - 90))

            if self.page == 0:
                draw_text("Show Planets", self.font, BLACK, (1800 - self.page_x, 50))
                for i in range(10):
                    draw_text(planet_names[i], self.font, BLACK, (1900 - self.page_x, 160 + 80*i))
                    screen.blit(self.check_mark[self.check_rect[i][1]], (1800 - self.page_x, 160 + 80*i))
                    if mouse_rect.colliderect(self.check_rect[i][0]) and pygame.mouse.get_pressed()[0] == 1 and self.click_allow == True:
                        self.click_allow = False
                        if self.check_rect[i][1] == 0:
                            self.check_rect[i][1] = 1
                        elif self.check_rect[i][1] == 1:
                            self.check_rect[i][1] = 0
            elif self.page == 1:
                draw_text("Options", self.font, BLACK, (1850 - self.page_x, 50))
                for i in range(6):
                    draw_text(page2_text[i], self.font, BLACK, (1880 - self.page_x, 160 + 80*i))
                    screen.blit(self.check_mark[self.check_rect2[i][1]], (1800 - self.page_x, 160 + 80*i))
                    if mouse_rect.colliderect(self.check_rect2[i][0]) and pygame.mouse.get_pressed()[0] == 1 and self.click_allow == True:
                        self.click_allow = False
                        if i == 0:
                            self.show_plane = not self.show_plane
                        elif i == 1:
                            self.show_axis = not self.show_axis
                        elif i == 2:
                            self.show_periapsis = not self.show_periapsis
                        elif i == 3:
                            self.show_apoapsis = not self.show_apoapsis
                        elif i == 4:
                            self.show_time = not self.show_time
                        elif i == 5:
                            self.show_time_bar = not self.show_time_bar
                        if self.check_rect2[i][1] == 0:
                            self.check_rect2[i][1] = 1
                        elif self.check_rect2[i][1] == 1:
                            self.check_rect2[i][1] = 0
                        

#Show detail about the planet
class Detail():
    def __init__(self):
        self.run = False
        self.page_timer = 10
        self.page_x = 0
        self.click_allow = False
        self.font = pygame.font.Font(resource_path('editundo.ttf'), 80)
        self.exit_rect = pygame.Rect(1445, 0, 50, 50)
        self.planet_show = 0
        self.show_orbit = False
        self.radius_vec = 0

    def update(self):
        if self.run == True:
            pos = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(pos[0],pos[1],5,5)
            if pygame.mouse.get_pressed()[0] == 0:
                self.click_allow = True
            elif self.exit_rect.colliderect(mouse_rect) and pygame.mouse.get_pressed()[0] == 1 and self.click_allow == True:
                self.run = False
                self.click_allow = False
                self.page_timer = 10
                self.page_x = 0
                self.show_orbit = False
                pygame.mouse.get_rel()
            elif pygame.mouse.get_pressed()[0] == 1 and self.click_allow == True:
                self.run = False
                self.click_allow = False
                self.page_timer = 10
                self.page_x = 0
                self.show_orbit = False
                pygame.mouse.get_rel()

            self.page_timer -= 1
            if self.page_timer <= 0:
                self.page_timer = 0
            self.page_x += self.page_timer**2
            self.radius_vec = sol_var[t][self.planet_show:self.planet_show+21:10]*zoom
            
            pygame.draw.rect(screen, GREY, (1739 - self.page_x, 0, 700, screen_height))
            pygame.draw.rect(screen, WHITE, (1739 - self.page_x, 0, 700, screen_height),15)
            pygame.draw.rect(screen, RED, (1730 - self.page_x, 0, 50, 50))

            self.font = pygame.font.Font(resource_path('editundo.ttf'), 80)
            draw_text(f'{planet_names[self.planet_show]}', self.font, BLACK, (1850 - self.page_x, 50))
            pygame.draw.line(screen, RED, (centers([0,0])), (centers(self.radius_vec)))
            self.font = pygame.font.Font(resource_path('editundo.ttf'), 30)
            draw_text('Semimajor Axis:', self.font, BLACK, (1760 - self.page_x, 200))
            draw_text(f'{semimajor[self.planet_show]:.2f}km', self.font, BLACK, (2000 - self.page_x, 200))

            draw_text('Eccentricity:', self.font, BLACK, (1760 - self.page_x, 250))
            draw_text(f'{eccentricity[self.planet_show]:.2f}', self.font, BLACK, (2000 - self.page_x, 250))

            draw_text('Inclination:', self.font, BLACK, (1760 - self.page_x, 300))
            draw_text(f'{inclination[self.planet_show]*180/np.pi:.2f}', self.font, BLACK, (2000 - self.page_x, 300))

            draw_text('Omega:', self.font, BLACK, (1760 - self.page_x, 350))
            draw_text(f'{omega[self.planet_show]*180/np.pi:.2f}', self.font, BLACK, (2000 - self.page_x, 350))

            draw_text('Arg of Periapsis:', self.font, BLACK, (1760 - self.page_x, 400))
            draw_text(f'{arg_peri[self.planet_show]*180/np.pi:.2f}', self.font, BLACK, (2000 - self.page_x, 400))


detail_class = Detail()
page_class = Pages()
while run:
    screen.fill(BLACK)
    transparent_surface.fill((0,0,0,0))
    pos = pygame.mouse.get_pos()
    mouse_rect = pygame.Rect(pos[0],pos[1],5,5)
    #Open page if user clicks on page button
    pygame.draw.rect(screen,GREY, (1800,0,100,100),0,5)
    open_page_rect = pygame.Rect((1800, 0), (100, 100))
    if open_page_rect.colliderect(mouse_rect) and pygame.mouse.get_pressed()[0] == 1 and page_class.run == False and is_held == False:
        page_class.run = True

    if pygame.mouse.get_pressed()[0] == 1 and is_pressed == False and page_class.run == False:
        is_pressed = True
        [x_moved,y_moved] = pygame.mouse.get_rel()
    elif is_pressed == True and page_class.run == False and moving_bar == False:
        is_held = True
        [x_moved,y_moved] = pygame.mouse.get_rel()
        ytheta += (x_moved)/100
        xtheta += (y_moved)/100
    if pygame.mouse.get_pressed()[0] == 0:
        is_pressed = False
        is_held = False
        moving_bar = False
    semimajor_vec[select_planet] = np.dot(np.transpose(new_basis_vec),semimajor_vec_basis[select_planet])
    semiminor_vec[select_planet] = np.dot(np.transpose(new_basis_vec),semiminor_vec_basis[select_planet])
    eccentricity_vec[select_planet] = np.dot(np.transpose(new_basis_vec),eccentricity_vec_basis[select_planet])
    normal_vec[select_planet] = np.dot(np.transpose(new_basis_vec),normal_vec_basis[select_planet])
    towards_center[select_planet] = np.dot(np.transpose(new_basis_vec),towards_center_basis[select_planet])

    if pause == False:
        t += 1*time_scale

    #If time reaches its maximum, calculate the next time
    if t >= 10**5:
        t = 0
        #initial_pos_vel = sol_basis[-1][:]*10**7
        #sol_basis = odeint(orbit,initial_pos_vel,tspace)
        #for i in range(np.shape(sol_basis)[0]):
            #sol_basis[i,:] = sol_basis[i,:]/10**7
        #sol_original = np.copy(sol_basis)
        #sol_basis = center_planet(sol_original,sol_basis, inertial_frame)
        #sol_var = np.copy(sol_basis)

    for i in range(10):
        sol_var[t][i:i+21:10] = np.dot(np.transpose(new_basis_vec),sol_basis[t][i:i+21:10])
        sol_var[t][30+i:i+51:10] = np.dot(np.transpose(new_basis_vec),sol_basis[t][30+i:i+51:10])
    for i in range(4):
        new_basis_surf[i] = np.dot(np.transpose(new_basis_vec),basis_surf[i])


    if page_class.show_plane == True:
        pygame.draw.polygon(transparent_surface, (255,255,255,50), (centers(new_basis_surf[0][0:2]),centers(new_basis_surf[1][0:2]),centers(new_basis_surf[2][0:2]),centers(new_basis_surf[3][0:2])))
    if page_class.show_axis == True:
        for i in range(3):
            pygame.draw.line(screen, basis_colors[i], (centers([0,0])),(centers(new_basis_vec[i][0:2]*300)))
    if page_class.show_periapsis == True and detail_class.run == True:
        periapsis_pos = np.dot(np.transpose(new_basis_vec),ellipse_vec_basis[0])
        apoapsis_pos = np.dot(np.transpose(new_basis_vec),ellipse_vec_basis[499])
        draw_text('periapsis', font, WHITE, centers(periapsis_pos[0:2]*zoom))
        draw_text('apoapsis', font, WHITE, centers(apoapsis_pos[0:2]*zoom))
        pygame.draw.circle(screen, RED, (centers(periapsis_pos[0:2]*zoom)),5)
        pygame.draw.circle(screen, RED, (centers(apoapsis_pos[0:2]*zoom)),5)
    if page_class.show_time_bar == True:
        time_bar_rect = pygame.Rect(450 + t/100, 40, 10, 30)
        if mouse_rect.colliderect(time_bar_rect) and pygame.mouse.get_pressed()[0] == 1:
                moving_bar = True
                is_held = True
                is_pressed = True
        if moving_bar == True and pos[0] > 200 and pos[0] < 1600:
            t = 100*(pos[0] - 450)
            t = sorted([0, t, 10**5 - 1])[1]
            for i in range(10):
                sol_var[t][i:i+21:10] = np.dot(np.transpose(new_basis_vec),sol_basis[t][i:i+21:10])
                sol_var[t][30+i:i+51:10] = np.dot(np.transpose(new_basis_vec),sol_basis[t][30+i:i+51:10])
        pygame.draw.rect(screen, WHITE, (450 , 50, 1000, 10))
        pygame.draw.rect(screen, RED, (450 + t/100, 40, 10, 30))
        
    if page_class.show_time == True:
        draw_text(f'{tspace[t]:.0f}hours', font, WHITE, (0,0))

    if detail_class.show_orbit == True and inertial_frame == 0:
        for i in range(1000):
            ellipse_vec = np.dot(np.transpose(new_basis_vec),ellipse_vec_basis[i])
            pygame.draw.circle(screen, RED, (centers([ellipse_vec[0]*zoom,ellipse_vec[1]*zoom])),1)

    for i in range(10):
        if scale_radius == True:
            radius = sorted([planet_radius[i]*zoom/1000, planet_radius[i]*zoom/1000 + sol_var[t][i+20]*zoom])[0]
        else:
            radius = 12
        if page_class.check_rect[i][1] == 1:
            pygame.draw.circle(screen, planet_colors[i], (centers([sol_var[t][i]*zoom,sol_var[t][i+10]*zoom])), radius)
            screen.blit(planet_images[i], (centers([sol_var[t][i]*zoom-15,sol_var[t][i+10]*zoom+15])))
            planet_rect[i] = pygame.Rect((centers([sol_var[t][i]*zoom - 10,sol_var[t][i+10]*zoom + 10])),(20,20))
            #pygame.draw.rect(screen,WHITE,planet_rect[i])
            if show_planet_name == True:
                draw_text(planet_names[i], font, WHITE, centers([sol_var[t][i]*zoom,sol_var[t][i+10]*zoom]))
        if show_trail == True:
            trail_particle.append([centers([sol_var[t][i]*zoom,sol_var[t][i+10]*zoom]), 5])
        if planet_rect[i].colliderect(mouse_rect) and pygame.mouse.get_pressed()[0] == 1 and detail_class.run == False and is_held == False:
            detail_class.run = True
            detail_class.show_orbit = True
            detail_class.planet_show = i
            select_planet = i
            ellipse_vec_basis = calculate_ellipse()
    if page_class.run == True:
        page_class.update()
    if detail_class.run == True:
        detail_class.update()
    screen.blit(transparent_surface, (0 ,0))

    #Key presses
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        xtheta += 0.01 
    elif key[pygame.K_q]:
        xtheta -= 0.01
    if key[pygame.K_s]:
        ytheta += 0.01
    elif key[pygame.K_a]:
        ytheta -= 0.01
    if key[pygame.K_x]:
        ztheta += 0.01
    elif key[pygame.K_z]:
        ztheta -= 0.01
    
    new_basis_vec = rotation(new_basis_vec,xtheta,0)
    new_basis_vec = rotation(new_basis_vec,ytheta,1)
    new_basis_vec = rotation(new_basis_vec,ztheta,2)
    xtheta = 0
    ytheta = 0
    ztheta = 0
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            for i,num in enumerate(keys_list):
                if event.key == keys_list[i]:
                    sol_basis = center_planet(sol_original,sol_basis, i)
                    inertial_frame = i
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_UP and time_scale != 30:
                time_scale += 1
            elif event.key == pygame.K_DOWN and time_scale != 0:
                time_scale -= 1
            elif event.key == pygame.K_t:
                show_planet_name = not show_planet_name
            elif event.key == pygame.K_o:
                show_trail = not show_trail
            elif event.key == pygame.K_r:
                scale_radius = not scale_radius
            elif event.key == pygame.K_SPACE:
                pause = not pause
        elif event.type == MOUSEWHEEL:
            zoom += 0.5*event.y
    if zoom <= 0:
        zoom = 0.5
    pygame.display.update()
pygame.quit()
