"""This module contains geometric primitives.

Object types:
- Point: Defined by point.
- Line: Defined by pair of points.
- Polygon: defined by list of faces.
- Bezier: C(1) composed bezier curve.
- B-spline: Composed b-spline curve.

Notes
-----
"""
from .point import Point
from .line import Line
from .curve import Curve, Interpolator
from .surface import Surface
from .wireframe import Wireframe
from .window import Window
