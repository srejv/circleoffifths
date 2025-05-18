class BlinkManager:
    """
    Handles blinking state for UI effects.
    """

    def __init__(self, interval: int = 30) -> None:
        """
        Initializes the BlinkManager.

        Args:
            interval (int): Number of ticks between blinks.
        """
        self.interval = interval
        self.blink = False
        self.counter = 0

    def update(self) -> bool:
        """
        Updates the blink state. Should be called once per tick/frame.

        Returns:
            bool: True if the blink state changed (toggle occurred), False otherwise.
        """
        self.counter += 1
        if self.counter > self.interval:
            self.blink = not self.blink
            self.counter = 0
            return True
        return False

    def reset(self) -> None:
        """
        Resets the blink state and counter to their initial values.
        """
        self.blink = False
        self.counter = 0
    
    def is_blinking(self) -> bool:
        """
        Returns the current blink state.

        Returns:
            bool: True if currently in the "blink" state, False otherwise.
        """
        return self.blink