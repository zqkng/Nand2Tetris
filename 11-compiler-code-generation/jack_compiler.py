###############################################################################
# 11-compiler-code-generation/jack_compiler.py
# --------------------------------------------
# The JackCompiler module module operates on a filename of the form <Xxx>.jack
# or a directory containing on or more .jack files.
# For each source Xxx.jack, the compiler takes the following steps:
#   1. Create a JackTokenizer from the <Xxx>.jack input file.
#   2. Create a SyntaxAnalyzer to parse the list of tokens.
#   3. Create an output file called <Xxx>.vm and prepare it for writing. 
#   4. Use the CompilationEngine (along with VMWriter) to compile
#       the parsed .jack class into .vm code.
#   5. Write the compiled .vm code to the .vm output file.
###############################################################################

import os
import sys

from compilation_engine import CompilationEngine
from jack_tokenizer import JackTokenizer
from syntax_analyzer import SyntaxAnalyzer


class JackCompiler:

    def __init__(self, path):
        """Initialize JackCompiler for a single or a directory of .jack file(s).

        Arguments: path -- the filepath to a .jack file or a directory (string)
        """
        jack_files = self._get_jack_files(path)
        for jack_file in jack_files:
            self._compile(jack_file)

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

    def _compile(self, jack_file):
        """Compiles Jack code into VM code.

        Initialize JackTokenizer to tokenize .jack file.
        Initialize SyntaxAnalyzer to parse the list of tokens returned from
        JackTokenizer. The parsed structure returned by SyntaxAnalyzer is passed
        to CompilationEngine for the compilation of VM code.
        Finally, the List of VM commands returned by the compiler is
        written to an .vm output file.

        Arguments: jack_file -- the .jack file to parse (string)
        """
        (jack_filename, jack_extension) = os.path.splitext(jack_file)
        vm_file = f"{jack_filename}.vm"

        finput = open(jack_file, 'r')
        jack_code = ''.join(finput.readlines())

        tokens = JackTokenizer.tokenize(jack_code)
        parse_tree = SyntaxAnalyzer.parse(tokens)
        compiler = CompilationEngine()
        vm_code = compiler.compile_vm_code(parse_tree)

        foutput = open(vm_file, 'w')
        foutput.write(vm_code)
        
        finput.close()
        foutput.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} [.jack file or directory ontaining .jack files]")
    JackCompiler(sys.argv[1])

