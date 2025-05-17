from typing import List, Any

class Chord:
    """
    A class to represent a musical chord, including alternative names.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes the Chord with a name and parses alternative names.

        Args:
            name (str): The name of the chord, with alternatives separated by '/'.
        """
        self.name: str = name
        self.alternative_names: List[str] = [n.strip() for n in name.split("/")]

    def __str__(self) -> str:
        """
        Returns the main name of the chord as its string representation.

        Returns:
            str: The main name of the chord.
        """
        return self.name

    def contains(self, name: str) -> bool:
        """
        Checks if the given name matches any of the chord's alternative names.

        Args:
            name (str): The name to check.

        Returns:
            bool: True if the name matches, False otherwise.
        """
        return name in self.alternative_names

    def __eq__(self, other: Any) -> bool:
        """
        Checks equality between two Chord objects based on their alternative names.

        Args:
            other (Any): The object to compare.

        Returns:
            bool: True if the chords are equal, False otherwise.
        """
        if not isinstance(other, Chord):
            return False
        return set(self.alternative_names) == set(other.alternative_names)

    def __hash__(self) -> int:
        """
        Returns a hash based on the chord's alternative names.

        Returns:
            int: The hash value.
        """
        return hash(tuple(sorted(self.alternative_names)))