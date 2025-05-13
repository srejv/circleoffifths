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

def main_loop():
    number_of_chords_to_ask_about = 1
    circle = CircleOfFifths()

    while True:
        question = random.choice(question_types)
        chord_type = random.choice(chord_types)

        selected_list = circle.get_chord_list(chord_type)
        selected_chord = random.choice(selected_list[0:number_of_chords_to_ask_about])

        print("")
        print_question(question, selected_chord)
        print("")

        chord_input = read_input()
        chord_answer = circle.find_chord(chord_input)
        if chord_answer is None:
            print(f"{chord_input} is not a valid chord.")
            continue

        circle.check_answer(chord_answer, selected_chord, question, chord_type)

if __name__ == "__main__":
    main_loop()

