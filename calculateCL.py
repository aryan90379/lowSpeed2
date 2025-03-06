import numpy as np

def compute_A0(M, P, alpha):
    """
    Compute A0 coefficient using the camber slope equation.
    
    Parameters:
    M : float -> Maximum camber
    P : float -> Position of maximum camber
    alpha : float -> Angle of attack in degrees
    
    Returns:
    A0 : float
    """
    theta = np.linspace(0.01, np.pi-0.01, 1000)  # Discretizing the integral
    x = (1 - np.cos(theta))/2  # Transforming to x-coordinates
    dz_dx = np.where(
        x < P, 
        (2 * M / P**2) * (P - x),
        (2 * M / (1 - P)**2) * (P - x)
    )
    
    integral = np.trapz(dz_dx, theta)  # Numerical integration
    A0 = np.radians(alpha) - (1 / np.pi) * integral
    return A0

def compute_An(M, P, n):
    """
    Compute An coefficients for thin airfoil theory.

    Parameters:
    M : float -> Maximum camber
    P : float -> Position of maximum camber
    n : int -> Fourier coefficient index

    Returns:
    An : float
    """
    theta = np.linspace(0.01, np.pi-0.01, 1000)
    x = (1 - np.cos(theta)) / 2
    dz_dx = np.where(
        x < P, 
        (2 * M / P**2) * (P - x),
        (2 * M / (1 - P)**2) * (P - x)
    )
    
    integrand = dz_dx * np.cos(n * theta)
    integral = np.trapz(integrand, theta)  # Numerical integration
    An = (2 / np.pi) * integral
    return An

def compute_Cl(naca_code, alpha):
    """
    Computes the lift coefficient Cl for a thin airfoil.

    Parameters:
    naca_code : str -> NACA 4-digit code (e.g., "2412")
    alpha : float -> Angle of attack in degrees

    Returns:
    Cl : float -> Lift coefficient
    """
    M = int(naca_code[0]) / 100  # Max camber
    P = int(naca_code[1]) / 10   # Position of max camber
    
    A0 = compute_A0(M, P, alpha)
    A1 = compute_An(M, P, 1)  # Only A1 is needed
    
    Cl = np.pi * (2 * A0 + A1)
    return Cl


import numpy as np

def compute_A0_poly(coeffs, alpha):
    """
    Compute A0 coefficient using a user-defined polynomial camber function.

    Parameters:
    coeffs : list -> Coefficients of the polynomial [a_n, ..., a_1, a_0] (highest order first)
    alpha : float -> Angle of attack in degrees

    Returns:
    A0 : float
    """
    theta = np.linspace(0.01, np.pi-0.01, 1000)  # Higher precision
    x = (1 - np.cos(theta)) / 2  # Transform to x-coordinates
    
    poly_derivative = np.polyder(coeffs)  # Differentiate camber function
    dz_dx = np.polyval(poly_derivative, x)  # Evaluate slope at x values

    integral = np.trapz(dz_dx, theta)  # Numerical integration
    A0 = np.radians(alpha) - (1 / np.pi) * integral
    return A0

def compute_An_poly(coeffs, n):
    """
    Compute An coefficients for a user-defined polynomial camber function.

    Parameters:
    coeffs : list -> Coefficients of the polynomial [a_n, ..., a_1, a_0] (highest order first)
    n : int -> Fourier coefficient index

    Returns:
    An : float
    """
    theta = np.linspace(0.01, np.pi-0.01, 1000)  # Higher precision
    x = (1 - np.cos(theta)) / 2  # Transform to x-coordinates
    
    poly_derivative = np.polyder(coeffs)  # Differentiate camber function
    dz_dx = np.polyval(poly_derivative, x)  # Evaluate slope at x values

    integrand = dz_dx * np.cos(n * theta)
    integral = np.trapz(integrand, theta)  # Numerical integration
    An = (2 / np.pi) * integral
    
    return An

def compute_Cl_poly(coeffs, alpha):
    """
    Computes the lift coefficient Cl for a user-defined polynomial camber airfoil.

    Parameters:
    coeffs : list -> Coefficients of the polynomial [a_n, ..., a_1, a_0] (highest order first)
    alpha : float -> Angle of attack in degrees

    Returns:
    Cl : float -> Lift coefficient
    """
    A0 = compute_A0_poly(coeffs, alpha)
    A1 = compute_An_poly(coeffs, 1)  # Only A1 is needed
    
    Cl = np.pi * (2 * A0 + A1)
    return Cl

# # Example usage for a custom polynomial camber function
# coeffs = [0.1, -0.05, 0.02, -0.01,0.29]  # Example: 0.1x³ - 0.05x² + 0.02x - 0.01
# alpha = 3  # Angle of attack in degrees

# Cl_poly = compute_Cl_poly(coeffs, alpha)
# print(f"Cl for polynomial camber at {alpha}°: {Cl_poly:.6f}")



# # Example usage:
# naca = "2412"  # NACA 2412 airfoil
# alpha = 2  # Angle of attack in degrees
# Cl = compute_Cl(naca, alpha)
# print(f"Cl for {naca} at {alpha}°: {Cl:.4f}")


import numpy as np

def compute_Circulation(naca_code, alpha, U_inf, chord):
    """
    Computes the circulation for a given NACA airfoil using thin airfoil theory.

    Parameters:
    naca_code : str -> NACA 4-digit code (e.g., "2412")
    alpha : float -> Angle of attack in degrees
    U_inf : float -> Free-stream velocity
    chord : float -> Chord length of the airfoil

    Returns:
    Gamma : float -> Circulation value
    """
    M = int(naca_code[0]) / 100  # Max camber
    P = int(naca_code[1]) / 10   # Position of max camber
    
    A0 = compute_A0(M, P, alpha)
    A1 = compute_An(M, P, 1)  # Only A1 is needed

    # Circulation formula
    Gamma = chord * U_inf * (np.pi * A0 + (np.pi / 2) * A1)
    return Gamma

def compute_Circulation_poly(coeffs, alpha, U_inf, chord):
    """
    Computes the circulation for an airfoil defined by a polynomial camber function.

    Parameters:
    coeffs : list -> Coefficients of the polynomial [a_n, ..., a_1, a_0] (highest order first)
    alpha : float -> Angle of attack in degrees
    U_inf : float -> Free-stream velocity
    chord : float -> Chord length of the airfoil

    Returns:
    Gamma : float -> Circulation value
    """
    A0 = compute_A0_poly(coeffs, alpha)
    A1 = compute_An_poly(coeffs, 1)  # Only A1 is needed

    # Circulation formula
    Gamma = chord * U_inf * (np.pi * A0 + (np.pi / 2) * A1)
    return Gamma

# Example usage for NACA airfoil
naca = "2412"
alpha = 2  # Angle of attack in degrees
U_inf = 20  # Free stream velocity (m/s)
chord = 1.0  # Chord length in meters

Gamma_naca = compute_Circulation(naca, alpha, U_inf, chord)
# print(f"Circulation for {naca} at {alpha}°: {Gamma_naca:.6f} m²/s")

# Example usage for Polynomial camber function
coeffs = [0.1, -0.05, 0.02, -0.01, 0.29]  # Example: 0.1x³ - 0.05x² + 0.02x - 0.01
Gamma_poly = compute_Circulation_poly(coeffs, alpha, U_inf, chord)
# print(f"Circulation for polynomial camber at {alpha}°: {Gamma_poly:.6f} m²/s")



