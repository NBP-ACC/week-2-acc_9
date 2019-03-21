#create randomised trials for jointBI experiment
import random
import itertools

def getBlockTrials(numtrial,ncatch):
    trialCond=[]
    for t in range(numtrial):
        for vflash in range(1,5):
            for sbeep in range(1,5):
                t=(vflash,sbeep)
                trialCond.append(t)

    catch = [(0,0)]*ncatch
    trialCond.extend(catch)
    random.shuffle(trialCond)
    return trialCond

def getTrainBlockTrials(numtrial,ncatch):
    trialCond=[]
    for t in range(1):
        for vflash in range(1,5):
            for sbeep in range(1,5):
                t=(vflash,sbeep)
                trialCond.append(t)

    catch = [(0,0)]*ncatch
    trialCond.extend(catch)
    #random.shuffle(trialCond)
    return trialCond


def getPilotBlock():
    s1 = [1]*5 #practice trials
    s2 = [2]*5
    s1.extend(s2)
    return s1

def getBlockType():
    block = [0]*7 + [1]*7
    random.shuffle(block)
    return block
