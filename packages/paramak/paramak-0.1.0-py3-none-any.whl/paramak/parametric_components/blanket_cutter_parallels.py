
from paramak import ExtrudeStraightShape


class BlanketCutterParallels(ExtrudeStraightShape):
    """Creates an extruded shape with a parallel rectangular section repeated
    around the reactor. The shape is used to cut other components (eg. blankets
    and firstwalls) in order to create a banana section of the blankets with
    parrallel sides.Typically used to divide a blanket into vertical
    sections with a fixed distance between each section.

    Args:
        distance (float): extruded distance (cm) of the cutter which translates
            to being the gap size between blankets when the cutter is used to
            segment blankets.
        gap_size (float): the distance between the inner edges of the two
            parrallel extrusions
        azimuth_placement_angle (iterable of floats or float, optional): the
            azimuth angle(s) used when positioning the shape. If an iterable of
            angles is provided, the shape is duplicated at all angles. Defaults
            to [0., 36., 72., 108., 144., 180., 216., 252., 288., 324.]
        height (float, optional): height (cm) of the port. Defaults to 2000
        width (float, optional): width (cm) of the port. Defaults to 2000
        stp_filename (str, optional): defaults to "BlanketCutterParallels.stp".
        stl_filename (str, optional): defaults to "BlanketCutterParallels.stl".
        name (str, optional): defaults to "blanket_cutter_Parallels".
        material_tag (str, optional): defaults to
            "blanket_cutter_parallels_mat".
    """

    def __init__(
        self,
        thickness,
        gap_size,
        azimuth_placement_angle=[0., 36., 72., 108., 144., 180., 216., 252.,
                                 288., 324.],
        height=2000,
        width=2000,
        stp_filename="BlanketCutterParallels.stp",
        stl_filename="BlanketCutterParallels.stl",
        name="blanket_cutter_parallels",
        material_tag="blanket_cutter_parallels_mat",
        **kwargs
    ):

        super().__init__(
            distance=gap_size / 2.0 + thickness,
            azimuth_placement_angle=azimuth_placement_angle,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            material_tag=material_tag,
            **kwargs
        )
        self.thickness = thickness
        self.height = height
        self.width = width
        self.gap_size = gap_size
        self.main_cutting_shape = \
            ExtrudeStraightShape(
                distance=self.gap_size / 2.0,
                azimuth_placement_angle=self.azimuth_placement_angle,
            )
        self.find_points()

    def find_points(self):

        points = [
            (0, -self.height / 2),
            (self.width, -self.height / 2),
            (self.width, self.height / 2),
            (0, self.height / 2)
        ]

        self.main_cutting_shape.points = points
        if self.cut is None:
            self.cut = [self.main_cutting_shape]
        elif not isinstance(self.cut, list) and \
                self.cut != self.main_cutting_shape:
            self.cut = [self.cut, self.main_cutting_shape]
        elif self.main_cutting_shape not in self.cut:
            self.cut.append(self.main_cutting_shape)

        self.points = points[:-1]
