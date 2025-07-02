import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit setup
st.set_page_config(page_title="Kinetic Energy vs Speed", layout="centered")
st.title("🚀 Kinetic Energy vs Speed (Relativistic vs Newtonian)")

# --- Equations ---
st.latex(r"""
\text{Relativistic: } KE = (\gamma - 1) m c^2 \quad \text{where } \gamma = \frac{1}{\sqrt{1 - \frac{v^2}{c^2}}}
""")
st.latex(r"""
\text{Newtonian: } KE = \frac{1}{2} m v^2
""")

# --- Input ---
mass = st.number_input("Enter rest mass \( m \):", min_value=0.0, value=1.0, step=0.1, format="%.4f")

# --- Speed values ---
v_vals = np.linspace(0, 0.999, 400)
gamma_vals = 1 / np.sqrt(1 - v_vals**2)

# --- Energy calculations ---
ke_rel = (gamma_vals - 1) * mass
ke_newton = 0.5 * mass * v_vals**2

# --- Deviation threshold ---
diff_pct = (ke_rel - ke_newton) / ke_rel
threshold_idx = np.argmax(diff_pct > 0.1)
v_thresh = v_vals[threshold_idx] if np.any(diff_pct > 0.1) else None

# --- Plot ---
st.subheader("📈 Kinetic Energy vs Speed")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(v_vals, ke_rel, label="Relativistic KE", color='blue')
ax.plot(v_vals, ke_newton, label="Newtonian KE", linestyle='--', color='green')

if v_thresh:
    ax.axvline(v_thresh, color='red', linestyle=':', label=f"Deviation >10% at v ≈ {v_thresh:.2f}c")

ax.set_xlabel(r"Speed $v$ (fraction of $c$)")
ax.set_ylabel("Kinetic Energy")
ax.set_title("Relativistic vs Newtonian Kinetic Energy")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# --- KE Comparison Table ---
st.subheader("📊 KE Comparison Table")

v_sample = np.linspace(0.1, 0.99, 10)
gamma_sample = 1 / np.sqrt(1 - v_sample**2)
ke_rel_sample = (gamma_sample - 1) * mass
ke_newton_sample = 0.5 * mass * v_sample**2
diff_pct_sample = 100 * (ke_rel_sample - ke_newton_sample) / ke_rel_sample

data = {
    "Speed (v/c)": v_sample.round(3),
    "Newtonian KE": ke_newton_sample.round(5),
    "Relativistic KE": ke_rel_sample.round(5),
    "% Difference": diff_pct_sample.round(2)
}
df = pd.DataFrame(data)
st.dataframe(df.style.format({
    "Speed (v/c)": "{:.3f}",
    "Newtonian KE": "{:.5f}",
    "Relativistic KE": "{:.5f}",
    "% Difference": "{:.2f}"
}))

# --- Educational Notes ---
st.markdown("""
### ℹ️ Insights:
- The Newtonian approximation fails significantly at high speeds (v > 0.6c).
- The deviation threshold is automatically identified and marked on the plot.
- Relativistic KE continues rising steeply as v → c, while Newtonian KE incorrectly levels off.
- This is crucial for particle physics, cosmology, and high-energy astrophysics.
""")
st.markdown("""
<hr style='margin-top: 50px; margin-bottom: 10px'>

<div style='text-align: center; font-size: 14px; color: gray;'>
&copy; 2025 Shivraj Deshmukh — All Rights Reserved<br>
Created with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
