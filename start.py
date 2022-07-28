from loadingAnimation import Loading, Color
from preprocess import Preprocess, getcwd, listdir, system
from processing import Process
from sys import argv
import getopt

FPS = 24
N_PER_BATCH = 1000

URL = ""
IN_PATH = ""
FILENAME = "out"
FILETYPE = "png"
OUT_PATH_LATEX = "{}/out_latex/default".format(getcwd())
OUT_PATH_IMAGES = "{}/out_png/default".format(getcwd())


def showHelp():
  print("""Accepted Arguments:
          -h : show help screen
          -f : filename. Default = \"out\"
          -e : extension. Default = \"png\"
          --url=<youtube_url> : Youtube video link that want to be processed
          --fps=<frame_per_second> : FPS of the output video
          --path="<frame_path> <out_path_images>": Frame input path. Use relative path. If path specified, latex file will be at "/out_latex/default", change this using --latex option.
          --latex=<out_latex_path>. Use this to specify latex output path when using --path option. 
          --batch_size=<size>: How many frames want to be computed per batch before save to a file. 
          """)
  
if __name__ == "__main__":
  try:
    opts, args = getopt.getopt(argv[1:], shortopts="hf:e:", longopts=["fps=", "url=", "path=", "latex=", "batch_size="])
  except getopt.GetoptError as err:
    print(err)
    print("Error : Invalid Argument")
    showHelp()
    exit(1)
    
  print(opts)
  
  for opt, arg in opts:
    if opt == "-h":
      showHelp()
      exit(0)
      
    if opt == "--url":
      URL = arg
      
    elif opt == "--fps":
      FPS = arg
      
    elif opt=="--path":
      temp = arg.split(" ")
      IN_PATH = getcwd() + temp[0]
      OUT_PATH_IMAGES = getcwd() + temp[1]
      print(Color.print_colored("INPUT_PATH:", utils=["bold"]), end=" ")
      print(Color.print_colored("{}".format(IN_PATH), color_fg=[10, 20, 80]))
      print(Color.print_colored("OUTPUT_PATH:", utils=["bold"]), end=" ")
      print(Color.print_colored("{}".format(OUT_PATH_IMAGES), color_fg=[10, 20, 80]))
      
      
    elif opt == "--latex":
      OUT_PATH_LATEX = getcwd() + arg
      print(Color.print_colored("OUTPUT_PATH_LATEX:", utils=["bold"]), end=" ")
      print(Color.print_colored("{}".format(OUT_PATH_LATEX), color_fg=[10, 20, 80]))
      
    elif opt == "-f":
      FILENAME = arg
      
    elif opt == "--batch_size":
      N_PER_BATCH = int(arg)
      
      
  if URL != "":
    IN_PATH, OUT_PATH_LATEX, OUT_PATH_IMAGES = Preprocess.convertVideoIntoFrames(URL, FPS, FILENAME, FILETYPE)  
    
  else:
    if IN_PATH == "":
      print("Please specified URL or a frame path!")
      exit(1)
  
  total_frames = len(listdir(IN_PATH))
  print("Starting processing {} frames".format(total_frames))
    
  proc = Process(IN_PATH, OUT_PATH_LATEX, FILENAME, FILETYPE, N_PER_BATCH)
  Loading.loading(proc.start)
  print("\rProcess is finished                                                                                                      ")
  print("Running backend server. Please wait!")
  
  # start server with params (in path, out path, total framse)
  cmd = "node ./backend/server.js {} {} {}".format(OUT_PATH_LATEX, OUT_PATH_IMAGES, total_frames)
  system(cmd)
      
    