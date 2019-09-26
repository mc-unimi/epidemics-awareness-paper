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
        
