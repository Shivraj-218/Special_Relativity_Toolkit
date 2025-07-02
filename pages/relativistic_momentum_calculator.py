import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit page setup
st.set_page_config(page_title="Relativistic Momentum Calculator", layout="centered")
st.title("🚀 Relativistic Momentum Calculator")

st.latex(r"""
p = \gamma m v \quad \text{where} \quad \gamma = \frac{1}{\sqrt{1 - \frac{v^2}{c^2}}}
""")

st.write("This formula modifies the classical momentum \( p = mv \) to obey special relativity.")

# User inputs
mass = st.number_input("Enter rest mass \( m \) (arbitrary units):", min_value=0.0, value=1.0, step=0.1, format="%.4f")
velocity = st.number_input("Enter velocity \( v \) (as a fraction of \( c \)):", min_value=0.0, max_value=0.999999, value=0.7, step=0.01, format="%.6f")

# Compute gamma and momenta
gamma = 1 / np.sqrt(1 - velocity**2)
p_rel = gamma * mass * velocity
p_newton = mass * velocity

st.latex(rf"""
\gamma = \frac{{1}}{{\sqrt{{1 - {velocity}^2}}}} = {gamma:.6f}
""")

st.latex(rf"""
p_{{\text{{rel}}}} = \gamma m v = {gamma:.6f} \times {mass} \times {velocity} = {p_rel:.6f}
""")

st.latex(rf"""
p_{{\text{{Newton}}}} = mv = {mass} \times {velocity} = {p_newton:.6f}
""")

# Comparative plot
st.subheader("📈 Relativistic vs Newtonian Momentum")

v_vals = np.linspace(0, 0.999, 300)
gamma_vals = 1 / np.sqrt(1 - v_vals**2)
p_rel_vals = gamma_vals * mass * v_vals
p_newton_vals = mass * v_vals

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(v_vals, p_rel_vals, label="Relativistic Momentum (γmv)", color='blue')
ax.plot(v_vals, p_newton_vals, label="Newtonian Momentum (mv)", linestyle='--', color='orange')
ax.set_xlabel(r"Velocity $v$ (fraction of $c$)")
ax.set_ylabel(r"Momentum $p$")
ax.set_title("Momentum vs Speed")
ax.legend()
ax.grid(True)
st.pyplot(fig)
