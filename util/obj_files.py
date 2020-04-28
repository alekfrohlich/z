"""This module provides a parser to Wavefront .obj files."""

import numpy as np


class DotObjParser:
    """Parser for Wavefront .obj files.

    Notes
    -----
        Constructs only one object for each .obj file. The object is a
        face element constructed with:

            name = name of the file containing the vertices
            points = 'v' statements in the file
            faces = 'f' statements in the file
            color = BLACK

    """
    def __init__(self, executor: 'Executor'):
        """Construct DotObjParser."""
        self._executor = executor

    def compile_obj_file(self, path: 'str') -> 'list':
        """Returns object described by .obj file."""
        with open(path) as obj:
            raw_file = obj.read()
        file_lines = [list(filter(lambda x:x != "", line.split(" ")))
                      for line in raw_file.split("\n")]
        obj_name = path.split("/")[-1].split(".")[0]
        vertices = []
        faces = []
        for line in file_lines:
            if line == []:
                continue
            if line[0] == "v":
                vertices.append(np.array(
                    [float(line[1]), float(line[2]), float(line[3]), 1]))
            elif line[0] == "f":
                # .obj indexes start at 1
                faces.append(
                    [int(v_vt_vn.split("/")[0])-1 for v_vt_vn in line[1:]])
        self._executor.add(
            name=obj_name,
            points=vertices,
            faces=faces,
            color=(0.0, 0.0, 0.0),
            obj_type="Wireframe")
