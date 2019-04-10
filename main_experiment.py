import pygame
import sys
import csv
import random
from parameter_list import *
clock = pygame.time.Clock()

def draw_stimulus(trialType):
    """
    Function to draw the stimulus
    green circle for trialType == 1
    red circle for trialType == 0
    parameters: trialType
    """
    if trialType:
        SCREEN.fill(BG_COLOR)
        pygame.draw.circle(SCREEN,GO_COLOR, [Cx, Cy], RADIUS, 0)
    else:
        SCREEN.fill(BG_COLOR)
        pygame.draw.circle(SCREEN,NOGO_COLOR, [Cx, Cy], RADIUS, 0)

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

def fill_background():
    SCREEN.fill(BG_COLOR)

#write the data into csv file
def writeData(datalist, subID):
    """
    Function to write the list of responses to a csv dataFile
    """
    
    ### TODO
    # create a csvfile for each subject and name it: Sub[subID].csv
    # Since datalist is created only for one subject no need to check for different subIDs
    save_path = DATAPATH + "Sub{}.csv".format(subID)
    with open (save_path, "w") as csvfile:

        # add a header ('SubjectID','StimulusType','response','RT') to the csvfile
        writer = csv.writer(csvfile)
        writer.writerow(["SubjectID", "StimulusType", "response", "RT"])

        # and write each entry of datalist to a single row
        for elem in datalist:
            writer.writerow(elem)
    ### ENDTODO

    
######                 main experiment loop            ##########
def experiment(subID):
    #List where all the repsonses are stored
    dataFile = []
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
                response = 0 # should be assigned 1 if K_SPACE is pressed
                RT = 0 # should be assigned value based on elapsed time from when stimulus is shown
                countdown = 2
                draw_fixation()
                pygame.display.flip()
                pygame.time.wait(500) # Display fixation cross for 500 milliseconds
                #clear event buffer so they are not misunderstood as responses
                pygame.event.clear(pygame.KEYDOWN)
                #show stimulus and get RT and response
                draw_stimulus(stim)
                pygame.display.flip()
                # get time at which stimulus is shown
                start = pygame.time.get_ticks()
                # check for events
                countdown_check = pygame.USEREVENT+1 #custom event to track counter
                pygame.time.set_timer(countdown_check, 1000) # timer that tracks counter every 1000ms
                while countdown > 0 and response == 0:
                    clock.tick(FPS)
                    for event in pygame.event.get():
                        # if the pygame exit button is pressed
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        # if 1000ms have passed do a countdown check
                        if event.type == countdown_check:
                            countdown -= 1
                        # if subject has pressed a button
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                # Time elapsed from stimulus to button press
                                ### TODO
                                RT = pygame.time.get_ticks() - start
                                response = 1
                                ### TODOEND

                fill_background()# clear the screen
                pygame.display.flip()
                pygame.time.wait(TRIALINTERVAL)
                dataFile.append([subID, stim, response, RT]) #append the data to the datafile

        done = True

    return dataFile

if __name__ == "__main__":
    #Fill this before start of the experiment
    subID = 1 # TODO ID of the subject
    dataFile = experiment(subID)
    print('*'*30)
    print('Writing in data file: Sub{}.csv'.format(subID))
    print('*'*30)
    writeData(dataFile, subID)
    pygame.quit()
    quit()
