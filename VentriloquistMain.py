import pygame
import time
import BlockData
import alsaaudio
import wave
import sys
import time
import threading
import math
import csv
import random
from parameter_list import *

class soundThread(threading.Thread):
    def __init__(self, devindex,fname):
        threading.Thread.__init__(self)
        self.devindex=devindex
        self.fname=fname
    def run(self):
        print "starting sound on thread"
        playsound(self.devindex,self.fname)
        print "sound ended on thread"

def playsound(devindex,fname):
    CHUNK=4096
    f=wave.open(fname, 'rb')
    dname='hw:'+devindex+',0'
    # ci = 'hw:'+devindex
    dev=alsaaudio.PCM(device=dname)
    # mixer=alsaaudio.Mixer(control = 'PCM', device = dname)
    # print mixer.getvolume()
    # mixer.setvolume(100)
    # dev.setchannels(f.getnchannels())
    # dev.setchannels(1)
    dev.setchannels(f.getnchannels())
    dev.setrate(f.getframerate())
    if f.getsampwidth() == 1:
        dev.setformat(alsaaudio.PCM_FORMAT_U8)
    # Otherwise we assume signed data, little endian
    elif f.getsampwidth() == 2:
        dev.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    elif f.getsampwidth() == 3:
        dev.setformat(alsaaudio.PCM_FORMAT_S24_LE)
    elif f.getsampwidth() == 4:
        dev.setformat(alsaaudio.PCM_FORMAT_S32_LE)
    else:
        raise ValueError('Unsupported format')
    dev.setperiodsize(4096)
    data = f.readframes(CHUNK)
    while data:
        # Read data from stdin
        code = dev.write(data)
        data = f.readframes(CHUNK)
    f.close()


def present_flash_beep(cloud, beep, block):

    responded = 0
    P1res = float('nan')
    P2res = float('nan')
    P1_RT = 0
    P2_RT = 0
    countdown = round(random.uniform(1.75,2.75), 2)
    print countdown
    pygame.time.set_timer(pygame.USEREVENT + 1,1000)

    if cloud == 0:

        SCREEN.fill(BLACK)
        pygame.display.flip()
        time.sleep(0.05)
        draw_fixation()
        start = time.time()

    else:
        meanx = CLOUDMEANx[cloud - 1]
        meany = CLOUDMEANy

        for x in range(20):
            x1 = int(round(random.gauss(meanx,CLOUDSPREADx)))
            y1 = int(round(random.gauss(meany,CLOUDSPREADy)))
            random.jumpahead(1)
            pygame.draw.circle(SCREEN,WHITE, [x1,y1], int(round(RADIUS)), 0)

        # sound=soundThread(BEEPKEY[beep],SOUNDFILE)
        # sound.start()
        # playsound(BEEPKEY[beep],SOUNDFILE)
        pygame.display.flip()
        sound=soundThread(BEEPKEY[beep],SOUNDFILE)
        sound.start()
        time.sleep(0.05)
        SCREEN.fill(BLACK)
        draw_fixation()
        start = time.time()
        print 'beep'
        pygame.display.flip()
        print 'cloud'


    while not countdown <= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.display.set_mode(SCREENSIZE)
            if event.type == pygame.USEREVENT+1:
                countdown = countdown - 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    P1_RT = float(time.time() - start)
                    P1res = 1
                if event.key == pygame.K_s:
                    P1_RT = float(time.time() - start)
                    P1res = 2
                if event.key == pygame.K_d:
                    P1_RT = float(time.time() - start)
                    P1res = 3
                if event.key == pygame.K_f:
                    P1_RT = float(time.time() - start)
                    P1res = 4
                if event.key == pygame.K_h:
                    P2_RT = float(time.time() - start)
                    P2res = 1
                if event.key == pygame.K_j:
                    P2_RT = float(time.time() - start)
                    P2res = 2
                if event.key == pygame.K_k:
                    P2_RT = float(time.time() - start)
                    P2res = 3
                if event.key == pygame.K_l:
                    P2_RT = float(time.time() - start)
                    P2res = 4


        # if block == 1 and not math.isnan(P1res):
        #     responded = 1
        # elif block == 2 and not math.isnan(P2res):
        #     responded = 1
        # elif block == 3 and not math.isnan(P1res) and not math.isnan(P2res) :
        #     responded = 1


    pygame.event.clear()
    return (P1res, P1_RT, P2res, P2_RT, countdown)





#select which message should be dislayed based on blocknum
def message_display(blockNum):
    f = pygame.font.SysFont('',FONTSIZE,False, False)
    SCREEN.fill(BLACK)
    if blockNum == 1:
        text = 'PLAYER-1 will play. Press SPACE to continue'
    elif blockNum == 2:
        text = 'PLAYER-2 will play. Press SPACE to continue'
    elif blockNum == 3:
        text = 'PLAYER-1 and PLAYER-2 will play. Press SPACE to continue'
    line = f.render(text,True, WHITE,BLACK)
    textrect = line.get_rect()
    textrect.centerx = SCREEN.get_rect().centerx
    textrect.centery = SCREEN.get_rect().centery
    SCREEN.blit(line, textrect)
    pygame.display.flip()
    buttonpress=0
    while buttonpress == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                buttonpress = 1
                print 'next frame'
        if buttonpress == 1:
            return 1
def message_display_train(blockNum):
    f = pygame.font.SysFont('',FONTSIZE,False, False)
    SCREEN.fill(BLACK)
    if blockNum == 1:
        text = 'PLAYER-1 will play. Press SPACE to continue'
    elif blockNum == 2:
        text = 'PLAYER-2 will play. Press SPACE to continue'
    elif blockNum == 3:
        text = 'Training Session . Press SPACE to continue'
    line = f.render(text,True, WHITE,BLACK)
    textrect = line.get_rect()
    textrect.centerx = SCREEN.get_rect().centerx
    textrect.centery = SCREEN.get_rect().centery
    SCREEN.blit(line, textrect)
    pygame.display.flip()
    buttonpress=0
    while buttonpress == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                buttonpress = 1
                print 'next frame'
        if buttonpress == 1:
            return 1

def setupSpeakers():
    SCREEN.fill(BLACK)
    for x in range(4):
        x1 = int(round(CLOUDMEANx[x - 1]))
        y1 = 800
        pygame.draw.circle(SCREEN,WHITE, [x1,y1], int(round(RADIUS)), 0)
    pygame.display.flip()
    buttonpress=0
    while buttonpress == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                buttonpress = 1
                print 'next frame'
        if buttonpress == 1:
            return 1

#draw fixation cross
def draw_fixation():
    SCREEN.fill(BLACK)
    pygame.draw.line(SCREEN,WHITE, VLINE[0], VLINE[1],VLINE[2])
    pygame.draw.line(SCREEN,WHITE, HLINE[0], HLINE[1],HLINE[2])
    pygame.display.flip()
    print 'fix'
    return 1

def writeData(datalist):
    fpath = DATAPATH + '/Pair' + str(pnum) + '.csv'
    with open(fpath, 'ab') as csvfile:
        fd = csv.writer(csvfile,dialect = 'excel')
        header = ['PairNumber','PlayerOrder','BlockType', 'FlashPos','BeepPos', 'P1_response','P1_RT','P2_response','P2_RT', 'TrialInterval','CondLabel']
        fd.writerow(header)
        for l in datalist:
            if l[3] == 1:
                if l[4] == 1:
                    l.append('congruent')
                elif l[4] == 2:
                    l.append('incongruent+1')
                elif l[4] == 3:
                    l.append('incongruent+2')
                elif l[4] == 4:
                    l.append('incongruent+3')
            elif l[3] == 2:
                if l[4] == 2:
                    l.append('congruent')
                elif l[4] == 1:
                    l.append('incongruent-1')
                elif l[4] == 4:
                    l.append('incongruent+2')
                elif l[4] == 3:
                    l.append('incongruent+1')
            elif l[3] == 3:
                if l[4] == 3:
                    l.append('congruent')
                elif l[4] == 4:
                    l.append('incongruent+1')
                elif l[4] == 1:
                    l.append('incongruent-2')
                elif l[4] == 2:
                    l.append('incongruent-1')
            elif l[3] == 4:
                if l[4] == 4:
                    l.append('congruent')
                elif l[4] == 3:
                    l.append('incongruent-1')
                elif l[4] == 2:
                    l.append('incongruent-2')
                elif l[4] == 1:
                    l.append('incongruent-3')
            elif l[3] == 0:
                if l[4] == 0:
                    l.append('catch trial')
            fd.writerow(l)

def experiment_train():
    pygame.mouse.set_visible(False)
    done = False
    blockSeq=[3]
    while not done:
        for block in blockSeq:
            setupSpeakers()
            code = message_display_train(block)
            if code == 1:
                nCatch = 3 #Number of catch trials
                for flash,beep in BlockData.getTrainBlockTrials(NUMTRIAL,nCatch):
                    print flash,beep
                    draw_fixation()
                    # TRIALINTERVAL = round(random.uniform(1.75,2.75), 2)
                    # print TRIALINTERVAL
                    pygame.event.clear(pygame.KEYDOWN)
                    p1res, p1rt, p2res, p2rt, TRIALINTERVAL = present_flash_beep(flash,beep,block)
                    print p1res,format(p1rt, '.5f'),p2res,format(p2rt, '.5f')
                    # time.sleep(TRIALINTERVAL) #randomise trial interval

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    pygame.display.set_mode(SCREENSIZE)
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.type == pygame.K_ESCAPE:
                    done = True

        done = True


######                 main experiment loop            ##########
def experiment():
    pygame.mouse.set_visible(False)
    done = False
    dataFile = []
    if startCue == 1:
        blockSeq=[1,3,2,1,3,2]
    elif startCue == 2:
        blockSeq=[2,1,3,2,1,3]
    elif startCue == 3:
        blockSeq=[3,2,1,3,2,1]
#todo: degree to pixel conversion stimulus position and spread of stimulus, add null trials 5%
#save trialinterval, add training block, stimulus duration 50 ms, task instructions, distance from screen 50 cm,
#
    while not done:
        for block in blockSeq:
            setupSpeakers()
            code = message_display(block)
            if code == 1:
                nCatch = random.randint(5,9) #Number of catch trials

                for flash,beep in BlockData.getBlockTrials(NUMTRIAL,nCatch):
                    draw_fixation()
                    print flash,beep
                    # TRIALINTERVAL = round(random.uniform(1.75,2.75), 2)
                    # print TRIALINTERVAL
                    pygame.event.clear(pygame.KEYDOWN)
                    p1res, p1rt, p2res, p2rt, TRIALINTERVAL = present_flash_beep(flash,beep,block)
                    dataFile.append([pnum,POSITION,block,flash,beep,p1res,p1rt,p2res,p2rt,TRIALINTERVAL])
                    print p1res,format(p1rt, '.5f'),p2res,format(p2rt, '.5f')
                    # time.sleep(TRIALINTERVAL) #randomise trial interval


            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    pygame.display.set_mode(SCREENSIZE)
                if event.type == pygame.QUIT:
                    done = True
                    return dataFile
                if event.type == pygame.KEYDOWN and event.type == pygame.K_ESCAPE:
                    done = True
                    return dataFile
        done = True

        return dataFile


pygame.init()
pnum = 999
POSITION = 'P1P2'
startCue = 1
clock = pygame.time.Clock()
experiment_train()
data = experiment()
print 'writing in data file'
writeData(data)
pygame.quit()
quit()
