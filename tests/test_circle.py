import unittest
from core.circle import CircleOfFifths, ChordType, QuestionType
from core.chord import Chord

class TestCircleOfFifths(unittest.TestCase):
    def setUp(self):
        self.circle = CircleOfFifths()

    def test_get_chord_list_major(self):
        major_list = self.circle.get_chord_list(ChordType.MAJOR)
        self.assertEqual(len(major_list), 12)
        self.assertIsInstance(major_list[0], Chord)

    def test_get_chord_list_minor(self):
        minor_list = self.circle.get_chord_list(ChordType.MINOR)
        self.assertEqual(len(minor_list), 12)
        self.assertIsInstance(minor_list[0], Chord)

    def test_find_chord(self):
        chord = self.circle.find_chord("C")
        self.assertIsInstance(chord, Chord)
        self.assertTrue(chord.contains("C"))
        self.assertIsNone(self.circle.find_chord("Nonexistent"))

    def test_get_chord_wraps(self):
        chord_list = self.circle.get_chord_list(ChordType.MAJOR)
        chord = self.circle.get_chord(12, ChordType.MAJOR)
        self.assertEqual(chord, chord_list[0])
        chord = self.circle.get_chord(-1, ChordType.MAJOR)
        self.assertEqual(chord, chord_list[-1])

    def test_get_next_chord_fill_in(self):
        chord = self.circle.get_chord_list(ChordType.MAJOR)[0]
        result = self.circle.get_next_chord(chord, QuestionType.FILL_IN, ChordType.MAJOR)
        self.assertEqual(result, [chord])

    def test_get_next_chord_clockwise(self):
        chord_list = self.circle.get_chord_list(ChordType.MAJOR)
        chord = chord_list[0]
        next_chord = chord_list[1]
        result = self.circle.get_next_chord(chord, QuestionType.CLOCKWISE, ChordType.MAJOR)
        self.assertEqual(result, [next_chord])

    def test_get_next_chord_counterclockwise(self):
        chord_list = self.circle.get_chord_list(ChordType.MAJOR)
        chord = chord_list[0]
        prev_chord = chord_list[-1]
        result = self.circle.get_next_chord(chord, QuestionType.COUNTERCLOCKWISE, ChordType.MAJOR)
        self.assertEqual(result, [prev_chord])

    def test_get_next_chord_alternative_circle(self):
        major_chord = self.circle.get_chord_list(ChordType.MAJOR)[0]
        minor_chord = self.circle.get_chord_list(ChordType.MINOR)[0]
        result = self.circle.get_next_chord(major_chord, QuestionType.ALTERNATIVE_CIRCLE, ChordType.MAJOR)
        self.assertEqual(result, [minor_chord])

    def test_get_next_chord_any(self):
        chord_list = self.circle.get_chord_list(ChordType.MAJOR)
        alt_list = self.circle.get_chord_list(ChordType.MINOR)
        chord = chord_list[0]
        expected = [chord_list[1], chord_list[-1], alt_list[0]]
        result = self.circle.get_next_chord(chord, QuestionType.ANY, ChordType.MAJOR)
        self.assertEqual(result, expected)

    def test_check_answer(self):
        chord = self.circle.get_chord_list(ChordType.MAJOR)[0]
        next_chord = self.circle.get_chord_list(ChordType.MAJOR)[1]
        self.assertTrue(self.circle.check_answer(next_chord, chord, QuestionType.CLOCKWISE, ChordType.MAJOR))
        self.assertFalse(self.circle.check_answer(chord, chord, QuestionType.CLOCKWISE, ChordType.MAJOR))

    def test_get_neighbor_indices(self):
        chord_list = self.circle.get_chord_list(ChordType.MAJOR)
        chord = chord_list[0]
        indices = self.circle.get_neighbor_indices(chord_list, chord)
        self.assertEqual(indices, [len(chord_list)-1, 1])

    def test_is_neighbor(self):
        chord_list = self.circle.get_chord_list(ChordType.MAJOR)
        chord = chord_list[0]
        neighbor = chord_list[1]
        not_neighbor = chord_list[2]
        self.assertTrue(self.circle.is_neighbor(chord_list, chord, neighbor))
        self.assertFalse(self.circle.is_neighbor(chord_list, chord, not_neighbor))

if __name__ == "__main__":
    unittest.main()