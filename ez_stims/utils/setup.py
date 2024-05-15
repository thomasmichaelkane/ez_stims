import yaml
from psychopy import visual, monitors

def load_config(config_file):
    
    with open(f"config/{config_file}") as config:
        config = yaml.load(config.read(), Loader=yaml.Loader)
        
    return config

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