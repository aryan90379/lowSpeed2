from calculateCL import *
from numpy import *
from matplotlib.pyplot import *
from camberline import *

def sumAn(M,P,x,n): # A function that peforms summation of small gamma
    Sum = 0
    theta = arccos(1-2*x)
    for i in range (1,n):
        Sum += (compute_An(M,P,i) * sin(i*theta))
    return Sum

def Calculate_gamma(M,P,x,alpha): # Function used to calculate big gamma
    u = 20 # Free Stream velocity as per our simulations
    AnTotal = sumAn(M,P,x,100) 
    A0 = compute_A0(M,P,alpha)
    theta = arccos(1-2*x)
    gamma = 2*u*((A0*(1+cos(theta))/sin(theta)) + AnTotal)
    return gamma






def compute_velocity(M, P, x, y, alpha):
    """
    Computes the net velocity at given points (x, y) by summing induced velocity 
    vectors and free-stream velocity.

    Parameters:
    M : float -> Maximum camber
    P : float -> Position of maximum camber
    x : array-like -> X-coordinates of the points 
    y : array-like -> Y-coordinates of the points 
    alpha : float -> Angle of attack (in radians)

    Returns:
    vel_x, vel_y : array-like -> Components of the velocity vector at (x, y)
    """
    # Ensure x and y are flattened to 1D arrays
    x = np.asarray(x).flatten()  # Shape: (n_points,)
    y = np.asarray(y).flatten()  # Shape: (n_points,)

    u = 20  # Free-stream velocity

    # Generate vortex element positions along the camber line
    vortex_points = np.linspace(0.005, 0.995, 100)  # Shape: (100,)
    yi = camber_line(vortex_points, M, P)  # Camber line heights (Shape: (100,))

    # Broadcast vortex points and circle points to compute distances
    dx = x[:, None] - vortex_points  # Shape: (len(x), 100)
    dy = y[:, None] - yi             # Shape: (len(y), 100)
    r = np.sqrt(dx**2 + dy**2)       # Distances (Shape: (len(x), 100))

    # Compute induced velocity strength for all vortex points and circle points
    gamma = Calculate_gamma(M, P, vortex_points, alpha)  # Circulation strengths (Shape: (100,))
    v_ind = gamma[None, :] * 0.01 / (2 * np.pi * r)      # Induced velocity magnitudes (Shape: (len(x), 100))

    # Compute induced velocity components
    sint = dy / r  # Sine of angle (Shape: (len(x), 100))
    cost = dx / r  # Cosine of angle (Shape: (len(x), 100))
    vel_x_ind = np.sum(v_ind * sint, axis=1)  # Total induced x-velocity (Shape: (len(x),))
    vel_y_ind = np.sum(-v_ind * cost, axis=1) # Total induced y-velocity (Shape: (len(x),))

    # Add free-stream velocity components
    vel_x = vel_x_ind + u * np.cos(alpha)
    vel_y = vel_y_ind + u * np.sin(alpha)
    # print(vel_x,vel_y)
    return vel_x, vel_y  # Return velocity components

     