
''' This module is for logging node attributes in the agent-based simulation'''
''' @author: samiramaghool@gmail.com>'''

import networkx as nx
from SimPy import Simulation as Sim
import utils


class NetworkLogger(Sim.Process):
        
    def __init__(self, sim, RESULTS_DIR, NET_IMAGES_DIR, logging_interval, printGIF):
        Sim.Process.__init__(self, sim=sim)
        self.sim = sim
        self.directory_results = RESULTS_DIR
        self.directory_netDraw = NET_IMAGES_DIR
        self.interval = logging_interval
        self.printGIF = printGIF
        self.SIRSNet = nx.Graph()
        self.SIRSStatesTuples = [] 
        
   
    def Run(self):
        while True:
            self.logCurrentState()
            yield Sim.hold, self, self.interval
            
    def logCurrentState(self):
        
        '''return the nodes of SIRS'''
        SIRSNodes = self.sim.SIRSNet.nodes(data=True)
        '''make a vector of states of nodes in SIRS network'''
        SIRSStates = [node[1]['agent'].SIRSState for node in SIRSNodes]       
        
        #log states
        '''adds to the end of SIRstates'''
        self.SIRSStatesTuples.append((self.sim.now(),SIRSStates))            
        
        
            
    def logTrialToFiles(self, id): 
        '''write states, topologies, and state vectors to file'''     
        utils.storeAllToFile(self.SIRSStatesTuples, self.directory_results, id)
        
