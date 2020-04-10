import os
import shutil
from configparser import ConfigParser
settings_path = os.path.expandvars(R"C:\Users\$USERNAME\Documents\VoiceAssistant\settings.ini")
config = ConfigParser()
config.read(settings_path)

source = config.get("General", "FolderToSort")
       
def cleanUp():
    try:
        for key in config["SortingFolders"]:
            if os.path.exists(os.path.join(source, key)) != True:
                os.mkdir(os.path.join(source, key.capitalize()))
        for file in os.listdir(source):
            file_path = os.path.join(source,file)
            if os.path.isfile(file_path):
                for key in config["SortingFolders"]:
                    extensions = config.get("SortingFolders", key).split(", ")
                    for extension in extensions:
                        if extension in file:
                            shutil.move(file_path, os.path.join(source,key,file))
            
    except PermissionError:
        pass
