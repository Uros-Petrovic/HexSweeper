import os
import json

class Config:

    def __init__(self, filePath: str) -> None:
        
        self.path = filePath
        self.attributes = None

    def doesExist(self):
        return os.path.exists(self.path)

    def loadConfig(self):

        try:

            file = open(self.path, "r")
            self.attributes = json.loads(file.read())

        except FileNotFoundError:

            file = open(self.path, "w")
            self.attributes = {}
            self.attributes["Music"] = 50
            self.attributes["Sfx"] = 50
            
        except TypeError:

            self.attributes = {}
            self.attributes["Music"] = 50
            self.attributes["Sfx"] = 50

    def saveConfig(self):  
        
        file = open(self.path, "w")
        file.write(json.dumps(self.attributes))
    
    def setAttribute(self, attribute: str, newValue: object) -> None:
        self.attributes[attribute] = newValue

    def getAttribute(self, attribute: str):
        return self.attributes[attribute]


configuration = Config(os.path.join("config", "hexsweeper.cfg"))