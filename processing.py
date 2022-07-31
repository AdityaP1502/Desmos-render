from time import time
import multiprocessing
import sys
import preprocess
from loadingAnimation import Color
from Images import Image

# FILTER RESULT : https://colab.research.google.com/drive/11YfMxNxRO7i2qGXt0SngsUwLUyB5tROe?usp=sharing

# TO DO : 
"""
1.  Use MultiProcess To Handle Multiple Conversion
2.  Sending Data directly through the front end, without first sending it through a text file then hardcode the expression in the html file
3.  Render The Video
"""

n_finished = multiprocessing.Value('i', 0)
n_finished_batch = multiprocessing.Value('i', 0)
N_FILES = multiprocessing.Value('i', 0)

class Process():
    def __init__(self, in_path, out_path, filename, filetype, n_per_batch, method) -> None:
       self.n = 0
       self.start_time = 0
       self.IN_PATH = in_path
       self.OUT_PATH = out_path
       self.FILENAME = filename
       self.FILETYPE = filetype
       self.N_PER_BATCH = n_per_batch
       self.method = method
       
    
    def processExpression(self, filename):
        exprs = Image.getLatexExpression(filename, self.method)
        
        with n_finished.get_lock():
            n_finished_batch.value += 1
        
        # time elapsed
        elapsed = (time() - self.start_time)
        rate = n_finished_batch.value / elapsed
        time_remaining = ((N_FILES.value - n_finished_batch.value) / rate)
        
        # get hours, minutes and seconds from time_remaining
        time_remaining_h = time_remaining // 3600
        time_remaining_m = (time_remaining % 3600) // 60
        time_remaining_s = (time_remaining % 3600) % 60
        
        sys.stdout.write('\r'+Color.print_colored('loading...', utils=["bold"]) + '  process '+str(n_finished_batch.value)+'/'+str(N_FILES.value)+' '+ '{:.2f}'.format(n_finished_batch.value/N_FILES.value*100)+'%' + " " + Color.print_colored("Time remaining:", color_fg=[120, 10, 0], utils=["bold"]) + " {:.2f}h, {:.2f}m, {:.2f}s".format(time_remaining_h, time_remaining_m, time_remaining_s) + "          ")
        return exprs
    
    def writeToFile(self, dir, frameFiles, batch):
        filename, filetype = "out{}", ".txt"
        preprocess.Preprocess.changeDir(self.OUT_PATH)

        for (i, exprs) in enumerate(frameFiles):
            f = open(filename.format(batch * self.N_PER_BATCH + i + 1) + filetype, 'w')
            line = ""
            for expr in exprs:
                line += expr + "\n" 

            f.write(line)
            f.close()
           
        print(Color.print_colored("\rDone!                    ", color_fg=[100, 10, 0], utils = ["bold"]))
        preprocess.Preprocess.changeDir(dir)
        
    def start(self):
        # Open the image 
        # change the path dir 
        temp = preprocess.getcwd()
        preprocess.Preprocess.changeDir(self.IN_PATH)

        # frame files
        n, batch = len(preprocess.listdir()), 0
        n_batch = n // self.N_PER_BATCH + (1 if n % self.N_PER_BATCH > 0 else 0)
        
        while batch < n_batch:
            with n_finished.get_lock():
                N_FILES.value = min(self.N_PER_BATCH, n - n_finished.value)
                
            print(Color.print_colored("\rProcessing", color_fg=[10, 120, 10], utils=["bold"]) + " {}th batch".format(batch + 1))
            frameFiles = ["{}{}.{}".format(self.FILENAME, batch * self.N_PER_BATCH + i + 1, self.FILETYPE) for i in range(N_FILES.value)]
            start_time = time()
            self.start_time = start_time

            # store each images exprs in a 2D array
            with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
                frameFiles = pool.map(self.processExpression, frameFiles)


            elapsed_time = time() - start_time
            elapsed_time_h = elapsed_time // 3600
            elapsed_time_m = (elapsed_time % 3600) // 60
            elapsed_time_s = (elapsed_time % 3600) % 60

            
            sys.stdout.flush()
            print()
            print("Done! Batch = {} / {}. Took about {:.2f} hours {:.2f} minutes {:.2f} seconds".format(batch + 1, n_batch, elapsed_time_h, elapsed_time_m, elapsed_time_s))
            print(f"Writting Latex Expressions to file in " + Color.print_colored(f"{self.OUT_PATH}", color_fg =[10, 10, 120]))
            print("Please Wait")
            
            self.writeToFile(temp, frameFiles, batch)
            frameFiles = []
            batch += 1
            n_finished.value += n_finished_batch.value
            n_finished_batch.value = 0 
            
            preprocess.Preprocess.changeDir(self.IN_PATH)
            
    
            
        preprocess.Preprocess.changeDir(temp)
    