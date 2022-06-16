import pygame
import os

import src.hexsweeper.menu.button as button

BUTTON_BACKGROUND = pygame.image.load(os.path.join("assets", "hexsweeper", "ButtonTemp.png"))
BUTTON_HIGHLIGHT_BACKGROUND = pygame.image.load(os.path.join("assets", "hexsweeper", "ButtonTempHighlight.png"))
font: pygame.font.Font = None

class Button:

    def __init__(self, text: str, width: int, height: int, x: int, y: int, id: int) -> None:
        self.text = text
        self.x = x
        self.y = y
        self.id = id
        self.width = width
        self.height = height
        self.isHighlighted = False
        self.font = pygame.font.Font("freesansbold.ttf", int(height / 4))
        button.font = pygame.font.Font("freesansbold.ttf", 16)
        
    def drawButton(self, window: pygame.Surface) -> None:
        
        if self.isHighlighted:
            
            window.blit(pygame.transform.scale(BUTTON_HIGHLIGHT_BACKGROUND.convert_alpha(), (self.width, self.height)), (self.x, self.y))

        else:

            window.blit(pygame.transform.scale(BUTTON_BACKGROUND.convert_alpha(), (self.width, self.height)), (self.x, self.y))

        text = self.font.render(self.text, True, (0, 0, 0)).convert_alpha()
        window.blit(text, (self.x + self.width / 2 - self.font.size(self.text)[0] / 2, self.y + self.height / 2 - self.font.size(self.text)[1] / 2))

    def doesCollide(self, mouseX: float, mouseY: float) -> bool:

        if self.x <= mouseX and mouseX <= (self.x + self.width):

            if self.y <= mouseY and mouseY <= (self.y + self.height):
                
                return True

        return False
        
    