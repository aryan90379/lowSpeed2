import numpy as np
import matplotlib.pyplot as plt
from camberline import camber_line
from camberSlope import camber_slope_at_x

def plot_camber_line(naca_code):
    """
    Plots the camber line for a given NACA 4-digit airfoil with correct aspect ratio.

    Parameters:
    naca_code : str -> NACA 4-digit code (e.g., "2412")
    """
    # Extract parameters from the NACA code
    M = int(naca_code[0]) / 100  # Max camber
    P = int(naca_code[1]) / 10   # Position of max camber

    # Define chordwise positions (0 to 1)
    x = np.linspace(0, 1, 100)

    # Compute camber line
    y_c = camber_line(x, M, P)

    # Plot
    plt.figure(figsize=(8, 2))  # Adjust figure size
    plt.plot(
        x, y_c, label=f'NACA {naca_code} Camber Line', color='b', linewidth=2)
    plt.axhline(0, color='black', linestyle='--', linewidth=0.8)  # Chord line
    plt.axvline(P, color='r', linestyle=':',
                label=f'Max Camber at x={P}')  # Max camber position
    plt.xlabel("Chord Position (x)")
    plt.ylabel("Camber Line (y_c)")
    plt.title(f'NACA {naca_code} Camber Line Plot')
    plt.legend()
    plt.grid(True)

    # Maintain correct aspect ratio (equal scaling for x and y)
    plt.axis("equal")  # Ensures proper scaling
    plt.show()

# GENERATE THE AIRFOIL PLOT

naca_number = input("type the naca number below: \n ")
plot_camber_line(naca_number)



# CALCULATE THE SLOPE AT A SPECIFIC X POSITION
naca_number = input("Type the NACA number below: \n")
x_value = float(input("Enter the x position (0 to 1): \n"))
slope = camber_slope_at_x(naca_number, x_value)
print(f"The slope at x = {x_value} for NACA {naca_number} is {slope:.6f}")
