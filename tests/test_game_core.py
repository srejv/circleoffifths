import unittest
from core.game_core import GameCore
from core.circle import ChordType, QuestionType
from core.chord import Chord

class TestGameCore(unittest.TestCase):
    def setUp(self):
        self.core = GameCore()

    def test_initial_state(self):
        self.assertEqual(self.core.chord_type, ChordType.MAJOR)
        self.assertEqual(self.core.selected_chord_indices, set(range(12)))
        self.assertIsNone(self.core.current_question)
        self.assertIsNone(self.core.current_chord)
        self.assertIsNone(self.core.last_result)
        self.assertEqual(self.core.correct_answers, 0)
        self.assertEqual(self.core.total_questions, 0)

    def test_set_and_get_selected_chord_indices(self):
        indices = [0, 2, 4]
        self.core.set_selected_chord_indices(indices)
        self.assertEqual(self.core.get_selected_chord_indices(), set(indices))

    def test_next_question_sets_state(self):
        self.core.set_selected_chord_indices([0, 1, 2])
        self.core.next_question()
        self.assertIn(self.core.current_chord, [self.core.circle.get_chord_list(self.core.chord_type)[i] for i in [0, 1, 2]])
        self.assertEqual(self.core.current_question, QuestionType.FILL_IN)
        self.assertIsNone(self.core.last_result)

    def test_submit_answer_correct(self):
        self.core.set_selected_chord_indices([0])
        self.core.next_question()
        chord = self.core.current_chord
        answer = chord.alternative_names[0]
        result = self.core.submit_answer(answer)
        self.assertTrue(result)
        self.assertTrue(self.core.last_result["correct"])
        self.assertEqual(self.core.last_result["answer"], chord)
        self.assertEqual(self.core.correct_answers, 1)
        self.assertEqual(self.core.total_questions, 1)

    def test_submit_answer_incorrect(self):
        self.core.set_selected_chord_indices([0])
        self.core.next_question()
        wrong_answer = "NonexistentChord"
        result = self.core.submit_answer(wrong_answer)
        self.assertFalse(result)
        self.assertFalse(self.core.last_result["correct"])
        self.assertEqual(self.core.last_result["reason"], "not_found")
        self.assertEqual(self.core.correct_answers, 0)
        self.assertEqual(self.core.total_questions, 1)

    def test_get_stats(self):
        self.core.correct_answers = 3
        self.core.total_questions = 5
        stats = self.core.get_stats()
        self.assertEqual(stats, (3, 5))

    def test_get_state(self):
        self.core.set_selected_chord_indices([1, 2])
        self.core.next_question()
        state = self.core.get_state()
        self.assertIn("chord_type", state)
        self.assertIn("current_chord", state)
        self.assertIn("current_question", state)
        self.assertIn("selected_chord_indices", state)
        self.assertIn("last_result", state)
        self.assertIsInstance(state["selected_chord_indices"], list)

    def test_get_chord_list(self):
        major_list = self.core.get_chord_list(ChordType.MAJOR)
        minor_list = self.core.get_chord_list(ChordType.MINOR)
        self.assertEqual(len(major_list), 12)
        self.assertEqual(len(minor_list), 12)
        self.assertIsInstance(major_list[0], Chord)
        self.assertIsInstance(minor_list[0], Chord)

    def test_major_minor_chords_properties(self):
        self.assertEqual(self.core.major_chords, self.core.circle.major_chords)
        self.assertEqual(self.core.minor_chords, self.core.circle.minor_chords)

if __name__ == "__main__":
    unittest.main()