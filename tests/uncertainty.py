import math
import unittest

import pytest

from wurst import rescale_exchange


class TestRescaleExchange(unittest.TestCase):
    def test_rescale_exchange_wrong_inputs(self):
        with self.assertRaises(AssertionError):
            rescale_exchange([], 4)
        with self.assertRaises(AssertionError):
            rescale_exchange({}, "four")

    def test_rescale_exchange(self):
        given = {"amount": 2, "foo": "bar", "minimum": 7, "uncertainty type": -1}
        expected = {"amount": 1, "loc": 1, "foo": "bar", "uncertainty type": 0}
        assert rescale_exchange(given, 0.5) == expected

    def test_rescale_no_uncertainty(self):
        exc = {"amount": 100, "uncertainty type": 0}
        scaled_exc = rescale_exchange(exc, 2, remove_uncertainty=False)
        self.assertEqual(scaled_exc["amount"], 200)
        self.assertEqual(scaled_exc["uncertainty type"], 0)

    def test_rescale_lognormal(self):
        exc = {"amount": 100, "uncertainty type": 2, "loc": 2, "scale": 0.5}
        scaled_exc = rescale_exchange(exc, 2, remove_uncertainty=False)
        self.assertEqual(scaled_exc["amount"], 200)
        self.assertEqual(scaled_exc["uncertainty type"], 2)
        self.assertAlmostEqual(scaled_exc["loc"], 2 + math.log(2), places=5)
        self.assertEqual(scaled_exc["scale"], 0.5)

    def test_rescale_normal(self):
        exc = {"amount": 100, "uncertainty type": 3, "loc": 100, "scale": 10}
        scaled_exc = rescale_exchange(exc, 2, remove_uncertainty=False)
        self.assertEqual(scaled_exc["amount"], 200)
        self.assertEqual(scaled_exc["uncertainty type"], 3)
        self.assertEqual(scaled_exc["loc"], 200)
        self.assertEqual(scaled_exc["scale"], 20)

    def test_remove_uncertainty(self):
        exc = {"amount": 100, "uncertainty type": 3, "loc": 100, "scale": 10}
        scaled_exc = rescale_exchange(exc, 2)
        self.assertEqual(scaled_exc["amount"], 200)
        self.assertEqual(scaled_exc["uncertainty type"], 0)
        self.assertNotIn("scale", scaled_exc)
        self.assertEqual(scaled_exc["loc"], 200)

    def test_scale_with_negative_factor(self):
        exc = {"amount": 100, "uncertainty type": 3, "loc": 100, "scale": 10}
        scaled_exc = rescale_exchange(exc, -2, remove_uncertainty=False)
        self.assertEqual(scaled_exc["amount"], -200)
        self.assertEqual(scaled_exc["uncertainty type"], 3)
        self.assertEqual(scaled_exc["loc"], -200)
        self.assertEqual(scaled_exc["scale"], 20)


if __name__ == "__main__":
    unittest.main()
