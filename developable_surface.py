#!/bin/env python3


import pygame, sys
from pygame.locals import *
from math import cos as cos
from math import sin as sin
from math import pi as pi
from math import sqrt as sqrt
import functools

# set up pygame
pygame.init()

# set up the window
win_size_x = 700
win_size_y = 550
windowSurface = pygame.display.set_mode((win_size_x, win_size_y), 0, 32)
pygame.display.set_caption('Hello world!')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG = (255,235,175)

# set up fonts
basicFont = pygame.font.SysFont(None, 48)

# set up the text
text = basicFont.render('Hello world!', True, WHITE, BLUE)
textRect = text.get_rect()
textRect.centerx = windowSurface.get_rect().centerx
textRect.centery = windowSurface.get_rect().centery

# draw the white background onto the surface
windowSurface.fill((255,235,175))

# draw a green polygon onto the surface
#pygame.draw.polygon(windowSurface, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

# draw some blue lines onto the surface
#pygame.draw.line(windowSurface, BLUE, (60, 60), (120, 60), 4)
#pygame.draw.line(windowSurface, BLUE, (120, 60), (60, 120))
#pygame.draw.line(windowSurface, BLUE, (60, 120), (120, 120), 4)

# draw a blue circle onto the surface
#pygame.draw.circle(windowSurface, BLUE, (300, 50), 20, 0)

# draw a red ellipse onto the surface
#pygame.draw.ellipse(windowSurface, RED, (300, 250, 40, 80), 1)

# draw the text's background rectangle onto the surface
#pygame.draw.rect(windowSurface, RED, (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))

# get a pixel array of the surface
pixArray = pygame.PixelArray(windowSurface)
pixArray[480][380] = BLACK
del pixArray


class Vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        return Vector(self.x*other, self.y*other, self.z*other)

    def __truediv__(self, other):
        return Vector(self.x/other, self.y/other, self.z/other)

    def __str__(self):
        return "(%f %f %f)" % (self.x, self.y, self.z)

    def cross(self, other):
        nx = self.y*other.z - self.z*other.y
        ny = self.z*other.x - self.x*other.z
        nz = self.x*other.y - self.y*other.x
        return Vector(nx,ny,nz)

    def length(self):
        return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

class Tri:
    def __init__(self, p0, p1, p2, col = BLUE):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.col = col

def my_cmp(tri_a, tri_b):
    if tri_a.p0.z+tri_a.p1.z+tri_a.p2.z > tri_b.p0.z+tri_b.p1.z+tri_b.p2.z:
        return -1
    return 1

aaa = 0.6

def to_2D(v):
    a = aaa
    y = cos(a)*v.y - sin(a)*v.z
    x = v.x
    z = cos(a)*v.z + sin(a)*v.y
    p = (z+40.0)/40.0
    x = x/p
    y = y/p
    return Vector(x, y, z)

def scale(v):
    s = 17.0
    return Vector(win_size_x/2+v.x*s, win_size_y/2+v.y*s, v.z*s)

def light1(tri):
    n = (tri.p1-tri.p0).cross(tri.p2-tri.p0)
    ln = n.length()
    n = n/ln
    sun = 256*n.z
    if sun < 0:
        sun = -sun
    if sun > 255:
        sun = 255
    return sun

def light2(tri):
    light = 355-tri.p0.length()*30
    if light > 255:
        light = 255
    if light < 0:
        light = 0
    return light

def light3(tri):
    light = light1(tri) + light2(tri)
    return light/2

def draw_tri(tri):
    n = (tri.p1-tri.p0).cross(tri.p2-tri.p0)
    ln = n.length()
    n = n/ln
    sun = light3(tri)
    n = Vector(0,0,0) - n + tri.p0
    p0 = scale(tri.p0)
    p1 = scale(tri.p1)
    p2 = scale(tri.p2)
    n = scale(n)
    pygame.draw.polygon(windowSurface, (sun,sun,sun), ((p0.x, p0.y), (p1.x, p1.y), (p2.x, p2.y)))
    #pygame.draw.line(windowSurface, (255,0,0), (p0.x, p0.y), (n.x, n.y))
    #pygame.draw.line(windowSurface, (0,0,0), (p0.x, p0.y), (p1.x, p1.y))
    #pygame.draw.line(windowSurface, (0,0,0), (p1.x, p1.y), (p2.x, p2.y))
    #pygame.draw.line(windowSurface, (0,0,0), (p2.x, p2.y), (p0.x, p0.y))

def torus():
    r0 = 3.0
    r1 = 12.0
    reso = 50
    tris = []
    for ti0 in range(0,reso):
        for ti1 in range(0,reso):
            t0 = ti0*2.0*pi/reso
            t1 = ti1*2.0*pi/reso
            t0p = (ti0+1)*2.0*pi/reso
            t1p = (ti1+1)*2.0*pi/reso
            x = 3.0*cos(t0)*sin(t1) + r1*sin(t1)
            y = 3.0*sin(t0)
            z = 3.0*cos(t0)*cos(t1) + r1*cos(t1)
            xp0 = 3.0*cos(t0p)*sin(t1) + r1*sin(t1)
            yp0 = 3.0*sin(t0p)
            zp0 = 3.0*cos(t0p)*cos(t1) + r1*cos(t1)
            xp1 = 3.0*cos(t0)*sin(t1p) + r1*sin(t1p)
            yp1 = 3.0*sin(t0)
            zp1 = 3.0*cos(t0)*cos(t1p) + r1*cos(t1p)
            xp01 = 3.0*cos(t0p)*sin(t1p) + r1*sin(t1p)
            yp01 = 3.0*sin(t0p)
            zp01 = 3.0*cos(t0p)*cos(t1p) + r1*cos(t1p)
            tris.append(Tri(Vector(x, y, z), Vector(xp0, yp0, zp0), Vector(xp1, yp1, zp1)))
            tris.append(Tri(Vector(xp0, yp0, zp0), Vector(xp01, yp01, zp01), Vector(xp1, yp1, zp1)))
    return tris

def f(t, n):
    v0 = t*pi
    v1 = t*5 + n*2*pi
    x = 8*sin(v0)*cos(v1)
    y = 8*cos(v0)
    z = 8*sin(v0)*sin(v1)
    return Vector(x, y, z)

def g(t, n):
    p = f(t, n)
    x = p.x*0.6
    y = p.y*0.9
    z = p.z*0.6
    return Vector(x, y, z)

#0--------------1
#|              |
#3--------------2
def append_quad(tris, p0, p1, p2, p3):
    d01 = (p1-p0).length()
    d12 = (p2-p1).length()
    subdiv = int(d01/d12)
    for i in range(0,subdiv):
        p01  = p0*(i  )/subdiv + p1*(subdiv-i  )/subdiv
        p32  = p3*(i  )/subdiv + p2*(subdiv-i  )/subdiv
        p01p = p0*(i+1)/subdiv + p1*(subdiv-i-1)/subdiv
        p32p = p3*(i+1)/subdiv + p2*(subdiv-i-1)/subdiv
        tris.append(Tri(p01, p01p, p32p))
        tris.append(Tri(p01, p32p, p32))
    return

def lamp():
    tris = []
    reso = 60
    pieces = 5
    for n in range(0,pieces):
        for ti in range(0,reso):
            t = ti*1.0/reso
            tp =(ti+1)*1.0/reso
            pf = f(t, n*1/pieces)
            pg = g(t, n*1/pieces)
            pfp = f(tp, n*1/pieces)
            pgp = g(tp, n*1/pieces)
            append_quad(tris, pf, pg, pgp, pfp)
    return tris

def square_nut():
    r0 = 3.0
    r1 = 12.0
    reso = 100
    tris = []
    twists = 4
    for ti0 in range(0,4):
        for ti1 in range(0,reso*4):
            t0 = (ti0)*2.0*pi/4
            t1 = ti1*2.0*pi/reso
            t0p = (ti0+1)*2.0*pi/4
            t1p = (ti1+1)*2.0*pi/reso
            x = 3.0*cos(t0+t1/4*twists)*sin(t1) + r1*sin(t1)
            y = 3.0*sin(t0+t1/4*twists)
            z = 3.0*cos(t0+t1/4*twists)*cos(t1) + r1*cos(t1)
            xp0 = 3.0*cos(t0p+t1/4*twists)*sin(t1) + r1*sin(t1)
            yp0 = 3.0*sin(t0p+t1/4*twists)
            zp0 = 3.0*cos(t0p+t1/4*twists)*cos(t1) + r1*cos(t1)
            xp1 = 3.0*cos(t0+t1p/4*twists)*sin(t1p) + r1*sin(t1p)
            yp1 = 3.0*sin(t0+t1p/4*twists)
            zp1 = 3.0*cos(t0+t1p/4*twists)*cos(t1p) + r1*cos(t1p)
            xp01 = 3.0*cos(t0p+t1p/4*twists)*sin(t1p) + r1*sin(t1p)
            yp01 = 3.0*sin(t0p+t1p/4*twists)
            zp01 = 3.0*cos(t0p+t1p/4*twists)*cos(t1p) + r1*cos(t1p)
            tris.append(Tri(Vector(x, y, z), Vector(xp0, yp0, zp0), Vector(xp1, yp1, zp1)))
            tris.append(Tri(Vector(xp0, yp0, zp0), Vector(xp01, yp01, zp01), Vector(xp1, yp1, zp1)))
    return tris

scene = lamp()
#scene = torus()

def render():
    scene_2d = []
    for tri in scene:
        p0 = to_2D(tri.p0)
        p1 = to_2D(tri.p1)
        p2 = to_2D(tri.p2)
        scene_2d.append(Tri(p0, p1, p2))
    for tri in sorted(scene_2d, key=functools.cmp_to_key(my_cmp)):
        draw_tri(tri)
    pygame.display.update()
    pygame.display.flip()


# draw the text onto the surface
#windowSurface.blit(text, textRect)

# run the game loop
pygame.display.update()
running = 1
down_point = None
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = 0
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("You pressed the left mouse button at (%d, %d)" % event.pos)
            down_point = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            print("You released the left mouse button at (%d, %d)" % event.pos)
            down_point = None
        elif event.type == pygame.MOUSEMOTION:
            if down_point != None:
                print("mouse at (%d, %d)" % (event.pos[0], event.pos[1]))
    
                windowSurface.fill(BG)
                aaa = aaa + (event.pos[1] - down_point[1])*0.01
                down_point = event.pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("LEFT")
            if event.key == pygame.K_RIGHT:
                pass
    render()

pygame.quit()
sys.exit()

