import os
import json

class Config:
    """Class to load a configuration from a specified location."""

    def __init__(self, filePath: str) -> None:
        """Config constructor."""
        
        self.path = filePath
        """Path to config file."""

        self.attributes = None
        """Attributes of this config."""

    def doesExist(self):
        """Checks if the given path is valid."""
        return os.path.exists(self.path)

    def loadConfig(self):
        """Loads values from the the specified file and applies them to the attribute property."""

        #tries to read the files
        try:

            file = open(self.path, "r")
            self.attributes = json.loads(file.read())

        #if the file does not exist
        except FileNotFoundError:
            
            #creates the file and sets the default attributes of the config
            #note: these could be dynamic but for my purpose they are unchanging
            file = open(self.path, "w")
            self.attributes = {}
            self.attributes["Music"] = 50
            self.attributes["Sfx"] = 50
        
        #if a file formatting error occurs
        except TypeError:

            #sets the default attributes of the config
            #note: these could be dynamic but for my purpose they are unchanging
            self.attributes = {}
            self.attributes["Music"] = 50
            self.attributes["Sfx"] = 50

    def saveConfig(self):  
        """Writes the current config values to the specified file."""

        #opens the file and overwrites the previous values
        file = open(self.path, "w")
        file.write(json.dumps(self.attributes))
    
    def setAttribute(self, attribute: str, newValue: object) -> None:
        """Setter for any config attribute."""
        self.attributes[attribute] = newValue

    def getAttribute(self, attribute: str):
        """Getter for any config attribute."""
        return self.attributes[attribute]


configuration = Config(os.path.join("config", "hexsweeper.cfg"))
"""HexSweeper config."""