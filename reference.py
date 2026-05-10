from .utils import MM


class RefGeometry:
    def __init__(self, part):
        self._part = part
        self._doc = part.model

    def offset_plane(self, distance, base_plane="front"):
        # NOTE: CreatePlaneAtOffset3 not yet verified against VBA
        from .sketch import PLANE_NAMES
        name = PLANE_NAMES.get(base_plane, base_plane)
        self._part.select(name, "PLANE")
        self._doc.CreatePlaneAtOffset3(distance * MM, 0, 0)

    def axis(self, x=0, y=0, z=0):
        self._part.clear_selection()
        self._part.select_at("FACE", x, y, z)
        self._doc.InsertAxis2(True)

    def plane_three_points(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        # NOTE: CreatePlaneThru3Points3 not yet verified against VBA
        self._doc.CreatePlaneThru3Points3(
            x1 * MM, y1 * MM, z1 * MM,
            x2 * MM, y2 * MM, z2 * MM,
            x3 * MM, y3 * MM, z3 * MM,
        )
