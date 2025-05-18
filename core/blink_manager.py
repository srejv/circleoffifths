class BlinkManager:
    """
    Handles blinking state for UI effects.
    """
    def __init__(self, interval: int = 30) -> None:
        """
        Args:
            interval (int): Number of ticks between blinks.
        """
        self.interval = interval
        self.blink = False
        self.counter = 0

    def update(self) -> bool:
        """
        Updates the blink state.
        """
        self.counter += 1
        if self.counter > self.interval:
            self.blink = not self.blink
            self.counter = 0
            return True
        return False

    def reset(self) -> None:
        """
        Resets the blink state.
        """
        self.blink = False
        self.counter = 0
    
    def is_blinking(self) -> bool:
        """
        Returns the current blink state.
        """
        return self.blink