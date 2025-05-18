class Config:
    """
    Configuration settings for the Circle of Fifths application.

    Attributes:
        SCREEN_WIDTH (int): Width of the game window in pixels.
        SCREEN_HEIGHT (int): Height of the game window in pixels.
        FPS (int): Frames per second for the game loop.
        FONT_SMALL_SIZE (int): Font size for small text.
        FONT_LARGE_SIZE (int): Font size for large text.
        COLORS (dict): Dictionary of commonly used colors.
        CIRCLE_CENTER (tuple): (x, y) coordinates for the center of the circle.
        CIRCLE_RADIUS (int): Outer radius of the circle.
        CIRCLE_INNER_RADIUS (int): Inner radius for minor chords.
        CIRCLE_TEXT_RADIUS (int): Radius for text labels.
        CIRCLE_INNER_OUTER_RADIUS (int): Inner radius for the inner circle.
    """
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    FONT_SMALL_SIZE = 20
    FONT_LARGE_SIZE = 48
    COLORS = {
        "background": (30, 30, 30),
        "text": (255, 255, 255),
    }
    CIRCLE_CENTER = (400, 360)
    CIRCLE_RADIUS = 200
    CIRCLE_INNER_RADIUS = 125
    CIRCLE_TEXT_RADIUS = 160
    CIRCLE_INNER_OUTER_RADIUS = 40