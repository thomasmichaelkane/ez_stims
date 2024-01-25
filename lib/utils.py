"""
This module provides utility functions for setting up a Psychopy experiment environment, including configuring a monitor, creating a stimulus presentation window, and calculating the viewing angle of the screen.

Module Functions:
- load_config(): Loads the configuration file.
- setup_monitor(resolution, screen_width, viewing_distance, **kwargs): Setup a Psychopy monitor object with specified settings.
- setup_window(monitor, screen_number, **kwargs): Setup a Psychopy window for stimulus presentation.
- get_viewing_angle(screen_width, viewing_distance): Calculate the viewing angle of the screen.
"""

import numpy as np
import yaml
from psychopy import visual, monitors

def load_config():
    
    with open('config.yaml') as config:
        settings = yaml.load(config.read(), Loader=yaml.Loader)
        
    return settings

def setup_monitor(resolution, screen_width, viewing_distance, **kwargs):
    """ 
    Setup a Psychopy monitor object with specified settings.

    Parameters:
    - resolution (tuple): Tuple representing the screen resolution in pixels (width, height).
    - screen_width (float): Physical width of the screen in meters.
    - viewing_distance (float): Distance from the observer to the screen in meters.
    - **kwargs: Additional keyword arguments for future expansion.

    Returns:
    - monitor (psychopy.monitors.Monitor): Psychopy Monitor object configured with the provided settings.
    """
    monitor = monitors.Monitor('temp')
    monitor.setSizePix(resolution)
    monitor.setWidth(screen_width)
    monitor.setDistance(viewing_distance)
    
    return monitor

def setup_window(monitor, screen_number, **kwargs):
    """
    Setup a Psychopy window for stimulus presentation.

    Parameters:
    - monitor (psychopy.monitors.Monitor): Psychopy Monitor object containing display settings.
    - screen_number (int): Index of the screen to use for the window.
    - **kwargs: Additional keyword arguments for future expansion.

    Returns:
    - window (psychopy.visual.Window): Psychopy Window object configured based on the provided monitor settings.
    """
    window = visual.Window(monitor.getSizePix(),
                           monitor=monitor,
                           fullscr=True,
                           screen=screen_number,
                           color=[1, 1, 1],  # Background color (white in RGB).
                           allowGUI=False)
    
    return window

def get_viewing_angle(screen_width, viewing_distance):
    """
    Calculate the viewing angle of the screen.

    Parameters:
    - screen_width (float): Physical width of the screen in meters.
    - viewing_distance (float): Distance from the observer to the screen in meters.

    Returns:
    - theta (float): Viewing angle of the screen in degrees.
    """
    theta = 2 * np.arctan((screen_width/2)/viewing_distance) * (360/(2*np.pi))
                      
    return theta