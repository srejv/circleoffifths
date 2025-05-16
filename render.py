import pygame
import math
import colorsys

from circle import ChordType

# Color generator using HSV for smooth variation
def hsv_color(i, total):
    hue = i / total
    r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))

# Convert polar coordinates to cartesian
def polar_to_cartesian(center, angle_deg, radius):
    angle_rad = math.radians(angle_deg)
    x = center[0] + radius * math.cos(angle_rad)
    y = center[1] + radius * math.sin(angle_rad)
    return (int(x), int(y))

class CircleOfFifthsDrawable:
    def __init__(self, majorChords=None, minorChords=None, font=None):

        self.majorChords = majorChords or []
        self.minorChords = minorChords or []

        self.WIDTH = 600
        self.HEIGHT = 600

        self.FONT = font or pygame.font.SysFont(None, 30)

        # Constants
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)
        self.RADIUS = 200
        self.INNER_RADIUS = 125
        self.TEXT_RADIUS = 160
        self.INNER_OUTER_RADIUS = 40
        self.SEGMENTS = len(self.majorChords)

        self.COLOR_BLACK = (30, 30, 30)
        self.COLOR_WHITE = (220, 220, 220)

    def set_center(self, center):
        """
        Set the center of the circle.
        :param center: Tuple (x, y) representing the center of the circle.
        """
        self.CENTER = center

    def _draw_segment(self, surface, angle_start, angle_end, color, outer_radius, inner_radius):
        """
        Draws a segment of the circle between two angles.
        :param surface: The surface to draw on.
        :param angle_start: Starting angle in degrees.
        :param angle_end: Ending angle in degrees.
        :param color: Color of the segment.
        :param outer_radius: Outer radius of the segment.
        :param inner_radius: Inner radius of the segment.
        """
        # Create a wedge as a polygon
        # TODO: Could precalculate the polygons because they are static
        points = [polar_to_cartesian(self.CENTER, angle_start, inner_radius)]
        for angle in range(int(angle_start), int(angle_end) + 1, 2):  # Outer arc
            points.append(polar_to_cartesian(self.CENTER, angle, outer_radius))
        for angle in range(int(angle_end), int(angle_start) - 1, -2):  # Inner arc (reversed)
            points.append(polar_to_cartesian(self.CENTER, angle, inner_radius))
        pygame.draw.polygon(surface, color, points)

    def _draw_segments(self, surface, outer_radius, inner_radius, alt=0):
        """
        Draws the segments of the circle.
        :param surface: The surface to draw on.
        :param outer_radius: Outer radius of the segments.
        :param inner_radius: Inner radius of the segments.
        :param alt: Offset for the color hue.
        """
        for i in range(self.SEGMENTS):
            angle_start = -90 + i * (360 / self.SEGMENTS) - 360/(self.SEGMENTS*2)
            angle_end = angle_start + (360 / self.SEGMENTS)
            color = hsv_color(i-alt, self.SEGMENTS)

            # Create a wedge as a polygon
            self._draw_segment(surface, angle_start, angle_end, color, outer_radius, inner_radius)

    def _draw_lines(self, surface, item_list):
        """
        Draws the lines and dividers for the circle.
        :param surface: The surface to draw on.
        :param item_list: List of items to draw lines for.
        """
        for i, _ in enumerate(item_list):
            angle_deg = -90 + i * 30
            line_deg = angle_deg  - 360/(self.SEGMENTS*2)
            # Divider lines
            line_end = polar_to_cartesian(self.CENTER, line_deg, self.RADIUS)
            line_start = polar_to_cartesian(self.CENTER, line_deg, self.INNER_OUTER_RADIUS)
            pygame.draw.line(surface, (40, 40, 40), line_start, line_end, 2)

    def _draw_text(self, surface, note_list, radius):
        """
        Draws the text labels for the notes.
        :param surface: The surface to draw on.
        :param note_list: List of notes to draw.
        :param radius: Radius for the text position.
        """
        # Draw lines and text
        for i, note in enumerate(note_list):
            angle_deg = -90 + i * 30

            # Text label
            text_pos = polar_to_cartesian(self.CENTER, angle_deg, radius)
            text = self.FONT.render(note.alternative_names[0], True, self.COLOR_BLACK)
            text_rect = text.get_rect(center=text_pos)
            surface.blit(text, text_rect)

    def draw_circle(self, surface):
        """
        Draws the circle of fifths on the given surface.
        :param surface: The surface to draw on.
        """
        self._draw_segments(surface, self.RADIUS, self.INNER_RADIUS)
        self._draw_segments(surface, self.INNER_RADIUS, self.INNER_OUTER_RADIUS, alt=-3)

        # Draw the border circle
        pygame.draw.circle(surface, self.COLOR_WHITE, self.CENTER, self.RADIUS+1, 2)
        pygame.draw.circle(surface, self.COLOR_BLACK, self.CENTER, self.INNER_RADIUS+1, 3)
        pygame.draw.circle(surface, self.COLOR_BLACK, self.CENTER, self.INNER_OUTER_RADIUS)
        
        self._draw_lines(surface, self.majorChords)

    def draw_circle_labels(self, surface):
        """
        Draws the labels for the notes and chords on the circle.
        :param surface: The surface to draw on.
        """
        self._draw_text(surface, self.majorChords, self.TEXT_RADIUS)
        self._draw_text(surface, self.minorChords, self.INNER_RADIUS - 30)
    
    def draw_highlighted_chord(self, surface, chord, chord_type, blink):
        """
        Draws the highlighted chord on the circle.
        :param surface: The surface to draw on.
        :param chord: The chord to highlight.
        :param chord_type: The type of chord (major or minor).
        """
        index = 0
        inner_radius = self.INNER_RADIUS
        outer_radius = self.RADIUS
        color = (255, 255, 255, 220)
        if blink:
            color = (0, 0, 0, 0)

        if chord_type == ChordType.MAJOR:
            index = self.majorChords.index(chord)
        else:
            index = self.minorChords.index(chord)
            inner_radius = self.INNER_OUTER_RADIUS
            outer_radius = self.INNER_RADIUS

        angle_start = -90 + index * (360 / self.SEGMENTS) - 360/(self.SEGMENTS*2) + 1
        angle_end = angle_start + (360 / self.SEGMENTS) - 1

        self._draw_segment(surface, angle_start, angle_end, color, outer_radius - 2, inner_radius + 2)
