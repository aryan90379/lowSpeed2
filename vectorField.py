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
    Computes the net velocity at a given point (x, y) by summing induced velocity 
    vectors and free-stream velocity.

    Parameters:
    M : float -> Maximum camber
    P : float -> Position of maximum camber
    x : float -> X-coordinate of the point
    y : float -> Y-coordinate of the point
    alpha : float -> Angle of attack (in radians)

    Returns:
    vel_x, vel_y : list -> Components of the velocity vector at (x, y)
    """
    u = 30  # Free-stream velocity
    vel_x, vel_y = 0, 0  # Initialize velocity components

    # Iterate over vortex elements along the camber line, ignoring points near edges
    for i in np.linspace(0.005, 0.995, 100):
        yi = camber_line(i, M, P)  # Get camber line height at i
        # print(i,yi)
        r = np.sqrt((x - i)**2 + (y - yi)**2)  # Distance from vortex element

        # Compute induced velocity using circulation strength
        v_ind = Calculate_gamma(M, P, i, alpha) * 0.01 / (2 * np.pi * r)

        # Compute velocity components due to induced flow
        cost = (x - i) / r
        sint = (y - yi) / r
        vel_x += v_ind * sint
        vel_y -= v_ind * cost

    # Add free-stream velocity components
    vel_x += u * np.cos(alpha)
    vel_y += u * np.sin(alpha)

    return [vel_x, vel_y]  # Return velocity components
  #Return X and Y component of velocity

def compute_vector_plot(M,P,alpha): # Compute vector field using quiver function and calling the velocity function
    u = 30
    x_cdn,y_cdn = meshgrid(linspace(-1,2,20),linspace(-2,2,30))
    c,d = compute_velocity(M, P, x_cdn, y_cdn, alpha)
    magnitude = sqrt(c**2 + d**2)
    quiver(x_cdn,y_cdn,c,d,magnitude,cmap='turbo',scale=900)
    colorbar()
    # plot_naca_airfoil(m, p)
    x_coords = linspace(0,1,1000)
    y_coords = []
    for i in x_coords :
        y_coords.append(camber_line(i,M,P))
    plot(x_coords,y_coords)
    show()

# compute_vector_plot(0.7,0.4,0.01) # Call the function toplot the vector field
     