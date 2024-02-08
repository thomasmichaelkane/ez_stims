from psychopy import logging

from ez_stims import GStim, Log, setup

def run():
    
    gstim_config = setup.config('gstim.yaml')
    monitor_config = setup.config('monitor.yaml')

    monitor = setup.setup_monitor(**monitor_config)
    window = setup.setup_window(monitor, **monitor_config)
    log = Log()
    
    logging.console.setLevel(logging.CRITICAL)
    
    gstim = GStim(gstim_config, monitor_config, log)
    gstim.add_window(window)
    gstim.add_stimuli()
    
    # wait for key press
    input("Press ENTER to start stimulus...")
    
    gstim.background()
    gstim.wait()
    gstim.start_timer()
    
    gstim.present()

    log.write_log()

if __name__ == '__main__':
    run()

