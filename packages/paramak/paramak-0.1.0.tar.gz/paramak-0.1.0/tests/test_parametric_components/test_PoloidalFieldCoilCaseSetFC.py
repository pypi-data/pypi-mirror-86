
import math
import unittest

import paramak
import pytest


class test_PoloidalFieldCoilCaseSetFC(unittest.TestCase):
    def test_PoloidalFieldCoilCaseSetFC_from_pf_coil_set(self):
        """Creates a set of PF coil cases from a PF coils object."""

        pf_coils_set = paramak.PoloidalFieldCoilSet(
            heights=[10, 10, 20, 20],
            widths=[10, 10, 20, 40],
            center_points=[
                (100, 100),
                (100, 150),
                (50, 200),
                (50, 50)
            ],
            rotation_angle=180
        )

        test_shape = paramak.PoloidalFieldCoilCaseSetFC(
            pf_coils=pf_coils_set,
            casing_thicknesses=[5, 5, 10, 10],
            rotation_angle=180
        )

        assert test_shape.solid is not None
        assert len(test_shape.solid.Solids()) == 4
        assert len(pf_coils_set.solid.Solids()) == 4

    def test_PoloidalFieldCoilCaseSetFC_with_zero_thickness(self):
        """Creates a set of PF coil cases from a PF coils object and sets one
        of the casing thicknesses to 0"""

        pf_coils_set = paramak.PoloidalFieldCoilSet(
            heights=[10, 10, 20, 20],
            widths=[10, 10, 20, 40],
            center_points=[
                (100, 100),
                (100, 150),
                (50, 200),
                (50, 50)
            ],
            rotation_angle=180
        )

        test_shape = paramak.PoloidalFieldCoilCaseSetFC(
            pf_coils=pf_coils_set,
            casing_thicknesses=[5, 5, 0, 10],
            rotation_angle=180
        )

        assert test_shape.solid is not None
        assert len(test_shape.solid.Solids()) == 3
        assert len(pf_coils_set.solid.Solids()) == 4

    def test_PoloidalFieldCoilCaseSetFC_from_pf_coil_set_absolute_volume(self):
        """Creates a set of pf coil cases from a pf coil set object and checks
        that the volume is correct"""

        pf_coils_set = paramak.PoloidalFieldCoilSet(
            heights=[10, 10, 20, 20],
            widths=[10, 10, 20, 40],
            center_points=[
                (100, 100),
                (100, 150),
                (50, 200),
                (50, 50)
            ],
        )

        test_shape = paramak.PoloidalFieldCoilCaseSetFC(
            pf_coils=pf_coils_set,
            casing_thicknesses=[5, 10, 5, 10],
        )

        assert test_shape.volume == pytest.approx((((20 * 5 * 2) + (10 * 5 * 2)) * math.pi * 2 * 100) + (((30 * 10 * 2) + (
            10 * 10 * 2)) * math.pi * 2 * 100) + (((30 * 5 * 2) + (20 * 5 * 2)) * math.pi * 2 * 50) + (((60 * 10 * 2) + (20 * 10 * 2)) * math.pi * 2 * 50))

    def test_PoloidalFieldCoilCaseSetFC_from_pf_coil_set_absolute_areas(self):
        """Creates a set of pf coil cases from a pf coil set object and checks
        that the areas are correct"""

        pf_coils_set = paramak.PoloidalFieldCoilSet(
            heights=[10, 10, 20, 20],
            widths=[10, 10, 20, 40],
            center_points=[
                (100, 100),
                (100, 150),
                (50, 200),
                (50, 50)
            ],
        )

        test_shape = paramak.PoloidalFieldCoilCaseSetFC(
            pf_coils=pf_coils_set,
            casing_thicknesses=[5, 10, 5, 10],
        )

        assert len(test_shape.areas) == 32
        # assert len(set(test_shape.areas)) == 16
        assert test_shape.areas.count(
            pytest.approx(10 * math.pi * 2 * 100)) == 6
        assert test_shape.areas.count(
            pytest.approx(40 * math.pi * 2 * 50)) == 4
        assert test_shape.areas.count(
            pytest.approx(30 * math.pi * 2 * 100)) == 4
        assert test_shape.areas.count(
            pytest.approx(30 * math.pi * 2 * 50)) == 2
        assert test_shape.areas.count(
            pytest.approx(10 * math.pi * 2 * 105)) == 3
        assert test_shape.areas.count(
            pytest.approx(10 * math.pi * 2 * 95)) == 2
        assert test_shape.areas.count(
            pytest.approx(20 * math.pi * 2 * 110)) == 1
        assert test_shape.areas.count(
            pytest.approx(20 * math.pi * 2 * 90)) == 1
        assert test_shape.areas.count(
            pytest.approx(30 * math.pi * 2 * 115)) == 1
        assert test_shape.areas.count(
            pytest.approx(30 * math.pi * 2 * 85)) == 1
        assert test_shape.areas.count(
            pytest.approx(20 * math.pi * 2 * 60)) == 1
        assert test_shape.areas.count(
            pytest.approx(20 * math.pi * 2 * 40)) == 2
        assert test_shape.areas.count(
            pytest.approx(30 * math.pi * 2 * 65)) == 1
        assert test_shape.areas.count(
            pytest.approx(20 * math.pi * 2 * 70)) == 1
        assert test_shape.areas.count(
            pytest.approx(20 * math.pi * 2 * 30)) == 1
        assert test_shape.areas.count(
            pytest.approx(40 * math.pi * 2 * 80)) == 1

    def test_PoloidalFieldCoilCaseSetFC_incorrect_args(self):
        """Creates a solid using the PoloidalFieldCoilCaseSet with incorrect
        args"""

        def test_PoloidalFieldCoilSet_incorrect_lengths_FC():
            """Checks PoloidalFieldCoilSet with the wrong number of casing
            thicknesses (3) using a coil set object with 4 pf_coils."""

            pf_coils_set = paramak.PoloidalFieldCoilSet(
                heights=[10, 10, 20, 20],
                widths=[10, 10, 20, 40],
                center_points=[(100, 100),
                               (100, 150),
                               (50, 200),
                               (50, 50)],
                rotation_angle=180)

            paramak.PoloidalFieldCoilCaseSetFC(
                pf_coils=pf_coils_set, casing_thicknesses=[
                    5, 5, 10], rotation_angle=180).solid

        self.assertRaises(
            ValueError,
            test_PoloidalFieldCoilSet_incorrect_lengths_FC)

        def test_PoloidalFieldCoilSet_incorrect_lengths():
            """Checks PoloidalFieldCoilSet with the wrong number of casing
            thicknesses using a list."""

            pf_coils_1 = paramak.PoloidalFieldCoil(
                height=10,
                width=10,
                center_point=(100, 100),
                rotation_angle=180)

            paramak.PoloidalFieldCoilCaseSetFC(
                pf_coils=[pf_coils_1],
                casing_thicknesses=[5, 5, 10, 10],
                rotation_angle=180).solid

        self.assertRaises(
            ValueError,
            test_PoloidalFieldCoilSet_incorrect_lengths)

        def test_PoloidalFieldCoilSet_incorrect_pf_coil():
            """Checks PoloidalFieldCoilSet with the pf_coils as an incorrect
            entry."""

            paramak.PoloidalFieldCoilCaseSetFC(
                pf_coils=20,
                casing_thicknesses=[5, 5, 10, 10],
                rotation_angle=180).solid

        self.assertRaises(
            ValueError,
            test_PoloidalFieldCoilSet_incorrect_pf_coil)

    def test_PoloidalFieldCoilCaseSetFC_from_list(self):
        """Creates a set of PF coil cases from a list of PF coils with a list
        of thicknesses"""

        pf_coils_1 = paramak.PoloidalFieldCoil(height=10,
                                               width=10,
                                               center_point=(100, 100),
                                               rotation_angle=180)

        pf_coils_2 = paramak.PoloidalFieldCoil(height=10,
                                               width=10,
                                               center_point=(100, 150),
                                               rotation_angle=180)

        pf_coils_3 = paramak.PoloidalFieldCoil(height=20,
                                               width=20,
                                               center_point=(50, 200),
                                               rotation_angle=180)

        pf_coils_4 = paramak.PoloidalFieldCoil(height=20,
                                               width=40,
                                               center_point=(50, 50),
                                               rotation_angle=180)

        test_shape = paramak.PoloidalFieldCoilCaseSetFC(
            pf_coils=[pf_coils_1, pf_coils_2, pf_coils_3, pf_coils_4],
            casing_thicknesses=[5, 5, 10, 10],
            rotation_angle=180
        )

        assert test_shape.solid is not None
        assert len(test_shape.solid.Solids()) == 4

    def test_PoloidalFieldCoilCaseFC_with_number_thickness(self):
        """Creates a set of PF coil cases from a list of PF coils with a
        single numerical thicknesses"""

        pf_coils_1 = paramak.PoloidalFieldCoil(height=10,
                                               width=10,
                                               center_point=(100, 100),
                                               rotation_angle=180)

        pf_coils_2 = paramak.PoloidalFieldCoil(height=10,
                                               width=10,
                                               center_point=(100, 150),
                                               rotation_angle=180)

        pf_coils_3 = paramak.PoloidalFieldCoil(height=20,
                                               width=20,
                                               center_point=(50, 200),
                                               rotation_angle=180)

        pf_coils_4 = paramak.PoloidalFieldCoil(height=20,
                                               width=40,
                                               center_point=(50, 50),
                                               rotation_angle=180)

        test_shape = paramak.PoloidalFieldCoilCaseSetFC(
            pf_coils=[pf_coils_1, pf_coils_2, pf_coils_3, pf_coils_4],
            casing_thicknesses=10,
            rotation_angle=180
        )

        assert test_shape.casing_thicknesses == 10
        assert test_shape.solid is not None
        assert len(test_shape.solid.Solids()) == 4
