import pygame
import os
import threading
import src.hexsweeper.config as config

SLIDER_BACKGROUND_IMAGE = pygame.image.load(os.path.join("assets", "hexsweeper", "SliderBackground.png"))
SLIDER_BAR_IMAGE = pygame.image.load(os.path.join("assets", "hexsweeper", "SliderBar.png"))

SLIDER_BACKGROUND_HIGHLIGHT_IMAGE = pygame.image.load(os.path.join("assets", "hexsweeper", "SliderBackgroundHighlight.png"))
SLIDER_BAR_HIGHLIGHT_IMAGE = pygame.image.load(os.path.join("assets", "hexsweeper", "SliderBarHighlight.png"))

class Slider:

    def __init__(self, text: str, xPos: int, yPos: int, width: int, height: int, minValue: int, maxValue: int, defaultValue: int, id: int) -> None:
        
        self.text = text
        self.x = xPos
        self.y = yPos
        self.width = width
        self.height = height
        self.min = minValue
        self.max = maxValue
        self.default = defaultValue
        self.value = defaultValue
        self.isHighlighted = False
        self.isHeld = False
        self.font = pygame.font.Font("freesansbold.ttf", int(height / 4))
        self.id = id

    def drawSlider(self, window: pygame.surface.Surface):
        
        SCALED_BG = pygame.transform.scale(SLIDER_BACKGROUND_HIGHLIGHT_IMAGE, (self.width, self.height)) if self.isHighlighted else pygame.transform.scale(SLIDER_BACKGROUND_IMAGE, (self.width, self.height)).convert_alpha()
        SCALED_BAR = pygame.transform.scale(SLIDER_BAR_HIGHLIGHT_IMAGE, (self.width / 16, self.height)) if self.isHighlighted else pygame.transform.scale(SLIDER_BAR_IMAGE, (self.width / 16, self.height)).convert_alpha()
        text = self.font.render(self.text.format(self.value / 100), False, (0, 0 ,0))

        window.blit(SCALED_BG, (self.x, self.y))
        window.blit(SCALED_BAR, (self.x + self.value / self.max * self.width - SCALED_BAR.get_width() / 2, self.y))
        window.blit(text, (self.x + self.width / 2 - self.font.size(self.text)[0] / 2, self.y + self.height / 2 - self.font.size(self.text)[1] / 2))

    def moveSliderBar(self, mouseX: float):
        
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

    def updateUntilRelease(self):

        def update():
            threadClock = pygame.time.Clock()

            while True:

                threadClock.tick(30)

                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]  

                if pygame.mouse.get_pressed()[0]:
                    
                    if self.isHeld or self.doesCollide(mouseX, mouseY):

                        self.moveSliderBar(mouseX)
                        self.isHeld = True

                        if self.id == 0:
                            config.configuration.attributes["Music"] = self.value
                        elif self.id == 1:
                            config.configuration.attributes["Sfx"] = self.value

                        config.configuration.saveConfig()
                        self.isHighlighted = True

                else:

                    self.isHighlighted = False
                    self.isHeld = False
                    break

        sThread = threading.Thread(target=update, args=())
        sThread.start()