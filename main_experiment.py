import pygame
import time
import sys
import csv
import random
from  parameter_list import *
# clock = pygame.time.Clock
# def waitFor(waitTime):
#     waitCount = 0
#     while waitCount < waitTime:
#         dt = clock.tick(60) # 60 is your FPS here
#         waitCount += dt
#         pygame.event.pump() # Tells pygame to handle it's event, instead of pygame.event.get()


def draw_stim(trialType):
    """
    Function to draw the stimulus
    green circle for trialType == 1
    red circle for trialType == 0
    The subject response is recorded by getting pygame.event.
    The function counts down 3 seconds for the subject to respond from the
    beginning of the stimulus presentation. If there is no response,
    the function returns to the main loop. If the subject responds, the Function
    returns the response and the time from stimulus presentation to time at
    button press

    parameters: trialType
    returns: response and response time
    """
    res = 0
    RT = 0
    countdown = 3
    # set pygame timer to countdown
    if trialType == 0:
        SCREEN.fill(BG_COLOR)
        pygame.draw.circle(SCREEN,NOGO_COLOR, [Cx, Cy], int(round(RADIUS)), 0)
        pygame.display.flip()
        #the stimulus is shown for 0.1s
        time.sleep(0.15)
        #start time from stimulus presentation
        start = time.time()
        SCREEN.fill(BG_COLOR)
        pygame.display.flip()

    else:
        SCREEN.fill(BG_COLOR)
        pygame.draw.circle(SCREEN,GO_COLOR, [Cx, Cy], int(round(RADIUS)), 0)
        pygame.display.flip()
        time.sleep(0.15)
        start = time.time()
        SCREEN.fill(BG_COLOR)
        pygame.display.flip()

    #start countdown to end of 3s or until a button is pressed
    pygame.time.set_timer(pygame.USEREVENT,1000)
    while not countdown <= 0 or res != 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                countdown -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    RT = float(time.time() - start)
                    res = 1
        #clear the event buffer so multiple button presses are ignored
        pygame.event.clear()

        return (RT, res)


def message_display(text):
    """
    Function to display a given message in the middle of the SCREEN
    handles the button press of the user to go to the main loop

    parameters: text to be shown
    Returns: 1 when button is pressed
    """
    f = pygame.font.SysFont('',FONTSIZE,False, False)
    SCREEN.fill(BG_COLOR)
    line = f.render(text,True, WHITE,BG_COLOR)
    textrect = line.get_rect()
    textrect.centerx = SCREEN.get_rect().centerx
    textrect.centery = SCREEN.get_rect().centery
    SCREEN.blit(line, textrect)
    pygame.display.flip()
    #wait for button press from the user
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
    """
    Function to draw fixation cross based on the parameters listed in
    parameter_list
    """
    SCREEN.fill(BG_COLOR)
    pygame.draw.line(SCREEN,WHITE, VLINE[0], VLINE[1],VLINE[2])
    pygame.draw.line(SCREEN,WHITE, HLINE[0], HLINE[1],HLINE[2])
    pygame.display.flip()
    return 1

def writeData(datalist, subID):
    """
    Function to write the list of responses to a csv dataFile
    """

    fpath = DATAPATH + '/Sub' + str(subID) + '.csv'
    with open(fpath, 'w') as csvfile:
        fd = csv.writer(csvfile,dialect = 'excel')
        header = ['SubjectID','StimulusType','response','RT']
        fd.writerow(header)
        for l in datalist:
            fd.writerow(l)

######                 main experiment loop            ##########
def experiment(subID):
    #List where all the repsonses are stores
    dataFile = []
    #round(random.uniform(1.75,2.75), 2)
    pygame.mouse.set_visible(False)
    stimuli_list = [1]*int(NUMTRIAL- NUMTRIAL*PCT_NOGO)
    nogo_trials = [0]*int(NUMTRIAL*PCT_NOGO)
    stimuli_list.extend(nogo_trials)
    random.shuffle(stimuli_list)
    #Flag to check when the experiment loop ends
    done = False
    while not done:
        text = 'Only press SPACE when GREEN circle is shown. Press c to continue'
        code = message_display(text)
        if code == 1:
            for stim in stimuli_list:
                draw_fixation()
                time.sleep(0.5)
                #clear event buffer so they are not misunderstood as responses
                pygame.event.clear(pygame.KEYDOWN)
                #show stimulus and get RT and response
                RT, res = draw_stim(stim)
                #append the data to the datafile
                dataFile.append([subID, stim, res, RT])
                time.sleep(TRIALINTERVAL)

            # when all stimulus is shown, experiment is done
            done = True
            # check for events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode(SCREENSIZE)

    return dataFile

if __name__ == "__main__":
    #Fill this before start of the experiment
    subID = 666
    dataFile = experiment(subID)
    print('writing in data file')
    writeData(dataFile, subID)
    pygame.quit()
    quit()
