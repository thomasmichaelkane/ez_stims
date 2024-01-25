"""
This class represents a distribution of cells and provides methods for analyzing and visualizing cell distributions.

Class Attributes:
- points (list): List of points representing cell coordinates.
- dim (tuple): Dimensions of the image.
- mpp (float): Microns per pixel.
- id (str): Identifier for the cell distribution.

Instance Attributes:
- points_array (np.array): Numpy array of points.
- alpha_override (float): Override value for the alpha parameter.
- dil_factor_override (float): Override value for the dilation factor.
- alpha (float): Alpha parameter for the Voronoi diagram.
- dilation_strength (float): Strength of dilation for border expansion.
- stat_prec (int): Precision for statistical values.
- vor (scipy.spatial.Voronoi): Voronoi diagram object.
- image_area (float): Area of the image.
- estimated_area (float): Estimated area of the cell distribution.
- num_unbound_cells (int): Number of unbound cells.
- cells (list): List of cell indices.
- dilated_poly (list): List of vertices for the dilated polygon.
- bound_cells (list): List of indices for bound cells.
- num_bound_cells (int): Number of bound cells.

Methods:
- set_dilation_factor(): Sets the dilation factor based on the override value.
- find_bound_cells(): Finds bound cells using the Voronoi diagram and dilated polygon.
- update_alpha(new_alpha): Updates the alpha parameter with a new value.
- find_border(): Finds the border of the cell distribution using the Voronoi diagram.
- dilate_border(): Dilates the border of the cell distribution.
- show_voronoi(): Displays the Voronoi diagram for bound cells.
- show_voronoi_unbound(): Displays the Voronoi diagram for all cells.
- show_points_with_border(): Displays the cell distribution with the dilated border.
- show_mask(): Displays the mask image.
- show_dil_mask(): Displays the dilated mask image.
- calc_stats(): Calculates various statistical measures for the cell distribution.
- show_histograms(): Displays histograms for various statistical measures.
- print_report_full(): Prints a detailed report with global and bound cell statistics.
- print_report(): Prints a concise report with key statistical measures.
- save(): Saves cell data to an output file.
- get_bound_stats(): Retrieves statistics for bound cells.
- get_icd(): Retrieves the mean inter-cell distance.
- get_nn(): Retrieves the mean nearest neighbor distance.
- get_mean_cell_area(): Retrieves the mean Voronoi domain cell area.
- get_nnri(): Retrieves the nearest neighbor regularity index.
- get_alt_nnri(): Retrieves an alternative nearest neighbor regularity index.
- get_vdri(): Retrieves the Voronoi domain regularity index.
- get_points_array(): Retrieves the array of cell points.
- get_area(): Retrieves the estimated area of the cell distribution.
"""

from psychopy import event, core, visual
import time
import sys
import numpy as np
from rich.table import Table
from rich.console import Console

from .utils import *
from .enums import StimType, Behavior
class Kalatsky():

    def __init__(self, settings):
        
        # assign settings as attributes
        for name, value in settings["monitor"].items():
            setattr(self, name, value)
            
        for name, value in settings["kalatsky"].items():
            setattr(self, name, value)
            
        self.stimulus_type = StimType[self.stimulus_type]
        self.behavior = Behavior[self.behavior]

        # initialise variables and left and right check arrays
        self.flipped = False
        self.checks_left = []
        self.checks_right = []
        self.cycles_complete = 0

        # calculate viewing angle and resolution ratio
        self.viewing_angle = get_viewing_angle(self.screen_width, self.viewing_distance)
        self.resolution_ratio = self.resolution[1]/self.resolution[0]

        # force direction if at an end location
        if self.starting_position == 1:
            self.direction = -1
        elif self.starting_position == -1:
            self.direction = 1
        
        # calculate time varaibles
        self.cycle_period = self.viewing_angle/self.velocity
        self.phase_advance = self.resolution_ratio * (2/(self.cycle_period*self.frame_rate)) * self.direction
        self.flip_period = 1/self.flip_frequency 
        
        # calculate size variables
        self.check_height = 2/self.number_of_checks
        self.check_width = self.check_height * self.resolution_ratio
        self.stim_width = (self.check_width*self.viewing_angle)
        self.loop_change = (2*self.check_width) + 2

        # find true starting position (weighted to ensure 1/-1 is offscreen)
        self.starting_position = self.starting_position * (1+self.check_width)/1
        
        # setup x coordinate variables
        self.centre = self.starting_position
        self.left_x = self.centre-(self.check_width/2)
        self.right_x = self.centre+(self.check_width/2)
            
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
        
        flip_timer = core.CountdownTimer(self.flip_period)
        colors = self.initial_colors
        
        # draw checkerboard or bars
        for i in np.linspace(start=(self.check_height/2)-1, stop=1-(self.check_height/2), num=self.number_of_checks):
        
            self.checks_left.append(visual.Rect(self.window, 
                                    size=(self.check_width, self.check_height), 
                                    units="norm",
                                    fillColor=colors[0],
                                    pos=(self.left_x, i),
                                    autoDraw=True))
            
            self.checks_right.append(visual.Rect(self.window, 
                                    size=(self.check_width, self.check_height), 
                                    units="norm",
                                    fillColor=colors[1],
                                    pos=(self.right_x, i),
                                    autoDraw=True))
            
            if self.stimulus_type.name == "CHECK": colors.reverse()
        
        self.window.flip()
        
        # play kalatsky stimulus
        while self.cycles_complete < self.cycles:
            
            key = self.get_keypress()
            
            self.advance()
            
            # when flip timer ends, reverse colours and reset timer
            if flip_timer.getTime() <= 0: 
                
                self.flip_stim()
                flip_timer.reset()
            
            # end if return is pressed  
            if key == "return":

                self.window.close()
                sys.exit()
        
    def flip_stim(self):
        """ Reverse the colours of checks or bars """

        if self.flipped is True:
            colors = self.initial_colors
            colors.reverse()
        else:
            colors = self.initial_colors

        for i in range(len(self.checks_left)):
            
            self.checks_left[i].color = colors[1]
            self.checks_right[i].color = colors[0]
            if self.stimulus_type.name == "CHECK": colors.reverse()
            
        self.flipped = not self.flipped
        self.window.flip()
         
    def advance(self):
        """ Advance the moving checks or bars """
        
        if self.behavior.name == "BOUNCE":
            
            self.check_reflect()
            
        elif self.behavior.name == "LOOP":
            
            self.check_repeat()
            
        self.centre += self.phase_advance
        self.update_pos(self.phase_advance)
        self.window.flip()
                
    def check_reflect(self):
        
        if (self.centre < -self.check_width-1) or (self.centre > 1+self.check_width):
                
            self.phase_advance = -self.phase_advance
            self.new_cycle()
                
    def check_repeat(self):
        
        if (self.centre < -self.check_width-1):
            
            self.centre = self.centre + self.loop_change
            self.update_pos(self.loop_change)
            self.new_cycle()
            
        elif (self.centre > 1+self.check_width):
            
            self.centre = self.centre - self.loop_change
            self.update_pos(-self.loop_change)
            self.new_cycle()
            
    def update_pos(self, increment):
        
        for i in range(len(self.checks_left)):
            self.checks_left[i].pos += (increment, 0)
            self.checks_right[i].pos += (increment, 0)
            
    def new_cycle(self):
        
        core.wait(self.lag)
        self.cycles_complete += 1
    
    def print_settings(self):
        
        table = Table(title="Stimulus Information")
        
        table.add_column("variable", style="cyan")
        table.add_column("units", style="yellow")
        table.add_column("value", justify="right", style="magenta")
        
        table.add_row("viewing angle", "degrees", "{:.1f}".format(self.viewing_angle))
        table.add_row("stimulus width", "degrees", "{:.1f}".format(self.stim_width))
        table.add_row("cycle period", "seconds", "{:.2f}".format(self.cycle_period))
        table.add_row("number of cycles", "--", "{:d}".format(self.cycles))
        
        console = Console()
        console.print(table)