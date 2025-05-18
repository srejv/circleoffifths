from typing import Tuple
import math

def is_inside_circle(center: Tuple[int, int], radius: int, point: Tuple[int, int]) -> bool:
    """
    Determine if a point is inside a given circle.

    Args:
        center (Tuple[int, int]): The (x, y) coordinates of the circle's center.
        radius (int): The radius of the circle.
        point (Tuple[int, int]): The (x, y) coordinates of the point to check.

    Returns:
        bool: True if the point is inside the circle, False otherwise.
    """
    x, y = point
    return (x - center[0])**2 + (y - center[1])**2 <= radius**2

def get_chord_index(center: Tuple[int, int], point: Tuple[int, int]) -> int:
    """
    Calculate the index of the chord segment at the given point in the circle.

    Args:
        center (Tuple[int, int]): The (x, y) coordinates of the circle's center.
        point (Tuple[int, int]): The (x, y) coordinates of the point to check.

    Returns:
        int: The index of the chord segment (0-11).
    """
    SEGMENTS = 12
    x, y = point
    segment_size = 360 / SEGMENTS
    angle = math.degrees(math.atan2(y - center[1], x - center[0])) % 360
    angle = angle + 90 + segment_size / 2
    if angle < 0:
        angle += 360
    if angle > 360:
        angle -= 360

    index = int(angle // segment_size)
    return index