###############################################################################
# 10-compiler-syntax-analysis/jack_analyzer.py
# ---------------------------------------------
# The JackAnalyzer module operates on a filename of the form <Xxx>.jack or a
# directory containing on or more .jack files.
# For each source Xxx.jack, the JackAnalyzer takes the following steps:
#   1. Create a JackTokenizer from the <Xxx>.jack input file.
#   2. Create an output file called <Xxx>.xml and prepare it for writing.
#   3. Use the CompilationEngine to compile the input JackTokenizer into the
#       output file.
################################################################################

import os
import sys

from compilation_engine import CompilationEngine
from jack_tokenizer import JackTokenizer


class JackAnalyzer:
    
    def __init__(self, path):
        """Initialize JackAnalyzer for a single or a directory of .jack file(s).

        Arguments: path -- the filepath to a .jack file or a directory (string)
        """
        jack_files = self._get_jack_files(path)
        for jack_file in jack_files:
            self._output_xml(jack_file)

    def _get_jack_files(self, path):
        """Gets a single .jack file or all .jack files from a directory.

        Arguments: path -- the filepath to .jack file or to a directory (string)
        Returns: jack_files -- a list of .jack files (list)
        """
        if os.path.isdir(path):
            jack_files = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith('.jack')]
            if len(jack_files) == 0:
                raise IOError(f"No .jack files in directory: {path}")
        elif os.path.isfile(path):
            jack_files = [path]
        else:
            raise IOError(f"{path} is not a file or directory.")
        return jack_files

    def _output_xml(self, jack_file):
        """
        Creates JackTokenizer for given .jack file and passes it to CompilationEngine for parsing.
        An XML file is opened for writing and output.
    
        Arguments: jack_file -- the .jack file to parse (string)
        """
        (jack_filename, jack_extension) = os.path.splitext(jack_file)
        xml_file = jack_filename + "FULL.xml"

        tokenizer = JackTokenizer(jack_file)
        xml_output = open(xml_file, 'w')
        compiler = CompilationEngine(tokenizer, xml_output)
        tokenizer.close()
        xml_output.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} [.jack file or directory containing .jack files]")
    JackAnalyzer(sys.argv[1])

