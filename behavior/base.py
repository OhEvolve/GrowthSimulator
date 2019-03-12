
import types
import numpy as np

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

# claimed traits
trait_names = ['trait1','trait2','trait3']
trait_count = len(trait_names)

def load_default_behavior(self):

    def dont_mutate(self,x,y):
        """ Creates a new trait set """
        return self.traits[x,y,:]

    def mutate(self,x,y):
        """ Creates a new trait set """
        dcolor = np.random.randint(0,3,trait_count)
        new_color = self.traits[x,y,:] + dcolor
        return np.fmin(np.fmax(new_color,0),1)
        
    def convert_color(self,trait):
        """ Converts a trait into a distinct color """
        return trait

    # METHODS FOR SIMULATION DYNAMICS

    def growth_rate(self,x,y):
        """ Returns the adjusted growth rate """ 
        return base_growth_rate

    def mutation_magnitude(self,x,y):
        """ Return magnitude of mutation """
        return base_mutation_magnitude

    def mutation_rate(self,x,y):
        """ Return rate of mutation on growth """
        return base_mutation_rate

    def resistance_rate(self,x,y,trait = None):
        """ Returns probability colony resists the drug """
        return base_resistance_rate

    def develop_rate(self,x,y):
        """ Returns probability colony resists the drug """
        return base_develop_rate

    self.mutate =               types.MethodType(mutate,self)
    self.dont_mutate =          types.MethodType(dont_mutate,self)
    self.convert_color =        types.MethodType(convert_color,self)
    self.growth_rate =          types.MethodType(growth_rate,self)
    self.mutation_magnitude =   types.MethodType(mutation_magnitude,self)
    self.mutation_rate =        types.MethodType(mutation_rate,self)
    self.resistance_rate =      types.MethodType(resistance_rate,self)
    self.develop_rate =         types.MethodType(develop_rate,self)







