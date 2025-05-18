import pygame
from ui.render import CircleOfFifthsDrawable
from enum import Enum
from config import Config
from localization import Localization
from core.game_core import GameCore
from core.blink_manager import BlinkManager
from ui.game_renderer import GameRenderer

class GameState(Enum):
    """Enumeration for the different game states."""
    ACTIVE = 1
    INACTIVE = 2
    ADVANCE = 3

class CircleOfFifthsGame:
    """
    Main game class for the Circle of Fifths Practice App.
    Handles game state, event processing, rendering, and quiz logic.
    """

    def __init__(self, lang: str = "en") -> None:
        """
        Initializes the game, pygame, and all game state.

        Args:
            lang (str): Language code for localization (default "en").
        """

        self.core = GameCore()
        self.core.next_question()

        pygame.display.set_caption("Circle of Fifths Quiz")
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.circle_render = CircleOfFifthsDrawable(self.core.major_chords, self.core.minor_chords)
        self.circle_render.set_center((400, 360))

        self.input_text: str = ""
        self.state: GameState = GameState.ACTIVE
        self.redraw: bool = True
        self.blink_manager = BlinkManager()

        screen: pygame.Surface = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        overlay: pygame.Surface = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
        font_small: pygame.font.Font = pygame.font.SysFont(None, Config.FONT_SMALL_SIZE)
        font_large: pygame.font.Font = pygame.font.SysFont(None, Config.FONT_LARGE_SIZE)

        loc: Localization = Localization(lang)

        self.renderer = GameRenderer(
            screen, overlay, font_small, font_large,
            self.circle_render, loc
        )

    def handle_events(self) -> None:
        """
        Handles all pygame events, including keyboard and mouse input.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                self.redraw = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif self.state == GameState.ACTIVE:
                    self.handle_input(event)
                elif self.state == GameState.INACTIVE and event.key == pygame.K_RETURN:
                    self.state = GameState.ADVANCE

            if self.state == GameState.ADVANCE and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.reset_for_next_question()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.circle_render.is_inside_circle(mouse_pos):
                        selected_chord_index = self.circle_render.get_chord_index(mouse_pos)
                        if selected_chord_index is not None:
                            indices = self.core.get_selected_chord_indices()
                            if selected_chord_index in indices:
                                indices.remove(selected_chord_index)
                            else:
                                indices.add(selected_chord_index)
                            self.core.set_selected_chord_indices(indices)
                            self.redraw = True

    def handle_input(self, event: pygame.event.Event) -> None:
        """
        Handles keyboard input for answering questions.

        Args:
            event (pygame.event.Event): The pygame event to process.
        """
        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_RETURN:
            self.state = GameState.INACTIVE
            self.core.submit_answer(self.input_text)
        else:
            self.input_text += event.unicode

    def reset_for_next_question(self) -> None:
        """
        Resets the state for the next quiz question.
        """
        self.input_text = ""
        self.core.next_question()
        self.state = GameState.ACTIVE
        self.blink_manager.reset()

    def render(self) -> None:
        """
        Renders the game screen and overlays.
        """
        if not self.redraw:
            return
        
        state = self.core.get_state()
        # Add any extra info needed by the renderer:
        state["game_state"] = self.state.name
        state["chord_list"] = self.core.get_chord_list(state["chord_type"])
        state["stats"] = self.core.get_stats()

        self.redraw = False
        self.renderer.render(state, self.input_text, self.blink_manager.is_blinking())

    def run(self) -> None:
        """
        Main game loop.
        """
        while True:
            self.handle_events()
            if self.blink_manager.update():
                self.redraw = True
            self.render()
            self.clock.tick(Config.FPS)