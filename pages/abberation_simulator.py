import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Page config
st.set_page_config(
    page_title="Relativistic Aberration Tool",
    page_icon="🌠",
    layout="centered"
)

# 2. Title & description
st.title("🌠 Relativistic Aberration Tool")
st.markdown("""
Explore how stars appear shifted due to motion at relativistic speeds.  
This is caused by **relativistic aberration**, which alters the apparent angle of incoming light.
""")

# 3. Render formula correctly
st.latex(r"\cos \theta' = \frac{\cos \theta - \beta}{1 - \beta \cos \theta}")

st.markdown("**Where:**")
st.latex(r"\beta = \frac{v}{c}")
st.latex(r"\theta\ \text{: original angle (stationary frame)}")
st.latex(r"\theta'\ \text{: observed angle (moving frame)}")


# Input for β (as a float near 1)
beta = st.number_input(
    "Enter β = v/c (must be between 0 and just under 1)",
    min_value=0.0,
    max_value=0.999999999,
    value=0.5,
    step=1e-4,
    format="%.9f"
)

epsilon = 1e-12  # To avoid division by zero when β → 1
beta = np.clip(beta, 0.0, 1 - epsilon)

st.markdown(f"**You entered:** β = {beta:.9f}")


# 5. Generate random starfield
num_stars = 500
theta = np.random.uniform(0, np.pi, num_stars)
phi   = np.random.uniform(0, 2 * np.pi, num_stars)

x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

# 6. Aberration transform
cos_tp = (z - beta) / (1 - beta * z)
cos_tp = np.clip(cos_tp, -1, 1)
theta_prime = np.arccos(cos_tp)

x_p = np.sin(theta_prime) * np.cos(phi)
y_p = np.sin(theta_prime) * np.sin(phi)

# 7. Force a dark style so white points show up
plt.style.use("dark_background")

# 8. Plot side by side
fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 5))
for ax, X, Y, title in [
    (ax0, x,   y,   "Starfield in Rest Frame"),
    (ax1, x_p, y_p, "Starfield in Moving Frame")
]:
    ax.scatter(X, Y, s=10, c="white")
    ax.set_facecolor("black")
    ax.set_title(title, color="white")
    ax.axis("off")

# 9. Ensure the figure itself is black
fig.patch.set_facecolor("black")
plt.tight_layout()

# 10. Render in Streamlit
st.pyplot(fig)

st.info("""
At high speeds, stars appear to cluster toward the direction of motion —  
a stunning effect of spacetime geometry.
""")
