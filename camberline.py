import numpy as np
import matplotlib.pyplot as plt


def camber_line(x, M, P):
    """
    Computes the camber line y_c and its slope dy_c/dx for given x values.

    Parameters:
    x : numpy array -> Chordwise position (0 to 1)
    M : float -> Maximum camber
    P : float -> Position of maximum camber

    Returns:
    y_c : numpy array -> Camber line values
    dy_c_dx : numpy array -> Slope of camber line
    """
    y_c = np.where(
        x < P, # codition of being less than p 
        (M / P**2) * (2 * P * x - x**2),  
        # Back section (P ≤ x ≤ 1)
        (M / (1 - P)**2) * (1 - 2 * P + 2 * P * x - x**2)
    )

    return y_c
