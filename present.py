"""Presentation of Kalatsky stimulus.

This script allows for timed or continuous presentation of a
fully customisabe Kalatsky stimulus with either coloured bars
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
values for reproducible results. The second is kalatsky settings 
that can be used to change the stimulus. It is reccomended to save 
a settings file with the date before changing to again allow for
reproducability.
"""
from psychopy import logging

from lib import experiments
from lib.utils import load_config

def main():
    
    settings = load_config()
    
    logging.console.setLevel(logging.CRITICAL)
    
    kalatsky = experiments.setup_kalatsky(settings)

    kalatsky.background()
    kalatsky.wait()
    kalatsky.start_timer()
    kalatsky.present()

main()