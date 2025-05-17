from chord import Chord
from enum import Enum

# Define the major and minor chords for the circle of fifths.
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
    """Enumeration for the different types of quiz questions."""
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2
    ALTERNATIVE_CIRCLE = 3
    ANY = 4
    FILL_IN = 5

class ChordType(Enum):
    """Enumeration for chord types (major or minor)."""
    MAJOR = 1
    MINOR = 2

question_types = [ QuestionType.CLOCKWISE, QuestionType.COUNTERCLOCKWISE, QuestionType.ALTERNATIVE_CIRCLE, QuestionType.ANY ]
chord_types = [ ChordType.MAJOR, ChordType.MINOR ]

CIRCLE_SIZE = 12  # Number of chords in the circle

class CircleOfFifths:
    """
    A class to represent the Circle of Fifths and provide utility methods
    for chord lookup, neighbor calculation, and answer checking.
    """

    def __init__(self):
        """
        Initializes the Circle of Fifths with major and minor chords.
        """
        self.majorChords = majorChords
        self.minorChords = minorChords

    def get_chord_list(self, chord_type: ChordType):
        """
        Returns the list of chords based on the chord type.

        Args:
            chord_type (ChordType): The type of chord (MAJOR or MINOR).

        Returns:
            list: The list of Chord objects for the specified type.
        """
        if chord_type == ChordType.MAJOR:
            return self.majorChords
        elif chord_type == ChordType.MINOR:
            return self.minorChords
        else:
            raise ValueError("Invalid chord type")

    def find_chord(self, name: str):
        """
        Finds the chord with the given name (including alternative names).

        Args:
            name (str): The name or alternative name of the chord.

        Returns:
            Chord or None: The matching Chord object, or None if not found.
        """
        for chord in self.minorChords + self.majorChords:
            if chord.contains(name):
                return chord
        return None

    def get_chord(self, index, is_major=True):
        """
        Returns the chord at the given index, wrapping around the circle.

        Args:
            index (int): The index of the chord.
            is_major (bool): Whether to use the major or minor circle.

        Returns:
            Chord: The chord at the specified index.
        """
        chord_list = self.majorChords if is_major else self.minorChords
        return chord_list[index % CIRCLE_SIZE]

    def get_next_chord(self, chord, direction, is_major=True):
        """
        Returns the next chord(s) based on the direction and chord type.

        Args:
            chord (Chord): The reference chord.
            direction (QuestionType): The direction/question type.
            is_major (bool): Whether to use the major or minor circle.

        Returns:
            list: List of Chord(s) that are the answer(s) for the given direction.
        """
        chord_list = self.majorChords if is_major else self.minorChords
        alt_list = self.minorChords if is_major else self.majorChords
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
            return [alt_list[idx]]
        else:  # ANY
            return [chord_list[(idx + 1) % n], chord_list[(idx - 1) % n], alt_list[idx]]
        
    def check_answer(
            self, 
            chord_answer, 
            selected_chord, 
            question_type, 
            chord_type
    ) -> tuple[bool, str]:
        """
        Checks if the provided answer is correct for the current question.

        Args:
            chord_answer (Chord): The chord provided as an answer.
            selected_chord (Chord): The chord the question is about.
            question_type (QuestionType): The type of question.
            chord_type (ChordType): The type of chord (major or minor).

        Returns:
            tuple: (bool, str) indicating if the answer is correct and a feedback message.
        """
        potential_answers = self.get_next_chord(
            selected_chord, question_type, chord_type == ChordType.MAJOR
        )
        is_correct = chord_answer in potential_answers

        # Feedback templates for correct and incorrect answers
        correct_msgs = {
            QuestionType.FILL_IN:      lambda: f"Correct! {chord_answer} is the correct answer.",
            QuestionType.ALTERNATIVE_CIRCLE: lambda: f"Correct! {chord_answer} is the next chord in the alternative circle direction from {selected_chord}.",
            QuestionType.ANY:          lambda: f"Correct! {chord_answer} is a neighbor chord of {selected_chord}.",
            QuestionType.CLOCKWISE:    lambda: f"Correct! {chord_answer} is the next chord in the clockwise direction from {selected_chord}.",
            QuestionType.COUNTERCLOCKWISE: lambda: f"Correct! {chord_answer} is the next chord in the counterclockwise direction from {selected_chord}.",
        }
        incorrect_msgs = {
            QuestionType.FILL_IN:      lambda: f"No. {chord_answer} is not the correct answer. Correct answer is {selected_chord.name}.",
            QuestionType.ALTERNATIVE_CIRCLE: lambda: f"No. {chord_answer} is not the next chord in the alternative circle direction from {selected_chord}.",
            QuestionType.ANY:          lambda: f"No. {chord_answer} is not a neighbor chord of {selected_chord}.",
            QuestionType.CLOCKWISE:    lambda: f"No. {chord_answer} is not the next chord in the clockwise direction from {selected_chord}.",
            QuestionType.COUNTERCLOCKWISE: lambda: f"No. {chord_answer} is not the next chord in the counterclockwise direction from {selected_chord}.",
        }

        msg = (
            correct_msgs.get(question_type, lambda: "Correct!")( )
            if is_correct
            else incorrect_msgs.get(question_type, lambda: "No.")( )
        )
        return is_correct, msg

    def get_neighbor_indices(self, chord_list, chord):
        """
        Returns the indices of the neighbors (clockwise and counterclockwise) of the given chord.

        Args:
            chord_list (list): The list of chords (major or minor).
            chord (Chord): The chord whose neighbors to find.

        Returns:
            list: Indices of the neighbor chords.
        """
        n = len(chord_list)
        try:
            idx = chord_list.index(chord)
        except ValueError:
            return []
        return [(idx - 1) % n, (idx + 1) % n]

    def is_neighbor(self, chord_list, chord, maybe_neighbor):
        """
        Checks if maybe_neighbor is a neighbor (clockwise or counterclockwise) of chord.

        Args:
            chord_list (list): The list of chords (major or minor).
            chord (Chord): The reference chord.
            maybe_neighbor (Chord): The chord to check.

        Returns:
            bool: True if maybe_neighbor is a neighbor of chord, False otherwise.
        """
        n = len(chord_list)
        try:
            idx = chord_list.index(chord)
            neighbor_indices = [(idx - 1) % n, (idx + 1) % n]
            return chord_list.index(maybe_neighbor) in neighbor_indices
        except ValueError:
            return False