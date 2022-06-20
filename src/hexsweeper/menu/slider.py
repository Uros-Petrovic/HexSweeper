from operator import truediv
import pygame
import os

SLIDER_BACKGROUND_IMAGE = pygame.image.load(os.path.join("assets", "hexsweeper", "SliderBackground.png"))
SLIDER_BAR_IMAGE = pygame.image.load(os.path.join("assets", "hexsweeper", "SliderBar.png"))


class Slider:

    def __init__(self, text: str, xPos: int, yPos: int, width: int, height: int, minValue: int, maxValue: int, defaultValue: int, increments: int, id: int) -> None:
        
        self.text = text
        self.x = xPos
        self.y = yPos
        self.width = width
        self.height = height
        self.min = minValue
        self.max = maxValue
        self.default = defaultValue
        self.value = defaultValue
        #self.increments = increments
        self.isHighlighted = False
        self.isHeld = False
        self.font = pygame.font.Font("freesansbold.ttf", int(height / 4))
        self.id = id

    
    def drawSlider(self, window: pygame.surface.Surface):
        
        #TODO fix l8r
        SCALED_BG = pygame.transform.scale(SLIDER_BACKGROUND_IMAGE, (self.width, self.height)).convert_alpha()
        SCALED_BAR = pygame.transform.scale(SLIDER_BAR_IMAGE, (16, self.height)).convert_alpha()
        text = self.font.render(self.text.format(self.value / 100), False, (0, 0 ,0))

        window.blit(SCALED_BG, (self.x, self.y))
        window.blit(SCALED_BAR, (self.x + self.value / self.max * self.width - SCALED_BAR.get_width() / 2, self.y))
        window.blit(text, (self.x + self.width / 2 - self.font.size(self.text)[0] / 2, self.y + self.height / 2 - self.font.size(self.text)[1] / 2))

    def moveSliderBar(self, mouseX: float, mouseY: float):
    
        pixels: float = min(max(mouseX - self.x, 0), self.width)
        self.value = self.min + self.max * (pixels / self.width)
        
    def doesCollide(self, mouseX: float, mouseY: float) -> bool:

        if self.x <= mouseX and mouseX <= (self.x + self.width):

            if self.y <= mouseY and mouseY <= (self.y + self.height):
                
                return True

        return False

    def doesCollideX(self, mouseX: float):

        if self.x <= mouseX and mouseX <= (self.x + self.width):

            return True

        return False