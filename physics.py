import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
import numpy as np

def hebrew(text):
    return text[::-1]

def calculate_images(angle):
    return int(360/angle)-1 if angle!=0 else 0

def update(val):
    global angle, num_images
    angle = val
    num_images = calculate_images(angle)

    # Update plot
    ax.cla()
    plot_images()

def reset_button_func(val):
    angle_slider.set_val(90)
    update(90)

def angle_text_box(val):
    angle_slider.set_val(float(val))
    update(float(val))

def rotation(num, angle):
    if num == 1:
        return np.array([[np.cos(np.radians(angle)), np.sin(np.radians(angle))],
                                    [np.sin(np.radians(angle)), -np.cos(np.radians(angle))]])
    return np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                                [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])

def plot_images():
    global num_images
    # Setting up
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.grid(True)

    # Plotting mirrors
    mirror1 = np.array([[0, 0], [np.cos(np.radians(angle / 2)), np.sin(np.radians(angle / 2))]])
    mirror2 = np.array([[0, 0], [np.cos(np.radians(-angle / 2)), np.sin(np.radians(-angle / 2))]])
    ax.plot(mirror1[:, 0], mirror1[:, 1], 'k-', lw=2)
    ax.plot(mirror2[:, 0], mirror2[:, 1], 'k-', lw=2)

    # Plotting reflections of mirrors
    for i in range(1, num_images):
        theta = i * angle
        rot_matrix = np.array([[np.cos(np.radians(theta)), np.sin(np.radians(theta))],
                                [np.sin(np.radians(theta)), -np.cos(np.radians(theta))]])
        ref_mirror1 = rot_matrix.dot(mirror1.T).T
        ref_mirror2 = rot_matrix.dot(mirror2.T).T
        ax.plot(ref_mirror1[:, 0], ref_mirror1[:, 1], 'k--', lw=2, alpha=0.3)
        ax.plot(ref_mirror2[:, 0], ref_mirror2[:, 1], 'k--', lw=2, alpha=0.3)

    # Plotting trapezoids representing the object
    obj = np.array([[0.5, 0.1],[0.6, 0.1] ,[0.6,-0.1],[0.6, 0.1] ,[0.6,-0.1],[0.4,-0.1], [0.5,0.1],[0.4,-0.1]]) 
    ax.plot(obj[:, 0], obj[:, 1], 'r-')

    # Bug fixes
    if angle > 120:
        num_images += 1
    num_of_reflections = 0
    num_inversion = 0

    # Plotting trapezoids representing the reflections
    for i in range(1, num_images):
        theta = i * angle
        rot_matrix = 0
        if num_inversion%2==0:
            rot_matrix = rotation(1,theta)
        else:
            rot_matrix = rotation(2,theta)
        img = rot_matrix.dot(obj.T).T
        ax.plot(img[:, 0], img[:, 1], 'b-')

        theta = -i * angle
        rot_matrix = 0
        if num_inversion%2==0:
            rot_matrix = rotation(1,theta)
        else:
            rot_matrix = rotation(2,theta) 
        img = rot_matrix.dot(obj.T).T
        ax.plot(img[:, 0], img[:, 1], 'b-')

        num_of_reflections += 2
        num_inversion += 1

    # Diagram (text)
    ax.plot(1.4, 1.4, 'ro')
    ax.text(1.3, 1.34, hebrew("חפץ"), verticalalignment='bottom', horizontalalignment='right')
    ax.plot(1.4, 1.2, 'bo')
    ax.text(1.3, 1.14, hebrew("השתקפות"), verticalalignment='bottom', horizontalalignment='right')
    ax.plot(1.4, 0.99, 'k_', lw=4)
    ax.text(1.3, 0.94, hebrew("מראה"), verticalalignment='bottom', horizontalalignment='right')
    ax.text(1.47, 0.76, hebrew("--- השתקפות של מראה"), verticalalignment='bottom', horizontalalignment='right')
    ax.text(0.45, 1.15, f"(360/α - 1)   {num_images} :{hebrew('כמות של השתקפויות')}", verticalalignment='bottom', horizontalalignment='right')

fig, ax = plt.subplots()
angle = 90
num_images = calculate_images(angle)
plot_images()

# Add slider
ax_slider = fig.add_axes([0.3, 0.2, 0.45, 0.05])
angle_slider = Slider(ax=ax_slider, label=hebrew('זווית'), valmin=0, valmax=180, valinit=90,valfmt='%0.0f',)
angle_slider.on_changed(update)
# Add button
ax_reset_button = fig.add_axes([0.45, 0.14, 0.15, 0.05])
reset_button = Button(ax=ax_reset_button, label=hebrew("אתחול"), color="white")
reset_button.on_clicked(reset_button_func)
# Add textbox
ax_text_box = fig.add_axes([0.3, 0.14, 0.1, 0.05])
text_box = TextBox(ax=ax_text_box, label=hebrew(' זווית'))
text_box.on_submit(angle_text_box)

plt.show()
