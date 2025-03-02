import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from camberline import camber_line
from camberSlope import camber_slope_at_x

st.set_page_config(layout="wide")

st.title("✈️ NACA Airfoil Camber Line Plotter")

st.markdown(
    """
    <style>
    .stSlider, .stNumberInput { margin-top: -10px !important; }
    .stButton>button { background: #0078FF; color: white; font-size: 16px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True
)

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("🔢 Input Parameters")

    # NACA Number Input
    naca_number = st.text_input("Enter NACA 4-digit Code", "2412")

    if naca_number.isdigit() and len(naca_number) == 4:
        M = int(naca_number[0]) / 100
        P = int(naca_number[1]) / 10

        # Generate camber line data
        x = np.linspace(0, 1, 200)
        y_c = camber_line(x, M, P)

        st.write("### Select x Position (0 to 1)")

        # Sync both inputs (text & slider)
        x_value = st.number_input("Enter exact x position", min_value=0.0, max_value=1.0, value=0.5, step=0.0001, format="%.6f")
        x_slider = st.slider("Select x position (0 to 1)", min_value=0.0, max_value=1.0, value=x_value, step=0.0001, format="%.6f")

        # Ensure both inputs sync
        x_value = x_slider if "slider" in st.session_state else x_value

        if st.button("📈 Calculate Slope"):
            slope = camber_slope_at_x(naca_number, x_value)
            st.success(f"**Slope at x = {x_value:.6f} for NACA {naca_number}:** {slope:.6f}")

with col2:
    st.subheader("Camber Line Visualization")

    fig, ax = plt.subplots(figsize=(12, 4))  # Set a square figure for even scaling
    ax.plot(x, y_c, label=f'NACA {naca_number} Camber Line', color='b', linewidth=3)
    
    # Max Camber Indicator
    ax.axvline(P, color='r', linestyle=':', label=f'Max Camber at x={P}')
    
    ax.set_xlabel("Chord Position (x)", fontsize=18)
    ax.set_ylabel("Camber Line (y_c)", fontsize=18)
    ax.set_title(f'NACA {naca_number} Camber Line Plot', fontsize=22)
    ax.legend(fontsize=14)
    ax.grid(True)

    # 🔥 Ensure x and y axes are equally scaled
    ax.set_aspect('equal', adjustable='datalim')  

    st.pyplot(fig)  # Display in Streamlit

