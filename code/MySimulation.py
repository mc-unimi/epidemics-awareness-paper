
''' This module is for running the agent-based simulation'''
''' @author: samiramaghool@gmail.com>'''

from os import sep
import NetworkSimulation
import SIRSAgent
import networkx as nx
from networkx import Graph, DiGraph
import random
from plotting import PlotCreator

#paths
SOURCE_DIR = 'source'
RESULTS_DIR = 'results'
NET_IMAGES_DIR = 'netDraw'  
myName = "SIR"
'''number of trials shown on plot'''
TRIALS = 20                        

title = "Simulation of agent-based SIRS, " + "trial=" + str(TRIALS)


#define three simulation-specific constants:
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2
SIRSNet_NAME = 'SIRS_edgelist.txt'

'''simulation parameters'''
'''specify number of time steps'''
MAX_SIMULATION_TIME = 20.0                    
NODES = 1000

'''Retrieve Networks'''

'''define the underlying network configuration'''
SIRSNet = nx.powerlaw_cluster_graph(NODES, 3, 0.6)   

''' in the case of reading network from source files un-comment next 4lines'''
#def retrieveNet(path, netType):
#    return read_edgelist(path, create_using=netType, nodetype=int)

#def storeNet(net, path):
#    write_edgelist(net, path)

    
def main():

    '''Node states initialization'''
    
    x = random.uniform(0, NODES)
    SIRSStates = setupInitialStates(SIRSNet, int(x), int(x+1), NetworkSimulation.INFECTED, NetworkSimulation.SUSCEPTIBLE)
    



    '''parameter setting'''
   
        
    for i in range(0, SIRSNet.__len__()):      
        '''initial amount of imitation if exist'''
        SIRSNet.nodes[i]['a_1'] = 1.0
        '''assign weight if imitation factor in logarithmic pool'''
        SIRSNet.nodes[i]['w_1'] = 0.5
        '''assign weight if self-awareness factor in logarithmic pool'''
        SIRSNet.nodes[i]['w_2'] = 0.5            

        '''define the density of consisting type of agents L/H/noAw'''
        Y = random.random()                  
        if Y < 0.7 :                            
           SIRSNet.nodes[i]['a_2'] = 1.0         #type1=1
        elif  0.7 <= Y < 1.0 :                   
           SIRSNet.nodes[i]['a_2'] = 10.0        #type2=10

      
        
    '''RUN SIMULATION'''
    simulation = NetworkSimulation.NetworkSimulation(SIRSNet, SIRSAgent, SIRSStates, 
                                                     RESULTS_DIR,
                                                     NET_IMAGES_DIR,
                                                     MAX_SIMULATION_TIME,
                                                     TRIALS)
    
    

    
    simulation.runSimulation()  #run rimulation
    
def setupInitialStates(Network, minRange, maxRange, specific_State, default_State):
    
    result1 = [default_State for i in range(0, minRange)]
    result2 = [specific_State for i in range(minRange, maxRange)]
    result3 = [default_State for i in range(maxRange, Network.__len__())]
    return result1 + result2 + result3


if __name__ == '__main__':
    main()
    


#statesToMonitor = [INFECTED, SUSCEPTIBLE, RECOVERED]
statesToMonitor = [INFECTED]
#colours = ["r", "b", "g"]
colours = ["r"]
labels = ["Infected"]
#labels = ["Infected", "Susceptible", "Recovered"] 
mapping = {SUSCEPTIBLE:"w", INFECTED:"r", RECOVERED:"0.4"}

p = PlotCreator(RESULTS_DIR, myName, title, statesToMonitor, colours, labels)
p.plotSimulation(show=True)
#show=True shows the graph directly,
#otherwise only a png file is created in the directory defined above.
