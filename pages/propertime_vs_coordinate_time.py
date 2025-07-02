import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit setup
st.set_page_config(page_title="Proper Time vs Coordinate Time", layout="centered")
st.title("⏱️ Proper Time vs Coordinate Time")

st.latex(r"""
\tau(t) = \frac{t}{\gamma} = t \sqrt{1 - v^2}
""")
st.write("Compare how much time passes for a traveler moving at constant speed versus an observer at rest (Earth frame).")

# Inputs
v = st.slider("Traveler's speed (as a fraction of c)", min_value=0.0, max_value=0.99, value=0.8, step=0.01)
t_max = st.slider("Total coordinate time on Earth (in arbitrary units)", min_value=1, max_value=20, value=10)

# Calculations
gamma = 1 / np.sqrt(1 - v**2)
t_vals = np.linspace(0, t_max, 300)
tau_vals = t_vals / gamma  # Proper time for moving observer

# Layout
col1, col2 = st.columns(2)

# Plot 1: Proper Time vs Coordinate Time
with col1:
    st.subheader("📈 Proper Time vs Coordinate Time")
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    ax1.plot(t_vals, tau_vals, color='purple', label=r"$\tau(t) = t \sqrt{1 - v^2}$")
    ax1.plot(t_vals, t_vals, linestyle='--', color='gray', label=r"$t$ (Earth)")
    ax1.set_xlabel(r"Coordinate Time $t$")
    ax1.set_ylabel(r"Proper Time $\tau$")
    ax1.set_title("Time Experienced by Traveler vs Earth")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

# Plot 2: Worldlines on Spacetime Diagram
with col2:
    st.subheader("🌌 Spacetime Worldlines")
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    ax2.plot([0, 0], [0, t_max], label="Earth (Rest Frame)", color='blue')
    ax2.plot([0, v * t_max], [0, t_max], label="Traveler", color='red')
    ax2.set_xlim(-1, max(1, v * t_max + 1))
    ax2.set_ylim(0, t_max)
    ax2.set_xlabel("x")
    ax2.set_ylabel("t")
    ax2.set_title("Spacetime Diagram")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

# Results
st.subheader("✅ Summary")
st.markdown(f"""
- Lorentz factor: $\\gamma = {gamma:.6f}$
- When Earth experiences $t = {t_max}$, traveler experiences only:
""")

st.latex(rf"""
\tau = \frac{{t}}{{\gamma}} = \frac{{{t_max}}}{{{gamma:.6f}}} = {t_max / gamma:.6f}
""")

