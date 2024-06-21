import os
from ez_stims import segmenting
from ez_stims.utils.util_funcs import *

def run():

    video_filename, log_filename, time_filename, parent_folder = get_filenames()
    
    output_folder = create_output_folder("subscans", parent_folder)
    
    log = segmenting.read_log(log_filename)
    scan_reader = segmenting.open_scan(video_filename)
    scan_unix_time = segmenting.read_start_time(time_filename)
    
    num_frames = segmenting.get_num_frames(scan_reader)
    
    timestamps = segmenting.get_frame_timestamps(scan_reader, num_frames, scan_unix_time)
    
    scan = scan_reader.data()
    
    for entry in log:
        
        start_time, end_time = segmenting.get_stim_times(entry)
        start_frame, end_frame = segmenting.get_stim_frames(timestamps, start_time, end_time)
        
        subscan = segmenting.get_subscan(scan, start_frame, end_frame)
        
        name = entry["Stimulus"] + segmenting.get_iteration_str(entry) + ".tif"
        path = os.path.join(output_folder, name)
  
        segmenting.write_subscan(path, subscan)
    
if __name__ == "__main__":
    run()