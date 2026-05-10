import win32com.client


class SwApp:
    def __init__(self, visible=True):
        raw = None
        try:
            raw = win32com.client.GetActiveObject("SldWorks.Application", dynamic=True)
        except Exception:
            pass

        if raw is None:
            raw = win32com.client.Dispatch("SldWorks.Application")
            raw.Visible = visible
        else:
            raw.Visible = visible

        self._sw = raw

    @property
    def sw(self):
        return self._sw

    def get_template(self, doc_type: int = 1):
        try:
            return self._sw.GetDocumentTemplate(doc_type, 0, 0, 0)
        except Exception:
            try:
                return self._sw.GetDocumentTemplate(doc_type, 0)
            except Exception:
                return ""

    def close(self, save_changes=False):
        try:
            self._sw.ExitApp()
        except Exception:
            pass
