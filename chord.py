class Chord:
    """
    A class to represent a musical chord.
    """

    def __init__(self, name):
        """
        Initializes the Chord with a name.
        """
        self.name = name
        self.alternative_names = [n.strip() for n in name.split("/")]

    def __str__(self):
        return self.name

    def contains(self, name):
        """
        Checks if the named chord is a part of this chord.
        """
        return name in self.alternative_names