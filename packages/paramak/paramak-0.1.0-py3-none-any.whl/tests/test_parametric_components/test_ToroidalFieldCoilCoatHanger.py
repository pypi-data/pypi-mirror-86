
import unittest

import paramak
import pytest


class test_ToroidalFieldCoilCoatHanger(unittest.TestCase):
    def test_ToroidalFieldCoilCoatHanger_creation_with_inner_leg(self):
        """creates a tf coil with inner leg using the ToroidalFieldCoilCoatHanger
        parametric component and checks that a cadquery solid is created"""

        test_shape = paramak.ToroidalFieldCoilCoatHanger(
            horizontal_start_point=(200, 500),
            horizontal_length=400,
            vertical_mid_point=(700, 0),
            vertical_length=500,
            thickness=50,
            distance=50,
            number_of_coils=1,
            with_inner_leg=True,
        )
        assert test_shape.solid is not None
        assert test_shape.volume > 1000
        assert test_shape.inner_leg_connection_points is not None

        test_inner_leg = paramak.ExtrudeStraightShape(
            points=test_shape.inner_leg_connection_points, distance=50
        )
        assert test_inner_leg.solid is not None

    def test_ToroidalFieldCoilCoatHanger_creation_no_inner_leg(self):
        """creates a tf coil with no inner leg using the ToroidalFieldCoilRectangle
        parametric component and checks that a cadquery solid is created"""

        test_shape_1 = paramak.ToroidalFieldCoilCoatHanger(
            horizontal_start_point=(200, 500), horizontal_length=400,
            vertical_mid_point=(700, 0), vertical_length=500, thickness=50,
            distance=50, number_of_coils=1, with_inner_leg=True,
        )
        test_volume_1 = test_shape_1.volume

        test_inner_leg = paramak.ExtrudeStraightShape(
            points=test_shape_1.inner_leg_connection_points, distance=50
        )
        inner_leg_volume = test_inner_leg.volume

        test_shape_2 = paramak.ToroidalFieldCoilCoatHanger(
            horizontal_start_point=(200, 500), horizontal_length=400,
            vertical_mid_point=(700, 0), vertical_length=500, thickness=50,
            distance=50, number_of_coils=1, with_inner_leg=False,
        )
        assert test_shape_2.solid is not None
        assert test_shape_2.volume == pytest.approx(
            test_volume_1 - inner_leg_volume)

    def test_ToroidalFieldCoilCoatHanger_absolute_volume(self):
        """creates a tf coil using the ToroidalFieldCoilCoatHanger parametric
        component and checks that the volume is correct"""

        test_shape = paramak.ToroidalFieldCoilCoatHanger(
            horizontal_start_point=(200, 500),
            horizontal_length=400,
            vertical_mid_point=(700, 0),
            vertical_length=500,
            thickness=50,
            distance=30,
            number_of_coils=1,
        )

        assert test_shape.volume == pytest.approx((400 * 50 * 30 * 2) +
                                                  ((50 * 50 * 30 / 2) * 2) + (50 * 500 * 30) +
                                                  (((150 * 250 * 30) - (((100 * 250) / 2) * 30) -
                                                    (((100 * 250) / 2) * 30)) * 2) + (50 * 1000 * 30), rel=0.1)

        test_shape.with_inner_leg = False
        assert test_shape.volume == pytest.approx((400 * 50 * 30 * 2) +
                                                  ((50 * 50 * 30 / 2) * 2) +
                                                  (50 * 500 * 30) + (((150 * 250 * 30) -
                                                                      (((100 * 250) / 2) * 30) -
                                                                      (((100 * 250) / 2) * 30)) * 2), rel=0.1)

        test_shape.with_inner_leg = True
        test_shape.number_of_coils = 8
        assert test_shape.volume == pytest.approx(((400 * 50 * 30 * 2) +
                                                   ((50 * 50 * 30 / 2) * 2) + (50 * 500 * 30) +
                                                   (((150 * 250 * 30) - (((100 * 250) / 2) * 30) -
                                                     (((100 * 250) / 2) * 30)) * 2) + (50 * 1000 * 30)) * 8, rel=0.1)

        test_shape.with_inner_leg = False
        assert test_shape.volume == pytest.approx(((400 * 50 * 30 * 2) +
                                                   ((50 * 50 * 30 / 2) * 2) + (50 * 500 * 30) +
                                                   (((150 * 250 * 30) - (((100 * 250) / 2) * 30) -
                                                     (((100 * 250) / 2) * 30)) * 2)) * 8, rel=0.1)

    def test_ToroidalFieldCoilCoatHanger_absolute_area(self):
        """creates a tf coil using the ToroidalFieldCoilCoatHanger parametric
        component and checks that the areas of the faces are correct"""

        test_shape = paramak.ToroidalFieldCoilCoatHanger(
            horizontal_start_point=(200, 500),
            horizontal_length=400,
            vertical_mid_point=(700, 0),
            vertical_length=500,
            thickness=50,
            distance=30,
            number_of_coils=1,
        )

        assert test_shape.area == pytest.approx((((400 * 50 * 2) +
                                                  (50 * 50 * 0.5 * 2) + (((150 * 250) - (100 * 250 * 0.5) -
                                                                          (100 * 250 * 0.5)) * 2) + (500 * 50)) * 2) +
                                                ((50 * 30) * 4) + ((400 * 30) * 4) + ((500 * 30) * 2) +
                                                ((((50**2 + 50**2)**0.5) * 30) * 2) +
                                                ((((100**2 + 250**2)**0.5) * 30) * 4) + ((50 * 1000) * 2) +
                                                ((1000 * 30) * 2), rel=0.1)
        assert len(test_shape.areas) == 24

        assert test_shape.areas.count(pytest.approx(50 * 30)) == 4
        assert test_shape.areas.count(pytest.approx(400 * 30)) == 4
        assert test_shape.areas.count(pytest.approx(500 * 30)) == 2
        assert test_shape.areas.count(
            pytest.approx(
                ((100**2 + 250**2)**0.5) * 30)) == 4
        assert test_shape.areas.count(pytest.approx(50 * 1000)) == 2
        assert test_shape.areas.count(pytest.approx(1000 * 30)) == 2

        test_shape.with_inner_leg = False
        assert test_shape.area == pytest.approx((((400 * 50 * 2) +
                                                  (50 * 50 * 0.5 * 2) + (((150 * 250) - (100 * 250 * 0.5) -
                                                                          (100 * 250 * 0.5)) * 2) + (500 * 50)) * 2) + ((50 * 30) * 2) +
                                                ((400 * 30) * 4) + ((500 * 30) * 2) +
                                                ((((50**2 + 50**2)**0.5) * 30) * 2) +
                                                ((((100**2 + 250**2)**0.5) * 30) * 4), rel=0.1)

    def test_ToroidalFieldCoilCoatHanger_rotation_angle(self):
        """Creates a tf coil with a rotation_angle < 360 degrees and checks
        that the correct cut is performed and the volume is correct."""

        test_shape = paramak.ToroidalFieldCoilCoatHanger(
            horizontal_start_point=(200, 500),
            horizontal_length=400,
            vertical_mid_point=(700, 0),
            vertical_length=500,
            thickness=50,
            distance=50,
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
