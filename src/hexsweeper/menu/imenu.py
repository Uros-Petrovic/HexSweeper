import abc

import pygame


class IMenu(metaclass=abc.ABCMeta):
    """Menu Interface."""

    @abc.abstractmethod
    def __init__(self) -> None:
        """Initializes the menu."""
        raise NotImplementedError

    @abc.abstractmethod
    def handleInput(self) -> None:
        """Performs the actions required on click."""
        raise NotImplementedError

    @abc.abstractmethod
    def drawBackground(self, window: pygame.Surface) -> None:
        """Draws the background of the menu."""
        raise NotImplementedError

    @abc.abstractmethod
    def closeMenu(self) -> None:
        """Closes menu."""
        raise NotImplementedError

    @abc.abstractmethod
    def updateScreen(self, window: pygame.Surface) -> None:
        """Updates the screen and draws any necessary assets."""
        raise NotImplementedError