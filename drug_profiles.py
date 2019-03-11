
import numpy as np

def linear_profile(nx,ny):
    """ Create a drug profile that peaks in middle """
    l = np.arange(0,nx)
    x = np.repeat(l,ny).reshape(nx,ny,1)
    x = ((nx - 1)/2 - abs(x - (nx - 1)/2))/((nx-1)/2)
    return x

def stepwise_profile(nx,ny,steps = 6):
    """ Create a drug profile that peaks in middle """
    l = np.arange(0,nx)
    x = np.repeat(l,ny).reshape(nx,ny,1)
    x = ((nx - 1)/2 - abs(x - (nx - 1)/2))
    x,_ = np.divmod(x,nx/(2*steps))
    x /= np.max(x)
    return x
