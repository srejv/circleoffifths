import unittest
from core.game_text import generate_question_text, get_feedback_message
from core.chord import Chord
from core.circle import QuestionType, ChordType
from unittest.mock import MagicMock

class DummyLoc:
    def __init__(self):
        self.calls = []
    def t(self, key, **kwargs):
        self.calls.append((key, kwargs))
        # Return a string that includes the key and any kwargs for test visibility
        return f"{key}|" + "|".join(f"{k}={v}" for k, v in kwargs.items())

class TestGameText(unittest.TestCase):
    def setUp(self):
        self.loc = DummyLoc()
        self.chord_list = [Chord("C"), Chord("G"), Chord("D"), Chord("A"), Chord("E"), Chord("B"),
                           Chord("F#/Gb"), Chord("C#/Db"), Chord("G#/Ab"), Chord("D#/Eb"), Chord("A#/Bb"), Chord("F")]
        self.loc.calls.clear()

    def test_generate_question_text_major(self):
        state = {
            "current_chord": self.chord_list[0],
            "chord_type": ChordType.MAJOR,
            "current_question": QuestionType.FILL_IN
        }
        result = generate_question_text(state, self.loc, self.chord_list)
        self.assertIn("question_fill_in", result)
        # Instead of checking kwargs, check that the result string contains chord_type
        self.assertIn("chord_type=", result)

    def test_generate_question_text_minor(self):
        state = {
            "current_chord": self.chord_list[1],
            "chord_type": ChordType.MINOR,
            "current_question": QuestionType.CLOCKWISE
        }
        result = generate_question_text(state, self.loc, self.chord_list)
        self.assertIn("question_clockwise", result)
        self.assertIn("chord_type=", result)

    def test_get_feedback_message_none(self):
        state = {"last_result": None}
        result = get_feedback_message(state, self.loc)
        self.assertEqual(result, "")

    def test_get_feedback_message_not_found(self):
        state = {"last_result": {"correct": False, "reason": "not_found"}}
        result = get_feedback_message(state, self.loc)
        self.assertIn("not_found", result)

    def test_get_feedback_message_correct(self):
        state = {
            "last_result": {"correct": True, "answer": "C"},
            "current_chord": Chord("C"),
            "current_question": QuestionType.FILL_IN
        }
        result = get_feedback_message(state, self.loc)
        self.assertIn("feedback_correct_fill_in", result)

    def test_get_feedback_message_incorrect(self):
        state = {
            "last_result": {"correct": False, "answer": "G"},
            "current_chord": Chord("C"),
            "current_question": QuestionType.CLOCKWISE
        }
        result = get_feedback_message(state, self.loc)
        self.assertIn("feedback_incorrect_clockwise", result)

    def test_get_feedback_message_default_key(self):
        # Unknown question type should fallback to fill_in
        state = {
            "last_result": {"correct": True, "answer": "C"},
            "current_chord": Chord("C"),
            "current_question": None
        }
        result = get_feedback_message(state, self.loc)
        self.assertIn("feedback_correct_fill_in", result)

if __name__ == "__main__":
    unittest.main()