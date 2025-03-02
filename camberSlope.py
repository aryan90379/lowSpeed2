import numpy as np
import matplotlib.pyplot as plt
def camber_slope_at_x(naca_code, x_point):
    """
    Computes the slope dy_c/dx of the camber line at a specific x position.

    Parameters:
    naca_code : str -> NACA 4-digit code (e.g., "2412")
    x_point : float -> Specific chordwise position (0 to 1)

    Returns:
    dy_c_dx : float -> Slope of the camber line at x_point
    """
    # Extract parameters from the NACA code
    M = int(naca_code[0]) / 100  # Max camber
    P = int(naca_code[1]) / 10   # Position of max camber

    # Compute slope based on x position
    if x_point < P:
        dy_c_dx = (2 * M / P**2) * (P - x_point)
    else:
        dy_c_dx = (2 * M / (1 - P)**2) * (P - x_point)

    return dy_c_dx

