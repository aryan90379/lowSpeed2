import numpy as np
from vectorField import compute_velocity,Calculate_gamma
from camberline import camber_line

def compute_circulation(M, P, alpha):
    """
    Compute the circulation around the entire airfoil using velocity line-integral approach at given 
    M -> max camber (0,1)
    P -> positon of it (0,1)
    alpha -> angle in radians 
     
    -> Here we are taking a circle of radius 2m at the orgin   
    """
    # Define angles and precompute trigonometric values
    theta = np.linspace(0, 2 * np.pi, 101)
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    
    # Parametric coordinates and tangential unit vectors
    circle_coords = np.stack((2 * cos_theta, 2 * sin_theta))  # Shape: (2, 101)
    tangents = np.stack((-2 * sin_theta, 2 * cos_theta))      # Shape: (2, 101)
    
    # Compute velocity vectors
    velocity = compute_velocity(M, P, circle_coords[0], circle_coords[1], alpha)  # Shape: (2, 101)
    
    # Compute circulation using vectorized dot product
    circulation = np.sum(tangents[0] * velocity[0] + tangents[1] * velocity[1])  # Element-wise dot product
    
    # Apply integration factor
    circulation *= -2 * np.pi / 100  # Precomputed factor for efficiency

    return circulation



def compute_bound_circulation(M, P, alpha):
    """
    Compute the bound circulation by integrating circulation distribution along camber line
    M -> max camber (0,1)
    P -> positon of it (0,1)
    alpha -> angle in radians
    
    """
    # Define constants
    num_points = 1000
    points = np.linspace(0.0001, 0.9999, num_points)
    
    # Compute camber line values for all points
    y = camber_line(points, M, P)  # Vectorized camber line computation
    y_next = np.roll(y, -1)  # Shift y values to calculate differences
    y_diff = y_next - y  # Vectorized y differences
    
    # Compute gamma values for all points
    gamma = Calculate_gamma(M, P, points, alpha)  # Vectorized gamma computation
    
    # Calculate ds (integration elements) using vectorized operations
    dx = points[1] - points[0]  # Constant step size in x-direction
    ds = np.sqrt(dx**2 + y_diff[:-1]**2)  # Exclude last point to match dimensions
    
    # Compute circulation using vectorized sum
    circulation = np.sum(gamma[:-1] * ds)  # Sum gamma * ds
    return circulation


