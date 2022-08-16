from fileinput import filename
import cv2
import numpy as np
import potrace

class Image():
    def __init__(self, filename=None, pixels=np.array([])) -> None:
        if filename == None and np.shape(pixels)[0] == 0:
          raise Exception("Must Provided filepath or pixels")
          
        if filename != None:
          self.pixels = cv2.imread(filename)
          
        if np.shape(pixels)[0] != 0:
          self.pixels = pixels
          
    def __adaptiveThreshold(self):
      thresh = cv2.adaptiveThreshold(self.pixels, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
      self.pixels = thresh

    def __simpleThresholding(self, type):
      rect, thresh = cv2.threshold(self.pixels, 127, 255, type)
      self.pixels = thresh

    def __threshold(self, params=["adaptive"]):
      if params[0] == "adaptive":
        self.__adaptiveThreshold()

      elif params[0] == "simple":
        self.__simpleThresholding(params[1])
  
    def __normalize(self):
      ny, nx = np.shape(self.pixels)
      for i in range(ny):
        for j in range(nx):
            self.pixels[i][j] = 1 if self.pixels[i][j] > 127 else 0

    def edge_detect_canny(self, nudge = .33, THRESHOLD_METHOD="adaptive"):
        """
        Edge detect images using canny filter
        """
        # convert to gryscale
        self.pixels = cv2.cvtColor(self.pixels, cv2.COLOR_BGR2GRAY)
        
        if THRESHOLD_METHOD == "simple":
          self.__threshold(["simple", cv2.THRESH_TOZERO])
          
        elif THRESHOLD_METHOD == "adaptive":
          self.__threshold(["adaptive"])

        # img_gray = cv2.GaussianBlur(img_gray, (3, 3), 0.5)
        
        # Auto Thresholding
        # get lower and upper threshold using the median of the images (http://www.kerrywong.com/2009/05/07/canny-edge-detection-auto-thresholding/)
        med = np.median(self.pixels)
        low = int(max(0, (1 - nudge) * med))
        high = int(max(255, (1 + nudge)* med))
      
        # first smoothen the image
        self.pixels = cv2.bilateralFilter(self.pixels, 5, 50, 50)

        # turn the image upside down
        self.pixels = self.pixels[::-1]

        # filter the image using filter2D
        self.pixels = cv2.Canny(image=self.pixels, threshold1=low, threshold2=high)

    def edge_detect_laplacian(self, BLUR_STRENGTH = 0, THRESHOLD_METHOD="simple"):
        """Edge detect using laplacian filter

        Args:
            BLUR_STRENGTH (int, optional): Specify the strength of gaussian blur. Defaults to 0.
            THRESHOLD_METHOD (str, optional): Threshold method: 1. Simple : Simple Threshold. Used CV2.THRESH_TRUNC
                                                                2. Adaptive : Adaptive Tresholding. Defaults to "simple".
        """
        # convert to gryscale
        self.pixels = cv2.cvtColor(self.pixels, cv2.COLOR_BGR2GRAY)

        # thereshold the images
        if THRESHOLD_METHOD == "simple":
          self.__threshold(["simple", cv2.THRESH_TRUNC])
          
        elif THRESHOLD_METHOD == "adaptive":
          self.__threshold(["adaptive"])

        # Blur the images
        self.pixels = cv2.GaussianBlur(self.pixels, (3, 3), BLUR_STRENGTH)

        # smoopthen the image
        self.pixels = cv2.bilateralFilter(self.pixels, 3, 50, 50)

        # filter the image using filter2D
        self.pixels = cv2.Laplacian(self.pixels,ddepth = cv2.CV_16S, ksize = 3) 
        self.pixels = cv2.convertScaleAbs(self.pixels)


        # turn the image upside down
        self.pixels = self.pixels[::-1]

        ny, nx = np.shape(self.pixels)
        for i in range(ny):
          for j in range(nx):
              self.pixels[i][j] = 255 if self.pixels[i][j] > 10 else 127
        
    @classmethod             
    def edge_detect_combine_method(cls, filename, ACCURATE_RENDER, factor=0.5):
        img1 = cls(filename=filename)
        img2 = cls(filename=filename)
        img_combine = []
        
        TH_1 = "simple"
        TH_2 = "simple"
        
        if ACCURATE_RENDER:
          # able to detect lot more edges in a pictures
          # end result can be noisy
          TH_2 = "adaptive"
          
        img1.edge_detect_canny(THRESHOLD_METHOD=TH_1)
        img2.edge_detect_laplacian(BLUR_STRENGTH=0.2, THRESHOLD_METHOD=TH_2)
        
        ny, nx = np.shape(img1.pixels) # must have the same dimensions
        for i in range(ny):
          colm_arr = []
          for j in range(nx):
            pix = img1.pixels[i][j] * factor + img2.pixels[i][j] * (1 - factor)
            colm_arr.append(pix)
            
          img_combine.append(colm_arr)
            
        return cls(pixels = np.array(img_combine))
        
    def changeBMPtoVector(self):
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
      
      
    @classmethod
    def getLatexExpression(cls, filename, method, THRESHOLD_METHOD, ACCURATE_RENDER):
      if method == "canny":
        img = Image(filename)
        img.edge_detect_canny(THRESHOLD_METHOD=THRESHOLD_METHOD)
        
        
      elif method == "laplacian":
        img = Image(filename)
        img.edge_detect_laplacian(BLUR_STRENGTH=0.2, THRESHOLD_METHOD=THRESHOLD_METHOD)
        
      elif method == "combine":
        img = Image.edge_detect_combine_method(filename, factor=0.3, ACCURATE_RENDER=ACCURATE_RENDER)
    
      else:
        raise Exception("invalid edge detect method. Method isn't supported")
      
      img.__normalize()
      vctr = img.changeBMPtoVector()
      exprs = img.changePathToLatexExpressions(vctr)
      
      return exprs