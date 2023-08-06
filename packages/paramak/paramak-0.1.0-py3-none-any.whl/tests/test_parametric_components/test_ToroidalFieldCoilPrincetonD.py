
import unittest

import paramak
import pytest


class test_ToroidalFieldCoilPrincetonD(unittest.TestCase):
    def test_ToroidalFieldCoilPrincetonD_creation_with_inner_leg(self):
        """creates a tf coil with inner leg using the ToroidalFieldCoilPrincetonD
        parametric component and checks that a cadquery solid is created"""

        test_shape = paramak.ToroidalFieldCoilPrincetonD(
            R1=100,
            R2=300,
            thickness=50,
            distance=50,
            number_of_coils=1,
            with_inner_leg=True
        )
        assert test_shape.solid is not None
        assert test_shape.volume > 1000
        assert test_shape.inner_leg_connection_points is not None

        test_inner_leg = paramak.ExtrudeStraightShape(
            points=test_shape.inner_leg_connection_points, distance=50
        )
        assert test_inner_leg.solid is not None

    def test_ToroidalFieldCoilPrincetonD_creation_no_inner_leg(self):
        """creates a tf coil with no inner leg using the ToroidalFieldCoilPrincetonD
        parametric component and checks that a cadquery solid is created"""

        test_shape_1 = paramak.ToroidalFieldCoilPrincetonD(
            R1=100, R2=300, thickness=50, distance=50, number_of_coils=1,
            with_inner_leg=True
        )
        test_volume_1 = test_shape_1.volume

        test_inner_leg = paramak.ExtrudeStraightShape(
            points=test_shape_1.inner_leg_connection_points, distance=50,
        )
        inner_leg_volume = test_inner_leg.volume

        test_shape_2 = paramak.ToroidalFieldCoilPrincetonD(
            R1=100, R2=300, thickness=50, distance=50, number_of_coils=1,
            with_inner_leg=False
        )

        assert test_shape_2.solid is not None
        assert test_shape_2.volume < test_volume_1

    def test_ToroidalFieldCoilPrincetonD_relative_volume(self):
        """creates tf coil shapes with different numbers of tf coils and checks that
        their relative volumes are correct"""

        test_shape_1 = paramak.ToroidalFieldCoilPrincetonD(
            R1=100, R2=300, thickness=50, distance=30, number_of_coils=4,
            with_inner_leg=True
        )
        test_volume_1 = test_shape_1.volume

        test_shape_2 = paramak.ToroidalFieldCoilPrincetonD(
            R1=100, R2=300, thickness=50, distance=30, number_of_coils=8,
            with_inner_leg=True
        )
        assert test_shape_2.volume == pytest.approx(test_volume_1 * 2)

    def test_ToroidalFieldCoilPrincetonD_rotation_angle(self):
        """Creates a tf coil with a rotation_angle < 360 degrees and checks
        that the correct cut is performed and the volume is correct."""

        test_shape = paramak.ToroidalFieldCoilPrincetonD(
            R1=50,
            R2=150,
            thickness=30,
            distance=30,
            number_of_coils=8,
        )

        test_shape.rotation_angle = 360
        test_shape.workplane = "XZ"
        test_volume = test_shape.volume
        test_shape.rotation_angle = 180
        assert test_shape.volume == pytest.approx(test_volume * 0.5, rel=0.01)

        test_shape.rotation_angle = 360
        test_shape.workplane = "YZ"
        test_volume = test_shape.volume
        test_shape.rotation_angle = 180
        assert test_shape.volume == pytest.approx(test_volume * 0.5, rel=0.01)

        # this test will remain commented until workplane issue #308 is resolved
        # currently causes terminal to crash due to large number of unions
        # test_shape.rotation_angle = 360
        # test_shape.workplane = "XY"
        # test_volume = test_shape.volume
        # test_shape.rotation_angle = 180
        # assert test_shape.volume == pytest.approx(test_volume * 0.5)
