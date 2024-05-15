
from psychopy import event, core, visual
import time
import sys
import numpy as np
import math
import random
from rich.table import Table
from rich.console import Console

from ez_stims.utils.util_funcs import *
from ez_stims.visual.geometry import tangent_linspace

class DotStim():

    def __init__(self, config, monitor_config):
        
        # assign config as attributes
        for name, value in monitor_config.items():
            setattr(self, name, value)
            
        for name, value in config.items():
            setattr(self, name, value)

        self.dots = []

        # calculate viewing angle and resolution ratio
        self.viewing_angle = get_viewing_angle(self.screen_width, self.viewing_distance)
        self.resolution_ratio = self.resolution[1]/self.resolution[0]
        self.screen_diagonal = math.hypot(self.resolution[0], self.resolution[1])
        
        # calculate time varaibles
        self.phase_advance = -(self.resolution_ratio * self.dot_velocity * 100)/self.frame_rate
        self.spawn_period = 1/self.spawn_frequency 
        
        self.angle_rad = math.radians(self.angle)
        self.x_increment = np.cos(self.angle_rad) * self.phase_advance
        self.y_increment = np.sin(self.angle_rad) * self.phase_advance
        
        self.screen_circle_radius = self.screen_diagonal*0.55
        self.spawn_exclusion_width = int(round(self.num_spawn_loc*self.dot_radius_pix/self.screen_diagonal))
        self.possible_spawn = range(self.num_spawn_loc)
        
        genx, geny = tangent_linspace(theta=self.angle_rad, 
                                      radius=self.screen_circle_radius, 
                                      length=self.screen_diagonal, 
                                      N=self.num_spawn_loc)
        
        self.spawn_linspace = list(zip(genx, geny))
        
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
        
        spawn_timer = core.CountdownTimer(self.spawn_period)
        kill_timer = core.CountdownTimer(self.kill_delay)
        
        self.killing = False

        # play kalatsky stimulus
        while True:
            
            key = self.get_keypress()
            
            self.advance()
            
            if kill_timer <= 0:
                self.killing = True
            
            # when flip timer ends, reverse colours and reset timer
            if spawn_timer.getTime() <= 0:
                
                # self.flip_stim()
                self.spawn_dot()
                spawn_timer.reset()
                print("Dot count: " + str(len(self.dots)), end="\r")

                # if killing:
                #     self.delete_dots()
            
            # end if return is pressed  
            if key == "return":

                print("Dot count: " + str(len(self.dots)))
                self.window.close()
                sys.exit()
        
    def advance(self):

        for i in range(len(self.dots)):
            
            # advance position
            self.dots[i].pos += (self.x_increment, self.y_increment)
            
        self.window.flip()
    
    def delete_dots(self):
        
        for i in range(len(self.dots)):
            
            # remove old dots
            if (abs(self.dots[i].pos[0]) > self.screen_circle_radius*1.5) or (abs(self.dots[i].pos[1]) > self.screen_circle_radius*1.5):
                self.dots.pop(i)
                print("dot deleted")
                break
    
    def spawn_dot(self):
        
        i = random.choice(self.possible_spawn)
        position = self.spawn_linspace[i]
        
        self.dots.append(visual.Circle(self.window, 
                                        radius=self.dot_radius_pix, 
                                        units="pix",
                                        fillColor="white",
                                        pos=position,
                                        autoDraw=True))
        
        self.possible_spawn = list(range(self.num_spawn_loc))
        
        bottom = i-self.spawn_exclusion_width if i > (self.spawn_exclusion_width/2) else 0
        top = i-self.spawn_exclusion_width if i < self.num_spawn_loc - (self.spawn_exclusion_width/2) else self.num_spawn_loc
        
        [self.possible_spawn.remove(x) for x in range(bottom, top)]
    
    def print_settings(self):
        
        table = Table(title="Stimulus Information")
        
        table.add_column("variable", style="cyan")
        table.add_column("units", style="yellow")
        table.add_column("value", justify="right", style="magenta")
        
        table.add_row("viewing angle", "degrees", "{:.1f}".format(self.viewing_angle))
        # table.add_row("stimulus width", "degrees", "{:.1f}".format(self.stim_width))
        # table.add_row("cycle period", "seconds", "{:.2f}".format(self.cycle_period))
        # table.add_row("number of cycles", "--", "{:d}".format(self.cycles))
        
        console = Console()
        console.print(table)