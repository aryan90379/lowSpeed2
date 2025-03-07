
from calculateCL import *
from numpy import *
from matplotlib.pyplot import *
from camberline import *

def sumAn(coeffs,x,n): # A function that peforms summation of small gamma
    Sum = 0
    theta = arccos(1-2*x)
    for i in range (1,n):
        Sum += (compute_An_poly(coeffs,i) * sin(i*theta))
    return Sum

def Calculate_gamma(coeffs,x,alpha): # Function used to calculate big gamma
    u = 20 # Free Stream velocity as per our simulations
    AnTotal = sumAn(coeffs,x,100)
    A0 = compute_A0_poly(coeffs,alpha)
    theta = arccos(1-2*x)
    gamma = 2*u*((A0*(1+cos(theta))/sin(theta)) + AnTotal)
    return gamma



def compute_velocity_poly(coeffs, x, y, alpha):
    """ 
    Computes the net velocity at a given point (x, y) by summing induced velocity 
    vectors and free-stream velocity.

    Parameters:

    x : float -> X-coordinate of the point
    y : float -> Y-coordinate of the point
    alpha : float -> Angle of attack (in radians)

    Returns:
    vel_x, vel_y : list -> Components of the velocity vector at (x, y)
    """
    u = 30  # Free-stream velocity
    vel_x, vel_y = 0,0# Initialize velocity components

    # Iterate over vortex elements along the camber line, ignoring points near edges
    for i in np.linspace(0.005, 0.995, 100):
        yi = np.polyval(coeffs, i)   # Get camber line height at i
        r = np.sqrt((x - i)**2 + (y - yi)**2)  # Distance from vortex element

        # Compute induced velocity using circulation strength
        v_ind = Calculate_gamma(coeffs,i, alpha) * 0.01 / (2 * np.pi * r)

        # Compute velocity components due to induced flow
        cost = (x - i) / r
        sint = (y - yi) / r
        vel_x += v_ind * sint
        vel_y -= v_ind * cost

    # Add free-stream velocity components
    vel_x += u * np.cos(alpha)
    vel_y += u * np.sin(alpha)

    return [vel_x, vel_y]  # Return velocity components


