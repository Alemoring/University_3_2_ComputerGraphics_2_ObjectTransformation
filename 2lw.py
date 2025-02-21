import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import CSS4_COLORS
import random


list_colors = ["red", "blue", "yellow", "white", "black", "purple", "pink", "grey", ]

def translate(points, dx, dy):
    translation_matrix = np.array([[1, 0, dx],
                                   [0, 1, dy],
                                   [0, 0, 1]])
    points_homogeneous = np.hstack((points, np.ones((points.shape[0], 1))))
    transformed_points = translation_matrix @ points_homogeneous.T
    return transformed_points[:2].T

def scale(points, sx, sy):
    scaling_matrix = np.array([[sx, 0, 0],
                               [0, sy, 0],
                               [0, 0, 1]])
    points_homogeneous = np.hstack((points, np.ones((points.shape[0], 1))))
    transformed_points = scaling_matrix @ points_homogeneous.T
    return transformed_points[:2].T

def rotate(points, angle):
    radians = np.radians(angle)
    rotation_matrix = np.array([[np.cos(radians), -np.sin(radians), 0],
                                [np.sin(radians), np.cos(radians), 0],
                                [0, 0, 1]])
    points_homogeneous = np.hstack((points, np.ones((points.shape[0], 1))))
    transformed_points = rotation_matrix @ points_homogeneous.T
    return transformed_points[:2].T

class TransformApp:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.color = '#00FFFF'
        self.shape = np.array([[0, 0], [1, 0], [0, 1]])  # Пример треугольника
        self.transformed_shape = self.shape.copy()
        self.draw_shape()
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def draw_shape(self):
        self.ax.clear()
        self.ax.fill(self.transformed_shape[:, 0], self.transformed_shape[:, 1], self.color, alpha=0.5)
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        plt.draw()

    def on_key_press(self, event):
        if event.key == 'up':
            self.transformed_shape = translate(self.transformed_shape, 0, 0.5)
        elif event.key == 'down':
            self.transformed_shape = translate(self.transformed_shape, 0, -0.5)
        elif event.key == 'left':
            self.transformed_shape = translate(self.transformed_shape, -0.5, 0)
        elif event.key == 'right':
            self.transformed_shape = translate(self.transformed_shape, 0.5, 0)
        elif event.key == '+':
            self.transformed_shape = scale(self.transformed_shape, 1.1, 1.1)
        elif event.key == '-':
            self.transformed_shape = scale(self.transformed_shape, 0.9, 0.9)
        elif event.key == 'r':
            self.transformed_shape = rotate(self.transformed_shape, 15)
        elif event.key == 's':
            self.save_transformed_shape()
        self.color = random.choice(list(CSS4_COLORS.values()))
        self.draw_shape()

    def save_transformed_shape(self):
        np.savetxt("transformed_shape.txt", self.transformed_shape)
    
app = TransformApp()
plt.show()