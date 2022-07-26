from os import system
from time import sleep
import sys
import threading

system("") # Enable ANSI 

class Color():
  util = {
    "reset": "\u001b[0m",
    "bold": "\u001b[1m",
    "underline": "\u001b[4m",
    "reverse": "\u001b[7m",
  }
  
  @staticmethod
  def __setFG(r, g, b):
    return f"\u001b[38;2;{r};{g};{b}m"
  
  @staticmethod
  def __setBG(r, g, b):
    return f"\u001b[48;2;{r};{g};{b}m"
  
  @classmethod
  def print_colored(cls, text: str, color_fg = None, color_bg = None, utils = None) -> str:
    """Print text with color that are specified in color_fg, color_bg, and util

    Args:
        text (str): Text that want to be printed with color
        color_fg (list[int], optional): Color of the text in RGB. Defaults to None.
        color_bg (list[int], optional): Color of the background in RGB. Defaults to None.
        util (list[str], optional): Extra params : bold, underline. Defaults to None.

    Returns:
        str: colored text
    """
    
    # add reset
    text = text + cls.util["reset"]
    
    # set fg
    if color_fg != None:
      text = cls.__setFG(*color_fg) + text
      
    # set bg
    if color_bg != None:
      text = cls.__setBG(*color_bg) + text
      
    if utils != None:
      for util in utils:
        if (x := cls.util.get(util)) != None:
          text = x + text
          
    return text 
          
class Loading():
  @staticmethod
  def __animated_loading():
    chars = "/—\|" 
    for char in chars:
        sys.stdout.write('\r'+ Color.print_colored('loading...', utils=["bold"]) + Color.print_colored(char, color_fg=[10, 120, 10]))
        sleep(.1)
        sys.stdout.flush() 
        
  @classmethod
  def loading(cls, process_fnc):
    s = threading.Thread(name='process', target=process_fnc, daemon=True)
    s.start()

    while s.is_alive():
        cls.__animated_loading()
  
  

