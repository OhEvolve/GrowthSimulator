

import types
import numpy as np

# coloring parameters
bg_color = [0,0,0]

# develop parameters (NOTE: this is mostly asethetic for the time being)
base_develop_rate = 0.3
max_develop_count = 3

# initial values 
base_growth_rate = 0.05
base_develop_rate = 0.05
base_resistance_rate = 1.0
base_mutation_rate = 0.10
base_mutation_magnitude =  0.05

# 
resistance_growth_rate = -0.01

# METHODS FOR INITIALIZATION 

# claimed traits
trait_names = ['resistance','mutation','fitness']
trait_count = len(trait_names)

def load_default_behavior(self):

    def dont_mutate(self,x,y):
        """ Creates a new trait set """
        return self.traits[x,y,:]

    def mutate(self,x,y):
        """ Creates a new trait set """
        dcolor = self.mutation_magnitude(x,y)*np.random.normal(size = 3)
        new_color = self.traits[x,y,:] + dcolor
        return np.fmin(np.fmax(new_color,0),1)
        
    def convert_color(self,x,y):
        """ Converts a trait into a distinct color """
        #return 1 - self.population[x,y]*(1 - self.traits[x,y,:])/max_develop_count
        #target = np.array((1.0 - self.resistance[x,y],1.0,1.0))
        #return 1 - self.population[x,y]*target/max_develop_count
        val = 1.0 - self.population[x,y]*self.resistance[x,y]/max_develop_count
        return np.array((1.0,val,val))

    # METHODS FOR SIMULATION DYNAMICS

    def growth_rate(self,x,y):
        """ Returns the adjusted growth rate """ 
        return base_growth_rate - resistance_growth_rate*self.resistance[x,y] 

    def mutation_magnitude(self,x,y):
        """ Return magnitude of mutation """
        return base_mutation_magnitude

    def mutation_rate(self,x,y):
        """ Return rate of mutation on growth """
        return base_mutation_rate

    def resistance_rate(self,x,y,drug = None,trait = None):
        """ Returns probability colony resists the drug """
        exp = 30
        if drug is None: drug = self.drug_profile[x,y]
        if trait is None: drug = self.trait[x,y,:]
        rs = trait[0]
        return np.power(10**exp,rs)/(np.power(10**exp,rs) + np.power(10**exp,drug-0.15))

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







