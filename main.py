# 

import random
from circle import *
import pygame
from render import CircleOfFifthsDrawable

def generate_question(question_type, selected_chord, chord_type):
    """
    Creates the question string based on the question type and selected chord.
    """
    if question_type == QuestionType.FILL_IN:
        if chord_type == ChordType.MAJOR:
            return f"What is the name of the major chord at {(selected_chord.index + 11) % 12 + 1} o'clock?"
        else:
            return f"What is the name of the minor chord at {(selected_chord.index + 11) % 12 + 1} o'clock?"
    elif question_type == QuestionType.CLOCKWISE:
        return f"What is the chord clockwise from the chord {selected_chord}?"
    elif question_type == QuestionType.COUNTERCLOCKWISE:
        return f"What is the chord counterclockwise from the chord {selected_chord}?"
    elif question_type == QuestionType.ALTERNATIVE_CIRCLE:
        return f"What is the alternative circle chord for the chord {selected_chord}?"
    else:
        return f"What is the name of any neighbor chord {selected_chord}?"


def new_question(circle, number_of_chords_to_ask_about):
    question = QuestionType.FILL_IN # random.choice(question_types)
    chord_type = random.choice(chord_types)

    selected_list = circle.get_chord_list(chord_type)
    selected_chord = random.choice(selected_list[0:number_of_chords_to_ask_about])
    return question, selected_chord, chord_type

def generate_question_range_string(number_of_chords_to_ask_about):
    return f"Range: {number_of_chords_to_ask_about}"

def generate_number_of_answers_string(correct_answers, total_questions):
    return f"{correct_answers} / {total_questions}"

def main_loop():
    pygame.init()

    number_of_chords_to_ask_about = 1
    circle = CircleOfFifths()
    circle_render = CircleOfFifthsDrawable(circle.majorChords, circle.minorChords)
    circle_render.set_center((400, 360))

    screen = pygame.display.set_mode((800, 600))
    overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
    pygame.display.set_caption("Circle of Fifths Quiz")
    clock = pygame.time.Clock()

    question_font = pygame.font.SysFont(None, 20)
    font = pygame.font.SysFont(None, 48)

    correct_answers = 0
    wrong_answers = 0
    total_questions = 0

    input_text = ""
    result_text = ""

    # These should be an enum QuizStates (Asking, Answered, Continue)
    active = True  # Whether input is being accepted
    advance = False

    chord_answer = None

    redraw = True

    question, selected_chord, chord_type = new_question(circle, number_of_chords_to_ask_about)

    blink_counter = 0
    blink = False

    while True:

        # Rendering
        if redraw:
            redraw = False

            screen.fill((30, 30, 30))
            overlay.fill((0,0,0,0))

            circle_render.draw_circle(screen)
            circle_render.draw_highlighted_chord(overlay, selected_chord, chord_type, blink)
            if not active:
                circle_render.draw_circle_labels(overlay)

            screen.blit(overlay, (0, 0))

            question_surface = question_font.render(generate_question(question, selected_chord, chord_type), True, (255, 255, 255))
            screen.blit(question_surface, (20, 10))

            text_surface = font.render(input_text, True, (255, 255, 255))
            screen.blit(text_surface, (20, 80))

            if not active:
                result_surface = question_font.render(result_text, True, (255, 255, 255))
                screen.blit(result_surface, (20, 110))

            range_surface = question_font.render(generate_question_range_string(number_of_chords_to_ask_about), True, (255, 255, 255))
            screen.blit(range_surface, (500, 20))

            answers_surface = question_font.render(generate_number_of_answers_string(correct_answers, total_questions), True, (255, 255, 255))
            screen.blit(answers_surface, (500, 50))


        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                redraw = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_PLUS:
                    number_of_chords_to_ask_about += 1
                    if number_of_chords_to_ask_about > 12:
                        number_of_chords_to_ask_about = 12
                    continue
                elif event.key == pygame.K_MINUS:
                    number_of_chords_to_ask_about -= 1
                    if number_of_chords_to_ask_about < 1:
                        number_of_chords_to_ask_about = 1
                    continue

            if active and event.type == pygame.KEYDOWN:
                redraw = True                                    
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    active = False
                    chord_answer = circle.find_chord(input_text)
                    if chord_answer is None:
                        result_text = f"{input_text} is not a valid chord."
                        continue
                    was_correct, result_text = circle.check_answer(chord_answer, selected_chord, question, chord_type)

                    total_questions += 1
                    if was_correct:
                        correct_answers += 1
                    else:
                        wrong_answers += 1

                else:
                    input_text += event.unicode

            if not active and event.type == pygame.KEYUP:
                redraw = True
                if event.key == pygame.K_RETURN:
                    advance = True
            
            if not active and event.type == pygame.KEYDOWN:
                redraw = True
                if event.key == pygame.K_RETURN and advance:
                    input_text = ""  # Clear after Enter
                    result_text = ""
                    question, selected_chord, chord_type = new_question(circle, number_of_chords_to_ask_about)
                    active = True
                    advance = False

        blink_counter += 1
        if blink_counter > 30:
            blink = not blink
            blink_counter = 0
            redraw = True

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_loop()

