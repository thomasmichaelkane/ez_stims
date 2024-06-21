from psychopy import event, core, visual
import time
import sys
from rich.table import Table
from rich.console import Console

from ez_stims.utils.util_funcs import *
from ez_stims.utils.enums import EdgeBehavior

class SingleDotStim():

    def __init__(self, config, monitor_config):
        
        # assign config as attributes
        for name, value in monitor_config.items():
            setattr(self, name, value)
            
        for name, value in config.items():
            setattr(self, name, value)

        # initialise variables and left and right check arrays
        self.cycles_complete = 0

        # calculate viewing angle and resolution ratio
        self.viewing_angle = get_viewing_angle(self.screen_width, self.viewing_distance)
        self.resolution_ratio = self.resolution[1]/self.resolution[0]
        
        self.behavior = EdgeBehavior[self.behavior]

        # force direction if at an end location
        if self.start_x == 1:
            self.direction = -1
        elif self.start_x == -1:
            self.direction = 1
            
        self.dot_width = self.dot_radius
        self.dot_height = self.dot_width/self.resolution_ratio
        
        # calculate time varaibles
        self.cycle_period = self.viewing_angle/self.velocity
        self.phase_advance = self.resolution_ratio * (2/(self.cycle_period*self.frame_rate)) * self.direction
        self.loop_change = (2*self.dot_radius) + 2

        # find true starting position (weighted to ensure 1/-1 is offscreen)
        self.start_x = self.start_x * (1+self.dot_radius)/1
        
        # setup x coordinate variables
        self.dot_x = self.start_x
            
    # methods
    def add_window(self, window):
        """ Add a psychopy window for the stimulus to be presented on """
        
        self.window = window
    
    def start_timer(self):
        """ Start timer for runtime of stimulus presentation """

        self.timer = core.Clock()

    def get_timestamp(self):
        """ Return milisecond timestamp """

        time_unix = time.time()
        time_ms = round(time_unix * 1000)
        
        return time_ms

    def get_keypress(self):
        """ Listen for key press """

        keys = event.getKeys()
        if keys:
            return keys[0]
        else:
            return None

    def wait(self):
        """ Wait for keypress before kalatsky presentation """

        waiting = True

        while waiting:
            
            key = self.get_keypress()
            if key == "space":
                waiting = False

    def background(self):
        """ Display background colour to the screen """
        
        self.background = visual.Rect(self.window, 
                                      size=3, 
                                      fillColor=self.background_color, 
                                      colorSpace='rgb',
                                      autoDraw=True)
        
        self.window.flip()
    
    def present(self):
        """ Prsent Kalatsky stimulus """
        
        self.dot = visual.Circle(self.window, 
                                size=(self.dot_width, self.dot_height), 
                                units="norm",
                                fillColor=self.dot_color,
                                pos=(self.start_x, self.path_y),
                                autoDraw=True)
        
        self.window.flip()
        
        # play kalatsky stimulus
        while self.cycles_complete < self.cycles:
            
            key = self.get_keypress()
            
            self.advance()
            
            # end if return is pressed  
            if key == "return":

                self.window.close()
                sys.exit()
         
    def advance(self):
        """ Advance the moving checks or bars """
        
        if self.behavior.name == "BOUNCE":
            
            self.check_reflect()
            
        elif self.behavior.name == "LOOP":
            
            self.check_repeat()
            
        self.dot_x += self.phase_advance
        self.update_pos(self.phase_advance)
        self.window.flip()
                
    def check_reflect(self):
        
        if (self.dot_x < -self.dot_radius-1) or (self.dot_x > 1+self.dot_radius):
                
            self.phase_advance = -self.phase_advance
            self.new_cycle()
                
    def check_repeat(self):
        
        if (self.dot_x < -self.dot_radius-1):
            
            self.dot_x = self.dot_x + self.loop_change
            self.update_pos(self.loop_change)
            self.new_cycle()
            
        elif (self.dot_x > 1+self.dot_radius):
            
            self.dot_x = self.dot_x - self.loop_change
            self.update_pos(-self.loop_change)
            self.new_cycle()
            
    def update_pos(self, increment):

        self.dot.pos += (increment, 0)
            
    def new_cycle(self):
        
        core.wait(self.lag)
        self.cycles_complete += 1
    
    def print_settings(self):
        
        table = Table(title="Stimulus Information")
        
        table.add_column("variable", style="cyan")
        table.add_column("units", style="yellow")
        table.add_column("value", justify="right", style="magenta")
        
        table.add_row("viewing angle", "degrees", "{:.1f}".format(self.viewing_angle))
        table.add_row("cycle period", "seconds", "{:.2f}".format(self.cycle_period))
        table.add_row("number of cycles", "--", "{:d}".format(self.cycles))
        
        console = Console()
        console.print(table)