# Desmos-render

This is library to using desmos to render any frames.

## 1. HOW

Every frames will be **edge detected** using python. Then, the edge detected images will be traced using potrace resulting in a bezier curves. The bezier curves will be saved inside a .txt file and then will be fed to the **desmos API** to be rendered using **Node.js** server.

### 1.1 Edge Detection

The edge detection algorithm that is supported is canny edge detection, laplacian edge detection, and combine method(using canny and laplacian).

#### 1.1.2 Canny

The canny filter takes two arguments, low threshold and high threshold. Each of them will used an adaptive thresholding where $lowThresholding= (1- nudge) * medianPixels$ and $highThreshold=(1 + nudge) * medianPixels$.

![original images](img/original.jpg)
![canny edge detection using simple Threshold method](img/canny-original.jpg)
