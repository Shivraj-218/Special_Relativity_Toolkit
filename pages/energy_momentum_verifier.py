import streamlit as st
import numpy as np

# Streamlit page setup
st.set_page_config(page_title="Energy-Momentum Relation", layout="centered")
st.title("⚛️ Energy-Momentum Relation Verifier")

st.latex(r"""
E^2 = (pc)^2 + (m c^2)^2
""")

# User input
mass = st.number_input("Enter rest mass \( m \):", min_value=0.0, value=1.0, step=0.1, format="%.4f")
velocity = st.number_input("Enter velocity \( v \) (as a fraction of \( c \)):", min_value=0.0, max_value=0.999999, value=0.6, step=0.01, format="%.6f")

# Lorentz factor
gamma = 1 / np.sqrt(1 - velocity**2)

# Compute momentum and energy
p = gamma * mass * velocity       # p = γmv
E = gamma * mass                  # E = γmc^2 (with c=1)
E_squared = E**2
pc_squared = (p)**2
mc_squared_squared = (mass)**2

# Display calculations
st.subheader("🧮 Computation")
st.latex(rf"""
\gamma = \frac{{1}}{{\sqrt{{1 - {velocity}^2}}}} = {gamma:.6f}
""")
st.latex(rf"""
p = \gamma m v = {p:.6f} \quad , \quad E = \gamma m = {E:.6f}
""")
st.latex(rf"""
E^2 = {E_squared:.6f} \quad , \quad (pc)^2 + (mc^2)^2 = {pc_squared:.6f} + {mc_squared_squared:.6f} = {pc_squared + mc_squared_squared:.6f}
""")

# Verification
st.subheader("✅ Verification")
if np.isclose(E_squared, pc_squared + mc_squared_squared, atol=1e-6):
    st.success("✔️ Energy-momentum relation holds!")
else:
    st.error("❌ Relation does not hold. Check inputs.")


st.markdown("""
<hr style='margin-top: 50px; margin-bottom: 10px'>

<div style='text-align: center; font-size: 14px; color: gray;'>
&copy; 2025 Shivraj Deshmukh — All Rights Reserved<br>
Created with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)

