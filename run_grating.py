from psychopy import logging

from ez_stims import GratStim, Log, setup

def run():
    
    grating_config = setup.load_config('grating.yaml')
    monitor_config = setup.load_config('monitor.yaml')

    monitor = setup.setup_monitor(**monitor_config)
    window = setup.setup_window(monitor, **monitor_config)
    log = Log()
    
    logging.console.setLevel(logging.CRITICAL)
    
    gstim = GratStim(grating_config, monitor_config, log)
    gstim.add_window(window)
    gstim.add_stimuli()
    
    # wait for key press
    input("Press ENTER to start stimulus...")
    
    gstim.background()
    # gstim.wait()
    gstim.start_timer()
    
    gstim.present()

    log.write_log()

if __name__ == '__main__':
    run()

