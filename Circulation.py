import numpy as np
from vectorField import compute_velocity,Calculate_gamma
from camberline import camber_line

def compute_circulation(M, P, alpha):
    # Generate theta values in a single step
    
    theta = np.linspace(0, 2*np.pi, 101)

    # Parametric coordinates of a circle centered at the origin
    x_cdn = 2 * np.cos(theta)
    y_cdn = 2 * np.sin(theta)

    # Tangential unit vectors
    tangent_x = -2 * np.sin(theta)
    tangent_y = 2 * np.cos(theta)

    # Compute velocities for all points at once (assuming vectorized compute_velocity)
    velocity_x, velocity_y = compute_velocity(M, P, x_cdn, y_cdn, np.radians(alpha))

    # Compute circulation using vectorized dot product
    circulation = np.dot(tangent_x, velocity_x) + np.dot(tangent_y, velocity_y)

    # Apply final scaling factors
    circulation *= -2 * np.pi / 100  # Sign convention 

    return circulation

import numpy as np

def compute_bound_circulation(M, P, alpha):
    u = 30
    num_points = 1000 # Change as per requirement of precision
    
    # Generate x-coordinates for integration
    points = np.linspace(0.0001, 0.9999, num_points)
    
    # Compute y-coordinates in a vectorized manner
    y = np.array([camber_line(x, M, P) for x in points])
    
    
    # Compute gamma values in a vectorized manner
    gamma_local = np.array([Calculate_gamma(M, P, x, alpha) for x in points])

    # Compute ds using NumPy operations
    dy = np.diff(y)  # Compute differences in y
    dx = np.full(num_points - 1, 0.001)  # dx is constant
    ds = np.sqrt(dx**2 + dy**2)  # Element-wise sqrt for ds

    # Compute circulation using vectorized dot product
    circulation = np.dot(gamma_local[:-1], ds)

    print("Bound circulation =", circulation)
    return circulation


print(compute_circulation(0.2, 0.4, 3))  # Example
