from core.circle import QuestionType, ChordType
from core.chord import Chord
from localization import Localization
from typing import List

def generate_question_text(state: dict, loc: Localization, chord_list: List[Chord]) -> str:
    """
    Generate the localized question text for the current quiz question.

    Args:
        state (dict): The current game state dictionary.
        loc (Localization): The localization instance to use for translations.
        chord_list (List[Chord]): The list of chords for the current circle.

    Returns:
        str: The localized question string.
    """
    selected_index = chord_list.index(state["current_chord"])
    chord_type_str = loc.t("major") if state["chord_type"] == ChordType.MAJOR else loc.t("minor")
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
    return loc.t(
        key,
        chord_type=chord_type_str,
        hour=hour,
        chord=chord_str
    )

def get_feedback_message(state: dict, loc: Localization) -> str:
    """
    Generate the localized feedback message for the user's answer.

    Args:
        state (dict): The current game state dictionary.
        loc (Localization): The localization instance to use for translations.

    Returns:
        str: The localized feedback message.
    """
    if state.get("last_result") is None:
        return ""

    if state["last_result"]["correct"] == False and state.get("last_result").get("reason") is not None:
        return loc.t(state["last_result"]["reason"])

    is_correct = state.get("last_result").get("correct")
    chord_str = str(state.get("current_chord"))
    answer_str = state.get("last_result").get("answer")
    correct_str = state.get("current_chord").name

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
    return loc.t(
        key,
        answer=answer_str,
        selected=chord_str,
        correct=correct_str
    )