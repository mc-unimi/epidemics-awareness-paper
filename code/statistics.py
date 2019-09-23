'''
Module for basic averaging of system states across multiple trials.
Used in plotting.

@author:samiramaghool@gmail.com>
'''
import csv
class TrialSIRSState(object):

    def __init__(self, trial_id, times, systemSIRSStates,
                 uniqueSIRSStates, stateCounterForSIRSStateX):
        self.trial_id = trial_id
        self.times = times
        self.systemSIRSStates = systemSIRSStates
        self.uniqueSIRSStates = uniqueSIRSStates
        self.stateCounterForSIRSStateX = stateCounterForSIRSStateX
    

class TrialSIRSStats(object):

    def __init__(self, allTrialSIRSStatesTuples):
        self.SIRSStatesTuples = allTrialSIRSStatesTuples
        self.trialSIRSStates = []
        self.trialAverage = None
        
        self.calculateAllSIRSStateCounts()
        self.calculateAverageSIRSStateCount()
        
    def calculateAllSIRSStateCounts(self):
        
        for trial in range(len(self.SIRSStatesTuples)):
            times = [t for (t,s) in self.SIRSStatesTuples[trial]]
            systemSIRSStates = [s for (t,s) in self.SIRSStatesTuples[trial]]
            uniqueSIRSStates = reduce(lambda x, y: set(y).union(set(x)), systemSIRSStates)
            SIRSStateCounterDict = {}
            for x in uniqueSIRSStates:
                SIRSStateXCounts = [SIRSState.count(x) for SIRSState in systemSIRSStates]
                SIRSStateCounterDict[x] = SIRSStateXCounts
            '''store info about this trial'''
            self.trialSIRSStates.append(TrialSIRSState(trial, times, systemSIRSStates,
                                                       uniqueSIRSStates, SIRSStateCounterDict))
            '''save the number of infected agent into csv file'''
            with open("trial_values_infected",'a') as csvfile:     
                       writer =csv.writer(csvfile)
                       writer.writerow(SIRSStateCounterDict[1])
                     
                                    
    def calculateAverageSIRSStateCount(self):
     
        times = self.trialSIRSStates[0].times
        uniqueSIRSStates = self.trialSIRSStates[0].uniqueSIRSStates
        for trial in self.trialSIRSStates:
            try:
                uniqueSIRSStates  = set(trial.uniqueSIRSStates).union(set(uniqueSIRSStates))
            except:
                pass
              
        SIRSStateCounterDict = {}
        dummy = [0 for x in trial.systemSIRSStates]
        for x in uniqueSIRSStates:
            array = [trial.stateCounterForSIRSStateX.get(x, dummy) for trial in self.trialSIRSStates]
            averages = [sum(value)/len(self.trialSIRSStates) for value in zip(*array)]
            SIRSStateCounterDict[x] = averages
            
        self.trialAverage = TrialSIRSState(-1, times, None, uniqueSIRSStates, SIRSStateCounterDict)
        
    
    
    
