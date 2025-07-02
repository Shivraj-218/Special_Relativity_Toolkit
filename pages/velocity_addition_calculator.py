import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set up Streamlit
st.set_page_config(page_title="Relativistic Velocity Addition", layout="centered")
st.title("⚡ Relativistic Velocity Addition Calculator")

st.latex(r"""
v = \frac{v_1 + v_2}{1 + \frac{v_1 v_2}{c^2}}
""")

st.write("This formula ensures that no matter how large \( v_1 \) and \( v_2 \) are, the combined velocity never exceeds the speed of light \( c \).")

# User inputs
v1 = st.number_input("Enter \( v_1 \) (as a fraction of \( c \)):", min_value=0.0, max_value=0.999999, value=0.5, step=0.01, format="%.6f")
v2 = st.number_input("Enter \( v_2 \) (as a fraction of \( c \)):", min_value=0.0, max_value=0.999999, value=0.7, step=0.01, format="%.6f")

# Compute relativistic velocity addition
def relativistic_velocity_addition(v1, v2):
    return (v1 + v2) / (1 + v1 * v2)

v_combined = relativistic_velocity_addition(v1, v2)

# Display result
st.latex(r"""
v = \frac{%.6f + %.6f}{1 + %.6f \cdot %.6f} = %.10f\,c
""" % (v1, v2, v1, v2, v_combined))

st.write("The result obeys the relativistic rule and stays below \( c = 1 \).")

# Plotting section
st.subheader("📈 Velocity Addition Curve")

v_vals = np.linspace(0, 0.999, 300)
v_combined_vals = relativistic_velocity_addition(v_vals, v2)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(v_vals, v_combined_vals, label=rf"$v_2 = {v2:.2f}c$", color='blue')
ax.axhline(1, color='red', linestyle='--', label='Speed of Light ($c$)')
ax.set_xlabel(r"$v_1$ (fraction of $c$)")
ax.set_ylabel(r"$v$ (combined)")
ax.set_title("Relativistic Velocity Addition")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.markdown("""
<hr style='margin-top: 50px; margin-bottom: 10px'>

<div style='text-align: center; font-size: 14px; color: gray;'>
&copy; 2025 Shivraj Deshmukh — All Rights Reserved<br>
Created with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
