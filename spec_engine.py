import yaml
import re
import math
from .app import SwApp
from .doc import PartDoc
from .sketch import Sketch
from .feature import Feature
from .reference import RefGeometry


class SpecEngine:
    def __init__(self):
        self._app = None
        self._part = None
        self._sketch = None
        self._feature = None
        self._params = {}
        self._steps = []

    def load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
        self._params = spec.get("params", {})
        self._steps = spec.get("steps", [])
        self._name = spec.get("name", "unnamed")
        return self

    def resolve(self, value):
        if isinstance(value, list):
            return [self.resolve(v) for v in value]
        if isinstance(value, dict):
            return {k: self.resolve(v) for k, v in value.items()}
        if isinstance(value, str):
            return self._resolve_str(value)
        return value

    def _resolve_str(self, text):
        pattern = re.compile(r"\$\w+")
        def replacer(m):
            name = m.group(0)[1:]
            v = self._params.get(name)
            if v is not None:
                return str(v)
            return m.group(0)
        result = pattern.sub(replacer, text)
        if result == text:
            return text
        ns = dict(self._params)
        ns["__builtins__"] = {}
        ns.update(math.__dict__)
        try:
            return eval(result, ns)
        except Exception:
            return result

    def execute(self, save_path=None):
        self._app = SwApp(visible=True)
        self._part = PartDoc(self._app)
        self._sketch = Sketch(self._part)
        self._feature = Feature(self._part)
        self._ref = RefGeometry(self._part)

        for step in self._steps:
            r = self.resolve(step)
            self._run_step(r)

        if save_path:
            resolved_path = self.resolve(save_path)
            self._part.save(resolved_path)

    def _run_step(self, step):
        if "extrude" in step:
            self._do_sketch(step["extrude"]["sketch"])
            d = step["extrude"]["depth"]
            self._feature.extrude(d)
        elif "extrude_cut" in step:
            self._do_sketch(step["extrude_cut"]["sketch"])
            d = step["extrude_cut"]["depth"]
            self._feature.extrude_cut(d)
        elif "extrude_midplane" in step:
            self._do_sketch(step["extrude_midplane"]["sketch"])
            d = step["extrude_midplane"]["depth"]
            self._feature.extrude_midplane(d)
        elif "revolve" in step:
            self._do_sketch(step["revolve"]["sketch"])
            angle = step["revolve"].get("angle", 360)
            self._feature.revolve(angle)
        elif "fillet" in step:
            r = step["fillet"]["radius"]
            edges = step["fillet"].get("edges", [])
            for e in edges:
                if len(e) >= 3:
                    self._part.select_edge(e[0], e[1], e[2])
            self._feature.fillet(r)
        elif "chamfer" in step:
            d1 = step["chamfer"]["dist"]
            edges = step["chamfer"].get("edges", [])
            for e in edges:
                if len(e) >= 3:
                    self._part.select_edge(e[0], e[1], e[2])
            self._feature.chamfer(d1)
        elif "shell" in step:
            t = step["shell"]["thickness"]
            faces = step["shell"].get("faces", [])
            for f in faces:
                if len(f) >= 3:
                    self._part.select_face(f[0], f[1], f[2])
            self._feature.shell(t)
        elif "circular_pattern" in step:
            self._feature.circular_pattern(
                step["circular_pattern"]["count"],
                step["circular_pattern"].get("total_angle", 360),
                step["circular_pattern"].get("equal_spacing", True),
                step["circular_pattern"].get("reverse", False),
                step["circular_pattern"].get("axis_name", "基准轴1"),
                step["circular_pattern"].get("feature_name", "凸台-拉伸2"),
            )
        elif "linear_pattern" in step:
            self._feature.linear_pattern(
                step["linear_pattern"]["count_x"],
                step["linear_pattern"]["spacing_x"],
                step["linear_pattern"].get("count_y", 1),
                step["linear_pattern"].get("spacing_y", 0),
            )
        elif "mirror" in step:
            self._feature.mirror(
                step["mirror"].get("plane", "right"),
                step["mirror"].get("body_xyz", None),
            )
        elif "countersink" in step:
            cs = step["countersink"]
            self._feature.countersink(
                cs["cs_depth"],
                cs["cs_radius"],
                cs["thru_radius"],
                cs["top_z"],
            )
        elif "offset_plane" in step:
            self._ref.offset_plane(
                step["offset_plane"]["distance"],
                step["offset_plane"].get("base", "front"),
            )
        elif "axis" in step:
            self._ref.axis()

    def _do_sketch(self, sketch_def):
        plane = sketch_def.get("plane", "front")
        self._part.clear_selection()

        if plane == "face":
            face_pos = sketch_def.get("face_xyz", [0, 0, 20])
            self._part.select_face(*face_pos)
            self._sketch.begin_face()
        else:
            self._sketch.begin(plane)

        draw_list = sketch_def.get("draw", [])
        for item in draw_list:
            if "rect" in item:
                r = item["rect"]
                self._sketch.rect(r[0], r[1], r[2], r[3])
            elif "center_rect" in item:
                r = item["center_rect"]
                self._sketch.center_rect(r[0], r[1], r[2], r[3])
            elif "circle" in item:
                c = item["circle"]
                self._sketch.circle(c[0], c[1], c[2])
            elif "line" in item:
                seg = item["line"]
                self._sketch.line(seg[0], seg[1], seg[2], seg[3])
            elif "slot" in item:
                s = item["slot"]
                self._sketch.slot(s[0], s[1], s[2], s[3], s[4])
            elif "polygon" in item:
                p = item["polygon"]
                self._sketch.polygon(p[0], p[1], p[2], p[3])
            elif "circle_xy" in item:
                c = item["circle_xy"]
                self._sketch.circle(c[0], c[1], c[2])
            elif "spline" in item:
                pts = item["spline"]
                self._sketch.spline(pts)
            elif "centerline" in item:
                cl = item["centerline"]
                self._sketch.centerline(cl[0], cl[1], cl[2], cl[3])

        self._sketch.end()

    def close(self):
        if self._part:
            self._part.close()
