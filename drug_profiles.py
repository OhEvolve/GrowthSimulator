
# library imports
import numpy as np

def linear_profile(nx,ny):
    """ Create a drug profile that peaks in middle """
    l = np.arange(0,nx+1)
    x = np.repeat(l,ny+1).reshape(nx+1,ny+1)
    x = ((nx+1 - 1)/2 - abs(x - (nx+1 - 1)/2))/((nx+1-1)/2)
    return x

def stepwise_profile(nx,ny,steps = 3):
    # NOTE: fix so that center drug concentration is half size
    """ Create a drug profile that peaks in middle """
    l = np.arange(0,nx+1)
    x = np.repeat(l,ny+1).reshape(nx+1,ny+1)
    x = ((nx+1 - 1)/2 - abs(x - (nx+1 - 1)/2))
    x,_ = np.divmod(x,(nx+1)/(2*steps))
    x /= np.max(x)
    return x
