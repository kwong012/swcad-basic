from .app import SwApp
from .doc import PartDoc, NULL_VAR
from .sketch import Sketch, PLANE_NAMES
from .feature import Feature
from .params import Params
from .reference import RefGeometry
from .spec_engine import SpecEngine
from . import utils


def create_part(visible=True):
    app = SwApp(visible=visible)
    part = PartDoc(app)
    return part, app


def connect_part(visible=True):
    app = SwApp(visible=visible)
    return PartDoc(app), app

