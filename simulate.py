
gen_per_second = 10


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# custom libraries
from drug_profiles import linear_profile,stepwise_profile
import behavior.basic as behavior_basic
import behavior.drug_only as behavior_drug_only 

diffs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

def add_remove_from_set(my_set,adds,removes):
    """ Simple function to add and remove for an existing set """
    for xy in adds: # add new points
        my_set.add(xy)
    for xy in removes: # remove saturated points
        my_set.remove(xy)

class Simulator(object):

    def __init__(self,nx,ny):
        """ Initialize the behavior for the species """
        self.nx = nx
        self.ny = ny

        self.initial_colonies = {}

        self.behavior = behavior_drug_only

        self.drug_profile = stepwise_profile(nx,ny,steps = 5)
    
    def _load_behavior(self):
        
        # transfer some important numbers to local namespace
        self.trait_count = self.behavior.trait_count
        self.max_develop_count = self.behavior.max_develop_count

        self.behavior.load_default_behavior(self)

    def start(self):

        self._load_behavior()

        # initialize data matrices
        self.population = np.zeros((self.nx+1,self.ny+1)) # state of each 
        self.traits = np.zeros((self.nx+1,self.ny+1,self.trait_count)) # state of each 
        self.color = np.dstack((rgb*np.ones((self.nx+1,self.ny+1)) for rgb in self.behavior.bg_color))

        # link layers to their respective names
        for index,trait in enumerate(self.behavior.trait_names):
            setattr(self,trait,self.traits[:,:,index])

        # create set samples (keep track of only active pixels
        self.developing_colonies = set()
        self.growing_colonies = set()

        self._set_initial_colonies() #
        self._init_figures() #

        anim = animation.FuncAnimation(self.fig, self.simulate_generation,interval=10)

        # figures
        plt.show()

    def simulate_generation(self,gen_number):
        """ Simulation a progression of generation """
        print("Generation {} | Growing Colonies {} | Developing Colonies {}".format(
            gen_number,len(self.growing_colonies),len(self.developing_colonies)))

        self._simulate_colony_development()
        self._simulate_colony_growth()

    def _simulate_colony_development(self):
        """ Simlate all steps in colony development """
        remove_xys = []

        # develop available colonies
        for (x,y) in self.developing_colonies:
            
            # check if fully developed
            if self._is_developed(x,y): # if point is saturated
                remove_xys.append((x,y))
                continue

            # check if colony will develop
            if np.random.random() < self.develop_rate(x,y):
                self._develop_colony(x,y)

        add_remove_from_set(self.developing_colonies,[],remove_xys)

    def _simulate_colony_growth(self):
        """ Simlate all steps in colony growth and spread """
        add_xys = []
        remove_xys = []

        for (x,y) in self.growing_colonies:
            is_available_moves = False

            for (dx,dy) in diffs:

                if x+dx < 0 or x+dx > self.nx: continue # if at x boundary
                if y+dy < 0 or y+dy > self.ny: continue # if at y boundary
                if self._is_occupied(x+dx,y+dy): continue

                is_available_moves = True

                if np.random.random() < self.growth_rate(x,y):
                    if np.random.random() < self.mutation_rate(x,y): # if mutation
                        new_trait = self.mutate(x,y)
                    else: # no mutation
                        new_trait = self.dont_mutate(x,y)

                    drug = self.drug_profile[x+dx,y+dy] # get new space drug concentration
                    if np.random.random() > self.resistance_rate(x,y,drug,new_trait):
                        continue

                    self._new_colony((x,y),(x+dx,y+dy),new_trait) # create new colony
                    add_xys.append((x+dx,y+dy))

            if not is_available_moves:
                remove_xys.append((x,y))

        add_remove_from_set(self.developing_colonies,add_xys,[])
        add_remove_from_set(self.growing_colonies,add_xys,remove_xys)

        self.im.set_data(self.color) # set data
        #self.drug_im.set_data(self.population) # set data

        if len(self.growing_colonies) == 0 and len(self.developing_colonies) == 0:
            plt.close() 
            raise IndexError('Simulation complete!') 


    def _init_figures(self):
        """ Initialize figures """
        self.fig = plt.figure(figsize = (10,10))

        self.ax1 = self.fig.add_subplot(121)
        plt.title('Bacterial Growth')
        plt.axis('off')

        self.ax2 = self.fig.add_subplot(122)
        plt.title('Drug Concentration')
        plt.axis('off')

        # set up image
        plt.sca(self.ax1)
        self.im = plt.imshow(self.color, vmin=0, vmax=1)
        self.im.set_data(self.color)

        # view drug profile
        plt.sca(self.ax2)
        self.drug_im = plt.imshow(self.drug_profile, vmin=0, vmax=1)
        #self.drug_im.set_data(self.drug_profile)


    def _is_occupied(self,x,y):
        """ Check if location has a colony """
        return self.population[x,y] > 0


    def _is_developed(self,x,y):
        """ Check if location has fully developed colony """
        return self.population[x,y] == self.max_develop_count

    def _set_initial_colonies(self):
        """ Set initial colonies on the map """
        for (x,y),trait in self.initial_colonies.items():
            self._set_colony(x,y,trait)
            self.growing_colonies.add((x,y))
            self.developing_colonies.add((x,y))

    def _new_colony(self,xy,dxy,new_trait = None):
        """ """
        x,y,dx,dy = xy + dxy

        if new_trait is None: new_trait = self.traits[x,y,:]

        self._set_colony(dx,dy,new_trait)


    def _develop_colony(self,x,y):
        """ """
        self.population[x,y] += 1 
        self.color[x,y,:] = self.convert_color(x,y) 

    def _set_colony(self,x,y,new_trait):
        """ Assign values to data matrices """
        self.population[x,y] = 1 
        self.traits[x,y,:] = new_trait
        self.color[x,y,:] = self.convert_color(x,y) 

if __name__ == "__main__":

    simulator = Simulator(300,100)
    simulator.initial_colonies = {
            (0,50):  np.array((0.0,0.0,0.0)),
            (300,50):np.array((0.0,0.0,0.0)),
            }
    simulator.start()

        
