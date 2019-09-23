
''' This module is for simulation of the agent-based simulation'''

''' @author: samiramaghool@gmail.com>'''
import os
import networkx as nx
from SimPy import Simulation as Sim
import NetworkLogger

'''Constants'''
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

        
class NetworkSimulation(Sim.Simulation):
    """Simulation support for agents in a complex network.
    
    Can run multiple fresh trials with the same input parameters. Writes system
    state evolution to file (states & network topologies)
    
    Parameters
    ----------
    
   
    
    SIRSNet: the network of social interaction that the SIRS dynamic run on it
    
    SIRSAgent: The class on which the behaviors of nodes of SIRSNet is defined
    
    SIRSStates: The list of agents states 
            
    directory_results: path to where output should be stored. It is recommended to
    have a different directory per simulation.
    
    maxTime : how long the simulation should run
    
    Optional parameters
    -------------------
    
    no_trials: the number of individual simulation trials 
    
    """

    def __init__(self, SIRSNet, SIRSAgent, SIRSStates, directory_name, NET_IMAGES_DIR, maxTime,
                 printGIF=False, no_trials= 50):

        
        Sim.Simulation.__init__(self)
        
        
        self.SIRSNet = SIRSNet
        self.SIRSAgent = SIRSAgent
        self.SIRSStates = SIRSStates
        self.directory_results = os.path.abspath(directory_name)
        self.directory_netDraw = os.path.abspath(NET_IMAGES_DIR)
        self.until = maxTime
        self.no_trials = no_trials
        self.printGIF = printGIF
        
        
        ''' the layout of network for Gif'''
        
        self.SIRSlayout = nx.spring_layout(self.SIRSNet)
        
    def runSimulation(self):
        print ("Starting simulation...")
        
        
        for i in range(self.no_trials):
            print "---Trial " + str(i) + " ---"
            self.runTrial(i)

        print ("Simulation completed. ")
        
    def runTrial(self, id):
        '''Sim.Simulation initialisation'''
        self.initialize()         
               
        
        print ("set up SIRS agents...")
        #set up agents
        for i in self.SIRSNet.nodes():
            agent = self.SIRSAgent.SIRSAgent(self.SIRSStates[i], (i, self, self.SIRSNet))
            self.SIRSNet.node[i]['agent'] = agent
            self.activate(agent, agent.Run())
            
        print ("set up logging...")
        #set up logging
        logging_interval = 1
        logger = NetworkLogger.NetworkLogger(self, self.directory_results, self.directory_netDraw, logging_interval, self.printGIF)
        self.activate(logger, logger.Run(), prior=True)
        
        #run simulation trial
        self.simulate(self.until)
        
        ''''write Files'''
        logger.logTrialToFiles(id)
        
        '''in the case of generating graphs un-comment the following line'''
        #GraphDrawer.drawAllGraphs(SUSCEPTIBLE, self.directory_results,id)
        
        
        ''''in the case of generating the GIF un-comment the following line'''
        #if self.printGIF:
        #    NetDrawer.drawGIF(self.directory_netDraw, delay=100)
            
        
