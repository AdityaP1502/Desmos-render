from loadingAnimation import Loading
from preprocess import Preprocess, getcwd
from processing import Process
from sys import argv
import getopt

URL = ""
FPS = 24

IN_PATH = ""
FILENAME = "out"
FILETYPE = "png"
OUT_PATH = "{}/out_latex/default".format(getcwd())



if __name__ == "__main__":
  try:
    opts, args = getopt.getopt(argv[1:], shortopts="f:e:", longopts=["fps=", "url=", "path="])
  except getopt.GetoptError as err:
    print(err)
    print("Error : Invalid Argument")
    print("""Accepted Arguments:
          -f : filename. Default = \"out\"
          -e : extension. Default = \"png\"
          --url=<youtube_url> : Youtube video link that want to be processed
          --fps=<frame_per_second> : FPS of the output video
          --path=<frame_path> : Frame input path. If path specified, out_path will be at "/out_latex/default"
          """)
    exit(1)
  
  print(opts)
  for opt, arg in opts:
    
    if opt == "--url":
      URL = arg
      
    elif opt == "--fps":
      FPS = arg
      
    elif opt=="--path":
      IN_PATH = getcwd() + arg
      
    elif opt == "-f":
      FILENAME = arg
      
      
  if URL != "":
    IN_PATH, OUT_PATH = Preprocess.convertVideoIntoFrames(URL, FPS, FILENAME, FILETYPE)  
    
  else:
    if IN_PATH == "":
      print("Please specified URL or a frame path!")
      exit(1)
      
  proc = Process(IN_PATH, OUT_PATH, FILENAME, FILETYPE)
  Loading.loading(proc.start)
  print("Process is finished")
  print("You can run the backend now")  
      
    