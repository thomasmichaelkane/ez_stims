"""
This module provides utility functions for setting up a Psychopy experiment environment, including configuring a monitor, creating a stimulus presentation window, and calculating the viewing angle of the screen.

Module Functions:
- load_config(): Loads the configuration file.
- setup_monitor(resolution, screen_width, viewing_distance, **kwargs): Setup a Psychopy monitor object with specified settings.
- setup_window(monitor, screen_number, **kwargs): Setup a Psychopy window for stimulus presentation.
- get_viewing_angle(screen_width, viewing_distance): Calculate the viewing angle of the screen.
"""

import numpy as np
import os

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

def set_stimulus_size(monitor_config):
    
    resolution = monitor_config["resolution"]
    ratio = monitor_config["ratio_stimulus-screen"]

    stim_size = (resolution[0]/ratio, resolution[1]/ratio)
    
    return stim_size

# create output folder
def create_output_folder(name, parent_folder):
    
    folder_path = os.path.join(parent_folder, name)
    
    os.mkdir(folder_path)
    
    return folder_path