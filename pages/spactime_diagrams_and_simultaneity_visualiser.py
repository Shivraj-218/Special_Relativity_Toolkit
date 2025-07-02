import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# — Page setup —
st.set_page_config(page_title="Minkowski Diagram Generator", layout="centered")
st.title("🕳️ Minkowski Diagram Generator")

st.latex(r"""
\text{Simultaneity is frame-dependent. Visualize this using a spacetime diagram.}
""")

# — Inputs —
v   = st.slider("Relative velocity (v/c)",    -0.99, 0.99, 0.6, 0.01)
xA, tA = st.number_input("Event A – x", 2.0), st.number_input("Event A – t", 2.0)
xB, tB = st.number_input("Event B – x", 4.0), st.number_input("Event B – t", 2.0)
frame = st.radio("Show simultaneity in frame:", ["S (rest frame)", "S′ (moving frame)"])

# — Lorentz helpers —
def gamma(v): return 1 / np.sqrt(1 - v**2)
def to_moving_frame(x, t, v):
    g   = gamma(v)
    x_p = g * (x - v * t)
    t_p = g * (t - v * x)
    return x_p, t_p

# — Compute transformed coords —
xA_p, tA_p = to_moving_frame(xA, tA, v)
xB_p, tB_p = to_moving_frame(xB, tB, v)

# — Table of event coordinates —
df = pd.DataFrame({
    "Frame": ["S", "S", "S′", "S′"],
    "Event": ["A", "B", "A", "B"],
    "x":     [xA,   xB,   xA_p,  xB_p],
    "t":     [tA,   tB,   tA_p,  tB_p]
}).round(3)

st.subheader("Event Coordinates in Each Frame")
st.table(df)

# — Draw Minkowski diagram —
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_aspect('equal', 'box')
ax.set_xlabel("x")
ax.set_ylabel("ct")

# Define x-array for lines
x = np.linspace(-5, 5, 200)

# Light‑cone
ax.plot(x,  x, 'k--', alpha=0.3)
ax.plot(x, -x, 'k--', alpha=0.3)

# Rest‑frame axes (black)
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

# Rest‑frame grid (gray)
for t0 in np.arange(-4, 5, 1):
    ax.plot(x, np.full_like(x, t0), color='gray', linewidth=0.5, alpha=0.2)
for x0 in np.arange(-4, 5, 1):
    ax.plot(np.full_like(x, x0), x, color='gray', linewidth=0.5, alpha=0.2)

# Moving‑frame axes (red)
ax.plot(x,     v * x,  color='red', linewidth=2, label="x′ axis")
ax.plot(v * x, x,      color='red', linewidth=2, label="ct′ axis")

# Moving‑frame grid (blue)
inv_g = gamma(v)
xp = np.arange(-5, 6, 1)
tp = np.arange(-5, 6, 1)
for t0p in tp:
    xs = inv_g * (xp + v * t0p)
    ts = inv_g * (t0p + v * xp)
    ax.plot(xs, ts, color='blue', linewidth=0.7, alpha=0.3)
for x0p in xp:
    xs = inv_g * (x0p + v * tp)
    ts = inv_g * (tp + v * x0p)
    ax.plot(xs, ts, color='blue', linewidth=0.7, alpha=0.3)

# Plot rest‑frame events A & B
ax.plot(xA, tA, 'go', markersize=8)
ax.text(xA + 0.2, tA + 0.1, "A", color='green')
ax.plot(xB, tB, 'mo', markersize=8)
ax.text(xB + 0.2, tB + 0.1, "B", color='magenta')

# Simultaneity slice
if frame == "S (rest frame)":
    ax.axhline(tA, color='green', linestyle='--', linewidth=2, label="Simultaneous in S")
    ax.fill_between(x, tA-0.02, tA+0.02, color='green', alpha=0.15)
else:
    t_sim = inv_g * (tA_p + v * x)
    ax.plot(x, t_sim, color='blue', linestyle='--', linewidth=2, label="Simultaneous in S′")
    ax.fill_between(x, t_sim-0.02, t_sim+0.02, color='blue', alpha=0.15)

ax.legend(loc='upper left')
ax.set_title("Minkowski Diagram (c=1 units)")
st.pyplot(fig)
