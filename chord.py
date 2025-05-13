
class Chord:
    """
    A class to represent a musical chord.
    """

    def __init__(self, name, index):
        """
        Initializes the Chord with a name and index.
        """
        self.name = name
        self.alternative_names = name.split("/")
        self.index = index

    def __str__(self):
        """
        Returns the string representation of the Chord.
        """
        return self.name
    
    def is_next_to(self, maybe_neighbor_index, total_chords):
        """
        Checks if the given index is next to the chord's index, considering wrapping.
        """
        return (self.index - 1) % total_chords == maybe_neighbor_index or \
               (self.index + 1) % total_chords == maybe_neighbor_index

    def contains(self, name):
        """
        Checks if the named chord is a part of this chord.
        """
        if self.name == name:
            return True
        for alt_name in self.alternative_names:
            if alt_name == name:
                return True
        return False