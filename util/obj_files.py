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
#          tree and applying transformations/drawing to the primitives
#
#       3. The renderizable primitive type would only store references to
#          vertices. Such vertices would be stored in a shared set (*).
#          Non-renderizable types such as points and lines would have their
#          vertices stored inside them; Curves and surfaces would store their
#          parameters and be drawn only for visualization (**)
#
#       4. Applicable to renderizable objects: Repeated vertices could be
#          detected during the creation of object, automatically changing the
#          reference of the repeated vertex to the old one.
#
#       5. Namespacing would be needed to avoid clashes between different
#          files, objects, and groups.
#
#
# (*) This design decision relies on the BIG assumption that renderizable
#     primivites are more heavily used than other types: point, line, curves,
#     and surfaces
#
# (**) As is already done
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
