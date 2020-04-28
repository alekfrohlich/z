"""This module contains geometric primitives.

Object types:
- Point: Defined by point.
- Line: Defined by pair of points.
- Polygon: defined by list of faces.
- Curve: C(1) composite cubic spline.
- Surface: Bicubic splines.

The possible interpolators for curves and surfaces are:
- Bezier
- B-Spline

"""
from .point import Point
from .line import Line
from .curve import Curve, Interpolator
from .surface import Surface
from .wireframe import Wireframe
from .window import Window
