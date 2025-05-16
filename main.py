import pygame
from game import CircleOfFifthsGame

def main():
    pygame.init()
    game = CircleOfFifthsGame()
    game.run()

if __name__ == "__main__":
    main()