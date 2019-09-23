'''
Module for the generation of plots of system states.

@author: samiramaghool@gmail.com>''' 

import utils
import statistics
import os
import matplotlib as plt
from matplotlib import pyplot
import NetworkSimulation
import networkx as nx
import csv
#from utilities.Utils import createIfNotExist, retrieveAndPopulate


class PlotCreator(object):
    '''Constructor - set examples=1 to get plot lines of first trial as well as the average'''
    def __init__(self, directory, name, title, statesToMonitor,
                 colours, labels, examples=0):
        self.directory = os.path.abspath(directory)
        self.name = name
        self.statesToMonitor = statesToMonitor
        self.colours = colours
        self.labels = labels
        self.examples = examples
        self.title = title        
    
    def plotSimulation(self, ret=False, show=False, verbose=True):
        '''plots a simulation, time on x axis, nodes on y.
        Set ret=True for return of lines and no image creation. '''
        
        SIRSStates = utils.retrieveAllTrialsInDirectory(self.directory)
        stats = statistics.TrialSIRSStats(SIRSStates)
        av = stats.trialAverage
        
        pyplot.figure()
        lines = []
       
        for i in range(len(self.statesToMonitor)):
            if self.examples > 0:
                t0 = stats.trialSIRSStates[0]
                pyplot.plot(t0.times, t0.stateCounterForSIRSStateX[self.statesToMonitor[i]], "k", alpha=0.5)
            
            try:
                pyplot.plot(av.times, av.stateCounterForSIRSStateX[self.statesToMonitor[i]], self.colours[i], label=self.labels[i])
                lines.append((av.times, av.stateCounterForSIRSStateX[self.statesToMonitor[i]], self.colours[i]))
            except KeyError:
                try:
                    print "Plotting warning: skipping state = %s, colour = %s, label = %s, %s" \
                            % (str(self.statesToMonitor[i]), str(self.colours[i]), str(self.labels[i]), 
                               "because no node is ever in this state in this trial")
                except KeyError:
                    print "Plotting error: one of 'colours' or 'labels' has fewer elements",
                    " than 'statesToMonitor'. Skipping this state."
            
        pyplot.legend(loc=0)
        pyplot.title(self.title)
        pyplot.xlabel("Time")
        pyplot.ylabel("Nodes")
        if ret:
            return lines
        else:        
            output_path = os.path.join(self.directory, "plot_" + self.name + ".png")
            pyplot.savefig(output_path)
            if verbose: 
                print "Plot at", output_path
            
            if show:
                pyplot.show()
