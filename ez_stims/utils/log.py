import os
import csv
from datetime import datetime

class Log():

    def __init__(self):
        
        self.log = []
        now = datetime.now()
        self.time_str = now.strftime("%Y-%m-%d_%H-%M-%S")	
        
        if not os.path.exists("logs"):
            
            os.mkdir("logs")
            
        self.log_name = "logs/log_{}.csv".format(self.time_str)
    
    def add_stim(self, name, iteration, start, end):
        
        entry = [name, iteration, start, end]
        
        self.log.append(entry)
        
    def print_log(self):
        
        print(self.log)
    
        
    def write_log(self):
        
        with open(self.log_name, 'w', newline='') as csv_file:
            log_writer = csv.writer(csv_file, delimiter=',')
            
            log_writer.writerow(['Stimulus', 'Iteration', 'Start time', 'End time'])
            
            for row in self.log:
                log_writer.writerow(row)