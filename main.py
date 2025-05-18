import pygame
from core.game import CircleOfFifthsGame

def main():
    """
    Initializes pygame and starts the Circle of Fifths game.
    """
    pygame.init()
    game = CircleOfFifthsGame("en")
    game.run()

if __name__ == "__main__":
    main()