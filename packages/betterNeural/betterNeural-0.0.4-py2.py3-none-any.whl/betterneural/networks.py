import numpy as np

ACTIVATIONLIST = ['relu','sigmoid']

def get_activation():
    """return the list of choosable activation fonctions"""
    return ACTIVATIONLIST


class layer:
    def __init__(self,inputs,nodes,activation):
        """create a layer
        inputs : an int for the number of inputs
        nodes : an int for the number of node
        activation : a str for the activation fonction use get_activation() to have the list of activation fonctions
        """
        self.nodes = nodes
        self.weights = np.random.rand(nodes,inputs)
        self.biases = np.random.rand(nodes,1)

class ANN:
    def __init__(self,ninputs):
        """Create an Artifitial Neural Network with
        ninputs : an int for the number of input that will enter in the network
        """

        self.layers = []
        self.ninputs = ninputs

    def add(self,nodes,activation = 'relu'):
        """Add a layer in the network
        nodes : an int for the number of node
        activation : a str for the activation fonction use get_activation() to have the list of activation fonctions
        """
        if self.layers == []:
            l = layer(self.ninputs,nodes,activation)
        else:
            l = layer(self.layers[-1].nodes,nodes,activation)

        self.layers.append(l)



