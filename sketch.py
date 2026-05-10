import math
from .utils import MM, DEG

PLANE_NAMES = {
    "front": "前视基准面",
    "top": "上视基准面",
    "right": "右视基准面",
    "前视": "前视基准面",
    "上视": "上视基准面",
    "右视": "右视基准面",
    "front_en": "Front Plane",
    "top_en": "Top Plane",
    "right_en": "Right Plane",
}


class Sketch:
    def __init__(self, part):
        self._part = part
        self._active = False

    def _m(self, val):
        return val * MM

    def begin(self, plane="front"):
        name = PLANE_NAMES.get(plane, plane)
        self._part.select(name, "PLANE")
        self._part.model.InsertSketch2(True)
        self._active = True

    def begin_face(self):
        self._part.model.InsertSketch2(True)
        self._active = True

    def end(self):
        self._part.model.InsertSketch2(True)
        self._active = False

    def line(self, x1, y1, x2, y2):
        self._part.sketch_mgr.CreateLine(
            self._m(x1), self._m(y1), 0,
            self._m(x2), self._m(y2), 0,
        )

    def circle(self, cx, cy, r):
        self._part.sketch_mgr.CreateCircle(
            self._m(cx), self._m(cy), 0,
            self._m(cx + r), self._m(cy), 0,
        )

    def rect(self, x1, y1, x2, y2):
        self._part.sketch_mgr.CreateCornerRectangle(
            self._m(x1), self._m(y1), 0,
            self._m(x2), self._m(y2), 0,
        )

    def center_rect(self, cx, cy, w, h):
        hw, hh = w / 2.0, h / 2.0
        self.rect(cx - hw, cy - hh, cx + hw, cy + hh)

    def slot(self, x1, y1, x2, y2, w):
        cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        self._part.sketch_mgr.CreateCenterPointStraightSlot(
            self._m(cx), self._m(cy), 0,
            self._m(x2), self._m(y2), 0,
            self._m(w),
        )

    def polygon(self, cx, cy, r, sides):
        pts = []
        for i in range(sides):
            angle = 2.0 * math.pi * i / sides - math.pi / 2.0
            pts.append(self._m(cx + r * math.cos(angle)))
            pts.append(self._m(cy + r * math.sin(angle)))
            pts.append(0.0)
        self._part.sketch_mgr.CreatePolygon(pts, True)

    def arc_3pt(self, x1, y1, x2, y2, x3, y3):
        self._part.sketch_mgr.Create3PointArc(
            self._m(x1), self._m(y1), 0,
            self._m(x2), self._m(y2), 0,
            self._m(x3), self._m(y3), 0,
        )

    def centerline(self, x1, y1, x2, y2):
        self._part.sketch_mgr.CreateCenterLine(
            self._m(x1), self._m(y1), 0,
            self._m(x2), self._m(y2), 0,
        )

    def ellipse(self, cx, cy, rx, ry):
        self._part.sketch_mgr.CreateEllipse(
            self._m(cx), self._m(cy), 0,
            self._m(cx + rx), self._m(cy), 0,
            self._m(cx), self._m(cy + ry), 0,
        )

    def spline(self, points):
        import array
        pt_arr = array.array('d')
        for x, y in points:
            pt_arr.extend([self._m(x), self._m(y), 0.0])
        return self._part.sketch_mgr.CreateSpline(pt_arr)
