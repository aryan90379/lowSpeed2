import numpy as np
import matplotlib.pyplot as plt
def camber_slope_at_x(M,P, x_point):
    """
    Computes the slope dy_c/dx of the camber line at a specific x position.

    Parameters:
    M = Max Camber
    P = Position of Max Camber
    x_point : float -> Specific chordwise position (0 to 1), or an Array

    Returns:
    dy_c_dx : float -> Slope of the camber line at x_point
    """
    # Compute slope based on x position
    if x_point < P:
        dy_c_dx = (2 * M / P**2) * (P - x_point)
    else:
        dy_c_dx = (2 * M / (1 - P)**2) * (P - x_point)

    return dy_c_dx

