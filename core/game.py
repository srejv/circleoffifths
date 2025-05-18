import pygame
import random
from typing import Set, Tuple, Optional
from core.circle import CircleOfFifths, QuestionType, ChordType
from core.chord import Chord
from ui.render import CircleOfFifthsDrawable
from enum import Enum
from config import Config
from localization import Localization

from core.game_core import GameCore

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

        self.circle: CircleOfFifths = CircleOfFifths()
        self.circle_render: CircleOfFifthsDrawable = CircleOfFifthsDrawable(self.circle.majorChords, self.circle.minorChords)
        self.circle_render.set_center((400, 360))

        self.selected_chord_indices: Set[int] = set(range(len(self.circle.get_chord_list(ChordType.MAJOR))))
        self.correct_answers: int = 0
        self.total_questions: int = 0
        self.input_text: str = ""
        self.result_text: str = ""
        self.state: GameState = GameState.ACTIVE
        self.blink: bool = False
        self.blink_counter: int = 0
        self.redraw: bool = True

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
                            if selected_chord_index in self.selected_chord_indices:
                                self.selected_chord_indices.remove(selected_chord_index)
                            else:
                                self.selected_chord_indices.add(selected_chord_index)
                            self.core.set_selected_indices(list(self.selected_chord_indices))
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
        self.result_text = ""
        self.core.next_question()
        self.state = GameState.ACTIVE
        self.blink = False
        self.blink_counter = 0

    def update_blink(self) -> None:
        """
        Updates the blink state for UI effects.
        """
        self.blink_counter += 1
        if self.blink_counter > 30:
            self.blink = not self.blink
            self.blink_counter = 0
            self.redraw = True

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

        self.circle_render.draw_circle(self.screen, self.selected_chord_indices)
        if state["current_chord"] is not None:
            self.circle_render.draw_highlighted_chord(self.overlay, state["current_chord"], state["chord_type"], self.blink)
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
        question_surface = self.font_small.render(self.generate_question_text(state), True, Config.COLORS["text"])
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
            text = ""
            if state["last_result"]["correct"] == False and state.get("last_result").get("reason") is not None:
                text = self.loc.t(state["last_result"]["reason"])
            elif state.get("last_result").get("reason") is None:
                text = self.get_feedback_message(
                    state,
                    state["last_result"]["correct"],
                    state["last_result"]["answer"],
                    state["current_chord"],
                    state["current_question"]
                )
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

    def generate_question_text(self, state) -> str:
        """
        Generates the localized question text for the current quiz question.

        Returns:
            str: The localized question string.
        """
        chord_list = self.circle.get_chord_list(state["chord_type"])
        selected_index = chord_list.index(state["current_chord"])
        chord_type_str = self.loc.t("major") if state["chord_type"] == ChordType.MAJOR else self.loc.t("minor")
        hour = (selected_index + 11) % 12 + 1
        chord_str = str(state["current_chord"])

        question_keys = {
            QuestionType.FILL_IN: "question_fill_in",
            QuestionType.CLOCKWISE: "question_clockwise",
            QuestionType.COUNTERCLOCKWISE: "question_counterclockwise",
            QuestionType.ALTERNATIVE_CIRCLE: "question_alternative_circle",
            QuestionType.ANY: "question_any",
        }
        key = question_keys.get(state["current_question"], "question_fill_in")
        return self.loc.t(
            key,
            chord_type=chord_type_str,
            hour=hour,
            chord=chord_str
        )

    def get_feedback_message(
        self,
        state,
        is_correct: bool,
        chord_answer: Chord,
        selected_chord: Chord,
        question_type: QuestionType
    ) -> str:
        """
        Generates the localized feedback message for the user's answer.

        Args:
            is_correct (bool): Whether the answer was correct.
            chord_answer (Chord): The user's answer.
            selected_chord (Chord): The correct chord.
            question_type (QuestionType): The type of question.

        Returns:
            str: The localized feedback message.
        """
        chord_str = str(state["current_chord"])
        answer_str = str(chord_answer)
        correct_str = selected_chord.name

        feedback_keys = {
            (True, QuestionType.FILL_IN): "feedback_correct_fill_in",
            (True, QuestionType.ALTERNATIVE_CIRCLE): "feedback_correct_alternative_circle",
            (True, QuestionType.ANY): "feedback_correct_any",
            (True, QuestionType.CLOCKWISE): "feedback_correct_clockwise",
            (True, QuestionType.COUNTERCLOCKWISE): "feedback_correct_counterclockwise",
            (False, QuestionType.FILL_IN): "feedback_incorrect_fill_in",
            (False, QuestionType.ALTERNATIVE_CIRCLE): "feedback_incorrect_alternative_circle",
            (False, QuestionType.ANY): "feedback_incorrect_any",
            (False, QuestionType.CLOCKWISE): "feedback_incorrect_clockwise",
            (False, QuestionType.COUNTERCLOCKWISE): "feedback_incorrect_counterclockwise",
        }
        key = feedback_keys.get((is_correct, state["current_question"]), "feedback_correct_fill_in" if is_correct else "feedback_incorrect_fill_in")
        return self.loc.t(
            key,
            answer=answer_str,
            selected=chord_str,
            correct=correct_str
        )

    def run(self) -> None:
        """
        Main game loop.
        """
        while True:
            self.handle_events()
            self.update_blink()
            self.render()
            self.clock.tick(Config.FPS)