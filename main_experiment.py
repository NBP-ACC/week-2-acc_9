import pygame
import time
import sys
import csv
import random
from  parameter_list import *
clock = pygame.time.Clock
def waitFor(waitTime):
    waitCount = 0
    while waitCount < waitTime:
        dt = clock.tick(60) # 60 is your FPS here
        waitCount += dt
        pygame.event.pump() # Tells pygame to handle it's event, instead of pygame.event.get()

def draw_stim(trialType):
    res = 0
    RT = 0
    countdown = 3
    # round(random.uniform(1.75,2.75), 2)
    pygame.time.set_timer(pygame.USEREVENT + 1,1000)
    if trialType == 0:
        SCREEN.fill(BG_COLOR)
        pygame.draw.circle(SCREEN,NOGO_COLOR, [Cx, Cy], int(round(RADIUS)), 0)
        pygame.display.flip()
        time.sleep(0.1)
        start = time.time()
        SCREEN.fill(BG_COLOR)
        pygame.display.flip()

    else:
        SCREEN.fill(BG_COLOR)
        pygame.draw.circle(SCREEN,GO_COLOR, [Cx, Cy], int(round(RADIUS)), 0)
        pygame.display.flip()
        time.sleep(0.1)
        start = time.time()
        SCREEN.fill(BG_COLOR)
        pygame.display.flip()

    while not countdown <= 0 or res != 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.display.set_mode(SCREENSIZE)
            if event.type == pygame.USEREVENT+1:
                countdown = countdown - 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    RT = float(time.time() - start)
                    res = 1
        pygame.event.clear()
        return (RT, res)


def message_display(text):
    f = pygame.font.SysFont('',FONTSIZE,False, False)
    SCREEN.fill(BG_COLOR)

    line = f.render(text,True, WHITE,BG_COLOR)
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                buttonpress = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.display.set_mode(SCREENSIZE)

    if buttonpress == 1:
        return 1



#draw fixation cross
def draw_fixation():
    SCREEN.fill(BG_COLOR)
    pygame.draw.line(SCREEN,WHITE, VLINE[0], VLINE[1],VLINE[2])
    pygame.draw.line(SCREEN,WHITE, HLINE[0], HLINE[1],HLINE[2])
    pygame.display.flip()
    return 1

def writeData(datalist, subID):
    fpath = DATAPATH + '/Sub' + str(subID) + '.csv'
    with open(fpath, 'w') as csvfile:
        fd = csv.writer(csvfile,dialect = 'excel')
        header = ['SubjectID','StimulusType','response','RT']
        fd.writerow(header)
        for l in datalist:
            fd.writerow(l)

######                 main experiment loop            ##########
def experiment(subID):
    dataFile = []
    TRIALINTERVAL = 0.5 #round(random.uniform(1.75,2.75), 2)
    pygame.mouse.set_visible(False)
    stimuli_list = [1]*(NUMTRIAL-PCT_NOGO)
    nogo_trials = [0]*PCT_NOGO
    stimuli_list.extend(nogo_trials)
    random.shuffle(stimuli_list)
    done = False
    while not done:
        text = 'Only press SPACE when GREEN circle is shown. Press c to continue'
        code = message_display(text)
        if code == 1:
            for stim in stimuli_list:
                draw_fixation()
                time.sleep(TRIALINTERVAL) #randomise trial interval
                pygame.event.clear(pygame.KEYDOWN)
                RT, res = draw_stim(stim)
                dataFile.append([subID, stim, res, RT])
                time.sleep(TRIALINTERVAL)
                # time.sleep(TRIALINTERVAL) #randomise trial interval
            done = True
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode(SCREENSIZE)
                    done = True
                    return dataFile
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # sys.exit()
                    return dataFile


    print(dataFile)

    return dataFile

# if __name__ == "__main__":
    # pygame.init()
subID = 666
dataFile = experiment(subID)
print(dataFile)
print('writing in data file')
writeData(dataFile, subID)
# pygame.quit()
quit()
