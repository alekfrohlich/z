"""This Package contains utilities."""
from .clipping import (
    clip_point, clip_line, clip_wireframe, clip_bezier, clip_bspline,
    generate_segment)
from .obj_files import DotObjParser
from .log import Logger, LogLevel
from .misc_types import Axis, Direction
