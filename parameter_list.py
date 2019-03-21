import os
import sys
import pygame
from math import atan2,degrees


SCREENSIZE = (800,600)
# SCREEN = pygame.display.set_mode(SCREENSIZE)
SCREEN = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
WIDTH, HEIGHT = SCREEN.get_size()

monitorHeight = 33.5 # in cm
monitorwidth = 60 # in cm
distance = 50
ymonitorRes = 1080
xmonitorRes = 1920
ydegree_per_px = degrees(atan2(.5*monitorHeight, distance)) / (.5*ymonitorRes)
xdegree_per_px = degrees(atan2(.5*monitorwidth, distance)) / (.5*xmonitorRes)
# vstdDev = 2.5 # in degrees
# hstdDev = 14

# CLOUDMEANx = [240,720,1200,1680]
# [-23.222817399055142, -7.74093913301838, 7.74093913301838, 23.222817399055142]

CLOUDMEANx = [960-10/xdegree_per_px,960-3.3/xdegree_per_px,960+3.3/xdegree_per_px,960+10/xdegree_per_px]

CLOUDMEANy = 540
CLOUDSPREADx = 2/xdegree_per_px
CLOUDSPREADy = 2.5/ydegree_per_px
RADIUS = round(0.43/ydegree_per_px)

(Cx,Cy) = (WIDTH/2, HEIGHT/2)
crosslen = 1.6/ydegree_per_px
VLINE = [(Cx,Cy - crosslen), (Cx, Cy + crosslen), 4]
HLINE = [(Cx - crosslen,Cy), (Cx + crosslen, Cy), 4]

WHITE = (255,255,255)
BLACK = (0,0,0)
BEEPKEY = {0: 'z', 1:'one',2:'two',3:'six',4:'seven'}

DATAPATH = os.getcwd() + '/Data'
FONTSIZE = 60
SOUNDFILE='beep1.wav'

NUMTRIAL = 11
TRIALINTERVAL = 1
FPS = 60

# cat /dev/urandom | aplay -D hw:one,0 -f S16_LE -c2
