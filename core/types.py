from typing import TypedDict, Set, Optional
from core.circle import ChordType, QuestionType
from core.chord import Chord

class GameStateDict(TypedDict):
    chord_type: ChordType
    current_chord: Optional[Chord]
    current_question: Optional[QuestionType]
    selected_chord_indices: Set[int]
    last_result: Optional[dict]
    game_state: str
    chord_list: list[Chord]
    stats: tuple[int, int]