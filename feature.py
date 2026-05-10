import math
from .utils import MM, DEG

# SW 2024 COM constants (verified from VBA macro recordings)
swFmFillet = 18
swFmCirPattern = 4
swConstRadiusFillet = 1
swFeatureFilletCircular = 1
swFilletOverFlowType_Default = 0


class Feature:
    def __init__(self, part):
        self._part = part

    def _fm(self):
        return self._part.feat_mgr

    def _sel(self):
        return self._part.model.SelectionManager

    def _d(self, val):
        return val * MM

    def _deg(self, val):
        return val * DEG

    # ==================== Extrude ====================

    def extrude(self, depth, direction="blind", draft_angle=0.0, flip=False):
        d = self._d(depth)
        t = 0 if direction == "blind" else 1
        self._fm().FeatureExtrusion2(
            True, flip, False,
            t, t,
            d, 0.01,
            draft_angle != 0, False, False, False,
            self._deg(draft_angle), self._deg(draft_angle),
            False, False, False, False,
            True, True, True,
            0, 0.0, False,
        )

    def extrude_cut(self, depth, direction="blind", rev_dir=True):
        d = self._d(depth)
        t = 0 if direction == "blind" else 1
        self._fm().FeatureCut4(
            rev_dir, False, False,
            t, 0,
            d, 0,
            False, False, False, False, 0.0, 0.0,
            False, False, False, False, False,
            True, True, True, True,
            False, 0, 0, False, False,
        )

    def extrude_midplane(self, depth, draft_angle=0.0):
        d = self._d(depth)
        self._fm().FeatureExtrusion2(
            True, False, False,
            6, 6, d, 0.01,
            draft_angle != 0, False, False, False,
            self._deg(draft_angle), self._deg(draft_angle),
            False, False, False, False,
            True, True, True,
            0, 0.0, False,
        )

    # ==================== Countersunk Hole ====================

    def countersink(self, cs_depth, cs_radius, thru_radius, top_z):
        """Two-step countersunk hole: cs from top face, thru from bottom face."""
        d_cs = self._d(cs_depth)
        r_cs = self._d(cs_radius)
        r_thru = self._d(thru_radius)
        top_m = self._d(top_z)

        # Step 1: countersink from top face (RevDir=True cuts into body)
        self._part.clear_selection()
        self._part.select_at("FACE", 0, 0, top_z)
        self._part.model.SketchManager.InsertSketch2(True)
        self._part.sketch_mgr.CreateCircle(0, 0, 0, r_cs, 0, 0)
        self._part.model.SketchManager.InsertSketch2(True)
        self._fm().FeatureCut4(
            True, False, False,
            0, 0,
            d_cs, 0,
            False, False, False, False, 0.0, 0.0,
            False, False, False, False, False,
            True, True, True, True,
            False, 0, 0, False, False,
        )

        # Step 2: through hole from bottom face (Z=0, RevDir=True = +Z into body)
        self._part.clear_selection()
        self._part.select_at("FACE", 0, 0, 0)
        self._part.model.SketchManager.InsertSketch2(True)
        self._part.sketch_mgr.CreateCircle(0, 0, 0, r_thru, 0, 0)
        self._part.model.SketchManager.InsertSketch2(True)
        self._fm().FeatureCut4(
            True, False, False,
            1, 0,
            0.01, 0,
            False, False, False, False, 0.0, 0.0,
            False, False, False, False, False,
            True, True, True, True,
            False, 0, 0, False, False,
        )

    # ==================== Revolve ====================

    def revolve(self, angle=360.0):
        self._fm().FeatureRevolve2(
            self._deg(angle), False, 0.0, 0,
            True, True, True,
            0, 0.0, False,
            False, False, False, False,
            0.0, 0.0,
            False, False, False, False,
        )

    def revolve_cut(self, angle=360.0):
        self._fm().FeatureRevolveCut2(
            self._deg(angle), False, 0.0, 0,
            True, True, True,
            0, 0.0, False,
            False, False, False, False,
            0.0, 0.0,
            False, False, False, False,
        )

    # ==================== Fillet ====================

    def fillet(self, radius):
        """Create fillet via CreateDefinition (verified from VBA).
        Edges must be pre-selected before calling this method."""
        sel = self._sel()
        fm = self._fm()
        edge_count = sel.GetSelectedObjectCount2(0)
        if edge_count < 1:
            raise RuntimeError("fillet: no edges selected")

        fd = fm.CreateDefinition(swFmFillet)
        fd.Initialize(swConstRadiusFillet)

        edges = [sel.GetSelectedObject6(i + 1, 0) for i in range(edge_count)]
        from win32com.client import VARIANT
        import pythoncom
        fd.Edges = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, edges)
        fd.AsymmetricFillet = False
        fd.DefaultRadius = self._d(radius)
        fd.ConicTypeForCrossSectionProfile = swFeatureFilletCircular
        fd.CurvatureContinuous = False
        fd.ConstantWidth = self._d(radius)
        fd.IsMultipleRadius = False
        fd.OverflowType = swFilletOverFlowType_Default
        return fm.CreateFeature(fd)

    # ==================== Chamfer ====================

    def chamfer(self, dist, angle=None):
        """Create angle-distance chamfer (verified from VBA).
        Edges must be pre-selected before calling this method.
        Default angle=45 degrees if not specified."""
        sel = self._sel()
        edge_count = sel.GetSelectedObjectCount2(0)
        if edge_count < 1:
            edge_count = 1
        angle = angle if angle is not None else math.pi / 4
        self._fm().InsertFeatureChamfer(
            1,
            edge_count,
            1,
            self._d(dist),
            angle,
            0, 0, 0, 0,
        )

    # ==================== Shell ====================

    def shell(self, thickness):
        self._part.model.InsertFeatureShell(self._d(thickness), 0)

    # ==================== Circular Pattern ====================

    def circular_pattern(self, count, total_angle=360.0, equal_spacing=True,
                          reverse=False, axis_name="基准轴1", feature_name="凸台-拉伸2"):
        """Create circular pattern via CreateDefinition.
        Pre-selects feature (mark=4) and axis (mark=1) by name.
        Pass None for feature_name if already selected in the UI.
        """
        self._part.clear_selection()
        ok = True
        if feature_name:
            ok = self._part.select(feature_name, "BODYFEATURE", mark=4) and ok
        if axis_name:
            ok = self._part.select(axis_name, "AXIS", append=True, mark=1) and ok
        if not ok:
            raise RuntimeError(f"circular_pattern: 无法选中 feature={feature_name} 或 axis={axis_name}")

        fm = self._fm()
        fd = fm.CreateDefinition(swFmCirPattern)
        fd.Direction2 = False
        fd.EqualSpacing = equal_spacing
        fd.GeometryPattern = False
        fd.ReverseDirection = reverse
        fd.Spacing = self._deg(total_angle)
        fd.TotalInstances = count
        fd.VarySketch = False
        return fm.CreateFeature(fd)

    # ==================== Linear Pattern ====================

    def linear_pattern(self, count_x, spacing_x, count_y=1, spacing_y=0.0):
        self._fm().FeatureLinearPattern2(
            count_x, self._d(spacing_x), 0, 0,
            count_y, self._d(spacing_y), 0, 0,
            0,
        )

    # ==================== Mirror ====================

    def mirror(self, plane="right", body_xyz=None):
        self._part.clear_selection()
        from .sketch import PLANE_NAMES
        plane_name = PLANE_NAMES.get(plane, plane)
        self._part.select(plane_name, "PLANE")
        if body_xyz:
            self._part.select_body(*body_xyz, append=True)
        else:
            self._part.select_body(0, 0, 10, append=True)
        self._fm().InsertMirrorFeature(False, False, False, False)
