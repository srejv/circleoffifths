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
        self.circle = CircleOfFifths()
        self.chord_type = ChordType.MAJOR
        self.selected_chord_indices = set(range(12))
        self.current_question = None
        self.current_chord = None
        self.last_result = None

    def set_selected_chord_indices(self, indices: List[int]) -> None:
        self.selected_chord_indices = set(indices)

    def get_selected_chord_indices(self):
        return self.selected_chord_indices

    def next_question(self) -> None:
        self.chord_type = random.choice(list(ChordType))
        chord_list = self.circle.get_chord_list(self.chord_type)
        available = [chord_list[i] for i in self.selected_chord_indices]
        self.current_chord = random.choice(available)
        self.current_question = QuestionType.FILL_IN # random.choice(list(QuestionType))
        self.last_result = None

    def submit_answer(self, answer: str) -> bool:
        chord = self.circle.find_chord(answer)
        if chord is None:
            self.last_result = {"correct": False, "reason": "not_found"}
            return False
        correct = self.circle.check_answer(
            chord, self.current_chord, self.current_question, self.chord_type
        )
        self.last_result = {"correct": correct, "answer": chord}
        return correct

    def get_state(self) -> Dict[str, Any]:
        return {
            "chord_type": self.chord_type,
            "current_chord": self.current_chord,
            "current_question": self.current_question,
            "selected_chord_indices": list(self.selected_chord_indices),
            "last_result": self.last_result,
        }

    def get_chord_list(self, chord_type: ChordType) -> List[Chord]:
        return self.circle.get_chord_list(chord_type)
    
    @property
    def major_chords(self):
        return self.circle.majorChords

    @property
    def minor_chords(self):
        return self.circle.minorChords