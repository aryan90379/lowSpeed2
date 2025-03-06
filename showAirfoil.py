import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from camberline import camber_line
from camberSlope import camber_slope_at_x
from calculateCL import compute_Cl, compute_Cl_poly
st.set_page_config(layout="wide")

# 🔷 **Global Styling**
st.markdown(
    """
    <style>
    /* Make everything look smoother */
    .stSlider, .stNumberInput { margin-top: -10px !important; }
    .stButton>button { 
        background: linear-gradient(to right, #0078FF, #00C6FF); 
        color: white; 
        font-size: 18px; 
        border-radius: 12px; 
        padding: 8px 20px;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover { 
        background: linear-gradient(to right, #0056b3, #009ac9); 
        transform: scale(1.05);
    }
    .stTextInput>div>div>input {
        font-size: 16px;
        padding: 6px;
        border-radius: 8px;
    }
    .stNumberInput>div>div>input {
        font-size: 16px;
        padding: 6px;
        border-radius: 8px;
    }
    .stSlider>div {
        padding: 5px 0;
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
        naca_number = st.text_input("Enter NACA 4-digit Code", "2412")

        if naca_number.isdigit() and len(naca_number) == 4:
            M = int(naca_number[0]) / 100
            P = int(naca_number[1]) / 10
            x = np.linspace(0, 1, 200)
            y_c = camber_line(x, M, P)
        else:
            st.error("❌ Please enter a valid 4-digit NACA code.")
            st.stop()

    else:  # User-defined function
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
            slope = camber_slope_at_x(naca_number, x_value)
        else:
            deriv = np.polyder(coeffs)  # Compute derivative directly from coefficients
            slope = np.polyval(deriv, x_value)
        st.success(f"**Slope at x = {x_value:.6f}:** `{slope:.6f}`")

    # 🔹 Compute Lift Coefficient (Cl)
    st.subheader("Compute Lift Coefficient (Cl)")

    alpha = st.number_input("Enter Angle of Attack (°)", value=2.0, step=0.1, format="%.2f")

    if option == "NACA 4-Digit":
        if st.button("Compute Cl for NACA Airfoil"):
            Cl = compute_Cl(naca_number, alpha)
            st.success(f"**Cl for NACA {naca_number} at {alpha}°:** `{Cl:.4f}`")
    else:
        if st.button("Compute Cl for Polynomial Camber"):
            Cl_poly = compute_Cl_poly(coeffs, alpha)
            st.success(f"**Cl for polynomial camber at {alpha}°:** `{Cl_poly:.6f}`")

with col2:
    st.subheader("Airfoil & Camber Line Visualization")

    fig, ax = plt.subplots(figsize=(8, 3))  # Reduce width for a more compact look

    # Plot camber line
    ax.plot(
        x, y_c, 
        label=f'{"NACA " + naca_number if option == "NACA 4-Digit" else "User-Defined Camber"}',
        color='#0078FF', linewidth=1
    )

    # Airfoil Thickness Calculation (Approximate)
    def thickness_distribution(x, t=0.12):
        """Approximate symmetric thickness distribution for visualization"""
        return 5 * t * (0.2969 * np.sqrt(x) - 0.126 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)

    y_t = thickness_distribution(x)  # Compute thickness distribution

    # Compute airfoil upper and lower surfaces
    y_upper = y_c + y_t
    y_lower = y_c - y_t

    # Plot airfoil shape
    ax.plot(x, y_upper, color='black', linewidth=1, label="Airfoil Upper Surface")
    ax.plot(x, y_lower, color='black', linewidth=1, label="Airfoil Lower Surface")

    # Highlight max camber for NACA
    if option == "NACA 4-Digit":
        ax.axvline(P, color='r', linestyle=':', linewidth=1, alpha=0.7, label=f'Max Camber at x={P}')
        ax.text(P + 0.02, max(y_c) * 0.8, "Max Camber", color='r', fontsize=12, fontweight='bold')

    # 🖥️ **Enhanced Axis Labels & Title**
    ax.set_xlabel("Chord Position", fontsize=14, fontweight='bold')
    ax.set_ylabel("Vertical Position", fontsize=14, fontweight='bold')
    ax.set_title(
        f'{"✈️ NACA " + naca_number if option == "NACA 4-Digit" else "User-Defined Airfoil"}',
        fontsize=16, color='#0078FF'
    )
    ax.legend(fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.6)

    # Keep equal aspect ratio
    ax.set_aspect('equal', adjustable='datalim')

    st.pyplot(fig)
    
    
    # slope vs x graph
    # 🔹 Compute and plot slope vs. x
    st.subheader("Slope of Camber Line vs. Chord Position")

    # Compute slope distribution
    if option == "NACA 4-Digit":
        slopes = np.array([camber_slope_at_x(naca_number, xi) for xi in x])
    else:
        deriv = np.polyder(coeffs)  # Compute derivative from polynomial
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

    

    
    

