
import math
import unittest

import paramak
import pytest


class test_PoloidalFieldCoilSet(unittest.TestCase):

    def test_PoloidalFieldCoilSet_creation(self):
        """Creates a solid using the PoloidalFieldCoilSet parametric component
        and checks that a cadquery solid is created."""

        test_shape = paramak.PoloidalFieldCoilSet(heights=[10, 10, 10],
                                                  widths=[20, 20, 20],
                                                  center_points=[(100, 100),
                                                                 (200, 200),
                                                                 (300, 300)])
        assert test_shape.solid is not None
        assert len(test_shape.solid.Solids()) == 3

    def test_PoloidalFieldCoilSet_absolute_volume(self):
        """Creates a set of pf coils using the PoloidalFieldCoilSet parametric
        component and checks that the volume is correct"""

        test_shape = paramak.PoloidalFieldCoilSet(
            heights=[10, 15, 5],
            widths=[20, 25, 30],
            center_points=[(100, 100), (200, 200), (300, 300)]
        )

        assert test_shape.volume == (pytest.approx((10 * 20 * math.pi * (2 * 100)) + (
            15 * 25 * math.pi * (2 * 200)) + (5 * 30 * math.pi * (2 * 300))))

    def test_PoloidalFieldCoilSet_absolute_areas(self):
        """Creates a set of pf coils using the PoloidalFieldCoilSet parametric
        component and checks that the areas of its faces are correct"""

        test_shape = paramak.PoloidalFieldCoilSet(
            heights=[10, 15, 5],
            widths=[20, 25, 30],
            center_points=[(100, 100), (200, 200), (300, 300)]
        )

        assert len(test_shape.areas) == 12
        # assert len(set(test_shape.areas)) == 9
        assert test_shape.areas.count(
            pytest.approx(20 * math.pi * (2 * 100))) == 2
        assert test_shape.areas.count(
            pytest.approx(25 * math.pi * (2 * 200))) == 2
        assert test_shape.areas.count(
            pytest.approx(30 * math.pi * (2 * 300))) == 2
        assert test_shape.areas.count(
            pytest.approx(10 * math.pi * (2 * 90))) == 1
        assert test_shape.areas.count(
            pytest.approx(10 * math.pi * (2 * 110))) == 1
        assert test_shape.areas.count(
            pytest.approx(15 * math.pi * (2 * 187.5))) == 1
        assert test_shape.areas.count(
            pytest.approx(15 * math.pi * (2 * 212.5))) == 1
        assert test_shape.areas.count(
            pytest.approx(5 * math.pi * (2 * 285))) == 1
        assert test_shape.areas.count(
            pytest.approx(5 * math.pi * (2 * 315))) == 1

    def test_PoloidalFieldCoilSet_incorrect_args(self):
        """Creates a solid using the PoloidalFieldCoilSet parametric component
        and checks that a cadquery solid is created."""

        def test_PoloidalFieldCoilSet_incorrect_height():
            """Checks PoloidalFieldCoilSet with height as the wrong type."""

            paramak.PoloidalFieldCoilSet(
                heights=10, widths=[
                    20, 20, 20], center_points=[
                    (100, 100), (200, 200), (300, 300)])

        self.assertRaises(
            ValueError,
            test_PoloidalFieldCoilSet_incorrect_height)

        def test_PoloidalFieldCoilSet_incorrect_width():
            """Checks PoloidalFieldCoilSet with width as the wrong type."""

            paramak.PoloidalFieldCoilSet(
                heights=[
                    10, 10, 10], widths=20, center_points=[
                    (100, 100), (200, 200), (300, 300)])

        self.assertRaises(
            ValueError,
            test_PoloidalFieldCoilSet_incorrect_width)

        def test_PoloidalFieldCoilSet_incorrect_center_points():
            """Checks PoloidalFieldCoilSet with center_points as the wrong
            type."""

            paramak.PoloidalFieldCoilSet(heights=[10, 10, 10],
                                         widths=[20, 20, 20],
                                         center_points=100)

        self.assertRaises(
            ValueError,
            test_PoloidalFieldCoilSet_incorrect_center_points)

        def test_PoloidalFieldCoilSet_incorrect_width_length():
            """Checks PoloidalFieldCoilSet with not enough entries in width."""
            paramak.PoloidalFieldCoilSet(
                heights=[
                    10, 10, 10], widths=[
                    20, 20], center_points=[
                    (100, 100), (200, 200), (300, 300)])

        self.assertRaises(
            ValueError,
            test_PoloidalFieldCoilSet_incorrect_width_length)
