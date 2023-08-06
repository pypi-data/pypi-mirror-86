
import unittest

import paramak
import pytest


class test_BlanketConstantThicknessArcV(unittest.TestCase):
    def test_BlanketConstantThickness_creation(self):
        """Creates a blanket using the BlanketConstantThicknessArcV parametric
        component and checks that a cadquery solid is created."""

        test_shape = paramak.BlanketConstantThicknessArcV(
            inner_lower_point=(300, -200),
            inner_mid_point=(500, 0),
            inner_upper_point=(300, 200),
            thickness=20,
            rotation_angle=180,
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_BlanketConstantThickness_relative_volume(self):
        """creates two blankets using the BlanketConstantThicknessArcV parametric
        component and checks that their relative volumes are correct"""

        # rotation_angle
        test_shape = paramak.BlanketConstantThicknessArcV(
            inner_lower_point=(300, -200),
            inner_mid_point=(500, 0),
            inner_upper_point=(300, 200),
            thickness=20,
            rotation_angle=360,
        )
        test_shape_volume = test_shape.volume

        test_shape.rotation_angle = 180
        assert test_shape.volume == pytest.approx(test_shape_volume * 0.5)

    def test_BlanketConstantThickness_faces(self):
        """creates a blanket using the BlanketConstantThicknessArcV parametric
        component and checks that a solid with the correct number of faces is produced"""

        test_shape = paramak.BlanketConstantThicknessArcV(
            inner_lower_point=(300, -200),
            inner_mid_point=(500, 0),
            inner_upper_point=(300, 200),
            thickness=20,
            rotation_angle=360,
        )
        assert len(test_shape.areas) == 4
        assert len(set(test_shape.areas)) == 3

        test_shape.rotation_angle = 180
        assert len(test_shape.areas) == 6
        assert len(set(test_shape.areas)) == 4
