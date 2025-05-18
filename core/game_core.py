from core.circle import CircleOfFifths, QuestionType, ChordType
from core.chord import Chord
import random
from typing import List, Dict, Any

class GameCore:
    """
    Core logic for the Circle of Fifths quiz.
    No UI or rendering code here.
    """

    def __init__(self):
        """
        Initializes the core game logic, including the circle, state, and statistics.
        """
        self.circle = CircleOfFifths()
        self.chord_type = ChordType.MAJOR
        self.selected_chord_indices = set(range(12))
        self.current_question = None
        self.current_chord = None
        self.last_result = None
        self.correct_answers: int = 0
        self.total_questions: int = 0

    def set_selected_chord_indices(self, indices: List[int]) -> None:
        """
        Sets the selected chord indices for the quiz.

        Args:
            indices (List[int]): List of selected chord indices.
        """
        self.selected_chord_indices = set(indices)

    def get_selected_chord_indices(self) -> set:
        """
        Returns the set of currently selected chord indices.

        Returns:
            set: The set of selected chord indices.
        """
        return self.selected_chord_indices

    def next_question(self) -> None:
        """
        Generates the next quiz question and selects a new chord.
        Resets the last result.
        """
        self.chord_type = random.choice(list(ChordType))
        chord_list = self.circle.get_chord_list(self.chord_type)
        available = [chord_list[i] for i in self.selected_chord_indices]
        self.current_chord = random.choice(available)
        self.current_question = QuestionType.FILL_IN  # random.choice(list(QuestionType))
        self.last_result = None

    def submit_answer(self, answer: str) -> bool:
        """
        Submits an answer and checks if it is correct.

        Args:
            answer (str): The user's answer.

        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        chord = self.circle.find_chord(answer)
        if chord is None:
            self.last_result = {"correct": False, "reason": "not_found"}
            return False
        correct = self.circle.check_answer(
            chord, self.current_chord, self.current_question, self.chord_type
        )
        self.last_result = {"correct": correct, "answer": chord}
        self.total_questions += 1
        if correct:
            self.correct_answers += 1
        return correct

    def get_stats(self) -> tuple:
        """
        Returns the current quiz statistics.

        Returns:
            tuple: (number of correct answers, total number of questions)
        """
        return self.correct_answers, self.total_questions

    def get_state(self) -> Dict[str, Any]:
        """
        Returns the current game state as a dictionary.

        Returns:
            Dict[str, Any]: The current game state.
        """
        return {
            "chord_type": self.chord_type,
            "current_chord": self.current_chord,
            "current_question": self.current_question,
            "selected_chord_indices": list(self.selected_chord_indices),
            "last_result": self.last_result,
        }

    def get_chord_list(self, chord_type: ChordType) -> List[Chord]:
        """
        Returns the list of chords for the specified chord type.

        Args:
            chord_type (ChordType): The type of chord (major or minor).

        Returns:
            List[Chord]: The list of chords.
        """
        return self.circle.get_chord_list(chord_type)
    
    @property
    def major_chords(self) -> List[Chord]:
        """
        Returns the list of major chords.

        Returns:
            List[Chord]: The list of major chords.
        """
        return self.circle.major_chords

    @property
    def minor_chords(self) -> List[Chord]:
        """
        Returns the list of minor chords.

        Returns:
            List[Chord]: The list of minor chords.
        """
        return self.circle.minor_chords