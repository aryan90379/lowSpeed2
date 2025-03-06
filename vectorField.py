from numpy import *
import matplotlib.pyplot as plt
from camberline import camber_line
from calculateCL import compute_A0, compute_An
# Ensure camber_line function is correctly imported

def sumAn(M, P, x, n):
    """Performs summation of small gamma."""
    Sum = 0
    theta = arccos(1 - 2 * x)
    for i in range(1, n):
        Sum += compute_An(M, P, i) * sin(i * theta)
    return Sum

def Calculate_gamma(M, P, x, alpha):
    """Calculates circulation Gamma."""
    u = 20  # Free-stream velocity
    AnTotal = sumAn(M, P, x, 100)
    A0 = compute_A0(M, P, alpha)
    theta = arccos(1 - 2 * x)
    gamma = 2 * u * ((A0 * (1 + cos(theta)) / sin(theta)) + AnTotal)
    return gamma

def compute_velocity(M, P, x, y, alpha):
    """Computes velocity components at (x, y) using Biot-Savart law."""
    u = 30  # Free-stream velocity
    vel_x, vel_y = 0, 0  # Initialize velocity components

    for i in linspace(0.005, 0.995, 100):  # Avoid 0 & 1 to prevent singularities
        yi = camber_line(i, M, P)  # Get camber line height
        r_sq = (x - i)**2 + (y - yi)**2  # Squared distance from vortex element

        if r_sq == 0:
            continue  # Prevent division by zero

        r = sqrt(r_sq)
        v_ind = Calculate_gamma(M, P, i, alpha) * 0.01 / (2 * pi * r)  # Induced velocity

        # Velocity components
        cost = (x - i) / r
        sint = (y - yi) / r
        vel_x += v_ind * sint
        vel_y -= v_ind * cost

    # Add free-stream velocity
    vel_x += u * cos(alpha)
    vel_y += u * sin(alpha)

    return vel_x, vel_y  # Return velocity components

def compute_vector_plot(M, P, alpha):
    """Plots vector field using quiver."""
    x_cdn, y_cdn = meshgrid(linspace(-1, 2, 20), linspace(-2, 2, 30))
    c = zeros_like(x_cdn)
    d = zeros_like(y_cdn)

    for i in range(x_cdn.shape[0]):
        for j in range(x_cdn.shape[1]):
            c[i, j], d[i, j] = compute_velocity(M, P, x_cdn[i, j], y_cdn[i, j], alpha)

    plt.figure(figsize=(10, 5))
    plt.quiver(x_cdn, y_cdn, c, d, color="b", alpha=0.6)

    # Plot camber line
    x_coords = linspace(0, 1, 1000)
    y_coords = [camber_line(i, M, P) for i in x_coords]
    plt.plot(x_coords, y_coords, "r-", linewidth=2, label="Camber Line (Airfoil)")

    plt.xlabel("Chordwise Position")
    plt.ylabel("Vertical Position")
    plt.title("Airflow Around an Airfoil (Biot-Savart Law)")
    plt.legend()
    plt.xlim(-1, 2)
    plt.ylim(-2, 2)
    plt.grid(True)
    plt.show()

compute_vector_plot(0.1, 4, 0.02)  # Call function to plot the vector field
