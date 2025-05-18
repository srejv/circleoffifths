from abc import ABC, abstractmethod
from core.types import GameStateDict

class IGameRenderer(ABC):
    """
    Interface for game renderer classes.

    Implementations should provide a render method that draws the game state to the screen.
    """

    @abstractmethod
    def render(self, state: GameStateDict, input_text: str, blink: bool) -> None:
        """
        Render the game state to the screen.

        Args:
            state (GameStateDict): The current game state dictionary.
            input_text (str): The current user input text.
            blink (bool): Whether the blink effect is active.
        """
        pass