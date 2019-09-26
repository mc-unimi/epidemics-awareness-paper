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
Module for the SIRSAgent class that can be subclassed by agents.

@author:samiramaghool@gmail.com
'''

from SimPy import Simulation as Sim
import random
import NetworkSimulation   
import math
SEED = 9154893043

#shared parameters for SIRSAgents
'''biological(basic) infection probabality is 1-P_S_base'''
P_S_base = 0.8
'''biological(basic) recovery probability'''
P_IR_base = 0.6
'''biological(basic) probability of staying Recovered'''
P_R_base = 0.5         
P_S_max = 1.0           #p_s_max
P_IR_max = 1.0
'''defining logistic function parameters'''
k = 0.5                 #growth
z = 4.5                 #Aw_mid
m = 1.0                 #sensitivity   

class SIRSAgent(Sim.Process):
    
    '''class variables, shared between all instances of this class'''
    r = random.Random(SEED)
    TIMESTEP_DEFAULT = 1.0
    
    def __init__(self, SIRSState, initialiser, name='network_process'):    
        Sim.Process.__init__(self, name)
        self.SIRSState = SIRSState
        self.initialize(*initialiser)
        
        
    def initialize(self, id, sim, SIRSNet):   
        ''' this gets called automatically '''        
        self.id = id
        self.sim = sim
        self.SIRSNet = SIRSNet
        
    
    def getAllNodes(self):
        ''' returns all of the nodes in SIRS Network '''
        return self.SIRSNet.nodes()
    
    def getAllAgents(self, SIRSState=None):
        ''' returns all of the agents in SIRS types '''
        neighs = self.getAllNodes()
        if SIRSState is not None:
            return [self.SIRSNet.node[n]['agent'] for n in neighs 
                      if self.SIRSNet.node[n]['agent'].SIRSState == SIRSState]
        else:
            return [self.SIRSNet.node[n]['agent'] for n in neighs] 

    def getNeighbouringAgents(self, SIRSState=None):
        ''' returns list of neighbours, but as agents, not nodes.
        so e.g. one can set result[0].state = INFECTED '''
        neighs = self.SIRSNet.neighbors(self.id)
        if SIRSState is not None:
            return [self.SIRSNet.node[n]['agent'] for n in neighs 
                      if self.SIRSNet.node[n]['agent'].SIRSState == SIRSState]
        else:
            return [self.SIRSNet.node[n]['agent'] for n in neighs]
        
    def getNeighbouringAgentsIter(self, SIRSState=None):
        '''same as getNeighbouringAgents, but returns generator expression, not list. '''
        neighs = self.SIRSNet.neighbors(self.id)
        if SIRSState is not None:
            return (self.SIRSNet.node[n]['agent'] for n in neighs 
                      if self.SIRSNet.node[n]['agent'].SIRSState == SIRSState)
        else:
            return (self.SIRSNet.node[n]['agent'] for n in neighs)
    
    def getNeighbouringNodes(self):
        ''' returns list of neighbours as nodes. 
        Call self.getAgent() on one of them to get the agent.'''
        return self.SIRSNet.neighbors(self.id)
   
    def getAgent(self, id):
        '''returns agent of specified ID.'''   
        return self.SIRSNet.node[id]['agent']
             
    def logTopoChange(self, action, node, node2=None):
        '''#TODO: test, add this to netlogger...'''
        print (action, node, node2)
             
        
    def Run(self):
        while True:
           
            if self.SIRSState == NetworkSimulation.SUSCEPTIBLE:
                self.mayStaySusceptible()
                yield Sim.hold, self, SIRSAgent.TIMESTEP_DEFAULT  #wait a step
            elif self.SIRSState == NetworkSimulation.INFECTED:
                self.mayBecomeRecovered()
                yield Sim.hold, self, SIRSAgent.TIMESTEP_DEFAULT  #wait a step
            elif self.SIRSState == NetworkSimulation.RECOVERED:
                self.mayReturnSusceptible()
                yield Sim.hold, self, SIRSAgent.TIMESTEP_DEFAULT  #wait a step
                

    '''comment the following function for rumor case'''
    def Imitation(self):
        ''' this function define and calculate the imitation amount for each agent for disease and addiction cases'''
        self.self_awareness()
        neighbours = self.getNeighbouringAgentsIter()
        self.number_of_neighbours  =  sum(1 for _ in neighbours)
        infected_neighbours = self.getNeighbouringAgentsIter(SIRSState=NetworkSimulation.INFECTED)
        self.number_of_infected_neighbours  =  sum(1 for _ in infected_neighbours)
        if self.SIRSState == NetworkSimulation.SUSCEPTIBLE:
           if self.self_awareness() == 10.0 :
              '''assign the threshold of imitation for each H type agents if they are in Susceptible state'''
              '''assign the gain of imitation for each H type agents if they are in Susceptible state'''
              if float(self.number_of_infected_neighbours)/float( self.number_of_neighbours) >= 0.5:   
                self.SIRSNet.nodes[self.id]['a_1'] = self.SIRSNet.nodes[self.id]['a_1'] + 3.0          
                if self.SIRSNet.nodes[self.id]['a_1'] > 10.0:
                    self.SIRSNet.nodes[self.id]['a_1'] = 10.0
           elif  self.self_awareness() == 1.0 :
              '''assign the threshold of imitation for each L type agents if they are in Susceptible state'''
              '''assign the gain of imitation for each L type agents if they are in Susceptible state'''
              if  float(self.number_of_infected_neighbours)/float( self.number_of_neighbours) >= 0.5:   
                  #self.SIRSNet.nodes[self.id]['a_1'] = self.SIRSNet.nodes[self.id]['a_1'] + 0.5     '''for disease case uncomment this line'''
                  #self.SIRSNet.nodes[self.id]['a_1'] = 0.2                                          '''for addiction case uncomment this line'''
                  if self.SIRSNet.nodes[self.id]['a_1'] > 10.0:
                    self.SIRSNet.nodes[self.id]['a_1'] = 10.0
           elif   self.self_awareness() == 0 :
              '''imitation amount for noAw agents in Susceptible state if exist'''
              self.SIRSNet.nodes[self.id]['a_1'] = 0                     
        elif self.SIRSState == NetworkSimulation.INFECTED:
            if self.self_awareness() == 10.0 :
              '''assign the threshold of imitation for each H type agents if they are in Infected state'''
              '''assign the gain of imitation for each H type agents if they are in Infected state'''
              if 1.0-(float(self.number_of_infected_neighbours)/float( self.number_of_neighbours)) >= 0.5:
                self.SIRSNet.nodes[self.id]['a_1'] = self.SIRSNet.nodes[self.id]['a_1'] + 3.0
                if self.SIRSNet.nodes[self.id]['a_1'] > 10.0:
                    self.SIRSNet.nodes[self.id]['a_1'] = 10.0
            elif  self.self_awareness() == 1.0 :
                '''assign the threshold of imitation for each L type agents if they are in Infected state'''
                '''assign the gain of imitation for each L type agents if they are in Infected state'''
                if  1.0-(float(self.number_of_infected_neighbours)/float( self.number_of_neighbours)) >= 0.5:
                  self.SIRSNet.nodes[self.id]['a_1'] = self.SIRSNet.nodes[self.id]['a_1'] + 0.5
                #else:                                                                      '''for addiction case uncomment these two lines'''
                #  self.SIRSNet.nodes[self.id]['a_1'] = 0.2
                if self.SIRSNet.nodes[self.id]['a_1'] > 10.0:
                    self.SIRSNet.nodes[self.id]['a_1'] = 10.0
            elif   self.self_awareness() == 0 :
              '''imitation amount for noAw agents in Infected state if exist'''
              self.SIRSNet.nodes[self.id]['a_1'] = 0
  
        return self.SIRSNet.nodes[self.id]['a_1']


    '''uncomment the following function for rumor case'''
    ''' this function define and calculate the imitation amount for each agent for rumor case'''
     #def Imitation(self):
       # neighbours = self.getNeighbouringAgentsIter()
       # self.number_of_neighbours  =  sum(1 for _ in neighbours)
       # infected_neighbours = self.getNeighbouringAgentsIter(SIRSState=NetworkSimulation.INFECTED)
       # self.number_of_infected_neighbours  =  sum(1 for _ in infected_neighbours)
       # if self.SIRSState == NetworkSimulation.SUSCEPTIBLE:
       #     if self.SIRSNet.nodes[self.id]['a_2'] > 2.0 :
       #         if  float(self.number_of_infected_neighbours)/float( self.number_of_neighbours) < 0.3:
       #           self.SIRSNet.nodes[self.id]['a_1'] = 1.0
       #         else:
       #           self.SIRSNet.nodes[self.id]['a_1'] = self.SIRSNet.nodes[self.id]['a_1'] + 3.0
       #           if self.SIRSNet.nodes[self.id]['a_1'] > 10.0:
       #                 self.SIRSNet.nodes[self.id]['a_1'] = 10.0
       #     elif self.SIRSNet.nodes[self.id]['a_2']  <= 1.0 :
       #         if float(self.number_of_infected_neighbours)/float( self.number_of_neighbours) < 0.5:
       #             self.SIRSNet.nodes[self.id]['a_1'] = 1.0
       #         else:
       #             self.SIRSNet.nodes[self.id]['a_1'] = 1.0/5.0
       # elif self.SIRSState == NetworkSimulation.INFECTED:
       #     if self.SIRSNet.nodes[self.id]['a_2']  > 2.0 :
       #       if 1.0-(float(self.number_of_infected_neighbours)/float( self.number_of_neighbours)) < 0.3:
       #         self.SIRSNet.nodes[self.id]['a_1'] = 1.0
       #       else:
       #         self.SIRSNet.nodes[self.id]['a_1'] = self.SIRSNet.nodes[self.id]['a_1'] + 3.0
       #         if self.SIRSNet.nodes[self.id]['a_1'] > 10.0:
       #             self.SIRSNet.nodes[self.id]['a_1'] = 10.0
       #     elif  self.SIRSNet.nodes[self.id]['a_2']  <= 1.0 :
       #         if  1.0-(float(self.number_of_infected_neighbours)/float( self.number_of_neighbours)) < 0.5:
       #           self.SIRSNet.nodes[self.id]['a_1'] = 1.0/5.0
       #         else:
       #           self.SIRSNet.nodes[self.id]['a_1'] = self.SIRSNet.nodes[self.id]['a_1'] + 0.5
       #           if self.SIRSNet.nodes[self.id]['a_1'] > 10.0:
       #             self.SIRSNet.nodes[self.id]['a_1'] = 10.0
       #     elif   self.SIRSNet.nodes[self.id]['a_2']  == 0 :
       #       self.SIRSNet.nodes[self.id]['a_1'] = 0     
       # return self.SIRSNet.nodes[self.id]['a_1']

    #def self_awareness(self):                     '''returns the a_2 value as self_awareness'''
    #    return self.SIRSNet.nodes[self.id]['a_2']

    
    
    '''uncomment the following function for rumor case'''
      #def Info_spreading(self):         #number of messages     
      #  neighboooors = self.getNeighbouringNodes()
  
      #  if self.SIRSNet.nodes[self.id]['a_2'] != 0:
      #      for i in neighboooors:
      #         if self.SIRSNet.node[i]['agent'].SIRSState == NetworkSimulation.INFECTED:
      #             self.SIRSNet.nodes[self.id]['a_3'] = self.SIRSNet.nodes[self.id]['a_3'] + 1.0
      #             if self.SIRSNet.nodes[self.id]['a_3'] == T:
      #                 self.SIRSNet.nodes[self.id]['a_3'] = 0
      #                 if self.SIRSNet.nodes[self.id]['a_2'] != 0:
      #                    self.SIRSNet.nodes[self.id]['a_2'] = self.SIRSNet.nodes[self.id]['a_2'] - 1.0
      #                    self.SIRSNet.nodes[self.id]['threshold'] = self.SIRSNet.nodes[self.id]['threshold'] + 1.0                
      #  else:
      #      self.SIRSNet.nodes[self.id]['a_3'] = 0
      #      self.SIRSNet.nodes[self.id]['threshold']         
      #  return self.SIRSNet.nodes[self.id]['a_2']

    '''this function returns the self_awareness value'''
    def self_awareness(self):
        return self.SIRSNet.nodes[self.id]['a_2']

    
    '''this function returns the awareness value'''
    def Awareness_function(self):                 
        
        a1 = self.Imitation ()
        '''comment this line for rumor case'''
        a2 = self.self_awareness ()
        '''uncomment next line for rumor case'''
        #a2 = self.Info_spreading()                     
        
        Awareness =(a1**self.SIRSNet.nodes[self.id]['w_1'])*(a2**self.SIRSNet.nodes[self.id]['w_2'])
        return Awareness 
             
    
            
    def mayStaySusceptible(self):
            Awareness = self.Awareness_function()
            a2 = self.self_awareness ()
            if a2 == 0:
                P_S = P_S_base
            else:
                P_S = P_S_base + (P_S_max - P_S_base)/(1.0 + m*math.exp(-k*(Awareness - z)))
            
            infected_neighbours = self.getNeighbouringAgentsIter(SIRSState=NetworkSimulation.INFECTED)
            for i in infected_neighbours:
               if SIRSAgent.r.random() <= 1-P_S:       
                  self.SIRSState = NetworkSimulation.INFECTED
                  break
      
    def mayBecomeRecovered(self):
            Awareness = self.Awareness_function ()
            a2 = self.self_awareness ()
            if a2 == 0:
                P_IR = P_IR_base
            else:
                P_IR = P_IR_base + (P_IR_max - P_IR_base)/(1.0 + m*math.exp(-k*(Awareness - z)))
           
            if SIRSAgent.r.random() <= P_IR:                
               self.SIRSState = NetworkSimulation.RECOVERED
               
            
    
    def mayReturnSusceptible(self):
            if SIRSAgent.r.random() <= 1-P_R_base:
                self.SIRSState = NetworkSimulation.SUSCEPTIBLE
                


                                                                 

    
                         
