import pythoncom
from win32com.client import VARIANT
from .utils import MM

NULL_VAR = VARIANT(pythoncom.VT_DISPATCH, None)


class PartDoc:
    def __init__(self, app):
        self._app = app
        self._swapp = app.sw
        template = app.get_template(1)
        try:
            self._doc = self._swapp.NewDocument(template, 0, 0, 0)
        except Exception:
            self._doc = self._swapp.NewDocument("", 0, 0, 0)

    @property
    def model(self):
        return self._doc

    @property
    def sketch_mgr(self):
        return self._doc.SketchManager

    @property
    def feat_mgr(self):
        return self._doc.FeatureManager

    @property
    def ext(self):
        return self._doc.Extension

    def select(self, name, obj_type, append=False, mark=0):
        return bool(self.ext.SelectByID2(
            name, obj_type, 0.0, 0.0, 0.0, append, mark,
            NULL_VAR, 0,
        ))

    def select_at(self, entity_type, x, y, z, append=False, mark=0):
        self.ext.SelectByID2(
            "", entity_type,
            x * MM, y * MM, z * MM,
            append, mark, NULL_VAR, 0,
        )

    def select_edge(self, x, y, z, append=False):
        self.select_at("EDGE", x, y, z, append)

    def select_face(self, x, y, z, append=False):
        self.select_at("FACE", x, y, z, append)

    def select_body(self, x, y, z, append=False):
        self.select_at("SOLIDBODY", x, y, z, append)

    def clear_selection(self):
        try:
            self._doc.ClearSelection2(True)
        except Exception:
            pass

    def save(self, path):
        self._doc.SaveAs3(path, 0, 0)

    def rebuild(self):
        self._doc.EditRebuild3()

    def close(self):
        try:
            self._swapp.CloseDoc(self._doc.GetTitle)
        except Exception:
            pass
