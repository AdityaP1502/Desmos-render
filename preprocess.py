from os import system, getcwd, walk, chdir, mkdir, listdir

class Preprocess():
    """
        Class to download and process the video into images
    """    
    @staticmethod
    def changeDir(filepath):
        try:
            chdir(filepath)
            
        except:
            print("Creating Downloaded_Videos Folder")
            mkdir(filepath)
            print("Folder Succesfully created")
            
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
        in_path = vids_path
        out_path = temp + "/out_latex/{}".format(vids_name)
        
        cls.changeDir(in_path)
        
        cmd = "ffmpeg -i {}.{} -vf fps={} {}%d.{}".format(vids_name, vids_ext, fps, filename, filetype)
        
        system(cmd)
        chdir(temp)
        
        return in_path, out_path
    

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=4QXCPuwBz2E"
    img = Preprocess.convertVideoIntoFrames(url)
    