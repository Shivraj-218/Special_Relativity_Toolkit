import streamlit as st
import numpy as np
import plotly.graph_objs as go
from mpmath import mp

# Set decimal precision (100 digits)
mp.dps = 100

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="Lorentz Factor Explorer", layout="centered")
st.title("🚀 Lorentz Factor Explorer")
st.markdown("Explore how the Lorentz factor γ changes with velocity.")
st.markdown("It quantifies time dilation, length contraction, and relativistic mass increase.")
st.latex(r"\gamma(v) = \frac{1}{\sqrt{1 - (v/c)^2}}")

# -----------------------------
# 🧮 High-Precision Calculator
# -----------------------------
st.subheader("🧮 Lorentz Factor Calculator (High Precision)")
v_input = st.text_input("Enter velocity as a fraction of c (e.g., 0.999999999999999...):", "0.9999")

try:
    v = mp.mpf(v_input.strip())
    if v < 0 or v >= 1:
        raise ValueError("Velocity must be ≥ 0 and < 1.")
    gamma = 1 / mp.sqrt(1 - v**2)
    st.success(f"γ = {mp.nstr(gamma, 20)}")  # 20 significant digits
except Exception as e:
    st.error(f"Invalid input: {e}")

# -----------------------------
# 📈 Plot: Lorentz Factor vs Velocity
# -----------------------------
def lorentz_gamma_array(v_array):
    """Compute Lorentz gamma for array of velocities (excluding v ≥ c)."""
    gamma = np.empty_like(v_array)
    gamma[:] = np.nan
    valid = v_array < 1.0
    gamma[valid] = 1.0 / np.sqrt(1.0 - v_array[valid]**2)
    return gamma

v_vals = np.linspace(0, 1.2, 1000)
gamma_vals = lorentz_gamma_array(v_vals)

fig = go.Figure()
fig.add_trace(go.Scatter(x=v_vals, y=gamma_vals, mode="lines",
                         line=dict(color="crimson", width=3)))

fig.update_layout(
    title="Lorentz Factor vs Velocity",
    xaxis_title="v/c",
    yaxis_title="γ",
    xaxis=dict(range=[0, 1.2]),
    yaxis=dict(range=[0, np.nanmin([100, np.nanmax(gamma_vals)])]),
    template="plotly_dark",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
st.caption("⚠️ γ diverges as v approaches c. For v ≥ c, γ is undefined and unphysical.")
