import streamlit as st
import numpy as np

st.set_page_config(page_title="Lorentz & EM Transformer", page_icon="🧲", layout="centered")
st.title("🧲 Lorentz Field Transformer & EM Tensor Calculator")

# Description
st.markdown("""
This tool computes:
- The transformed electric and magnetic fields \\(\\vec{E}'\\) and \\(\\vec{B}'\\) under a Lorentz boost along the x-axis.
- The electromagnetic field tensor \\(F^{\\mu\\nu}\\) from the input fields.

⚠️ **Assumption:** E and B inputs are in consistent units with c=1 (natural units), so boost velocity `v` is dimensionless.
""")

# Lorentz Boost Equations
st.markdown("### 📐 Lorentz Boost Equations")
st.latex(r"""
\begin{aligned}
E'_x &= E_x \\ 
E'_y &= \gamma (E_y - v B_z) \\ 
E'_z &= \gamma (E_z + v B_y) \\ 
B'_x &= B_x \\ 
B'_y &= \gamma (B_y + v E_z) \\ 
B'_z &= \gamma (B_z - v E_y)
\end{aligned}
""")

# Input Fields
st.subheader("🧮 Input Fields")
col1, col2 = st.columns(2)
with col1:
    E_x = st.number_input("Eₓ", value=0.0)
    E_y = st.number_input("Eᵧ", value=3.0)
    E_z = st.number_input("E_z", value=0.0)
with col2:
    B_x = st.number_input("Bₓ", value=0.0)
    B_y = st.number_input("Bᵧ", value=0.0)
    B_z = st.number_input("B_z", value=2.0)

# Lorentz Transformation
v_frac = st.slider("Boost velocity (fraction of c)", 0.0, 0.99, 0.6)
gamma = 1 / np.sqrt(1 - v_frac**2)
v = v_frac  # dimensionless v in natural units

# Transformed Electric Field
E_xp = E_x
E_yp = gamma * (E_y - v * B_z)
E_zp = gamma * (E_z + v * B_y)

# Transformed Magnetic Field
B_xp = B_x
B_yp = gamma * (B_y + v * E_z)
B_zp = gamma * (B_z - v * E_y)

# Display Transformed Fields
st.subheader("📊 Lorentz-Transformed Fields")
st.latex(r"""
\vec{E}' = \begin{bmatrix}
%.3f \\ %.3f \\ %.3f
\end{bmatrix}, \quad
\vec{B}' = \begin{bmatrix}
%.3f \\ %.3f \\ %.3f
\end{bmatrix}
""" % (E_xp, E_yp, E_zp, B_xp, B_yp, B_zp))

st.info("Boost applied along the x-axis with dimensionless velocity v (c=1). Ensure your E and B inputs are in compatible units.")

# Electromagnetic Field Tensor
st.subheader("📐 Electromagnetic Field Tensor (F^{μν})")

F = np.array([
    [ 0.0,  -E_x,  -E_y,  -E_z],
    [ E_x,   0.0, -B_z,   B_y],
    [ E_y,  B_z,   0.0,  -B_x],
    [ E_z, -B_y,   B_x,   0.0]
])

tensor_latex = r"F^{\mu\nu} = \begin{bmatrix}" + \
    r" \\ ".join([
        " & ".join([f"{val:+.3f}" for val in row]) for row in F
    ]) + r"\end{bmatrix}"

st.latex(tensor_latex)

# Explanation
st.markdown("""
**About the Tensor:**
- \(F^{\mu\nu}\) combines electric and magnetic fields in a single antisymmetric tensor.
- It satisfies **antisymmetry**: \(F^{\mu\nu}=-F^{\nu\mu}\).
- Maxwell’s equations compactly express as:
  \[
  \partial_\mu F^{\mu\nu} = \mu_0 J^\nu
  \]
""")
st.info("Antisymmetry reflects fundamental field constraints: \( F^{\mu\nu} = -F^{\nu\mu} \)")
