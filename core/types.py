from typing import TypedDict, Set, Optional
from core.circle import ChordType, QuestionType
from core.chord import Chord

class GameStateDict(TypedDict):
    """
    Typed dictionary representing the state of the Circle of Fifths game.

    Attributes:
        chord_type (ChordType): The current chord type (major or minor).
        current_chord (Optional[Chord]): The currently selected chord for the question.
        current_question (Optional[QuestionType]): The type of the current question.
        selected_chord_indices (Set[int]): The set of selected chord indices.
        last_result (Optional[dict]): The result of the last submitted answer.
        game_state (str): The current state of the game (e.g., 'ACTIVE', 'INACTIVE').
        chord_list (list[Chord]): The list of chords for the current chord type.
        stats (tuple[int, int]): A tuple containing (number of correct answers, total questions).
    """
    chord_type: ChordType
    current_chord: Optional[Chord]
    current_question: Optional[QuestionType]
    selected_chord_indices: Set[int]
    last_result: Optional[dict]
    game_state: str
    chord_list: list[Chord]
    stats: tuple[int, int]