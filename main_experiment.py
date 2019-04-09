import pygame
import time
import sys
import csv
import random
from  parameter_list import *


def draw_stim(trialType):
    """
    Function to draw the stimulus
    green circle for trialType == 1
    red circle for trialType == 0
    The subject response is recorded by getting pygame.event which keeps track of button presses
    The function counts down 2 seconds for the subject to respond from the
    beginning of the stimulus presentation. If there is no response,
    the function returns to the main loop. If the subject responds, the Function
    returns the response and the time from stimulus presentation to time at
    button press

    parameters: trialType
    returns: response and response_time
    """
    response = 0 # should be assigned 1 if K_SPACE is pressed
    RT = 0 # should be assigned value based on elapsed time from when stimulus is shown
    countdown = 2
    if trialType == 0:
        SCREEN.fill(BG_COLOR)
        pygame.draw.circle(SCREEN,NOGO_COLOR, [Cx, Cy], int(round(RADIUS)), 0)
        # flip the screen to display the drawn stimulus
        pygame.display.flip()
        start = time.time() #start timer when the stimulus is shown


    else:
        SCREEN.fill(BG_COLOR)
        pygame.draw.circle(SCREEN,GO_COLOR, [Cx, Cy], int(round(RADIUS)), 0)
        # flip the screen to display the drawn stimulus
        pygame.display.flip()
        start = time.time() #start timer when the stimulus is shown

    #start countdown to end of 2s or until a button is pressed
    # pygame.USEREVENT is a custom event handler.
    #In the code below it updates itself every 1000ms
    pygame.time.set_timer(pygame.USEREVENT,1000)
    while not countdown <= 0 or res != 1:
        for event in pygame.event.get():
            # if the pygame exit button is pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 1000ms have passed and USEREVENT has occurred
            if event.type == pygame.USEREVENT:
                countdown -= 1 # reduce the countdown
            # Subject has pressed a button
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # TODO
                    # What should happen when the space key is pressed?
                    
        #clear the event buffer so multiple button presses are ignored
        pygame.event.clear()
        return (RT, response)


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

    # create a csvfile for each subject and name it: Sub[subID].csv
    # add a header ('SubjectID','StimulusType','response','RT') to the csvfile
    # and write each entry of datalist to a single row
    # TODO


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

# Give information about the subject and start experiment
if __name__ == "__main__":
    #Fill this before start of the experiment
    subID = # ID of the subject
    dataFile = experiment(subID)
    print('writing in data file')
    writeData(dataFile, subID)
    pygame.quit()
    quit()
