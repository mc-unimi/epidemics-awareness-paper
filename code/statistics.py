#Copyright (C) 2019 Samira Maghool and Marco Cremonini
#
#This file is part of the multiagent epidemic simulator developed by the research project described in the paper titled "A multicomponent model of awareness for different categories of network epidemics", by Samira Maghool, Nahid Maleki-Jirsaraei, and Marco Cremonini.
#
#    The multiagent epidemic simulator is free software: you can  
#    redistribute it and/or modify it under the terms of the GNU General
#    Public License as published by the Free Software Foundation, either
#    version 3 of the License, or (at your option) any later version.
#
#    The multiagent epidemic simulator is distributed in the hope that it 
#    will be useful, but WITHOUT ANY WARRANTY; without even the implied 
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
#    See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with the multiagent epidemic simulator.  
#    If not, see <https://www.gnu.org/licenses/>.

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
        
    
    
    
