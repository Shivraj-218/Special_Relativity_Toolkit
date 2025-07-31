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
v   = st.slider("Relative velocity (v/c)",     -0.99, 0.99, 0.6, 0.01)
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
    "x":       [xA,    xB,    xA_p,  xB_p],
    "t":       [tA,    tB,    tA_p,  tB_p]
}).round(3)

st.subheader("Event Coordinates in Each Frame")
st.table(df)

# — Draw Minkowski diagram —
fig, ax = plt.subplots(figsize=(6,6))

# --- DYNAMIC SCALING LOGIC ---
all_coords = [xA, tA, xB, tB, xA_p, tA_p, xB_p, tB_p]
# Filter out non-finite values if any appear due to extreme gamma (though unlikely with max_v=0.99)
all_coords = [c for c in all_coords if np.isfinite(c)]

# Calculate max absolute coordinate value
max_coord_abs = max(abs(c) for c in all_coords) if all_coords else 1.0 # Default to 1.0 if all are 0

plot_buffer = 1.2 # 20% padding around the max coordinate
min_plot_lim = 5.0 # Ensure a minimum scale for visibility if coordinates are very small

plot_lim = max(min_plot_lim, max_coord_abs * plot_buffer)

ax.set_xlim(-plot_lim, plot_lim)
ax.set_ylim(-plot_lim, plot_lim)
ax.set_aspect('equal', 'box') # Maintain aspect ratio for correct light cone and axes skewing
ax.set_xlabel("x")
ax.set_ylabel("ct")

# Define x-array for lines based on dynamic limits
x = np.linspace(-plot_lim, plot_lim, 200)

# Light‑cone
ax.plot(x,  x, 'k--', alpha=0.3)
ax.plot(x, -x, 'k--', alpha=0.3)

# Rest‑frame axes (black)
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

# Rest‑frame grid (gray)
# Adjust grid line spacing if plot_lim is very large, or keep fixed for clarity
grid_step = 1.0
if plot_lim > 10: # Adjust step for larger scales
    grid_step = 2.0
if plot_lim > 20:
    grid_step = 5.0
if plot_lim > 50:
    grid_step = 10.0

grid_coords = np.arange(-int(plot_lim) - grid_step, int(plot_lim) + grid_step, grid_step)

for t0 in grid_coords:
    ax.plot(x, np.full_like(x, t0), color='gray', linewidth=0.5, alpha=0.2)
for x0 in grid_coords:
    ax.plot(np.full_like(x, x0), x, color='gray', linewidth=0.5, alpha=0.2)


# Moving‑frame axes (red)
ax.plot(x,      v * x,    color='red', linewidth=2, label="x′ axis")
ax.plot(v * x, x,        color='red', linewidth=2, label="ct′ axis")


# Moving‑frame grid (blue)
g_val = gamma(v) # Calculate gamma for plotting once
# inv_g_val = 1 / g_val # Not explicitly needed after simultaneity line fix

# Use scaled ranges for xp and tp
xp_grid = np.arange(-int(plot_lim) - grid_step, int(plot_lim) + grid_step, grid_step)
tp_grid = np.arange(-int(plot_lim) - grid_step, int(plot_lim) + grid_step, grid_step)

for t0p in tp_grid: # Lines of constant t'
    xs = g_val * (xp_grid + v * t0p)
    ts = g_val * (t0p + v * xp_grid)
    ax.plot(xs, ts, color='blue', linewidth=0.7, alpha=0.3)
for x0p in xp_grid: # Lines of constant x'
    xs = g_val * (x0p + v * tp_grid)
    ts = g_val * (tp_grid + v * x0p)
    ax.plot(xs, ts, color='blue', linewidth=0.7, alpha=0.3)


# Plot rest‑frame events A & B
ax.plot(xA, tA, 'go', markersize=8)
ax.text(xA + 0.05 * plot_lim, tA + 0.05 * plot_lim, "A", color='green') # Adjust text offset
ax.plot(xB, tB, 'mo', markersize=8)
ax.text(xB + 0.05 * plot_lim, tB + 0.05 * plot_lim, "B", color='magenta') # Adjust text offset

# Simultaneity slice fill tolerance, relative to scale
fill_tolerance = 0.005 * plot_lim # e.g., 0.5% of the plot range

if frame == "S (rest frame)":
    ax.axhline(tA, color='green', linestyle='--', linewidth=2, label="Simultaneous in S")
    ax.fill_between(x, tA - fill_tolerance, tA + fill_tolerance, color='green', alpha=0.15)
else: # S' (moving frame)
    t_sim = v * x + tA_p / g_val # Corrected line, using g_val from above
    ax.plot(x, t_sim, color='blue', linestyle='--', linewidth=2, label="Simultaneous in S′")
    ax.fill_between(x, t_sim - fill_tolerance, t_sim + fill_tolerance, color='blue', alpha=0.15)

ax.legend(loc='upper left')
ax.set_title("Minkowski Diagram (c=1 units)")
st.pyplot(fig)

st.markdown("""
<hr style='margin-top: 50px; margin-bottom: 10px'>

<div style='text-align: center; font-size: 14px; color: gray;'>
&copy; 2025 Shivraj Deshmukh — All Rights Reserved<br>
Created with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
