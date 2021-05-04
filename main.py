import pygame as pg
from pygame.constants import QUIT
import time
import random
import math
import vector
import numpy as np

# globals
radius = 20
window_width = 800
window_height = 800
num_of_objects = 3
start_pos = (window_width/2, radius+5)
gravity = 0  # meters / sec ^2
fps = 120
scale = 30
horizontal_vector = vector.vector2d(-40, 0, 0)

# predefined colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 255)
bright_green = (0, 255, 0)
yellow = (255, 255, 0)

pg.init()
dis = pg.display.set_mode((window_width, window_height))
pg.display.set_caption("phy")
fpsclk = pg.time.Clock()
ptime = 0


class sphere():
    def update_vector(self):
        self.velocity_vector.i = self.vel_x
        self.velocity_vector.j = self.vel_y
        """"if self.vel_x == 0:
            self.theta = 90
        else:
            slope = self.vel_y/self.vel_x
            self.theta = math.degrees(math.atan(slope))
"""""
        # cos0 = (u.v) / (|u|.|v|)
        uv = (horizontal_vector.i * self.velocity_vector.i) + \
            (horizontal_vector.j * self.velocity_vector.j)
        umag_x_vmag = math.sqrt(horizontal_vector.i**2 + horizontal_vector.j**2) * \
            math.sqrt(self.velocity_vector.i**2 + self.velocity_vector.j**2)

        if (self.vel_y > 0):
            self.velocity_vector.theta = self.theta = 360-math.degrees(
                math.acos(uv/umag_x_vmag))
        else:
            self.velocity_vector.theta = self.theta = math.degrees(
                math.acos(uv/umag_x_vmag))

    def __init__(self, pos, vel, mass):
        self.radius = mass*5
        self.colour = yellow
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.vel_x = vel[0]
        self.vel_y = vel[1]
        self.mass = mass
        self.theta = 0

        self.velocity_vector = vector.vector2d(
            self.vel_x, self.vel_y, self.theta)

        self.update_vector()


def event_handler():

    for event in pg.event.get():
        if (event.type == QUIT):
            pg.quit()
            quit()


def display_vectors(objects):
    for sphere in objects:
        x = (sphere.pos_x+sphere.vel_x*scale)
        y = (sphere.pos_y+sphere.vel_y*scale)

        end_pos = (x, y)
        pg.draw.aaline(dis, red, (sphere.pos_x, sphere.pos_y),
                       end_pos, blend=1)
        font = pg.font.Font(None, 20)

        t = str("%.2f" % round(sphere.theta, 2))
        txt_surface2 = font.render(t, True, red)
        vel = math.sqrt(sphere.vel_x**2 + sphere.vel_y**2)
        t = str("%.2f" % round(vel, 2))
        txt_surface = font.render(t, True, red)

        dis.blit(txt_surface2, (sphere.pos_x, sphere.pos_y))
        dis.blit(txt_surface, (sphere.pos_x, sphere.pos_y+20))


def display_objects(objects):
    for sphere in objects:
        pg.draw.circle(dis, sphere.colour,
                       (sphere.pos_x, sphere.pos_y), sphere.radius)


def check_collision(obj1, obj2):
    x1 = obj1.pos_x
    y1 = obj1.pos_y
    x2 = obj2.pos_x
    y2 = obj2.pos_y

    dist = math.sqrt((x2-x1)**2+(y2-y1)**2)
    dist = "%.2f" % round(dist, 2)
    if float(dist) <= obj1.radius+obj2.radius:
        return True
    else:
        return False


def collision_response1(obj1, obj2):
    pass


def collision_response(obj1, obj2):

    v_1 = np.array([obj1.vel_x, obj1.vel_y])  # velocity of object 1
    v_2 = np.array([obj2.vel_x, obj2.vel_y])  # velocity of object 2
    m_1 = obj1.mass  # kg ; mass of object 1
    m_2 = obj2.mass  # kg ; mass of object 2

    x_1 = np.array([obj1.pos_x, obj1.pos_y])  # vector of position 1
    x_2 = np.array([obj2.pos_x, obj2.pos_y])  # vector of position 2

    v_1_p = v_1 - 2*m_2/(m_1 + m_2)*((v_1 - v_2)@(x_1 - x_2))/(np.linalg.norm(
        x_2 - x_1)**2)*(x_1 - x_2)  # velocity after colision for object 1
    v_2_p = v_2 - 2*m_1/(m_1 + m_2)*((v_2 - v_1)@(x_2 - x_1))/(np.linalg.norm(
        x_2 - x_1)**2)*(x_2 - x_1)  # velocity after colision for object 2

    obj1.vel_x = v_1_p[0]
    obj1.vel_y = v_1_p[1]

    obj2.vel_x = v_2_p[0]
    obj2.vel_y = v_2_p[1]

    font = pg.font.Font(None, 20)
    txt_surface = font.render("Collision", True, red)
    dis.blit(txt_surface, (0, 40))


def update_physics(objects):
    t = False
    for obj in objects:

        # f = ma
        ay = gravity/obj.mass
        obj.vel_y += ay
        obj.pos_y += obj.vel_y
        obj.pos_x += obj.vel_x
        radius = obj.radius
        if(obj.pos_y >= window_height-radius):
            obj.pos_y = window_height-radius
            obj.vel_y *= -1
            obj.update_vector()

        if(obj.pos_y <= radius):
            obj.pos_y = radius
            obj.vel_y *= -1
            obj.update_vector()

        if(obj.pos_x >= window_width-radius):
            obj.pos_x = window_width-radius
            obj.vel_x *= -1
            obj.update_vector()

        if(obj.pos_x <= radius):
            obj.pos_x = radius
            obj.vel_x *= -1
            obj.update_vector()

        if objects.__len__() > 1:
            for o in objects:
                if not o == obj:
                    if check_collision(obj, o):
                        collision_response(obj, o)
                        '''obj.vel_x = v[0]
                        obj.vel_y = v[1]
                        obj.update_vector()
                        t = True
                        obj1 = obj
                        obj2 = o
                        
    if t == True:
        if obj1.pos_x > obj2.pos_x:
            obj1.pos_x += s
            obj2.pos_x -= s
        else:
            obj1.pos_x -= s
            obj2.pos_x += s

        if obj1.pos_y > obj2.pos_y:
            obj1.pos_y += s
            obj2.pos_y -= s
        else:
            obj1.pos_y -= s
            obj2.pos_y += s

'''


def displayfps(frametime):
    font = pg.font.Font(None, 18)
    if frametime > 0:
        fps_achived = 1/(frametime)
        fps_achived = "%.2f" % round(fps_achived, 2)
        text = str(fps_achived)
    else:
        text = "0"

    txt_surface = font.render(text, True, white)
    dis.blit(txt_surface, (0, 0))


def main_loop():
    objects = []
    '''
    for i in range(num_of_objects):
        a = random.randint(1, 3)
        m = random.randint(1, 8)
        #m = 5
        i = random.randint(-2, 5)
        j = random.randint(-2, 5)

        objects.append(sphere((window_width/a, (m*5)+5), (i, j), m))
    '''
    objects.append(sphere((window_width/2, (5*5)+5), (2, 1), 5))
    objects.append(sphere((window_width/4, (6*5)+5), (3, 0.5), 6))
    frametime = 0
    i = 0

    while(True):
        if i > 5:
            update_physics(objects)
        else:
            i += 1
        # write(objects[0], objects[1])
        curr = time.time()
        event_handler()
        display_objects(objects)
        update_physics(objects)
        display_vectors(objects)
        displayfps(frametime)
        pg.display.update()
        dis.fill(black)
        fpsclk.tick(fps)

        frametime = ((time.time() - curr) + frametime)/2


main_loop()
