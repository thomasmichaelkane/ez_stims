from .utils import setup_monitor, setup_window
from .kalatsky import Kalatsky

def setup_kalatsky(settings):
    """
    Setup a Kalatsky stimulus with specific monitor settings.

    This function configures a monitor, creates a Kalatsky stimulus, prints its settings,
    waits for user input, sets up a stimulus presentation window, and adds the window to the Kalatsky instance.

    Returns:
    - kalatsky (Kalatsky): Instance of the Kalatsky class configured with the specified monitor settings.
    """
    monitor = setup_monitor(**settings["monitor"])

    kalatsky = Kalatsky(settings)
    kalatsky.print_settings()
    
    input("Press ENTER to start stimulus...")
    
    window = setup_window(monitor, **settings["monitor"])
    kalatsky.add_window(window)

    return kalatsky
    
   

