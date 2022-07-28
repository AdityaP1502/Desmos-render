from fileinput import filename
from time import time
import cv2
import numpy as np
import multiprocessing
import potrace
import sys
import preprocess
from loadingAnimation import Loading, Color


# FILTER RESULT : https://colab.research.google.com/drive/11YfMxNxRO7i2qGXt0SngsUwLUyB5tROe?usp=sharing

# TO DO : 
"""
1.  Use MultiProcess To Handle Multiple Conversion
2.  Sending Data directly through the front end, without first sending it through a text file then hardcode the expression in the html file
3.  Render The Video
"""

n_finished = multiprocessing.Value('i', 0)
N_PER_BATCH = 1000

class Image():
    def __init__(self, filename) -> None:
        self.pixels = cv2.imread(filename)

    def threshold(self, factor = 0.5):
      ny, nx = np.shape(self.pixels)
      max = np.max(self.pixels) # max pixel value

      # Threshold the value of the pixel
      for i in range(ny):
        for j in range(nx):
          if self.pixels[i][j] > factor * max:
            self.pixels[i][j] = 1
          else:
            self.pixels[i][j] = 0

    def invertColor(self):
      ny, nx = np.shape(self.pixels)
      for i in range(ny):
        for j in range(nx):
          if self.pixels[i][j] == 0:
            self.pixels[i][j] = 1
          else:
            self.pixels[i][j] = 0

    def edge_detect_canny(self):
        """
        Edge detect images using canny filter
        """
        # convert to gryscale
        img_gray = cv2.cvtColor(self.pixels, cv2.COLOR_BGR2GRAY)

      
        # first smoothen the image
        img = cv2.bilateralFilter(img_gray, 5, 50, 50)

        # Auto Thresholding
        # get lower and upper threshold using the median of the images (http://www.kerrywong.com/2009/05/07/canny-edge-detection-auto-thresholding/)
        med = np.median(img)
        low = int(max(0, 0.66 * med))
        high = int(max(255, 1.33 * med))

        # filter the image using filter2D
        canny = cv2.Canny(image=img, threshold1=low, threshold2=high)

        # because the original image isn't used again
        self.pixels = canny[::-1]
        
    def edge_detect_laplacian(self, BLUR_STRENGTH = 0, THRESHOLD = 0.5):
        # convert to gryscale
        img_gray = cv2.cvtColor(self.pixels, cv2.COLOR_BGR2GRAY)
        
        # first smoothen the image
        img = cv2.GaussianBlur(img_gray, (3, 3), BLUR_STRENGTH)

        # filter the image using filter2D
        laplacian = cv2.Laplacian(img,ddepth = cv2.CV_16S, ksize = 5) 
        laplacian = cv2.convertScaleAbs(laplacian)

        self.pixels = laplacian[::-1]

        # threshold the image
        self.threshold(THRESHOLD)

        # smoopthen the image
        self.pixels = cv2.bilateralFilter(self.pixels, 5, 50, 50)

        # invert the color
        self.invertColor()
        
    def changeBMPtoVector(self):
        # # first detech the edges of the image
        # self.edge_detect_canny() 
        
        # # potrace only accept 2D numpy array
        # ny, nx = np.shape(self.pixels)

        # for i in range(ny):
            # for j in range(nx):
                # if self.pixels[i][j] > 1:
                    # self.pixels[i][j] = 1
	

        # laplacian can pick up intricate details in images, but the trace path isn't clean
        # canny seems to miss a lot of details in the images
	
        self.edge_detect_laplacian(BLUR_STRENGTH = 0.2, THRESHOLD = 0.3)
        bmp = potrace.Bitmap(self.pixels)
        path = bmp.trace()
        
        return path
    
    @staticmethod
    def changePathToLatexExpressions(vector_image : potrace.Path):
        # Path is a collection of curves which is a collection of segments
        expr = []
        for curve in vector_image.curves:
            x0, y0 = curve.start_point # starting point
            for segment in curve.segments:
                if segment.is_corner:
                    x1, y1 = segment.c
                    x2, y2 = segment.end_point
                    # corner segment (consist of two linear bezier)
                    expr.append("((1-t)%f+t%f,(1-t)%f+t%f)" %(x0, x1, y0, y1))
                    expr.append("((1-t)%f+t%f,(1-t)%f+t%f)" %(x1, x2, y1, y2))
                    
                    
                else:
                    # bezier segment (single cubic bezier)
                    x1, y1 = segment.c1
                    x2, y2 = segment.c2
                    x3, y3 = segment.end_point
                    
                    # seems to create the correct graph, i dunno why
                    expr.append('((1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)),(1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)))' % \
                (x0, x1, x1, x2, x1, x2, x2, x3, y0, y1, y1, y2, y1, y2, y2, y3))
                    
                x0, y0 = segment.end_point
            
        return expr

class Process():
    def __init__(self, in_path, out_path, filename, filetype) -> None:
       self.n = 0
       self.start_time = 0
       self.IN_PATH = in_path
       self.OUT_PATH = out_path
       self.FILENAME = filename
       self.FILETYPE = filetype
       
    
    def getLatexExpr(self, filename):
        img = Image(filename)
        vctr = img.changeBMPtoVector()
        exprs = img.changePathToLatexExpressions(vctr)
        
        # print(f"{filename} has already been processed")
        with n_finished.get_lock():
            n_finished.value += 1
        
        # processed files 
        n_files = min(N_PER_BATCH, self.n - n_finished.value)
        
        # time elapsed
        elapsed = (time() - self.start_time)
        rate = n_finished.value / elapsed
        
        time_remaining = ((n_files - n_finished.value) / rate)
        time_remaining_h = time_remaining // 3600
        time_remaining_m = (time_remaining % 3600) // 60
        time_remaining_s = (time_remaining % 3600) % 60
        
        sys.stdout.write('\r'+Color.print_colored('loading...', utils=["bold"]) + '  process '+str(n_finished.value)+'/'+str(n_files)+' '+ '{:.2f}'.format(n_finished.value/n_files*100)+'%' + " " + Color.print_colored("Time remaining:", color_fg=[120, 10, 0], utils=["bold"]) + " {:.2f}h, {:.2f}m, {:.2f}s".format(time_remaining_h, time_remaining_m, time_remaining_s))
        return exprs
    
    def writeToFile(self, dir, frameFiles, batch):
        filename, filetype = "out{}", ".txt"
        preprocess.Preprocess.changeDir(self.OUT_PATH)

        for (i, exprs) in enumerate(frameFiles):
            f = open(filename.format(batch * N_PER_BATCH + i + 1) + filetype, 'w')
            line = ""
            for expr in exprs:
                line += expr + "\n" 

            f.write(line)
            f.close()
           
        print(Color.print_colored("\rDone!                    ", color_fg=[100, 10, 0], utils = ["bold"]))
        preprocess.Preprocess.changeDir(dir)
        
    def start(self):
        # Open the image 
        print("Starting...")
        # change the path dir 
        temp = preprocess.getcwd()
        preprocess.Preprocess.changeDir(self.IN_PATH)

        # frame files
        n, batch = len(preprocess.listdir()), 0
        n_batch = n // N_PER_BATCH + 1 if n % N_PER_BATCH > 1 else 0
        self.n = n
        
        while batch < n_batch:
            print(Color.print_colored("\rProcessing", color_fg=[10, 120, 10], utils=["bold"]) + " {}th batch".format(batch + 1))
            frameFiles = ["{}{}.{}".format(self.FILENAME, batch * N_PER_BATCH + i + 1, self.FILETYPE) for i in range(min(N_PER_BATCH, n - n_finished.value))]
            start_time = time()
            self.start_time = start_time

            # store each images exprs in a 2D array
            with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
                frameFiles = pool.map(self.getLatexExpr, frameFiles)


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
            n_finished.value = 0
            
            preprocess.Preprocess.changeDir(self.IN_PATH)
            
    
    