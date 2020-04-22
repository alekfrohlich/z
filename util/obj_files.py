"""This module contains a parser to Wavefront .obj files."""

import numpy as np

from client.objects import Object

# NOTE - Dealing with hierarchical objects (compatibility with .obj format)
#
# Allowing multiple objects to share the same vertex would imply in drastic
# changes to the software architecture:
#
#       1. Distinction between a primitive object and a compound object would
#          have to be made

#       2. Manipulation/drawing would impy on visiting each object as a
#          tree and applying transformations/drawing to it's primitives.
#          Manipulation of single sub-groups would be possible.
#
#       3. Each compound object would have it's set of vertices and members.
#          This would allow for repeated vertices while comparing different
#          objects, but not when comparing sub-groups of an object.
#
# (*) As is already done
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
        # FIXME: Not compatible with Wire-frame model.
        with open(path) as obj:
            raw_file = obj.read()
        file_lines = [line.split(" ") for line in raw_file.split("\n")]
        # Name of the file containing object.
        obj_name = path.split("/")[-1].split(".")[0]
        vertices = []
        for line in file_lines:
            if line[0] == "v":
                vertices.append(np.array([float(line[1]), float(line[2]), float(line[3]), 1]))
        self._executor.add(obj_name, vertices, (0.0, 0.0, 0.0))
