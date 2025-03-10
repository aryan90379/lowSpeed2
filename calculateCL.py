import numpy as np

def compute_A0(M, P, alpha):
    """
    Compute the value of A0 , the fourier constant used in our thin airfoil theory derivation
    """
    points_integration = np.linspace(0, np.pi, 1001)  
    x = (1 - np.cos(points_integration)) / 2  # Compute x values

    # Compute dz/dx using vectorized approach
    dz_dx = np.where(x < P, (2 * M / P**2) * (P - x), (2 * M / (1 - P)**2) * (P - x))
    
    #Integrating using trapezoid
    integral = np.trapz(dz_dx, points_integration)
    
    # Compute A0
    A0 = alpha - integral / np.pi  
    return A0

def compute_An(M,P,n):  
    """
    Compute the value of An , the fourier constant used in our thin airfoil theory derivation
    """
    points_integration = np.linspace(0, np.pi, 1001)  
    x = (1 - np.cos(points_integration)) / 2  # Compute x values

    # Compute dz/dx using vectorized approach
    dz_dx = np.where(x < P, (2 * M / P**2) * (P - x), (2 * M / (1 - P)**2) * (P - x))

    # Compute cos(nθ) term
    cos_n_theta = np.cos(n * points_integration)


    integral = np.trapz(dz_dx * cos_n_theta, points_integration)

    # Compute An
    An = (2 / np.pi) * integral  
    return An

def compute_Cl(M,P, alpha):
    """
    Computes the lift coefficient Cl for a thin airfoil.

    Returns:
    Cl : float -> Lift coefficient
    """

    
    A0 = compute_A0(M, P, alpha)
    A1 = compute_An(M, P, 1)  # Only A1 is needed
    
    Cl = np.pi * (2 * A0 + A1)
    return Cl



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
    A0 = alpha - (1 / np.pi) * integral
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





