"""Presentation of single_dot stimulus.

This script allows for timed or continuous presentation of a
fully customisabe single_dot stimulus with either coloured bars
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
values for reproducible results. The second is single_dot settings 
that can be used to change the stimulus. It is reccomended to save 
a settings file with the date before changing to again allow for
reproducability.
"""
from psychopy import logging

from ez_stims import SingleDotStim, setup

def run():
    
    single_dot_config = setup.load_config('single_dot.yaml')
    monitor_config = setup.load_config('monitor.yaml')
    
    logging.console.setLevel(logging.CRITICAL)
    
    monitor = setup.setup_monitor(**monitor_config)
    window = setup.setup_window(monitor, **monitor_config)

    single_dot = SingleDotStim(single_dot_config, monitor_config)
    single_dot.add_window(window)
    
    single_dot.print_settings()
    
    # input("Press ENTER to start stimulus...")

    single_dot.background()
    # single_dot.wait()
    single_dot.start_timer()
    
    single_dot.present()

if __name__ == '__main__':
    run()