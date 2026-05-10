import math

METER = 1.0
MM = 0.001
CM = 0.01
INCH = 0.0254
DEG = math.pi / 180.0
RAD = 1.0


def mm(val):
    return val * 0.001


def inch(val):
    return val * 0.0254


def deg(val):
    return val * math.pi / 180.0


def rad(val):
    return val


def to_meters(val):
    return val * MM


def to_radians(val):
    return val * DEG
