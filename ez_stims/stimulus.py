from psychopy import core, visual

from ez_stims.enums import GBehavior
from ez_stims.utils import *

class Stimulus:
    def __init__(self, window, monitor_config, stimulus_config, size):
        
        self.window = window
        self.frame_rate = monitor_config["frame_rate"]
        
        for name, value in stimulus_config.items():
            setattr(self, name, value)
            
        self.behavior = GBehavior[self.behavior]
            
        self.size = size            
        
        self.period = 1 / self.velocity
            
        self.temporal_frequency = self.velocity * self.spatial_frequency
        self.phase_advance = self.temporal_frequency / self.frame_rate

        # create stimulus
        self.grating = visual.GratingStim(self.window, 
                                          tex="sin", 
                                          units="deg", 
                                          size=self.size, 
                                          sf=self.spatial_frequency,
                                          ori=self.orientation)
    
    def advance(self):
        
        if self.behavior.name == "FLICKER":
            
            self.flicker()
            
        elif self.behavior.name == "DRIFT":
            
            self.drift()
          
    def drift(self):
        
        self.grating.setPhase(self.phase_advance, '+')
        self.grating.draw()
        
    def flicker(self):
        
        self.grating.setPhase(0.5, '+')
        self.grating.draw()
        core.wait(self.period)
        
    def get_duration(self):
        
        return self.duration
    
    def get_name(self):
        
        return self.name
        
        