import pygame
from core.game_text import generate_question_text, get_feedback_message
from config import Config
from core.types import GameStateDict
from core.chord_lists import major_chords, minor_chords
from ui.render import CircleOfFifthsDrawable
from ui.interfaces import IGameRenderer
from localization import Localization

class GameRenderer(IGameRenderer):
    """
    Handles all rendering for the Circle of Fifths game.
    """

    def __init__(self, lang: str = "en") -> None:
        
        self.screen: pygame.Surface = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.overlay: pygame.Surface = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.font_small: pygame.font.Font = pygame.font.SysFont(None, Config.FONT_SMALL_SIZE)
        self.font_large: pygame.font.Font = pygame.font.SysFont(None, Config.FONT_LARGE_SIZE)
        self.loc: Localization = Localization(lang)

        self.circle_render = CircleOfFifthsDrawable(
            major_chords, minor_chords,
            center=Config.CIRCLE_CENTER,
            radius=Config.CIRCLE_RADIUS,
            inner_radius=Config.CIRCLE_INNER_RADIUS,
            text_radius=Config.CIRCLE_TEXT_RADIUS,
            inner_outer_radius=Config.CIRCLE_INNER_OUTER_RADIUS,
        )

    def render(self, state: GameStateDict, input_text: str, blink: bool) -> None:
        """
        Renders the entire game screen, including the circle, overlays, question, input, results, and stats.

        Args:
            state (GameStateDict): The current game state dictionary.
            input_text (str): The current user input text.
            blink (bool): Whether the blink effect is active.
        """
        self.screen.fill(Config.COLORS["background"])
        self.overlay.fill((0, 0, 0, 0))

        self.circle_render.draw_circle(self.screen, state["selected_chord_indices"])
        if state.get("current_chord") is not None:
            self.circle_render.draw_highlighted_chord(
                self.overlay, state["current_chord"], state["chord_type"], blink
            )
        if state.get("game_state") != "ACTIVE":
            self.circle_render.draw_circle_labels(self.overlay)

        self.screen.blit(self.overlay, (0, 0))
        self.render_question(state)
        self.render_input(input_text)
        self.render_results(state)
        self.render_stats(state)
        pygame.display.flip()

    def render_question(self, state) -> None:
        """
        Renders the current quiz question at the top of the screen.

        Args:
            state (GameStateDict): The current game state dictionary.
        """
        chord_list = state["chord_list"]
        question_surface = self.font_small.render(
            generate_question_text(state, self.loc, chord_list), True, Config.COLORS["text"]
        )
        question_text_rect = question_surface.get_rect(center=(400, 20))
        self.screen.blit(question_surface, question_text_rect)

    def render_input(self, input_text: str) -> None:
        """
        Renders the user's current input.

        Args:
            input_text (str): The current user input text.
        """
        input_surface = self.font_large.render(input_text, True, Config.COLORS["text"])
        input_text_rect = input_surface.get_rect(center=(400, 80))
        self.screen.blit(input_surface, input_text_rect)

    def render_results(self, state) -> None:
        """
        Renders the result/feedback message after an answer is submitted.

        Args:
            state (GameStateDict): The current game state dictionary.
        """
        if state.get("last_result") is not None:
            text = get_feedback_message(state, self.loc)
            result_surface = self.font_small.render(text, True, Config.COLORS["text"])
            result_text_rect = result_surface.get_rect(center=(400, 110))
            self.screen.blit(result_surface, result_text_rect)

    def render_stats(self, state) -> None:
        """
        Renders the user's score and statistics.

        Args:
            state (GameStateDict): The current game state dictionary.
        """
        correct, total = state.get("stats", (0, 0))
        answers_surface = self.font_small.render(
            f"{correct} / {total}", True, Config.COLORS["text"]
        )
        self.screen.blit(answers_surface, (700, 20))