import pygame
import os
import threading
import src.hexsweeper.config as config

SLIDER_BACKGROUND_IMAGE = pygame.image.load(os.path.join("assets", "textures", "SliderBackground.png"))
"""Slider background image."""
SLIDER_BAR_IMAGE = pygame.image.load(os.path.join("assets", "textures", "SliderBar.png"))
"""Slider bar image."""

SLIDER_BACKGROUND_HIGHLIGHT_IMAGE = pygame.image.load(os.path.join("assets", "textures", "SliderBackgroundHighlight.png"))
"""Highlighted slider background image."""
SLIDER_BAR_HIGHLIGHT_IMAGE = pygame.image.load(os.path.join("assets", "textures", "SliderBarHighlight.png"))
"""Highlighted slider bar image."""

class Slider:
    """Class to create and use sliders."""

    def __init__(self, text: str, xPos: int, yPos: int, width: int, height: int, minValue: int, maxValue: int, defaultValue: int, id: int) -> None:
        """Slider constructor."""

        self.text = text
        """The text displayed on this slider."""

        self.x = xPos
        """The x position of this slider."""
        self.y = yPos
        """The y position of this slider."""

        self.width = width
        """The width of this slider."""
        self.height = height
        """The height of this slider."""

        self.min = minValue
        """The minimum value of this slider."""
        self.max = maxValue
        """The maximum value of this slider."""
        self.default = defaultValue
        """The default value of this slider."""
        self.value = defaultValue
        """The current value of this slider."""

        self.isHighlighted = False
        """Whether the users cursor is hovering over this slider."""

        self.isHeld = False
        "Whether the user is holding down their LMB on this slider."

        self.font = pygame.font.Font("freesansbold.ttf", int(height / 4))
        """The scaled font for this slider."""

        self.id = id
        """The ID of this slider (should be unique)."""

    def drawSlider(self, window: pygame.surface.Surface):
        """Draws this slider on the specified window."""

        #checks if the slider is highlighted
        #scales the proper images and renders the text
        SCALED_BG = pygame.transform.scale(SLIDER_BACKGROUND_HIGHLIGHT_IMAGE, (self.width, self.height)) if self.isHighlighted else pygame.transform.scale(SLIDER_BACKGROUND_IMAGE, (self.width, self.height)).convert_alpha()
        SCALED_BAR = pygame.transform.scale(SLIDER_BAR_HIGHLIGHT_IMAGE, (self.width / 16, self.height)) if self.isHighlighted else pygame.transform.scale(SLIDER_BAR_IMAGE, (self.width / 16, self.height)).convert_alpha()
        text = self.font.render(self.text.format(self.value / 100), False, (0, 0 ,0))

        #blits the scaled images in the desired locations
        window.blit(SCALED_BG, (self.x, self.y))
        window.blit(SCALED_BAR, (self.x + self.value / self.max * self.width - SCALED_BAR.get_width() / 2, self.y))
        window.blit(text, (self.x + self.width / 2 - self.font.size(self.text)[0] / 2, self.y + self.height / 2 - self.font.size(self.text)[1] / 2))

    def moveSliderBar(self, mouseX: float):
        """Sets the value of this slider depending on the x position of the cursor relative to this slider."""

        #gets the amount of pixels from the left-most side to the cursor 
        pixels: float = min(max(mouseX - self.x, 0), self.width)
        #sets the value of the slider based on the pixels
        self.value = self.min + self.max * (pixels / self.width)
        
    def doesCollide(self, mouseX: float, mouseY: float) -> bool:
        """Checks if the users cursor collides with the x and y coordinates of this slider."""

        #checks if the cursors x position is greater than the left-most side and smaller than the left-most side + the width of the slider
        if self.x <= mouseX and mouseX <= (self.x + self.width):
            
            #checks if the cursors y position is greater than the top-most side and smaller than the top-most side + the height of the slider
            if self.y <= mouseY and mouseY <= (self.y + self.height):
                
                return True

        return False

    def doesCollideX(self, mouseX: float):
        """Checks if the users cursor collides with the x coordinates of this slider."""

        #checks if the cursors x position is greater than the left-most side and smaller than the left-most side + the width of the slider
        if self.x <= mouseX and mouseX <= (self.x + self.width):

            return True

        return False

    def updateUntilRelease(self):
        """Updates a slider while the user is holding down the LMB on this slider."""

        def update():
            """Updates a slider while the user is holding down the LMB on this slider."""

            threadClock = pygame.time.Clock()
            """Tick rate of the thread, to preserve resources."""

            while True:
                
                #tick at 30 FPS
                threadClock.tick(30)

                #get the cursor positions each cycle
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]  

                #checks if the LMB is being pressed
                if pygame.mouse.get_pressed()[0]:
                    
                    #checks if the slider is already held or if the slider
                    if self.isHeld or self.doesCollide(mouseX, mouseY):
                        
                        #updates the slider values
                        self.moveSliderBar(mouseX)
                        self.isHeld = True
                        self.isHighlighted = True

                        #hard-coded slider implementation to edit specified config values
                        if self.id == 0:
                            config.configuration.attributes["Music"] = self.value
                        elif self.id == 1:
                            config.configuration.attributes["Sfx"] = self.value

                        #saves the config
                        config.configuration.saveConfig()

                #if the LMB is no longer being pressed
                else:
                    
                    #update slider values and break from this loop
                    self.isHighlighted = False
                    self.isHeld = False
                    break
        
        #creates and starts a new thread that will update the sliders value
        sThread = threading.Thread(target=update, args=())
        sThread.start()