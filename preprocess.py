from os import system, getcwd, walk, chdir, mkdir, listdir

class Preprocess():
    """
        Class to download and process the video into images
    """
    def __init__(self, filename : str, filetype : str, filepath : str) -> None:
        self.filename = filename
        self.filetype = filetype
        self.filepath = filepath
        
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
        filepath = temp + "\\Downloaded_Videos"
        
        cls.changeDir(filepath)
        
        n = len(listdir())
                 
        filepath += "\\video{}".format(n + 1)
        filename = "video{}".format(n + 1)
        ext = "mp4"
         
        cmd = "yt-dlp -f \"[height<=480][ext={}]\" -o {}\\{}.%(ext)s {}".format(ext, filepath, filename, url)
        system(cmd)
        
        chdir(temp)
        return filepath, filename, ext
    
    @classmethod    
    def convertVideoIntoFrames(cls, url : str):
        """
        Convert Video File to Frames Using FFMPEG
        """
        
        vids_path, vids_name, vids_ext = cls.getVideos(url)
        
        temp = getcwd()
        filepath = vids_path
        
        cls.changeDir(filepath)
        
        cmd = "ffmpeg -i {}.{} -vf fps=24 out%d.png".format(vids_name, vids_ext)
        
        system(cmd)
        chdir(temp)
        
        return Preprocess(filename="out", filetype="png", filepath=filepath)
    

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=4QXCPuwBz2E"
    img = Preprocess.convertVideoIntoFrames(url)
    