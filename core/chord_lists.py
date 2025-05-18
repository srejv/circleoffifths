from typing import List
from core.chord import Chord

# Define the major and minor chords for the circle of fifths.
major_chords: List[Chord] = [
    Chord("C"), Chord("G"), Chord("D"), Chord("A"), Chord("E"), Chord("B"),
    Chord("F#/Gb"), Chord("C#/Db"), Chord("G#/Ab"), Chord("D#/Eb"), Chord("A#/Bb"), Chord("F")
]
minor_chords: List[Chord] = [
    Chord("Am"), Chord("Em"), Chord("Bm"), Chord("F#m/Gbm"), Chord("C#m/Dbm"),
    Chord("G#m/Abm"), Chord("D#m/Ebm"), Chord("A#m/Bbm"), Chord("Fm"), Chord("Cm"),
    Chord("Gm"), Chord("Dm")
]