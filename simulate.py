
gen_per_second = 10


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# custom libraries
from drug_profiles import linear_profile,stepwise_profile
from behavior.base import Behavior

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

        self.behavior = Behavior()

        self.drug_profile = stepwise_profile(nx,ny)
    
    def _load_behavior(self):
        
        # transfer some important numbers to local namespace
        self.trait_count = self.behavior.trait_count
        self.max_develop_count = self.behavior.max_develop_count

        self.mutate = self.behavior.mutate # does this work?
        self.dont_mutate = self.behavior.dont_mutate # does this work?

    def start(self):

        self._load_behavior()

        # initialize data matrices
        self.population = np.zeros((self.nx+1,self.ny+1)) # state of each 
        self.traits = np.zeros((self.nx+1,self.ny+1,self.trait_count)) # state of each 
        self.color = np.ones((self.nx+1,self.ny+1,3)) # state of each 

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
        print("Generation {}".format(gen_number))

        self._simulate_colony_development()
        self._simulate_colony_growth()

    def _simulate_colony_development(self):
        """ Simlate all steps in colony development """
        add_xys = [] # unused
        remove_xys = []

        # develop available colonies
        for (x,y) in self.developing_colonies:
            
            # check if fully developed
            if self._is_developed(x,y): # if point is saturated
                remove_xys.append((x,y))
                continue

            # check if colony will develop
            if np.random.random() < self.behavior.develop_rate:
                self._develop_colony(x,y)

        add_remove_from_set(self.developing_colonies,add_xys,remove_xys)

    def _simulate_colony_growth(self):
        """ Simlate all steps in colony growth and spread """
        add_xys = []
        remove_xys = []

        for (x,y) in self.growing_colonies:
            is_available_moves = False

            for (dx,dy) in diffs:

                print(x,y,dx,dy)
                if x+dx < 0 or x+dx > self.nx: continue # if at x boundary
                if y+dy < 0 or y+dy > self.ny: continue # if at y boundary
                if self._is_occupied(x+dx,y+dy): continue

                is_available_moves = True

                if np.random.random() < self.behavior.growth_rate(x,y):
                    if np.random.random() < self.behavior.mutation_rate(x,y): # if mutation
                        new_trait = self.mutate(x,y)
                    else: # no mutation
                        new_trait = self.dont_mutate(x,y)

                    if np.random.random() > resistance_rate(x+dx,y+dy,new_trait):
                        continue

                    _new_colonies((x,y),(x+dx,y+dy),new_trait) # create new colony

            if not is_available_moves:
                remove_xys.append((x,y))

        add_remove_from_set(self.developing_colonies,add_xys,[])
        add_remove_from_set(self.growing_colonies,add_xys,remove_xys)

        self.im.set_data(self.color) # set data

        if len(self.growing_colonies) == 0 and len(self.developing_colonies) == 0:
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
        drug_im = plt.imshow(self.drug_profile, vmin=0, vmax=1)

    def _is_occupied(self,x,y):
        """ Check if location has a colony """
        return self.population[x,y] > 0

    def _is_developed(self,x,y):
        """ Check if location has fully developed colony """
        return self.population[x,y] > 0
        return self.population[x,y] == self.max_develop_count

    def _set_initial_colonies(self):
        """ Set initial colonies on the map """
        for (x,y),trait in self.initial_colonies.items():
            self._set_colony(x,y,trait)
            self.growing_colonies.add((x,y))
            self.developing_colonies.add((x,y))

    def _new_colony(self,xy,xy2,new_traits = None):
        """ """
        x,y,dx,dy = xy + dxy

        if new_trait == None: new_trait = self.traits[x,y,:]

        set_colony(dx,dy,new_trait)


    def _develop_colony(self,x,y):
        """ """
        self.population[x,y] += 1 


    def _set_colony(self,x,y,new_trait):
        """ Assign values to data matrices """
        self.population[x,y] = 1 
        self.traits[x,y,:] = new_trait
        self.color[x,y,:] = self.behavior.color_conversion(new_trait) 

        #self.developing_colonies.add((x,y))
        #self.growing_colonies.add((x,y))


if __name__ == "__main__":

    simulator = Simulator(200,50)
    simulator.initial_colonies = {
            (0,25):  np.array((0,1,0)),
            (200,25):np.array((0,1,0)),
            }
    simulator.start()

        

'''
#--------------------#

nx = 300 
ny = 150 

diffs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
starting_xy = [(0,int(ny/2)),(nx-1,int(ny/2))]

behavior = Behavior(nx,ny)

for (x,y) in starting_xy:
    behavior.set_colony(x,y,[0,0,0])

#-----FUNCTIONS-----#



def animate(i,xys):

    add_xys = []
    remove_xys = []

    print('Generation {} : Active colonies {}'.format(i+1,len(xys)))

    for (x,y) in xys:
        is_available_moves = False
        
        # promote self growth
        if data[x,y,0] < max_colony_size: # if point is saturated
            is_available_moves = True
            if np.random.random() > 1 - max_growth_rate + max_growth_rate*data[x,y,0]/max_colony_size:
                data[x,y,0] += 1

        for (dx,dy) in diffs:

            if x+dx < 0 or x+dx > nx-1: continue # if at x boundary
            if y+dy < 0 or y+dy > ny-1: continue # if at y boundary
            if data[x+dx,y+dy,0] > 0:    continue # if point is colonized 

            is_available_moves = True

            if np.random.random() < get_colonization_rate(color[x,y,:]):
                # no mutation :(
                if np.random.random() > get_mutation_rate(color[x,y,:]):
                    color[x+dx,y+dy,:] = color[x,y,:]
                # mutation!
                else:
                    dcolor = np.array((0.,0.,0.))
                    dcolor[np.random.randint(3)] += get_mutation_magnitude(color[x,y,:])*(np.random.normal())
                    new_color = color[x,y,:] + dcolor
                    color[x+dx,y+dy,:] = np.fmin(np.fmax(new_color,0),1)
                # check if passes resistance check
                if np.random.random() > get_resistance_rate(
                        color[x+dx,y+dy,:],
                        drug_concentration[x+dx,y+dy,:]):
                    continue

                data[x+dx,y+dy,0] = 1
                add_xys.append((x+dx,y+dy))
        if not is_available_moves:
            remove_xys.append((x,y))

    for xy in add_xys: # add new points
        xys.add(xy)
    for xy in remove_xys: # remove saturated points
        xys.remove(xy)

    im.set_data(np.multiply(color,data/max_colony_size)) # set data

    if len(xys) == 0:
       raise IndexError('Simulation complete!') 

    return im

data = np.zeros((nx, ny, 1)) # colony density

color = np.dstack((rgb*np.ones((nx,ny)) for rgb in starting_colony_state))
drug_color = np.dstack((rgb*np.ones((nx,ny)) for rgb in drug_color))

drug_concentration = stepwise_profile(nx,ny)

# setting up figure dimension & properties
fig = plt.figure(figsize = (10,10))
ax1 = fig.add_subplot(121)
plt.title('Bacterial Growth')
plt.axis('off')

ax2 = fig.add_subplot(122)
plt.title('Drug Concentration')
plt.axis('off')


plt.sca(ax1)
im = plt.imshow(np.multiply(color,data), vmin=0, vmax=1)

plt.sca(ax2)
drug_im = plt.imshow(np.ones((nx,ny,3)) - np.multiply(drug_color,drug_concentration), vmin=0, vmax=1)

plt.sca(ax1)
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=nx * ny,
                               interval=10,fargs = (xys,))

plt.show()
'''
