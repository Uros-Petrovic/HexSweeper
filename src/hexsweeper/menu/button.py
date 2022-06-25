import pygame
import os

BUTTON_BACKGROUND = pygame.image.load(os.path.join("assets", "textures", "Button.png"))
"""Button background image."""
BUTTON_HIGHLIGHT_BACKGROUND = pygame.image.load(os.path.join("assets", "textures", "ButtonHighlight.png"))
"""Highlighted button background image."""

class Button:
    """Class to create and use buttons."""

    def __init__(self, text: str, width: int, height: int, xPos: int, yPos: int, id: int) -> None:
        """Button constructor."""

        self.text = text
        """The text displayed on this button."""

        self.x = xPos
        """The x position of this button."""
        self.y = yPos
        """The y position of this button."""

        self.width = width
        """The width of this button."""

        self.height = height
        """The height of this button."""

        self.isHighlighted = False
        """Whether the users cursor is hovering over this button."""

        self.font = pygame.font.Font("freesansbold.ttf", int(height / 4))
        """The scaled font for this button."""

        self.id = id
        """The ID of this button (should be unique)."""

    def drawButton(self, window: pygame.Surface) -> None:
        """Draws this button on the specified window."""

        #modifies the image drawn based on whether the button is highlighted
        if self.isHighlighted:
            
            #draws the scaled, highlighted button backgrouund, at the given coordinates
            window.blit(pygame.transform.scale(BUTTON_HIGHLIGHT_BACKGROUND.convert_alpha(), (self.width, self.height)), (self.x, self.y))

        else:

            #draws the scaled, highlighted button backgrouund, at the given coordinates
            window.blit(pygame.transform.scale(BUTTON_BACKGROUND.convert_alpha(), (self.width, self.height)), (self.x, self.y))

        #renders the text on the button
        text = self.font.render(self.text, True, (0, 0, 0)).convert_alpha()
        #draws the button text at the given coordinates
        window.blit(text, (self.x + self.width / 2 - self.font.size(self.text)[0] / 2, self.y + self.height / 2 - self.font.size(self.text)[1] / 2))

    def doesCollide(self, mouseX: float, mouseY: float) -> bool:
        """Checks if the users cursor collides with the x and y coordinates of this button."""

        #checks if the cursors x position is greater than the left-most side and smaller than the left-most side + the width of the slider
        if self.x <= mouseX and mouseX <= (self.x + self.width):
            
            #checks if the cursors y position is greater than the top-most side and smaller than the top-most side + the height of the slider
            if self.y <= mouseY and mouseY <= (self.y + self.height):
                
                return True

        return False
        
    