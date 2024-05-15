import math
import numpy as np
import matplotlib.pyplot as plt

def tangent_linspace(theta, radius, length, N):

    x0 = (math.sin(theta) * length/2) + (np.cos(theta) * radius)
    y0 = (-math.cos(theta) * length/2) + (np.sin(theta) * radius)
    
    x1 = (-math.sin(theta) * length/2) + (np.cos(theta) * radius)
    y1 = (math.cos(theta) * length/2) + (np.sin(theta) * radius)
    
    xn = np.linspace(x0, x1, N)
    yn = np.linspace(y0, y1, N)
    
    return xn, yn

def plot_circle_and_tangent(R, xn, yn):
    # Generate points for the circle
    circle_theta = np.linspace(0, 2*np.pi, 100)
    circle_x = R * np.cos(circle_theta)
    circle_y = R * np.sin(circle_theta)

    # Plot the circle and tangent line
    plt.figure(figsize=(8, 8))
    plt.plot(circle_x, circle_y, label='Circle')
    
    plt.plot(xn, yn, 'ro')
    plt.axis('equal')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Circle and Tangent Line Visualization')
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.legend()
    plt.show()
    

if __name__ == '__main__':

    # Example usage
    R = 3  # Radius of the circle
    L = 3.5
    N = 20
    theta = 45
    theta = math.radians(theta)

    xn, yn = tangent_linspace(theta, R, L, N)

    generator_line = list(zip(xn, yn))
    
    plot_circle_and_tangent(R, xn, yn)