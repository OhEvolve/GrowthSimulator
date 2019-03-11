
gen_per_second = 10


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

from drug_profiles import linear_profile,stepwise_profile

#-----PARAMETERS-----#

# colonization properties
base_colonization_rate = 0.05
bonus_colonization_rate = 0.10
mutation_colonization_rate = -0.05
resistance_colonization_rate = -0.10

# growth properties 
max_growth_rate = 0.3
max_colony_size = 3

# mutation properties
base_mutation_rate = 0.05
bonus_mutation_rate = 0.25

# mutation properties
base_mutation_magnitude =  0.1
bonus_mutation_magnitude = 0.2

resistance_index   = 0
mutation_index     = 1
colonization_index = 2

starting_colony_state = [0,0,0.5]
#starting_colony_state = [0.8,0,0]
#starting_colony_state = [0,0.75,0]
drug_color = [1,1,1]

#--------------------#

nx = 300 
ny = 150 

diffs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
starting_xy = [(0,int(ny/2))]
starting_xy = [(0,int(ny/2)),(nx-1,int(ny/2))]

#-----FUNCTIONS-----#

def get_colonization_rate(traits):
    colonization_score = traits[colonization_index]
    resistance_score   = traits[resistance_index]
    mutation_score     = traits[mutation_index]
    
    return base_colonization_rate + \
            bonus_colonization_rate*colonization_score + \
            mutation_colonization_rate*mutation_score + \
            resistance_colonization_rate*resistance_score

def get_mutation_magnitude(traits):
    mutation_score = traits[mutation_index]
    return base_mutation_magnitude + bonus_mutation_magnitude*mutation_score

def get_mutation_rate(traits):
    mutation_score = traits[mutation_index]
    return base_mutation_rate + bonus_mutation_rate*mutation_score

def get_resistance_rate(traits,drug):
    exp = 30
    rs = traits[resistance_index]
    return np.power(10**exp,rs)/(np.power(10**exp,rs) + np.power(10**exp,drug-0.15))
    


def init():
    im.set_data(np.zeros((nx, ny, 3)))

    for (x,y) in starting_xy:
        data[x,y,0] = 1

    bact_coordinates = set(starting_xy)

xys = set(starting_xy)

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

