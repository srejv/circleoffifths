import unittest
from core.blink_manager import BlinkManager

class TestBlinkManager(unittest.TestCase):
    def test_initial_state(self):
        bm = BlinkManager(interval=5)
        self.assertFalse(bm.blink)
        self.assertEqual(bm.counter, 0)

    def test_update_no_toggle(self):
        bm = BlinkManager(interval=3)
        # Should not toggle until interval is exceeded
        for _ in range(3):
            self.assertFalse(bm.update())
        # Next update should toggle
        self.assertTrue(bm.update())
        self.assertTrue(bm.blink)
        self.assertEqual(bm.counter, 0)

    def test_update_toggle_multiple_times(self):
        bm = BlinkManager(interval=2)
        toggles = 0
        for i in range(10):
            if bm.update():
                toggles += 1
        # Should toggle every (interval+1) updates
        self.assertEqual(toggles, 3)
        self.assertEqual(bm.counter, 1)

    def test_reset(self):
        bm = BlinkManager(interval=2)
        for _ in range(3):
            bm.update()
        bm.reset()
        self.assertFalse(bm.blink)
        self.assertEqual(bm.counter, 0)

    def test_is_blinking(self):
        bm = BlinkManager(interval=1)
        self.assertFalse(bm.is_blinking())
        bm.update()  # Should not toggle yet
        self.assertFalse(bm.is_blinking())
        bm.update()  # Should toggle now
        self.assertTrue(bm.is_blinking())

if __name__ == "__main__":
    unittest.main()