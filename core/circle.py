from core.chord import Chord
from enum import Enum
from typing import List, Optional
from core.chord_lists import major_chords, minor_chords

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

question_types: List[QuestionType] = [
    QuestionType.CLOCKWISE, QuestionType.COUNTERCLOCKWISE,
    QuestionType.ALTERNATIVE_CIRCLE, QuestionType.ANY
]
chord_types: List[ChordType] = [ChordType.MAJOR, ChordType.MINOR]

CIRCLE_SIZE: int = 12  # Number of chords in the circle

class CircleOfFifths:
    """
    Represents the Circle of Fifths and provides utility methods
    for chord lookup, neighbor calculation, and answer checking.
    """

    def __init__(self) -> None:
        """
        Initializes the Circle of Fifths with major and minor chords.
        """
        self.major_chords: List[Chord] = major_chords
        self.minor_chords: List[Chord] = minor_chords

    def get_chord_list(self, chord_type: ChordType) -> List[Chord]:
        """
        Returns the list of chords based on the chord type.

        Args:
            chord_type (ChordType): The type of chord (MAJOR or MINOR).

        Returns:
            List[Chord]: The list of Chord objects for the specified type.
        """
        if chord_type == ChordType.MAJOR:
            return self.major_chords
        elif chord_type == ChordType.MINOR:
            return self.minor_chords
        else:
            raise ValueError("Invalid chord type")

    def find_chord(self, name: str) -> Optional[Chord]:
        """
        Finds the chord with the given name (including alternative names).

        Args:
            name (str): The name or alternative name of the chord.

        Returns:
            Optional[Chord]: The matching Chord object, or None if not found.
        """
        for chord in self.minor_chords + self.major_chords:
            if chord.contains(name):
                return chord
        return None

    def get_chord(self, index: int, chord_type: ChordType = ChordType.MAJOR) -> Chord:
        """
        Returns the chord at the given index, wrapping around the circle.

        Args:
            index (int): The index of the chord.
            chord_type (ChordType): The type of chord (MAJOR or MINOR).

        Returns:
            Chord: The chord at the specified index.
        """
        chord_list = self.get_chord_list(chord_type)
        return chord_list[index % CIRCLE_SIZE]

    def get_next_chord(
        self,
        chord: Chord,
        direction: QuestionType,
        chord_type: ChordType = ChordType.MAJOR
    ) -> List[Chord]:
        """
        Returns the next chord(s) based on the direction and chord type.

        Args:
            chord (Chord): The reference chord.
            direction (QuestionType): The direction/question type.
            chord_type (ChordType): The type of chord (MAJOR or MINOR).

        Returns:
            List[Chord]: List of Chord(s) that are the answer(s) for the given direction.
        """
        chord_list = self.get_chord_list(chord_type)
        alt_list = self.get_chord_list(ChordType.MINOR if chord_type == ChordType.MAJOR else ChordType.MAJOR)
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
        chord_answer: Chord,
        selected_chord: Chord,
        question_type: QuestionType,
        chord_type: ChordType
    ) -> bool:
        """
        Checks if the provided answer is correct for the current question.

        Args:
            chord_answer (Chord): The chord provided as an answer.
            selected_chord (Chord): The chord the question is about.
            question_type (QuestionType): The type of question.
            chord_type (ChordType): The type of chord (major or minor).

        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        potential_answers = self.get_next_chord(
            selected_chord, question_type, chord_type
        )
        return chord_answer in potential_answers

    def get_neighbor_indices(self, chord_list: List[Chord], chord: Chord) -> List[int]:
        """
        Returns the indices of the neighbors (clockwise and counterclockwise) of the given chord.

        Args:
            chord_list (List[Chord]): The list of chords (major or minor).
            chord (Chord): The chord whose neighbors to find.

        Returns:
            List[int]: Indices of the neighbor chords.
        """
        n = len(chord_list)
        try:
            idx = chord_list.index(chord)
        except ValueError:
            return []
        return [(idx - 1) % n, (idx + 1) % n]

    def is_neighbor(
        self,
        chord_list: List[Chord],
        chord: Chord,
        maybe_neighbor: Chord
    ) -> bool:
        """
        Checks if maybe_neighbor is a neighbor (clockwise or counterclockwise) of chord.

        Args:
            chord_list (List[Chord]): The list of chords (major or minor).
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

