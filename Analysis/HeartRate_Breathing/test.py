import numpy as np
import matplotlib.pyplot as plt

# Generate some sample data
x = np.linspace(0, 2 * np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)
y4 = np.arctan(x)

# Create a 2x2 grid of plots
fig, axes = plt.subplots(3, 1, figsize=(10, 10))

# Plot the data in each subplot
axes[0].plot(x, y1, 'r-')
axes[0].set_title('sin(x)')

axes[1].plot(x, y2, 'b-')
axes[1].set_title('cos(x)')

axes[2].plot(x, y3, 'g-')
axes[2].set_ylim(-10, 10)
axes[2].set_title('tan(x)')

# Add some space between the subplots
plt.subplots_adjust(hspace=0.4, wspace=0.4)

# Show the plots
plt.show()