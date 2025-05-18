import pygame
from core.circle import ChordType
from core.game_text import generate_question_text, get_feedback_message
from config import Config
from core.types import GameStateDict
from ui.interfaces import IGameRenderer

class GameRenderer(IGameRenderer):
    """
    Handles all rendering for the Circle of Fifths game.
    """

    def __init__(self, screen: pygame.Surface, overlay: pygame.Surface, font_small: pygame.font.Font,
                 font_large: pygame.font.Font, circle_render, loc):
        self.screen = screen
        self.overlay = overlay
        self.font_small = font_small
        self.font_large = font_large
        self.circle_render = circle_render
        self.loc = loc

    def render(self, state: GameStateDict, input_text: str, blink: bool) -> None:
        """
        Renders the entire game screen.
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
        chord_list = state["chord_list"]
        question_surface = self.font_small.render(
            generate_question_text(state, self.loc, chord_list), True, Config.COLORS["text"]
        )
        question_text_rect = question_surface.get_rect(center=(400, 20))
        self.screen.blit(question_surface, question_text_rect)

    def render_input(self, input_text: str) -> None:
        input_surface = self.font_large.render(input_text, True, Config.COLORS["text"])
        input_text_rect = input_surface.get_rect(center=(400, 80))
        self.screen.blit(input_surface, input_text_rect)

    def render_results(self, state) -> None:
        if state.get("last_result") is not None:
            text = get_feedback_message(state, self.loc)
            result_surface = self.font_small.render(text, True, Config.COLORS["text"])
            result_text_rect = result_surface.get_rect(center=(400, 110))
            self.screen.blit(result_surface, result_text_rect)

    def render_stats(self, state) -> None:
        correct, total = state.get("stats", (0, 0))
        answers_surface = self.font_small.render(
            f"{correct} / {total}", True, Config.COLORS["text"]
        )
        self.screen.blit(answers_surface, (700, 20))