from .utils import MM, DEG
import math


class Params:
    def __init__(self, part):
        self._part = part
        self._doc = part.model

    @property
    def _em(self):
        return self._doc.GetEquationMgr

    def set(self, name, value):
        expr = f'"{name}" = {value}'
        self._em.Add(0, expr)

    def set_mm(self, name, value_mm):
        self.set(name, value_mm)

    def set_deg(self, name, value_deg):
        self.set(name, value_deg)

    def equation(self, name, expression):
        expr = f'"{name}" = {expression}'
        self._em.Add(0, expr)

    def get_value(self, name):
        full_name = f'"{name}"'
        p = self._doc.Parameter(full_name)
        if p:
            return p.SystemValue
        return None

    def get_value_mm(self, name):
        v = self.get_value(name)
        if v is None:
            return None
        return v / MM

    def list_all(self):
        out = []
        count = self._em.GetCount
        for i in range(count):
            eq = self._em.Equation(i)
            out.append(eq)
        return out
