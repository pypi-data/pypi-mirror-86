import numpy as np
import math
ACTIVATIONLIST = ['relu','sigmoid']

def get_activation():
    """return the list of choosable activation fonctions"""
    return ACTIVATIONLIST

def relu(x):
    return np.maximum(0,x)



class layerDense:
    def __init__(self,inputs,nodes,activation):
        """create a layer
        inputs : an int for the number of inputs
        nodes : an int for the number of node
        activation : a str for the activation fonction use get_activation() to have the list of activation fonctions
        """
        self.activation = activation
        self.nodes = nodes
        self.weights = np.random.uniform(-1,1,(inputs,nodes))
        self.biases = np.zeros((1,nodes))

    def forward(self,inputs):
        """go forward through the layer and transform inputs to outputs with a dot pruduct between inputs and weights + biases""" 
        self.output = self.activation(np.dot(inputs,self.weights)+self.biases)
        return self.output

class ANN:
    def __init__(self,ninputs):
        """Create an Artifitial Neural Network with
        ninputs : an int for the number of input that will enter in the network
        """

        self.layers = []
        self.ninputs = ninputs

    def add(self,nodes,activation = relu):
        """Add a layer in the network
        nodes : an int for the number of node
        activation : a function for the activation fonction use get_activation() to have the list of activation fonctions
        """
        if self.layers == []:
            l = layerDense(self.ninputs,nodes,activation)
        else:
            l = layerDense(self.layers[-1].nodes,nodes,activation)

        self.layers.append(l)

    def forward(self,inputs):
        """loop through the layers to transform the input into an output"""
        current = inputs
        for l in self.layers:
            current = l.forward(current)
        return current



