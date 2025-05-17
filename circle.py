from chord import Chord
from enum import Enum

majorChords = [
    Chord("C"), Chord("G"), Chord("D"), Chord("A"), Chord("E"), Chord("B"),
    Chord("F#/Gb"), Chord("C#/Db"), Chord("G#/Ab"), Chord("D#/Eb"), Chord("A#/Bb"), Chord("F")
]
minorChords = [
    Chord("Am"), Chord("Em"), Chord("Bm"), Chord("F#m/Gbm"), Chord("C#m/Dbm"),
    Chord("G#m/Abm"), Chord("D#m/Ebm"), Chord("A#m/Bbm"), Chord("Fm"), Chord("Cm"),
    Chord("Gm"), Chord("Dm")
]


class QuestionType(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2
    ALTERNATIVE_CIRCLE = 3
    ANY = 4
    FILL_IN = 5

class ChordType(Enum):
    MAJOR = 1
    MINOR = 2

question_types = [ QuestionType.CLOCKWISE, QuestionType.COUNTERCLOCKWISE, QuestionType.ALTERNATIVE_CIRCLE, QuestionType.ANY ]
chord_types = [ ChordType.MAJOR, ChordType.MINOR ]

class CircleOfFifths:
    """
    A class to represent the Circle of Fifths.
    """

    def __init__(self):
        """
        Initializes the Circle of Fifths with major and minor chords.
        """
        self.majorChords = majorChords
        self.minorChords = minorChords

    def get_chord_list(self, chord_type):
        """
        Returns the list of chords based on the chord type.
        """
        if chord_type == ChordType.MAJOR:
            return self.majorChords
        elif chord_type == ChordType.MINOR:
            return self.minorChords
        else:
            raise ValueError("Invalid chord type")

    def find_chord(self, name):
        """
        Finds the chord with the given name.
        """
        for chord in self.minorChords:
            if chord.contains(name):
                return chord
        for chord in self.majorChords:
            if chord.contains(name):
                return chord
        return None

    def get_chord(self, index, is_major=True):
        """
        Returns the chord at the given index.
        """
        if is_major:
            return self.majorChords[index]
        else:
            return self.minorChords[index]
    
    def get_next_chord(self, chord, direction, is_major=True):
        chord_list = self.majorChords if is_major else self.minorChords
        n = len(chord_list)
        try:
            idx = chord_list.index(chord)
        except ValueError:
            return []
        if direction == QuestionType.FILL_IN:
            return [chord_list[idx % n]]
        elif direction == QuestionType.CLOCKWISE:
            return [chord_list[(idx + 1) % n]]
        elif direction == QuestionType.COUNTERCLOCKWISE:
            return [chord_list[(idx - 1) % n]]
        elif direction == QuestionType.ALTERNATIVE_CIRCLE:
            alt_list = self.minorChords if is_major else self.majorChords
            return [alt_list[idx]]
        else:  # ANY
            alt_list = self.minorChords if is_major else self.majorChords
            return [chord_list[(idx + 1) % n], chord_list[(idx - 1) % n], alt_list[idx]]
        
    def check_answer(self, chord_answer, selected_chord, question_type, chord_type):
        """
        Checks if the answer is correct.
        """
        potential_answers = self.get_next_chord(selected_chord, question_type, chord_type == ChordType.MAJOR)
        if chord_answer in potential_answers:
            if question_type == QuestionType.FILL_IN:
                return True, f"Correct! {chord_answer} is the correct answer."
            elif question_type == QuestionType.ALTERNATIVE_CIRCLE:
                return True, f"Correct! {chord_answer} is the next chord in the alternative circle direction from {selected_chord}."
            elif question_type == QuestionType.ANY:
                return True, f"Correct! {chord_answer} is a neighbor chord of {selected_chord}."
            return True, f"Correct! {chord_answer} is the next chord in the {question_type.name.lower()} direction from {selected_chord}."
        else:
            if question_type == QuestionType.FILL_IN:
                return False, f"No. {chord_answer} is not the correct answer. Correct answer is {selected_chord.name}."
            elif question_type == QuestionType.ALTERNATIVE_CIRCLE:
                return False, f"No. {chord_answer} is not the next chord in the alternative circle direction from {selected_chord}."
            elif question_type == QuestionType.ANY:
                return False, f"No. {chord_answer} is not a neighbor chord of {selected_chord}."
            return False, f"No. {chord_answer} is not the next chord in the {question_type.name.lower()} direction from {selected_chord}."

    def get_neighbor_indices(self, chord_list, chord):
        """
        Returns the indices of the neighbors of the given chord in the chord_list.
        """
        n = len(chord_list)
        try:
            idx = chord_list.index(chord)
        except ValueError:
            return []
        return [(idx - 1) % n, (idx + 1) % n]

    def is_neighbor(self, chord_list, chord, maybe_neighbor):
        """
        Checks if maybe_neighbor is a neighbor of chord in chord_list.
        """
        n = len(chord_list)
        try:
            idx = chord_list.index(chord)
            neighbor_indices = [(idx - 1) % n, (idx + 1) % n]
            return chord_list.index(maybe_neighbor) in neighbor_indices
        except ValueError:
            return False