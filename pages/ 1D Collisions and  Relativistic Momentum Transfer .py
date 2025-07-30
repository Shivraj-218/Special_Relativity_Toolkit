

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

st.set_page_config(page_title="Relativistic Collision Simulator", layout="centered")
st.title("\U0001F4A8 Relativistic Collision Simulator")

st.latex(r"""
\text{In this simulation, we explore 1D relativistic collisions using natural units where } c = 1.
""")

st.latex(r"""
\text{Principles used:}
\begin{align*}
\text{Total momentum and energy are conserved.} \\
\text{Velocities are given as a fraction of light speed.}
\end{align*}
""")

st.latex(r"""
\begin{align*}
\gamma &= \frac{1}{\sqrt{1 - v^2}} \\
 p &= \gamma m v \\
 E &= \gamma m
\end{align*}
""")

# ---------------- Inputs ----------------
st.subheader("⚙️ Inputs")
col1, col2 = st.columns(2)

with col1:
    m1 = st.number_input("Mass of particle 1 (m₁)", min_value=0.1, value=1.0, step=0.1)
    v1 = st.number_input("Initial velocity of particle 1 (v₁ / c)", min_value=-0.999, max_value=0.999, value=0.6)

with col2:
    m2 = st.number_input("Mass of particle 2 (m₂)", min_value=0.1, value=1.0, step=0.1)
    v2 = st.number_input("Initial velocity of particle 2 (v₂ / c)", min_value=-0.999, max_value=0.999, value=-0.3)

mode = st.radio("Collision type:", ["Elastic", "Perfectly Inelastic"])

def gamma(v):
    return 1 / np.sqrt(1 - v**2)

# ---------------- Pre-Collision ----------------
g1, g2 = gamma(v1), gamma(v2)
E1, E2 = g1 * m1, g2 * m2
p1, p2 = g1 * m1 * v1, g2 * m2 * v2
E_total, p_total = E1 + E2, p1 + p2

# ---------------- Collision ----------------
if mode == "Perfectly Inelastic":
    # Correct relativistic treatment
    vf = p_total / E_total
    gf = gamma(vf)
    M = np.sqrt(E_total**2 - p_total**2)
    E_final = E_total
    p_final = p_total
    v1f = v2f = vf
    E1f = E2f = None
    p1f = p2f = None
else:
    def to_solutions(vars):
        v1f, v2f = vars
        g1f, g2f = gamma(v1f), gamma(v2f)
        p1f = g1f * m1 * v1f
        p2f = g2f * m2 * v2f
        E1f = g1f * m1
        E2f = g2f * m2
        return [p1f + p2f - p_total, E1f + E2f - E_total]

    guess = [v2, v1]  # reverse guess
    v1f, v2f = fsolve(to_solutions, guess)
    g1f, g2f = gamma(v1f), gamma(v2f)
    E1f, E2f = g1f * m1, g2f * m2
    p1f, p2f = g1f * m1 * v1f, g2f * m2 * v2f

# ---------------- Output Display ----------------
st.subheader("\U0001F4C8 Results")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🔹 Initial State")
    st.latex(rf"v_1 = {v1:.4f}, \quad E_1 = {E1:.4f}, \quad p_1 = {p1:.4f}")
    st.latex(rf"v_2 = {v2:.4f}, \quad E_2 = {E2:.4f}, \quad p_2 = {p2:.4f}")
    st.latex(rf"E_{{\text{{total}}}} = {E_total:.4f}, \quad p_{{\text{{total}}}} = {p_total:.4f}")

with col2:
    if mode == "Perfectly Inelastic":
        st.markdown("#### 🔹 Final State (Composite Object)")
        st.latex(rf"v_f = {vf:.4f}, \quad \gamma_f = {gf:.4f}")
        st.latex(rf"E_f = {E_final:.4f}, \quad p_f = {p_final:.4f}")
        st.latex(rf"M = \sqrt{{E^2 - p^2}} = {M:.4f}")
    else:
        st.markdown("#### 🔹 Final State")
        st.latex(rf"v_1' = {v1f:.4f}, \quad E_1' = {E1f:.4f}, \quad p_1' = {p1f:.4f}")
        st.latex(rf"v_2' = {v2f:.4f}, \quad E_2' = {E2f:.4f}, \quad p_2' = {p2f:.4f}")
        st.latex(rf"\Delta E = {E1f + E2f - E_total:+.4e}, \quad \Delta p = {p1f + p2f - p_total:+.4e}")

# ---------------- CoM Frame ----------------
v_com = p_total / E_total
st.latex(rf"\text{{🧭 Center-of-Momentum Frame Velocity:}} \quad v_{{\text{{com}}}} = {v_com:.4f}")

# ---------------- Bar Plot ----------------
st.subheader("\U0001F4C8 Energy & Momentum Comparison")

if mode == "Elastic":
    labels = ['p₁', 'p₂', "p₁′", "p₂′"]
    momentum_values = [p1, p2, p1f, p2f]
    energy_labels = ['E₁', 'E₂', "E₁′", "E₂′"]
    energy_values = [E1, E2, E1f, E2f]
else:
    labels = ['p_initial', 'p_final']
    momentum_values = [p_total, p_final]
    energy_labels = ['E_initial', 'E_final']
    energy_values = [E_total, E_final]

fig, ax = plt.subplots(1, 2, figsize=(10, 4))

ax[0].bar(labels, momentum_values, color='gray')
ax[0].set_title("Momentum")
ax[0].axhline(0, color='black', linewidth=0.5)

ax[1].bar(energy_labels, energy_values, color='gray')
ax[1].set_title("Energy")
ax[1].axhline(0, color='black', linewidth=0.5)

st.pyplot(fig)

# ---------------- Footer ----------------
st.markdown("""
<hr style='margin-top: 50px; margin-bottom: 10px'>
<div style='text-align: center; font-size: 14px; color: gray;'>
&copy; 2025 Shivraj Deshmukh — All Rights Reserved<br>
Created with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
