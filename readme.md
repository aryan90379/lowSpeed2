# Airfoil Web UI

- Provides a Streamlit Web UI for visualizing and analyzing airfoils.
- Supports both NACA airfoils and user-defined airfoils (polynomial input).
- Computes lift coefficient (Cl) for NACA and custom airfoils.
- Calculates camber line and camber slope based on input parameters.
- Displays vector field around the airfoil for flow visualization.
- Computes circulation using velocity line integrals.
- Calls relevant functions dynamically based on user input.

## Project Structure

- `showAirfoil.py`: Main UI that integrates all functions.
- `calculateCl.py`: Computes A0, An, and Cl for NACA and polynomial airfoils.
- `camber_line.py`: Computes camber line (M, P, x as inputs).
- `camber_slope.py`: Computes camber slope (M, P, x as inputs).
- `vector_field.py`:  
  - Computes velocity field (M, P, x, y, α).  
  - Includes `calculate_gamma()` for circulation strength and `SumAn()` for summing Aₙ values.
- `circulation.py`:  
  - `compute_circulation()`: Computes circulation for given (M, P, α).  
  - `compute_bound_circulation()`: Computes bound circulation (M, P, α).

## Running the Application

```sh
# Install dependencies
pip install streamlit numpy matplotlib scipy

# Run the UI (ensure you're in the correct directory)
python -m streamlit run showAirfoil.py



