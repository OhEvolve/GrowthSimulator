
import numpy as np

class Behavior(object):

    # develop parameters (NOTE: this is mostly asethetic for the time being)
    base_develop_rate = 0.3
    max_develop_count = 3

    # inital values 
    base_growth_rate = 0.05
    base_develop_rate = 0.05
    base_resistance_rate = 1.0
    base_mutation_rate = 0.05
    base_mutation_magnitude =  0.1

    # METHODS FOR INITIALIZATION 

    def __init__(self,trait_names = ['trait1','trait2','trait3']):
        """ Initialize the behavior for the species """
        self.trait_names = trait_names
        self.trait_count = len(trait_names)

    def dont_mutate(self,x,y):
        """ Creates a new trait set """
        return self.traits[x,y,:]

    def mutate(self,x,y):
        """ Creates a new trait set """
        dcolor = np.random.randint(0,3,self.trait_count)
        new_color = self.traits[x,y,:] + dcolor
        return np.fmin(np.fmax(new_color,0),1)
        
    def color_conversion(self,trait):
        """ Converts a trait into a distinct color """
        return trait

    # METHODS FOR SIMULATION DYNAMICS

    def growth_rate(self,x,y):
        """ Returns the adjusted growth rate """ 
        return self.base_growth_rate

    def mutation_magnitude(self,x,y):
        """ Return magnitude of mutation """
        return self.base_mutation_magnitude

    def mutation_rate(self,x,y):
        """ Return rate of mutation on growth """
        return self.base_mutation_rate

    def resistance_rate(self,x,y,trait = None):
        """ Returns probability colony resists the drug """
        return self.base_resistance_rate

    def develop_rate(self,x,y):
        """ Returns probability colony resists the drug """
        return self.base_develop_rate







