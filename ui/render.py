import pygame
import math
import colorsys
from typing import List, Tuple

from core.circle import ChordType

def hsv_color(i: int, total: int, selected: bool = False) -> Tuple[int, int, int]:
    """
    Generates an RGB color using HSV for smooth variation.

    Args:
        i (int): The index of the segment.
        total (int): Total number of segments.
        selected (bool): Whether the segment is selected (affects saturation).

    Returns:
        Tuple[int, int, int]: The RGB color.
    """
    hue = (i % total) / total
    saturation = 0.7 if selected else 0.3
    value = 1.0 if selected else 0.5
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return (int(r * 255), int(g * 255), int(b * 255))

def polar_to_cartesian(center: Tuple[int, int], angle_deg: float, radius: float) -> Tuple[int, int]:
    """
    Converts polar coordinates to cartesian coordinates.

    Args:
        center (Tuple[int, int]): The center point (x, y).
        angle_deg (float): The angle in degrees.
        radius (float): The radius.

    Returns:
        Tuple[int, int]: The cartesian coordinates (x, y).
    """
    angle_rad = math.radians(angle_deg)
    x = center[0] + radius * math.cos(angle_rad)
    y = center[1] + radius * math.sin(angle_rad)
    return (int(x), int(y))

class CircleOfFifthsDrawable:
    """
    Handles rendering of the Circle of Fifths, including chords, highlights, and labels.
    """

    def __init__(
        self,
        major_chords,
        minor_chords,
        center=(400, 360),
        radius=200,
        inner_radius=125,
        text_radius=160,
        inner_outer_radius=40,
        font=None
    ):
        """
        Initializes the drawable circle with chord lists and font.

        Args:
            major_chords (List): List of major chords.
            minor_chords (List): List of minor chords.
            center (Tuple[int, int], optional): Center of the circle. Defaults to (400, 360).
            radius (int, optional): Outer radius of the circle. Defaults to 200.
            inner_radius (int, optional): Inner radius for minor chords. Defaults to 125.
            text_radius (int, optional): Radius for text labels. Defaults to 160.
            inner_outer_radius (int, optional): Inner radius for the inner circle. Defaults to 40.
            font (pygame.font.Font, optional): Font to use for labels. Defaults to None.
        """
        self.major_chords = major_chords or []
        self.minor_chords = minor_chords or []

        self.WIDTH = 600
        self.HEIGHT = 600

        self.CENTER: Tuple[int, int] = center
        self.RADIUS: int = radius
        self.INNER_RADIUS: int = inner_radius
        self.TEXT_RADIUS: int = text_radius
        self.INNER_OUTER_RADIUS: int = inner_outer_radius
        self.SEGMENTS: int = len(self.major_chords)
        self.FONT = font or pygame.font.SysFont(None, 30)

        self.COLOR_BLACK: Tuple[int, int, int] = (30, 30, 30)
        self.COLOR_WHITE: Tuple[int, int, int] = (220, 220, 220)

        self.segments_polygons: List[List[Tuple[int, int]]] = []
        self.inner_segments_polygons: List[List[Tuple[int, int]]] = []
        self.precalculate_wedges()

    def set_center(self, center: Tuple[int, int]) -> None:
        """
        Set the center of the circle.

        Args:
            center (Tuple[int, int]): (x, y) representing the center of the circle.
        """
        self.CENTER = center
        self.precalculate_wedges()

    def _draw_lines(self, surface: pygame.Surface, item_list: List) -> None:
        """
        Draws the lines and dividers for the circle.

        Args:
            surface (pygame.Surface): The surface to draw on.
            item_list (List): List of items to draw lines for.
        """
        for i, _ in enumerate(item_list):
            angle_deg = -90 + i * 30
            line_deg = angle_deg  - 360/(self.SEGMENTS*2)
            # Divider lines
            line_end = polar_to_cartesian(self.CENTER, line_deg, self.RADIUS)
            line_start = polar_to_cartesian(self.CENTER, line_deg, self.INNER_OUTER_RADIUS)
            pygame.draw.line(surface, (40, 40, 40), line_start, line_end, 2)

    def _draw_text(self, surface: pygame.Surface, note_list: List, radius: int) -> None:
        """
        Draws the text labels for the notes.

        Args:
            surface (pygame.Surface): The surface to draw on.
            note_list (List): List of notes to draw.
            radius (int): Radius for the text position.
        """
        for i, note in enumerate(note_list):
            angle_deg = -90 + i * 30
            text_pos = polar_to_cartesian(self.CENTER, angle_deg, radius)
            text = self.FONT.render(note.alternative_names[0], True, self.COLOR_BLACK)
            text_rect = text.get_rect(center=text_pos)
            surface.blit(text, text_rect)
    
    def precalculate_wedges(self) -> None:
        """
        Precompute the polygons for the outer and inner wedges.
        """
        self.segments_polygons = []
        self.inner_segments_polygons = []
        for i in range(self.SEGMENTS):
            angle_start = -90 + i * (360 / self.SEGMENTS) - 360/(self.SEGMENTS*2)
            angle_end = angle_start + (360 / self.SEGMENTS)
            # Outer wedge
            poly = self._make_wedge_polygon(angle_start, angle_end, self.RADIUS, self.INNER_RADIUS)
            self.segments_polygons.append(poly)
            # Inner wedge
            poly_inner = self._make_wedge_polygon(angle_start, angle_end, self.INNER_RADIUS, self.INNER_OUTER_RADIUS)
            self.inner_segments_polygons.append(poly_inner)

    def _make_wedge_polygon(
        self, angle_start: float, angle_end: float, outer_radius: float, inner_radius: float
    ) -> List[Tuple[int, int]]:
        """
        Helper to create a wedge polygon point list.

        Args:
            angle_start (float): Starting angle in degrees.
            angle_end (float): Ending angle in degrees.
            outer_radius (float): Outer radius of the wedge.
            inner_radius (float): Inner radius of the wedge.

        Returns:
            List[Tuple[int, int]]: List of (x, y) points for the polygon.
        """
        points = [polar_to_cartesian(self.CENTER, angle_start, inner_radius)]
        for angle in range(int(angle_start), int(angle_end) + 1, 2):
            points.append(polar_to_cartesian(self.CENTER, angle, outer_radius))
        for angle in range(int(angle_end), int(angle_start) - 1, -2):
            points.append(polar_to_cartesian(self.CENTER, angle, inner_radius))
        return points

    def draw_circle(self, surface: pygame.Surface, selected_chord_indices: List[int]) -> None:
        """
        Draws the circle of fifths on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
            selected_chord_indices (List[int]): Indices of selected chords.
        """
        for i, poly in enumerate(self.segments_polygons):
            color = hsv_color(i, self.SEGMENTS, i in selected_chord_indices)
            pygame.draw.polygon(surface, color, poly)
        for i, poly in enumerate(self.inner_segments_polygons):
            color = hsv_color(i-3, self.SEGMENTS, i in selected_chord_indices)
            pygame.draw.polygon(surface, color, poly)

        # Draw the border circle
        pygame.draw.circle(surface, self.COLOR_WHITE, self.CENTER, self.RADIUS+1, 2)
        pygame.draw.circle(surface, self.COLOR_BLACK, self.CENTER, self.INNER_RADIUS+1, 3)
        pygame.draw.circle(surface, self.COLOR_BLACK, self.CENTER, self.INNER_OUTER_RADIUS)
        
        self._draw_lines(surface, self.major_chords)

    def draw_circle_labels(self, surface: pygame.Surface) -> None:
        """
        Draws the labels for the notes and chords on the circle.

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        self._draw_text(surface, self.major_chords, self.TEXT_RADIUS)
        self._draw_text(surface, self.minor_chords, self.INNER_RADIUS - 30)
    
    def draw_highlighted_chord(
        self, surface: pygame.Surface, chord, chord_type: ChordType, blink: bool
    ) -> None:
        """
        Draws the highlighted chord on the circle.

        Args:
            surface (pygame.Surface): The surface to draw on.
            chord: The chord to highlight.
            chord_type (ChordType): The type of chord (major or minor).
            blink (bool): Whether to blink the highlight.
        """
        color = (255, 255, 255, 220) if not blink else (0, 0, 0, 0)
        index = self.major_chords.index(chord) if chord_type == ChordType.MAJOR else self.minor_chords.index(chord)
        polygon_list = self.segments_polygons if chord_type == ChordType.MAJOR else self.inner_segments_polygons
        pygame.draw.polygon(surface, color, polygon_list[index])
