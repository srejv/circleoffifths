import pygame
from typing import Set
from core.circle import ChordType
from ui.render import CircleOfFifthsDrawable
from enum import Enum
from config import Config
from localization import Localization
from core.game_text import generate_question_text, get_feedback_message
from core.game_core import GameCore
from core.blink_manager import BlinkManager

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
        self.screen: pygame.Surface = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.overlay: pygame.Surface = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.font_small: pygame.font.Font = pygame.font.SysFont(None, Config.FONT_SMALL_SIZE)
        self.font_large: pygame.font.Font = pygame.font.SysFont(None, Config.FONT_LARGE_SIZE)

        self.loc: Localization = Localization(lang)

        self.circle_render = CircleOfFifthsDrawable(self.core.major_chords, self.core.minor_chords)
        self.circle_render.set_center((400, 360))

        self.correct_answers: int = 0
        self.total_questions: int = 0
        self.input_text: str = ""
        self.state: GameState = GameState.ACTIVE
        self.redraw: bool = True
        self.blink_manager = BlinkManager()

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
            is_correct = self.core.submit_answer(self.input_text)
            self.total_questions += 1
            if is_correct:
                self.correct_answers += 1
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

        self.redraw = False
        self.screen.fill(Config.COLORS["background"])
        self.overlay.fill((0, 0, 0, 0))

        self.circle_render.draw_circle(self.screen, self.core.get_selected_chord_indices())
        if state.get("current_chord") is not None:
            self.circle_render.draw_highlighted_chord(self.overlay, state["current_chord"], state["chord_type"], self.blink_manager.is_blinking())
        if self.state != GameState.ACTIVE:
            self.circle_render.draw_circle_labels(self.overlay)

        self.screen.blit(self.overlay, (0, 0))
        self.render_question(state)
        self.render_input()
        self.render_results(state)
        self.render_stats()

        pygame.display.flip()

    def render_question(self, state) -> None:
        """
        Renders the current quiz question at the top of the screen.
        """
        chord_list = self.core.get_chord_list(state["chord_type"])
        question_surface = self.font_small.render(generate_question_text(state, self.loc, chord_list), True, Config.COLORS["text"])
        question_text_rect = question_surface.get_rect(center=(400, 20))
        self.screen.blit(question_surface, question_text_rect)

    def render_input(self) -> None:
        """
        Renders the user's current input.
        """
        input_surface = self.font_large.render(self.input_text, True, Config.COLORS["text"])
        input_text_rect = input_surface.get_rect(center=(400, 80))
        self.screen.blit(input_surface, input_text_rect)

    def render_results(self, state) -> None:
        """
        Renders the result/feedback message after an answer is submitted.
        """
        if state.get("last_result") is not None:
            text = get_feedback_message(state, self.loc)
            result_surface = self.font_small.render(text, True, Config.COLORS["text"])
            result_text_rect = result_surface.get_rect(center=(400, 110))
            self.screen.blit(result_surface, result_text_rect)

    def render_stats(self) -> None:
        """
        Renders the user's score and statistics.
        """
        answers_surface = self.font_small.render(
            f"{self.correct_answers} / {self.total_questions}", True, Config.COLORS["text"]
        )
        self.screen.blit(answers_surface, (700, 20))

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