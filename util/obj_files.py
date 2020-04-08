"""This module contains a parser to Wavefront .obj files."""

import numpy as np

from client.objects import Object

# TODO: DotObjParser class.
# QUESTION: How to deal with hierarchical objects, i.e., one 'o' statement
#           followed by multiple 'g' statements.
# NOTE: Allowing multiple objects to share the same vertex would imply
#       in drastic changes to the software architecture:
#           1. Objects wouldn't store vertex anymore, just point/line/face
#              elements.
#           2. Curves and Surfaces would share parameters?
#           3. (1) and (2) do not satisfy multiple 'g's either, one would
#              need to allow objects to store groups instead of
#              point/line/face.
#           4. (3) implies in recusively defined objects, e.g., an object
#              might be of type (arbitrary name) CompoundObject or
#              PrimitiveObject. The latter containing the drawable elements.
#           5. Namespacing, e.g., an object/group named `engine` would be
#              stored and addressed by file_that_defined_engine::engine.
#
# NOTE: Also, a new question would arise: How to deal with repeated vertices
#       on different .obj files?
#
#           That could be solved by turning `vertex` into a set and
#           recalculating vertex indexes during parsing.
#

class DotObjParser:
    """Parser for Wavefront .obj files.

    Notes
    -----
        Constructs only one object for each .obj file. The object is a
        face element constructed with:

            name = name of the file containing the vertices.
            points = 'v' statements in the file.
            color = BLACK

    """
    def __init__(self, executor: 'Executor'):
        """Construct DotObjParser."""
        self._executor = executor

    def compile_obj_file(self, path: 'str') -> 'list':
        """Returns object described by vertices .obj file."""
        with open(path) as obj:
            raw_file = obj.read()
        file_lines = [line.split(" ") for line in raw_file.split("\n")]
        # Name of the file containing object.
        obj_name = path.split("/")[-1].split(".")[0]
        vertices = []
        for line in file_lines:
            if line[0] == "v":
                vertices.append(np.array([float(line[1]), float(line[2]), 1]))
        self._executor.add(obj_name, vertices, (0.0, 0.0, 0.0))
