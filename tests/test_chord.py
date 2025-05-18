import unittest
from core.chord import Chord

class TestChord(unittest.TestCase):
    def test_init_and_str(self):
        chord = Chord("C#/Db")
        self.assertEqual(chord.name, "C#/Db")
        self.assertEqual(chord.alternative_names, ["C#", "Db"])
        self.assertEqual(str(chord), "C#/Db")

    def test_init_no_slash(self):
        chord = Chord("F")
        self.assertEqual(chord.name, "F")
        self.assertEqual(chord.alternative_names, ["F"])
        self.assertEqual(str(chord), "F")
        self.assertTrue(chord.contains("F"))
        self.assertFalse(chord.contains("G"))

    def test_contains(self):
        chord = Chord("F#/Gb")
        self.assertTrue(chord.contains("F#"))
        self.assertTrue(chord.contains("Gb"))
        self.assertFalse(chord.contains("G#"))

    def test_equality(self):
        chord1 = Chord("A/Bb")
        chord2 = Chord("Bb/A")
        chord3 = Chord("A/Bb/C")
        chord4 = Chord("A/Bb")
        self.assertEqual(chord1, chord2)
        self.assertNotEqual(chord1, chord3)
        self.assertEqual(chord1, chord4)
        self.assertNotEqual(chord1, "A/Bb")  # Not a Chord instance

    def test_hash(self):
        chord1 = Chord("C#/Db")
        chord2 = Chord("Db/C#")
        chord_set = {chord1, chord2}
        self.assertEqual(len(chord_set), 1)
        chord3 = Chord("C#/Db/Eb")
        chord_set.add(chord3)
        self.assertEqual(len(chord_set), 2)

if __name__ == "__main__":
    unittest.main()