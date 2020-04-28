"""This module provides a parser to .oml files."""


class DotOmlParser:
    """Parser for Object Manipulation Language (OML) files.

    Notes
    -----
        The parser breaks the file into one-line commands, then
        forwards each one to the underlying interpreter.

    """

    def __init__(self, interpreter: 'Interpreter'):
        """Construct DotOmlParser."""
        self._interpreter = interpreter

    def interpret_oml_file(self, path: 'str'):
        """Interpret commands from .oml file."""
        with open(path) as obj:
            raw_file = obj.read()
        file_lines = raw_file.split("\n")
        for line in file_lines:
            if line == "" or line[0] == "#":
                continue
            self._interpreter.interpret(line)
