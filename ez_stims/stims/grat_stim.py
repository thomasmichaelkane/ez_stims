from psychopy import event, core, visual
import random
import time
import sys
from rich import print as rprint

from ez_stims.utils.util_funcs import *
from ez_stims.visual.stimulus import Stimulus
from ez_stims.utils.util_funcs import *

class GratStim():

    def __init__(self, config, monitor_config, log):
        
        self.global_config = config["global"]
        self.paradigm = config["paradigm"]
        self.monitor_config = monitor_config
        self.log = log
        
        self.stim_size = set_stimulus_size(self.monitor_config)
        
        # assign config as attributes
        for name, value in self.monitor_config.items():
            setattr(self, name, value)
            
        for name, value in self.global_config.items():
            setattr(self, name, value)
            
        if self.randomise:
            
            random.shuffle(self.paradigm)
            
        self.stimuli = []
            
    # methods
    def background(self):
        """ Display background colour to the screen """
        
        self.baseline.draw()
        self.window.flip()

    def wait(self):
        """ Wait for keypress before kalatsky presentation """

        waiting = True

        while waiting:
            
            key = self.get_keypress()
            if key == "space":
                waiting = False

    def add_window(self, window):
        """ Add a psychopy window for the stimulus to be presented on """
        
        self.window = window
    
    def add_stimuli(self):
        # A light green text
        self.baseline = visual.Rect(self.window, size=3, fillColor=self.baseline_color, colorSpace='rgb')
        for i in range(len(self.paradigm)):
            self.stimuli.append(Stimulus(self.window, self.monitor_config, self.paradigm[i], self.stim_size))
            
        self.num_stimuli = len(self.stimuli)

    def start_timer(self):
        """ Start timer for runtime of stimulus presentation """

        self.timer = core.Clock()
        
    def present(self):
        
        exp_start_time = self.get_timestamp()
        
        if self.is_intro_active():
            self.intro(exp_start_time)

        for i in range(1, self.iterations+1):
            for j in range(self.num_stimuli):

                rprint(f"Baseline", end='\r')
                self.present_baseline()
                
                stim_name = self.stimuli[j].get_name()
                stim_init_time = self.get_timestamp()
                stim_init_time_seconds = round((stim_init_time-exp_start_time)/1000, 1)
                
                rprint(f"Iteration {i} - Stimulus {stim_name} [{stim_init_time_seconds}]", end='\r')
                
                self.present_stimulus(j)
                
                stim_end_time = self.get_timestamp()
                stim_end_time_seconds = round((stim_end_time-exp_start_time)/1000, 1)
                
                self.log.add_stim(stim_name, i, stim_init_time, stim_end_time)
                
                rprint(f"Iteration {i} - Stimulus {stim_name} [{stim_init_time_seconds}-{stim_end_time_seconds}]")
        
        if self.is_outro_active():
            self.outro(exp_start_time)

    def get_timestamp(self):
        
        time_unix = time.time()
        time_ms = round(time_unix * 1000)
        
        return time_ms
    
    def get_stimulus_name(self, j):
        
        current_stim = self.paradigm[j]
        
        return current_stim["name"]

    def get_keypress(self):
        """ Listen for key press """

        keys = event.getKeys()
        if keys:
            return keys[0]
        else:
            return None

    def intro(self, exp_start_time):
        
        intro_timer = core.CountdownTimer(self.intro_duration)
        self.baseline.draw()
        self.window.flip()
        
        rprint(f"Intro [0.0]", end='\r')

        while intro_timer.getTime() > 0:

            pass
        
        intro_end_time = self.get_timestamp()
        intro_end_time_seconds = round((intro_end_time-exp_start_time)/1000, 1)
        
        rprint(f"Intro [0.0-{intro_end_time_seconds}]")
        
    def outro(self, exp_start_time):
        
        outro_timer = core.CountdownTimer(self.outro_duration)
        self.baseline.draw()
        self.window.flip()
        
        outro_start_time = self.get_timestamp()
        outro_start_time_seconds = round((outro_start_time-exp_start_time)/1000, 1)
        
        rprint(f"Outro [{outro_start_time_seconds}]", end='\r')

        while outro_timer.getTime() > 0:

            pass
        
        exp_end_time = self.get_timestamp()
        exp_end_time_seconds = round((exp_end_time-exp_start_time)/1000, 1)
        
        rprint(f"Outro [{outro_start_time_seconds}-{exp_end_time_seconds}]")

    def present_baseline(self):
        
        baseline_timer = core.CountdownTimer(self.baseline_duration)
        
        self.baseline.draw()
        self.window.flip()
        # core.wait(self.baseline_duration)
        
        # # advance phase of grating continuously until key press command
        while baseline_timer.getTime() > 0:

        # check for key press
            key = self.get_keypress()

            if key == "return":

                # stop
                self.window.close()
                sys.exit()

        #     # wait
        #     continue
            
    def present_stimulus(self, j):
        
        # done = False
        # paused = False
        
        stimulus = self.stimuli[j]

        stimulus_timer = core.CountdownTimer(stimulus.get_duration())

        # advance phase of grating continuously until key press command
        while stimulus_timer.getTime() > 0:

            stimulus.advance()
            self.window.flip()
            
            # check for key press
            key = self.get_keypress()

            if key == "return":

                # stop
                self.window.close()
                sys.exit()

            # elif key == "space":

            #     # pause
            #     done = self.pause()
         
    def is_intro_active(self):
        
        return self.intro_active
        
    def is_outro_active(self):
        
        return self.outro_active
            
    def randomising_order(self):
        
        return self.randomise

    def shuffle(self):
        
        random.shuffle(self.stimuli)
        
    def get_num_iterations(self):
        
        return self.iterations
        
    def get_num_stimuli(self):
        
        return self.num_stimuli






    # def pause(self):
    #     """ Pause stimulus and timer """

    #     # find time at pause
    #     self.duration = self.timer.getTime()
    #     print("Pause time: " + "{:.2f}".format(self.duration))

    #     paused = True

    #     while paused:

    #         # check for key press
    #         key = event.waitKeys()[0]

    #         if key == "return":

    #             # stop
    #             paused = False
    #             done = True
    #             self.window.close()

    #             return done

    #         elif key == "space":

    #             # resume
    #             self.restart_timer()

    #             paused = False
    #             done = False

    #             return done

    # def restart_timer(self):
    #     """ Restart timer """

    #     # restart timer from time of pause
    #     self.timer.reset(newT=(self.duration*-1))

    #def stop(self):
    #     """ Stop stimulus presentation and return total time """

    #     self.duration = self.timer.getTime()
    #     return self.duration