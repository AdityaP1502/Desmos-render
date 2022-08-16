from os import chdir
from loadingAnimation import Loading, Color
from preprocess import Preprocess, getcwd, listdir, system
from processing import Process
from sys import argv
import getopt

ACCURATE_RENDER = False
EXIT = False
GET = False

FPS = 24
N_PER_BATCH = 1000

URL = ""
METHOD = "canny"
THRESHOLD_METHOD = "simple"
IN_PATH = ""
FILENAME = "out"
FILETYPE = "png"
OUT_PATH_LATEX = "{}/out_latex/default".format(getcwd())
OUT_PATH_IMAGES = "{}/out_png/default".format(getcwd())
VID_PATH = ""


def showInfo():
  print(Color.print_colored("INPUT_PATH:", utils=["bold"]), end=" ")
  print(Color.print_colored("{}".format(IN_PATH), color_fg=[10, 20,150]))
  print(Color.print_colored("OUTPUT_PATH:", utils=["bold"]), end=" ")
  print(Color.print_colored("{}".format(OUT_PATH_IMAGES), color_fg=[10, 20,150]))
  print(Color.print_colored("OUTPUT_PATH_LATEX:", utils=["bold"]), end=" ")
  print(Color.print_colored("{}".format(OUT_PATH_LATEX), color_fg=[10, 20,150]))
  print(Color.print_colored("METHOD:", utils=["bold"]), end=" ")
  print(Color.print_colored("{}".format(METHOD), color_fg=[10, 20,150]))
  
def showHelp():
  print("""Accepted Arguments:
          -g : Only download videos from youtube.
          -h : show help screen
          -f : filename. Default = \"out\"
          -e : extension. Default = \"png\"
          --url=<youtube_url> : Youtube video link that want to be processed. Use this option if you want to render video from youtube. If you use this options, no need to specify path
          --vid_path=<video_path> : Video path using relative path. Specify this option if you want to render using existing video. Use --frame_path, --out_path_images, and --latex to specify output location
          --fps=<frame_per_second> : FPS of the output video.
          --frame_path=<frame_path> : Frame input path(Use relative path).
          --out_path_images=<out_images_path>: Desmos rendered frames location. Default location /out_png/default.
          --latex=<out_latex_path>: Use this to specify latex output path when using --path option. 
          --batch_size=<size>: How many frames want to be computed per batch before save to a file. 
          --edge_method=<edge_detect_method>: Specify the method that want to be used to detect edges. Available option are:    1. canny (use --threshold_method opts to specify the Threshold Method. Default is "simple")
                                                                                                                                2. laplacian (--threshold_method opts to specify the Threshold Method. Default is "simple")
                                                                                                                                3. combine : combine laplacian and canny method(use --acurrate flag to give a much more accurate representation of the images.)
                                                                                                                                
          --threshold_method=<THRESHOLD_METHOD>: Specify the threshold method used. Only applicable to edge method : canny and laplacian. Available options : simple and adaptive
          --accurate : Accurate render. Give a close representation to the original images. Can lead to a noisy result.                                                                                                                                                                                                              
          """)
  
if __name__ == "__main__":
  try:
    opts, args = getopt.getopt(argv[1:], shortopts="hf:e:g", longopts=["fps=", "url=", "vid_path=", "frame_path=", "out_path_images=", "latex=", "batch_size=", "edge_method=", "threshold_method=", "accurate"])
  except getopt.GetoptError as err:
    print(err)
    print("Error : Invalid Argument")
    showHelp()
    exit(1)
    
  print(opts)
  
  for opt, arg in opts:
    if opt == "-g":
      GET = True
      
    if opt == "-h":
      showHelp()
      exit(0)
      
    if opt == "--url":
      URL = arg
      print(Color.print_colored("URL:", utils=["bold"]), end=" ")
      print(Color.print_colored("{}".format(URL), color_fg=[10, 20, 150]))
      
    elif opt == "vid_path":
      VID_PATH = arg
      
    elif opt == "--fps":
      FPS = arg
      
    # elif opt=="--path":
      # temp = arg.split(" ")
      # IN_PATH = getcwd() + temp[0]
      # OUT_PATH_IMAGES = getcwd() + temp[1]
      
      # # make sure out_path_images exist
      # temp = getcwd()
      # Preprocess.changeDir(OUT_PATH_IMAGES)
      # chdir(temp)
      
    elif opt == "--frame_path":
      temp = getcwd()
      IN_PATH = temp + arg
      Preprocess.changeDir(IN_PATH)
      chdir(temp)
      
    elif opt == "--out_path_images":
      temp = getcwd()
      OUT_PATH_IMAGES = temp + arg 
      Preprocess.changeDir(OUT_PATH_IMAGES)
      chdir(temp)
        
    elif opt == "--latex":
      OUT_PATH_LATEX = getcwd() + arg
      
    elif opt == "-f":
      FILENAME = arg
      
    elif opt == "--batch_size":
      N_PER_BATCH = int(arg)
      
    elif opt == "--edge_method":
      METHOD = arg
    
    elif opt == "--threshold_method":
      THRESHOLD_METHOD = arg
      
    elif opt == "--vid_path":
      VID_PATH = getcwd() + arg
    
    elif opt == "--accurate":
      ACCURATE_RENDER = True
      
      
  if URL != "":
    print(GET)
    if GET:
      Preprocess.getVideos(URL)
      EXIT = True
      
    else:
      print("WTF, IM DUMB")
      IN_PATH, OUT_PATH_LATEX, OUT_PATH_IMAGES = Preprocess.convertVideoIntoFramesFromURL(URL, FPS, FILENAME, FILETYPE)  
    
  elif VID_PATH != "" and IN_PATH != "":
    Preprocess.convertVideosIntoFrames(VID_PATH, IN_PATH, FPS)
    
  else:
    if IN_PATH == "":
      print("Please specified URL or a frame path!")
      raise Exception("Cannot process frames if not given an input file")
  
  if not EXIT:   
    showInfo()
    total_frames = len(listdir(IN_PATH))
    print(Color.print_colored("Starting ", utils=["bold"]) + "processing" +Color.print_colored(" {} ".format(total_frames), color_fg=[0, 50, 200]) + "frames")

    proc = Process(IN_PATH, OUT_PATH_LATEX, FILENAME, FILETYPE, N_PER_BATCH, METHOD, THRESHOLD_METHOD, ACCURATE_RENDER)
    try:
      s = Loading.loading(proc.start)
      s.join()
    except Exception as e:
      print(e)
      EXIT = True
      
    if not EXIT:
      # start server with params (in path, out path, total framse)
      print("\rProcess is finished                                                                                                      ")
      print("Running backend server. Please wait!")
      cmd = "node ./backend/server.js {} {} {} {}".format(OUT_PATH_LATEX, OUT_PATH_IMAGES, total_frames, 50)
      system(cmd)
      