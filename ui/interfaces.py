from abc import ABC, abstractmethod
from core.types import GameStateDict

class IGameRenderer(ABC):
    @abstractmethod
    def render(self, state: GameStateDict, input_text: str, blink: bool) -> None:
        pass