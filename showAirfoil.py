import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from camberline import camber_line
from camberSlope import camber_slope_at_x
from calculateCL import compute_Cl, compute_Cl_poly
from vectorField import compute_velocity
from vectorFieldUDF import compute_velocity_poly
from Circulation import compute_circulation,compute_bound_circulation 
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    /* Make input elements sleek */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>textarea {
        font-size: 16px;
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #0078FF;
        box-shadow: 0px 4px 10px rgba(0, 120, 255, 0.2);
        transition: all 0.3s ease-in-out;
    }
    
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus, .stTextArea>div>textarea:focus {
        border-color: #00C6FF;
        box-shadow: 0px 4px 15px rgba(0, 198, 255, 0.4);
    }

    /* Style sliders */
    .stSlider>div {
        padding: 8px 0;
    }

    /* Modern buttons */
    .stButton>button { 
        background: linear-gradient(to right, #0078FF, #00C6FF); 
        color: white; 
        font-size: 18px; 
        font-weight: bold;
        border-radius: 12px; 
        padding: 10px 25px;
        border: none;
        box-shadow: 0px 5px 15px rgba(0, 120, 255, 0.3);
        transition: all 0.3s ease-in-out;
    }

    .stButton>button:hover { 
        background: linear-gradient(to right, #0056b3, #009ac9); 
        transform: scale(1.08);
        box-shadow: 0px 8px 20px rgba(0, 120, 255, 0.5);
    }

    /* Stylish select box */
    .stSelectbox>div>div {
        border-radius: 8px;
        border: 2px solid #0078FF;
        box-shadow: 0px 4px 10px rgba(0, 120, 255, 0.2);
        transition: all 0.3s ease-in-out;
    }

    /* Checkbox style */
    .stCheckbox>div {
        padding: 5px;
        border-radius: 8px;
        transition: all 0.3s ease-in-out;
    }

    /* Headers & Titles */
    h1, h2, h3, h4 {
        font-weight: bold;
        color: #0078FF;
        text-shadow: 1px 1px 4px rgba(0, 120, 255, 0.3);
    }

    /* Styling Expander */
    .stExpander>summary {
        font-size: 16px;
        font-weight: bold;
        color: white;
        background: linear-gradient(to right, #0078FF, #00C6FF);
        padding: 10px;
        border-radius: 10px;
        cursor: pointer;
        box-shadow: 0px 4px 12px rgba(0, 120, 255, 0.3);
    }
    
    /* Progress bar */
    .stProgress>div>div>div {
        background: linear-gradient(to right, #0078FF, #00C6FF);
        border-radius: 10px;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)


st.title("NACA & Custom Camber Line Plotter")

option = st.selectbox(
    "Choose Camber Definition:",
    ["NACA 4-Digit", "User-Defined Function"]
)

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Input Parameters")

    if option == "NACA 4-Digit":
        M = st.number_input("Enter Maximum Camber (M) [0-1]", min_value=0.0, max_value=1.0, value=0.02, step=0.001, format="%.3f")
        P = st.number_input("Enter Position of Maximum Camber (P) [0-1]", min_value=0.0, max_value=1.0, value=0.4, step=0.001, format="%.3f")
        T = st.number_input("Enter Maximum Thickness (T) [0-1]", min_value=0.0, max_value=1.0, value=0.12, step=0.001, format="%.3f")

        x = np.linspace(0, 1, 200)
        y_c = camber_line(x, M, P)
    

    else:  # User-defined polynomial camber function
        coeffs_input = st.text_input(
            "✏️ Enter polynomial coefficients (comma-separated)", 
            "0.1, -0.05, 0.02, -0.01, 0.29"
        )

        try:
            coeffs = [float(c.strip()) for c in coeffs_input.split(",")]
            x = np.linspace(0, 1, 200)
            y_c = np.polyval(coeffs, x)  # Use polynomial coefficients for camber line
        except ValueError:
            st.error("❌ Invalid coefficients! Please enter numeric values separated by commas.")
            st.stop()

    # 🔹 **Ensure slider and number input sync**
    if "x_value" not in st.session_state:
        st.session_state.x_value = 0.5  # Default value

    def update_x_slider():
        """Update slider when number input changes."""
        st.session_state.x_slider = st.session_state.x_value

    def update_x_number():
        """Update number input when slider changes."""
        st.session_state.x_value = st.session_state.x_slider

    st.write("### Select x Position (0 to 1)")
    x_value = st.number_input(
        "Enter exact x position",
        min_value=0.0, max_value=1.0,
        value=st.session_state.x_value,
        step=0.0001, format="%.6f",
        key="x_value", on_change=update_x_slider
    )
    x_slider = st.slider(
        "Slide to select x position",
        min_value=0.0, max_value=1.0,
        value=st.session_state.x_value,
        step=0.0001, format="%.6f",
        key="x_slider", on_change=update_x_number
    )

    # Ensure latest synchronized value is used
    x_value = st.session_state.x_value

    if st.button("Calculate Slope"):
        if option == "NACA 4-Digit":
            slope = camber_slope_at_x_custom(M, P, x_value)
        else:
            deriv = np.polyder(coeffs)  # Compute derivative directly from coefficients
            slope = np.polyval(deriv, x_value)
        st.success(f"**Slope at x = {x_value:.6f}:** `{slope:.6f}`")

    # 🔹 Compute Lift Coefficient (Cl)
    st.subheader("Compute Lift Coefficient (Cl)")

    alpha = st.number_input("Enter Angle of Attack (°)", value=2.0, step=0.1, format="%.2f")

    if option == "NACA 4-Digit":
        if st.button("Compute Cl for NACA Airfoil"):
            Cl = compute_Cl(M, P, (alpha*np.pi)/180)
            st.success(f"**Cl for NACA airfoil at {alpha}°:** `{Cl:.4f}`")
    else:
        if st.button("Compute Cl for Polynomial Camber"):
            Cl_poly = compute_Cl_poly(coeffs, (alpha*np.pi)/180)
            st.success(f"**Cl for polynomial camber at {alpha}°:** `{Cl_poly:.6f}`")
            
            
    # ---------------------
    # CIRCULATION DUE TO VELOCITY LINE INTEGRAL
            
            
    if option == "NACA 4-Digit":
        st.subheader("Circulation (Velocity Line Integral)")
        alpha1 = st.number_input("Enter Angle of Attack (°)", value=2.0, step=0.1, format="%.2f", key="alpha_input")

        if st.button("Compute Circulation", key="compute_circulation_btn"):
            # Show an initial status message
            status = st.status("Computing circulation...", expanded=True)

            # Compute circulation
            circulation = compute_circulation(M, P, ((alpha1*np.pi)/180))

            # Update the status message
            status.update(label="Computation complete!", state="complete", expanded=False)

            st.success(f"**Circulation at {alpha1}°:** `{circulation:.4f}`")


    if option == "NACA 4-Digit":
        st.subheader("Bound Circulation (Integrating Circulation Distribution)")
        
        alpha2 = st.number_input(
            "Enter Angle of Attack (°)", 
            value=2.0, 
            step=0.1, 
            format="%.2f", 
            key="alpha_input_For_Bound"
        )

        if st.button("Compute Circulation", key="compute_bound_circulation_btn"):
            # Show an initial status message
            status = st.status("Computing circulation...", expanded=True)
            
            # Compute circulation
            circulation = compute_bound_circulation(M, P, ((alpha2*np.pi)/180))

            # Update the status message
            status.update(label="Computation complete!", state="complete", expanded=False)
            
            st.success(f"**Bound Circulation at {alpha2}°:** `{circulation:.4f}`")


with col2:
    st.subheader("Airfoil Analysis")

    # Dropdown for selecting which graph to show
    option_selected = st.selectbox(
        "Select a Plot to Display:",
        ["Airfoil & Camber Line", "Slope vs Chord Position", "Lift Coefficient vs Angle of Attack", "Vector Field Plot"]
    )

    if option_selected == "Airfoil & Camber Line":
        st.subheader("Airfoil & Camber Line Visualization")
        fig, ax = plt.subplots(figsize=(8, 3))

        # Plot camber line
        ax.plot(x, y_c, label="Camber Line", color='#0078FF', linewidth=1)

        # Compute airfoil thickness
        def thickness_distribution(x, t=0.10):
            return 5 * t * (0.2969 * np.sqrt(x) - 0.126 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)

        y_t = thickness_distribution(x, T)
        y_upper, y_lower = y_c + y_t, y_c - y_t

        # Plot upper & lower surfaces
        ax.plot(x, y_upper, color='black', linewidth=1, label="Airfoil Upper Surface")
        ax.plot(x, y_lower, color='black', linewidth=1, label="Airfoil Lower Surface")

        # Formatting
        ax.set_xlabel("Chord Position", fontsize=14, fontweight='bold')
        ax.set_ylabel("Vertical Position", fontsize=14, fontweight='bold')
        ax.set_title("Airfoil & Camber Line", fontsize=16, color='#0078FF')
        ax.legend(fontsize=12)
        ax.set_xlim(0, 1)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.set_aspect('equal', adjustable='datalim')

        st.pyplot(fig)

    elif option_selected == "Slope vs Chord Position":
        st.subheader("Slope of Camber Line vs. Chord Position")

        # Compute slope distribution
        if option == "NACA 4-Digit":
            slopes = np.array([camber_slope_at_x(M, P, xi) for xi in x])
        else:
            deriv = np.polyder(coeffs)
            slopes = np.polyval(deriv, x)

        # Create slope plot
        fig_slope, ax_slope = plt.subplots(figsize=(8, 3))
        ax_slope.plot(x, slopes, color='r', linewidth=1.5, label="Camber Slope (dy/dx)")

        # Highlight maximum slope
        max_idx = np.argmax(np.abs(slopes))
        ax_slope.scatter(x[max_idx], slopes[max_idx], color='black', zorder=3, label="Max Slope")

        # Formatting
        ax_slope.set_xlabel("Chord Position (x)", fontsize=12, fontweight='bold')
        ax_slope.set_ylabel("Camber Slope (dy/dx)", fontsize=12, fontweight='bold')
        ax_slope.set_title("Slope Distribution Along Chord", fontsize=14, color='r')
        ax_slope.axhline(0, color="gray", linestyle="--", linewidth=1)
        ax_slope.legend(fontsize=10)
        ax_slope.grid(True, linestyle="--", alpha=0.5)
        ax_slope.set_xlim(0, 1)

        st.pyplot(fig_slope)

    elif option_selected == "Lift Coefficient vs Angle of Attack":
        st.subheader("Lift Coefficient (Cl) vs Angle of Attack (α)")
        alpha_range = np.linspace(-10, 15, 100)

        if option == "NACA 4-Digit":
            Cl_values = np.array([compute_Cl(M, P, a) for a in alpha_range])
        else:
            Cl_values = np.array([compute_Cl_poly(coeffs, a) for a in alpha_range])

        # Save data to CSV
        df = pd.DataFrame({"Angle_of_Attack (α)": alpha_range, "Lift_Coefficient (Cl)": Cl_values})
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        # Download button
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="Cl_vs_Alpha.csv",
            mime="text/csv"
        )

        # Create Cl vs Alpha plot
        fig_Cl, ax_Cl = plt.subplots(figsize=(8, 3))
        ax_Cl.plot(alpha_range, Cl_values, color='g', linewidth=1.5, label="Lift Coefficient (Cl)")

        # Highlight zero-lift angle
        zero_lift_idx = np.argmin(np.abs(Cl_values))
        ax_Cl.axvline(alpha_range[zero_lift_idx], color='r', linestyle='--', linewidth=1, alpha=0.7, label="Zero-Lift Angle")
        ax_Cl.scatter(alpha_range[zero_lift_idx], Cl_values[zero_lift_idx], color='black', zorder=3)

        # Formatting
        ax_Cl.set_xlabel("Angle of Attack (α)", fontsize=12, fontweight='bold')
        ax_Cl.set_ylabel("Lift Coefficient (Cl)", fontsize=12, fontweight='bold')
        ax_Cl.set_title("Lift Coefficient vs Angle of Attack", fontsize=14, color='g')
        ax_Cl.axhline(0, color="gray", linestyle="--", linewidth=1)
        ax_Cl.legend(fontsize=10)
        ax_Cl.grid(True, linestyle="--", alpha=0.5)

        st.pyplot(fig_Cl)

    elif option_selected == "Vector Field Plot":
        st.subheader("Vector Field Plot")

        alpha = st.number_input("Angle of Attack (α in degrees)", min_value=-10.0, max_value=15.0, value=0.01)
        alpha_rad = np.radians(alpha)

        fig, ax = plt.subplots(figsize=(9, 4))
        x_cdn, y_cdn = np.meshgrid(np.linspace(-1.5, 2.5, 30), np.linspace(-1, 2, 20))

        if option == "NACA 4-Digit":
            slopes = np.array([camber_slope_at_x(M, P, xi) for xi in x])
            c, d = compute_velocity(M, P, x_cdn, y_cdn, alpha_rad)
        else:
            c, d = compute_velocity_poly(coeffs, x_cdn, y_cdn, alpha_rad)

        magnitude = np.sqrt(c**2 + d**2)

        q = ax.quiver(x_cdn, y_cdn, c, d, magnitude, cmap='turbo', scale=900, width=0.003, edgecolors='k', alpha=0.8)
        cb = plt.colorbar(q, ax=ax, shrink=0.8, aspect=20, pad=0.02)
        cb.set_label("Vector Magnitude", fontsize=12, weight='bold')

        # Plot camber line
        x_coords = np.linspace(0, 1, 1000)
        y_coords = np.polyval(coeffs, x_coords) if option != "NACA 4-Digit" else [camber_line(i, M, P) for i in x_coords]
        ax.plot(x_coords, y_coords, color="black", linewidth=1.5)

        ax.set_xlabel("X-Coordinate")
        ax.set_ylabel("Y-Coordinate")
        ax.set_title("Velocity Vector Field Around Airfoil")
        ax.set_xlim(-1.5, 2.5)
        ax.set_ylim(-1, 2)
        ax.grid(True, linestyle="--", alpha=0.5)

        st.pyplot(fig)



             
