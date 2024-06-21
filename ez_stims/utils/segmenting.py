import csv
import tifffile
from ScanImageTiffReader import ScanImageTiffReader
from bisect import bisect

# csv read
def read_log(filename):
    
    with open(filename, mode='r') as csv_file:
        log_reader = csv.DictReader(csv_file, delimiter=',')
        return list(log_reader)
    
# txt read
def read_start_time(filename):
    
    with open(filename, mode='r') as file:
        unix_start_time = int(file.read().rstrip())
        return unix_start_time

# extract start and end times of a stim
def get_stim_times(log_stim):
    
    start = int(log_stim["Start time"])
    end =  int(log_stim["End time"])
    return start, end

# open main scan file
def open_scan(filename): 
    
    scan = ScanImageTiffReader(filename);
    return scan

# find numbeer of frames in scan
def get_num_frames(scan):
    
    num_frames = scan.data().shape[0]
    return num_frames

# change timestamp from seconds to milliseconds
def to_msec(timestamp_sec):
    
    timestamp_msec = int(round(float(timestamp_sec) * 1000))
    return timestamp_msec

# get the timestamp from the scan frame
def get_frame_timestamps(scan, num_frames, scan_unix_time):
    
    frame_timestamps = []
    
    for i in range(num_frames):
        frame_info = scan.description(i)
        info_list = frame_info.split()
        info_list = [i for i in info_list if i != "="]
        time_index = info_list.index("frameTimestamps_sec") + 1
        frame_time = (to_msec(info_list[time_index])) + scan_unix_time
        frame_timestamps.append(frame_time)
    
    return frame_timestamps
    
# change frame times to unix time
def normalise_frame_timestamps(frame_times, scan_unix_time):
    
    frame_unix_times = [frame_time + scan_unix_time for frame_time in frame_times]
    return frame_unix_times

# get timestamps for all frames
def get_stim_frames(frame_times, start_time, end_time):
    
    start_frame = bisect(frame_times, start_time) - 1 
    end_frame = bisect(frame_times, end_time)
    return start_frame, end_frame

# create sub_array
def get_subscan(scan, start, end):
    
    subscan = scan[start:end]
    return subscan

# get string of iteration for file naming
def get_iteration_str(entry):
    
    raw = int(entry["Iteration"])
    iter_string = "_Iteration-" + str(raw)
    return iter_string
    
# save video
def write_subscan(path, subscan):
    
    tifffile.imwrite(path, subscan)