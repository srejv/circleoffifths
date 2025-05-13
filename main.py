# 

import random
from circle import *

def read_input():
    """
    Reads input from the user.
    """
    return input("Answer: ")

def print_question(question_type, selected_chord):
    """
    Prints the question based on the question type and selected chord.
    """
    print_question(generate_question(question_type, selected_chord))

def generate_question(question_type, selected_chord):
    """
    Creates the question string based on the question type and selected chord.
    """
    if question_type == QuestionType.CLOCKWISE:
        return f"What is the chord clockwise from the chord {selected_chord}?"
    elif question_type == QuestionType.COUNTERCLOCKWISE:
        return f"What is the chord counterclockwise from the chord {selected_chord}?"
    elif question_type == QuestionType.ALTERNATIVE_CIRCLE:
        return f"What is the alternative circle chord for the chord {selected_chord}?"
    else:
        return f"What is the name of any neighbor chord {selected_chord}?"

import pygame

def new_question(circle, number_of_chords_to_ask_about):
    question = random.choice(question_types)
    chord_type = random.choice(chord_types)

    selected_list = circle.get_chord_list(chord_type)
    selected_chord = random.choice(selected_list[0:number_of_chords_to_ask_about])
    return question, selected_chord, chord_type

def generate_question_range_string(number_of_chords_to_ask_about):
    return f"Range: {number_of_chords_to_ask_about}"

def generate_number_of_answers_string(correct_answers, total_questions):
    return f"{correct_answers} / {total_questions}"

def main_loop():
    number_of_chords_to_ask_about = 1
    circle = CircleOfFifths()

    pygame.init()
    screen = pygame.display.set_mode((600, 200))
    pygame.display.set_caption("Circle of Fifths Quiz")
    clock = pygame.time.Clock()
    question_font = pygame.font.SysFont(None, 20)
    font = pygame.font.SysFont(None, 48)

    correct_answers = 0
    wrong_answers = 0
    total_questions = 0
    input_text = ""
    result_text = ""
    active = True  # Whether input is being accepted
    advance = False

    chord_answer = None

    question, selected_chord, chord_type = new_question(circle, number_of_chords_to_ask_about)

    while True:

        # Rendering
        screen.fill((30, 30, 30))

        question_surface = question_font.render(generate_question(question, selected_chord), True, (255, 255, 255))
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
                if event.key == pygame.K_RETURN:
                    advance = True
            
            if not active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and advance:
                    input_text = ""  # Clear after Enter
                    result_text = ""
                    question, selected_chord, chord_type = new_question(circle, number_of_chords_to_ask_about)
                    active = True
                    advance = False


        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_loop()

