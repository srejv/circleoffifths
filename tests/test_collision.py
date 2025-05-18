import unittest
from core.collision import is_inside_circle, get_chord_index

class TestCollision(unittest.TestCase):
    def test_is_inside_circle_true(self):
        center = (100, 100)
        radius = 50
        point_inside = (120, 120)
        self.assertTrue(is_inside_circle(center, radius, point_inside))

    def test_is_inside_circle_false(self):
        center = (100, 100)
        radius = 30
        point_outside = (200, 200)
        self.assertFalse(is_inside_circle(center, radius, point_outside))

    def test_is_inside_circle_on_edge(self):
        center = (0, 0)
        radius = 10
        point_on_edge = (10, 0)
        self.assertTrue(is_inside_circle(center, radius, point_on_edge))

    def test_get_chord_index_top(self):
        center = (100, 100)
        # Point directly above center (should be index 0)
        point = (100, 0)
        idx = get_chord_index(center, point)
        self.assertIsInstance(idx, int)
        self.assertGreaterEqual(idx, 0)
        self.assertLess(idx, 12)

    def test_get_chord_index_various(self):
        center = (0, 0)
        radius = 100
        # Test 12 points around the circle
        for i in range(12):
            angle_deg = i * 30 - 90  # -90 so 0 is at the top
            import math
            x = center[0] + radius * math.cos(math.radians(angle_deg))
            y = center[1] + radius * math.sin(math.radians(angle_deg))
            idx = get_chord_index(center, (int(x), int(y)))
            self.assertEqual(idx, i)

if __name__ == "__main__":
    unittest.main()