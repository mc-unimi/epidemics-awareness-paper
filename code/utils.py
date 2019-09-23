'''author:samiramaghool@gmail.com'''

import cPickle
from cPickle import Pickler, Unpickler
import os
import glob
import networkx as nx
from customexceptions import *

PYTHON_PICKLE_EXTENSION = ".pickled"
STATE = "_SIRSStates"
BASE = os.sep + "log_trial_"


def createIfNotExist(directory):
    if not os.path.exists(directory):
            os.makedirs(directory)


def states_to_colourString(SIRSStates, mapping=None):
    '''
    takes a list of states (integers) and a mapping, e.g.
    
    mapping = { 0 : "g",
                1 : "r",
                2 : "k"}
                
    Returns a list of colours to use in animation. Assumes matplotlib style
    colour strings. Defaults to black ("k") if state not found in mapping, and
    defaults to all nodes being black if no mapping defined.
    '''
    return [mapping.get(SIRSState, "k") for SIRSState in SIRSStates]

            
def makeFileNameSIRSState(dir, id):
    return dir + BASE + str(id) + STATE + PYTHON_PICKLE_EXTENSION 

def retrieveTrial(directory, trial_number):
    ''' For a specific trial in a given directory, retrieve states, topologies
    and statevectors.
    '''    
    SIRSStates = retrieve(makeFileNameSIRSState(directory, trial_number))
    return SIRSStates

def retrieveAllTrialsInDirectory(directory):
    '''Retrieves all trials in a directory '''
    file_list = glob.glob(os.path.join(directory, "*" + PYTHON_PICKLE_EXTENSION))
    SIRSStates = []
    for f in file_list:
        SIRSStates.append(f)

    SIRSState_list = [retrieve(f) for f in SIRSStates]
    return (SIRSState_list)
    
def storeAllToFile(SIRSStatesTuples, directory, trial_id):
    storeToFile(SIRSStatesTuples, makeFileNameSIRSState(directory, str(trial_id)))                         
            
def storeToFile(stuff, filename, verbose=True):   
    ''' Store one item (e.g. state list or networkx graph) to file. '''
    filename = os.path.normcase(filename)   
    directory = os.path.dirname(filename)
    createIfNotExist(directory)
    
    f = open(filename, 'wb')
    p = Pickler(f, protocol=2)
    p.dump(stuff)
    f.close()
    if verbose:
        total = len(stuff)
        print "Written %i items to pickled binary file: %s" % (total, filename) 
    return filename

def retrieve(filename): 
    ''' Retrieve a pickled object (e.g. state list or networkx graph) from file
    '''
    filename = os.path.normcase(filename)
    
    try:      
        f = open(filename, 'rb')   
        u = Unpickler(f)
        stuff = u.load()
        f.close()
        return stuff
    except IOError:
        raise LogOpeningError("No file found for %s" % filename, filename)

 

