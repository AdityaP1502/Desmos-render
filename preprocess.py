from os import system, getcwd, chdir, mkdir, listdir
from loadingAnimation import Color

class Preprocess():
    """
        Class to download and process the video into images
    """
    @staticmethod
    def makeDir(filepath):
        folder = filepath.split("/")[-1]
        print(Color.print_colored("Creating", utils=["bold"]) + Color.print_colored(" {}".format(folder), color_fg=[200, 120, 10]))
        mkdir(filepath)
        print("Folder" + Color.print_colored(" Succesfully", color_fg=[0, 120, 0]) + " created")

    @classmethod
    def changeDir(cls, filepath):
        try:
            chdir(filepath)
            
        except:
            cls.makeDir(filepath)
            chdir(filepath)       

    @classmethod
    def getVideos(cls, url) -> str:
        # download file from youtube use yt-dlp https://github.com/yt-dlp/yt-dlp
        
        # find any video file with the name video
        temp = getcwd()
        filepath = temp + "/Downloaded_Videos"
        
        cls.changeDir(filepath)
        
        n = len(listdir())
                 
        filepath += "/video{}".format(n + 1)
        filename = "video{}".format(n + 1)
        ext = "mp4"
         
        cmd = "yt-dlp -f \"[height<=480][ext={}]\" -o \"{}/{}.%(ext)s\" {}".format(ext, filepath, filename, url)
        system(cmd)
        chdir(temp)
        
        return filepath, filename, ext
    
    @classmethod    
    def convertVideoIntoFrames(cls, url : str, fps=24, filename="out", filetype="png"):
        """
        Convert Video File to Frames Using FFMPEG
        """
        
        vids_path, vids_name, vids_ext = cls.getVideos(url)
        
        temp = getcwd()
        
        in_path = temp + "/frames/{}".format(vids_name)
        out_path = temp + "/out_latex/{}".format(vids_name)
        out_path_img = temp + "/out_png/{}".format(vids_name)
        
        # create out_path_img if not exist
        cls.changeDir(out_path_img)
        cls.changeDir(vids_path)
        
        cmd = "ffmpeg -i {}.{} -vf fps={} {}/{}%d.{}".format(vids_name, vids_ext, fps, in_path, filename, filetype)
        system(cmd)
        
        chdir(temp)
        return in_path, out_path, out_path_img
    

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=4QXCPuwBz2E"
    img = Preprocess.convertVideoIntoFrames(url)
    