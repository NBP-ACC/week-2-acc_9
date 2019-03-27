import os
import sys
import pygame
from math import atan2,degrees

pygame.init()
SCREENSIZE = (800,600)
infoObject = pygame.display.Info()
SCREEN = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
# SCREEN = pygame.display.set_mode(SCREENSIZE)
# SCREEN = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
WIDTH, HEIGHT = SCREEN.get_size()

xmonitorRes, ymonitorRes = (infoObject.current_w, infoObject.current_h)
distance = 30
ydegree_per_px = degrees(atan2(.5*HEIGHT, distance)) / (.5*ymonitorRes)
xdegree_per_px = degrees(atan2(.5*WIDTH, distance)) / (.5*xmonitorRes)

RADIUS = round(5/ydegree_per_px)

(Cx,Cy) = (int(round(WIDTH/2)), int(round(HEIGHT/2)))
crosslen = 1.6/ydegree_per_px
VLINE = [(Cx,Cy - crosslen), (Cx, Cy + crosslen), 4]
HLINE = [(Cx - crosslen,Cy), (Cx + crosslen, Cy), 4]

#Default colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BG_COLOR = (123,123,123)
NOGO_COLOR = (255, 0 , 0)
GO_COLOR = (0, 255, 0)

DATAPATH = os.getcwd() + '/Data'
if not os.path.exists(DATAPATH):
    os.makedirs(DATAPATH)
FONTSIZE = 60

NUMTRIAL = 10
PCT_NOGO = 5
TRIALINTERVAL = 1
FPS = 60
