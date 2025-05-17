import pygame
import random
from circle import CircleOfFifths, QuestionType, ChordType
from render import CircleOfFifthsDrawable
from enum import Enum
from config import Config

class GameState(Enum):
    ACTIVE = 1
    INACTIVE = 2
    ADVANCE = 3

class CircleOfFifthsGame:

    def __init__(self):
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption("Circle of Fifths Quiz")
        self.clock = pygame.time.Clock()

        self.font_small = pygame.font.SysFont(None, Config.FONT_SMALL_SIZE)
        self.font_large = pygame.font.SysFont(None, Config.FONT_LARGE_SIZE)

        self.circle = CircleOfFifths()
        self.circle_render = CircleOfFifthsDrawable(self.circle.majorChords, self.circle.minorChords)
        self.circle_render.set_center((400, 360))

        self.number_of_chords_to_ask_about = 1
        self.correct_answers = 0
        self.total_questions = 0
        self.input_text = ""
        self.result_text = ""
        self.state = GameState.ACTIVE
        self.blink = False
        self.blink_counter = 0
        self.redraw = True

        self.question, self.selected_chord, self.chord_type = self.new_question()

    def new_question(self):
        question = QuestionType.FILL_IN
        chord_type = random.choice([ChordType.MAJOR, ChordType.MINOR])
        selected_list = self.circle.get_chord_list(chord_type)
        selected_chord = random.choice(selected_list[:self.number_of_chords_to_ask_about])
        return question, selected_chord, chord_type

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                self.redraw = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_PLUS:
                    self.number_of_chords_to_ask_about = min(self.number_of_chords_to_ask_about + 1, 12)
                elif event.key == pygame.K_MINUS:
                    self.number_of_chords_to_ask_about = max(self.number_of_chords_to_ask_about - 1, 1)
                elif self.state == GameState.ACTIVE:
                    self.handle_input(event)
                elif self.state == GameState.INACTIVE and event.key == pygame.K_RETURN:
                    self.state = GameState.ADVANCE

            if self.state == GameState.ADVANCE and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.reset_for_next_question()

    def handle_input(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_RETURN:
            self.state = GameState.INACTIVE
            chord_answer = self.circle.find_chord(self.input_text)
            if chord_answer is None:
                self.result_text = f"{self.input_text} is not a valid chord."
            else:
                was_correct, self.result_text = self.circle.check_answer(
                    chord_answer, self.selected_chord, self.question, self.chord_type
                )
                self.total_questions += 1
                if was_correct:
                    self.correct_answers += 1
        else:
            self.input_text += event.unicode

    def reset_for_next_question(self):
        self.input_text = ""
        self.result_text = ""
        self.question, self.selected_chord, self.chord_type = self.new_question()
        self.state = GameState.ACTIVE
        self.blink = False
        self.blink_counter = 0

    def update_blink(self):
        self.blink_counter += 1
        if self.blink_counter > 30:
            self.blink = not self.blink
            self.blink_counter = 0
            self.redraw = True

    def render(self):
        if not self.redraw:
            return

        self.redraw = False
        self.screen.fill(Config.COLORS["background"])
        self.overlay.fill((0, 0, 0, 0))

        self.circle_render.draw_circle(self.screen)
        self.circle_render.draw_highlighted_chord(self.overlay, self.selected_chord, self.chord_type, self.blink)
        if self.state != GameState.ACTIVE:
            self.circle_render.draw_circle_labels(self.overlay)

        self.screen.blit(self.overlay, (0, 0))
        self.render_question()
        self.render_input()
        self.render_results()
        self.render_stats()

        pygame.display.flip()

    def render_question(self):
        question_surface = self.font_small.render(self.generate_question_text(), True, Config.COLORS["text"])
        question_text_rect = question_surface.get_rect(center=(400, 20))
        self.screen.blit(question_surface, question_text_rect)

    def render_input(self):
        input_surface = self.font_large.render(self.input_text, True, Config.COLORS["text"])
        input_text_rect = input_surface.get_rect(center=(400, 80))
        self.screen.blit(input_surface, input_text_rect)

    def render_results(self):
        if self.state != GameState.ACTIVE:
            result_surface = self.font_small.render(self.result_text, True, Config.COLORS["text"])
            result_text_rect = result_surface.get_rect(center=(400, 110))
            self.screen.blit(result_surface, result_text_rect)

    def render_stats(self):
        range_surface = self.font_small.render(
            f"Range: {self.number_of_chords_to_ask_about}", True, Config.COLORS["text"]
        )
        self.screen.blit(range_surface, (700, 20))

        answers_surface = self.font_small.render(
            f"{self.correct_answers} / {self.total_questions}", True, Config.COLORS["text"]
        )
        self.screen.blit(answers_surface, (700, 50))

    def generate_question_text(self):
        chord_list = self.circle.get_chord_list(self.chord_type)
        selected_index = chord_list.index(self.selected_chord)
        templates = {
            QuestionType.FILL_IN: lambda: f"What is the name of the {'major' if self.chord_type == ChordType.MAJOR else 'minor'} chord at {(selected_index + 11) % 12 + 1} o'clock?",
            QuestionType.CLOCKWISE: lambda: f"What is the chord clockwise from the chord {self.selected_chord}?",
            QuestionType.COUNTERCLOCKWISE: lambda: f"What is the chord counterclockwise from the chord {self.selected_chord}?",
            QuestionType.ALTERNATIVE_CIRCLE: lambda: f"What is the alternative circle chord for the chord {self.selected_chord}?",
            QuestionType.ANY: lambda: f"What is the name of any neighbor chord {self.selected_chord}?",
        }
        return templates.get(self.question, lambda: "Unknown question type")()

    def run(self):
        while True:
            self.handle_events()
            self.update_blink()
            self.render()
            self.clock.tick(Config.FPS)