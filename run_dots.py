"""Presentation of dots stimulus.

This script allows for timed or continuous presentation of a
fully customisabe dots stimulus with either coloured bars
or a vertical checkerboard.

Example
-------
Simply type::

    $ python present.py
    
Once the window/background us presented, you will then need to 
hit enter to begin the stimulus.

Attributes
----------
There are no command line attributes for this program. 
Instead the settings file should be edited for customisation.

Please navigate to lib/settings/settings.py

There are two dictionaries of settings. The first relates to the 
monitor used for presentation - these must be changed to the correct 
values for reproducible results. The second is dots settings 
that can be used to change the stimulus. It is reccomended to save 
a settings file with the date before changing to again allow for
reproducability.
"""
from psychopy import logging

from ez_stims import DotStim, setup

def run():
    
    dots_config = setup.load_config('dots.yaml')
    monitor_config = setup.load_config('monitor.yaml')
    
    logging.console.setLevel(logging.CRITICAL)
    
    monitor = setup.setup_monitor(**monitor_config)
    window = setup.setup_window(monitor, **monitor_config)

    dots = DotStim(dots_config, monitor_config)
    dots.add_window(window)
    
    dots.print_settings()
    
    # input("Press ENTER to start stimulus...")

    dots.background()
    # dots.wait()
    # dots.start_timer()
    
    dots.present()

if __name__ == '__main__':
    run()