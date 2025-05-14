from chord import Chord
from enum import Enum

majorChords = [
    Chord("C", 0), Chord("G", 1), Chord("D", 2), Chord("A", 3), Chord("E", 4), Chord("B", 5),
    Chord("F#/Gb", 6), Chord("C#/Db", 7), Chord("G#/Ab", 8), Chord("D#/Eb", 9), Chord("A#/Bb", 10), Chord("F", 11)
]
minorChords = [
    Chord("Am", 0), Chord("Em", 1), Chord("Bm", 2), Chord("F#m/Gbm", 3), Chord("C#m/Dbm", 4),
    Chord("G#m/Abm", 5), Chord("D#m/Ebm", 6), Chord("A#m/Bbm", 7), Chord("Fm", 8), Chord("Cm", 9),
    Chord("Gm", 10), Chord("Dm", 11)
]


class QuestionType(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2
    ALTERNATIVE_CIRCLE = 3
    ANY = 4,
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
        """
        Returns the next chord in the given direction.
        """
        if is_major:
            n = len(self.majorChords)
            if direction == QuestionType.FILL_IN:
                return [self.majorChords[chord.index % n]]
            elif direction == QuestionType.CLOCKWISE:
                return [self.majorChords[(chord.index + 1) % n]]
            elif direction == QuestionType.COUNTERCLOCKWISE:
                return [self.majorChords[(chord.index - 1) % n]]
            elif direction == QuestionType.ALTERNATIVE_CIRCLE:
                return [self.minorChords[chord.index]]
            else:
                return [self.majorChords[(chord.index + 1) % n], self.majorChords[(chord.index - 1) % n], self.minorChords[chord.index]]

        else:
            n = len(self.minorChords)
            if direction == QuestionType.FILL_IN:
                return [self.minorChords[chord.index % n]]
            elif direction == QuestionType.CLOCKWISE:
                return [self.minorChords[(chord.index + 1) % n]]
            elif direction == QuestionType.COUNTERCLOCKWISE:
                return [self.minorChords[(chord.index - 1) % n]]
            elif direction == QuestionType.ALTERNATIVE_CIRCLE:
                return [self.majorChords[chord.index]]
            else:
                return [self.minorChords[(chord.index + 1) % n], self.minorChords[(chord.index - 1) % n], self.majorChords[chord.index]]
    
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
