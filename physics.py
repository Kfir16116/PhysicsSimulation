import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

def hebrew(text):
    return text[ : :-1]

def calculate_images(angle):
    if int(angle) != 0:
        return int(360 / angle) - 1

angle = 90
num_images = calculate_images(angle)

def update(val):
    global angle, ax, num_images
    angle = val
    num_images = calculate_images(angle)
    # Clear plot
    ax.cla()
    
    plot_images()

fig, ax = plt.subplots()

def plot_images():
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')

    # Plotting mirrors
    mirror1 = np.array([[0, 0], [np.cos(np.radians(angle / 2)), np.sin(np.radians(angle / 2))]])
    mirror2 = np.array([[0, 0], [np.cos(np.radians(-angle / 2)), np.sin(np.radians(-angle / 2))]])
    ax.plot(mirror1[:, 0], mirror1[:, 1], 'k-', lw=2)
    ax.plot(mirror2[:, 0], mirror2[:, 1], 'k-', lw=2)

    # Plotting object
    obj = np.array([0.5, 0])
    ax.plot(obj[0], obj[1], 'ro')

    # Diagram
    ax.plot(1.4,1.4, 'ro')
    ax.text(1.3,1.34, hebrew("חפץ"), verticalalignment='bottom', horizontalalignment='right')
    ax.plot(1.4,1.2, 'bo')
    ax.text(1.3,1.14, hebrew("השתקפות"), verticalalignment='bottom', horizontalalignment='right')
    ax.plot(1.4,0.99, 'k_', lw=4)
    ax.text(1.3,0.94, hebrew("מראה"), verticalalignment='bottom', horizontalalignment='right')
    ax.text(0.3,1.15, f"{num_images} :{hebrew('כמות של השתקפויות')}", verticalalignment='bottom', horizontalalignment='right')

    # Calculate and plot images (create reflections)
    try:
        for i in range(1, num_images + 1):
            theta = i * angle
            rot_matrix = np.array([[np.cos(np.radians(theta)), -np.sin(np.radians(theta))],
                                    [np.sin(np.radians(theta)),  np.cos(np.radians(theta))]])
            img = rot_matrix.dot(obj)
            ax.plot(img[0], img[1], 'bo')
    except TypeError:
        pass
plot_images()

# Add slider
axred = fig.add_axes([0.3, 0.2, 0.45, 0.05])
red = Slider(axred, hebrew('זווית'), 0.0, 180, 90)
red.on_changed(update)

plt.grid(True)
plt.show()
