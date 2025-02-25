import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import CSS4_COLORS
import random

list_colors = ["red", "blue", "yellow", "white", "black", "purple", "pink", "grey"]

def transposition(transformed_shape, center):
    transformed_shape[:, 0] += center[0]  # Сдвиг по X
    transformed_shape[:, 1] += center[1]  # Сдвиг по Y
    print("center = " + str(center[0]) + " " + str(center[1]))
    return transformed_shape

def translate(points, dx, dy):
    translation_matrix = np.array([[1, 0, dx],
                                   [0, 1, dy],
                                   [0, 0, 1]])
    points_homogeneous = np.hstack((points, np.ones((points.shape[0], 1))))
    transformed_points = translation_matrix @ points_homogeneous.T
    return transformed_points[:2].T

def scale(points, sx, sy, center):
    translated_points = points - center
    scaling_matrix = np.array([[sx, 0, 0],
                               [0, sy, 0],
                               [0, 0, 1]])
    points_homogeneous = np.hstack((translated_points, np.ones((points.shape[0], 1))))
    transformed_points = scaling_matrix @ points_homogeneous.T
    return transformed_points[:2].T + center

def rotate(points, angle, center):
    translated_points = points - center
    
    radians = np.radians(angle)
    rotation_matrix = np.array([[np.cos(radians), -np.sin(radians), 0],
                                [np.sin(radians), np.cos(radians), 0],
                                [0, 0, 1]])
    points_homogeneous = np.hstack((translated_points, np.ones((points.shape[0], 1))))
    transformed_points = rotation_matrix @ points_homogeneous.T
    return transformed_points[:2].T + center

class TransformApp:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.color = '#00FFFF'
        # Начальная фигура (центрированный квадрат)
        self.shape = np.array([[-0.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5]])
        self.transformed_shape = self.shape.copy()
        self.draw_shape()
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)

    def draw_shape(self):
        self.ax.clear()
        self.ax.fill(self.transformed_shape[:, 0], self.transformed_shape[:, 1], self.color, alpha=1)
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        plt.draw()

    def on_key_press(self, event):
        if event.key == 'up':
            self.transformed_shape = translate(self.transformed_shape, 0, 0.5)
            self.color = random.choice(list(CSS4_COLORS.values()))
        elif event.key == 'down':
            self.transformed_shape = translate(self.transformed_shape, 0, -0.5)
            self.color = random.choice(list(CSS4_COLORS.values()))
        elif event.key == 'left':
            self.transformed_shape = translate(self.transformed_shape, -0.5, 0)
            self.color = random.choice(list(CSS4_COLORS.values()))
        elif event.key == 'right':
            self.transformed_shape = translate(self.transformed_shape, 0.5, 0)
            self.color = random.choice(list(CSS4_COLORS.values()))
        elif event.key == '=' or event.key == "+":
            self.transformed_shape = scale(self.transformed_shape, 1.1, 1.1, np.mean(self.transformed_shape, axis=0))
            self.color = random.choice(list(CSS4_COLORS.values()))
        elif event.key == '-':
            self.transformed_shape = scale(self.transformed_shape, 0.9, 0.9, np.mean(self.transformed_shape, axis=0))
            self.color = random.choice(list(CSS4_COLORS.values()))
        elif event.key == 'r' or event.key == 'к':
            self.transformed_shape = rotate(self.transformed_shape, -15, np.mean(self.transformed_shape, axis=0))
            self.color = random.choice(list(CSS4_COLORS.values()))
        elif event.key == 'e' or event.key == 'у':
            self.transformed_shape = rotate(self.transformed_shape, 15, np.mean(self.transformed_shape, axis=0))
            self.color = random.choice(list(CSS4_COLORS.values()))
        elif event.key == '1':
            self.color = random.choice(list(CSS4_COLORS.values()))
            center = np.mean(self.transformed_shape, axis=0)
            # Центрированный треугольник
            self.transformed_shape = np.array([[0.0, -0.577], [-0.5, 0.289], [0.5, 0.289]])
            self.transformed_shape = transposition(self.transformed_shape, center)
        elif event.key == '2':
            self.color = random.choice(list(CSS4_COLORS.values()))
            center = np.mean(self.transformed_shape, axis=0)
            # Центрированный квадрат
            self.transformed_shape = np.array([[-0.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5]])
            self.transformed_shape = transposition(self.transformed_shape, center)
        elif event.key == '3':
            self.color = random.choice(list(CSS4_COLORS.values()))
            radius = 1.0
            theta = np.linspace(0, 2 * np.pi, 360)
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            center = np.mean(self.transformed_shape, axis=0)
            self.transformed_shape = np.column_stack((x, y))
            self.transformed_shape = transposition(self.transformed_shape, center)
        elif event.key == 's' or event.key == 'ы':
            self.save_transformed_shape()
        self.draw_shape()

    def on_scroll(self, event):
        if event.button == 'up':
            self.transformed_shape = scale(self.transformed_shape, 0.9, 0.9, np.mean(self.transformed_shape, axis=0))
        elif event.button == 'down':
            self.transformed_shape = scale(self.transformed_shape, 1.1, 1.1, np.mean(self.transformed_shape, axis=0))
        self.color = random.choice(list(CSS4_COLORS.values()))
        self.draw_shape()

    def save_transformed_shape(self):
        np.savetxt("transformed_shape.txt", self.transformed_shape)
    
app = TransformApp()
plt.show()