###############################################################################
# 06-assembler/parser.py
# ----------------------
# The Parser module reads and assembly language command, parses it, and provides
# convenient access to the command's components (fields and symbols).
# In addtion, it removes all white space and comments.
#
###############################################################################

import re
from code import Code
from code import Translate


class Parser:
    
    def __init__(self, filename):
        """
        Constructs Parser object by opening input file/stream for parsing.
        """
        self._file = open(filename)
        self.reset()

    def close(self):
        """Closes the input file/stream."""
        self._file.close()

    def reset(self):
        """Rewinds the input file/stream to the beginning for second pass/read."""
        self._file.seek(0)
        # Must read (initialize) next command for has_more_commands() to
        # function properly, since advance() has not been called yet and
        # there is no current command initially.
        self._read_next_command()

    def has_more_commands(self):
        """Checks if more there are commands in the input file/stream."""
        return self._next_command != None

    def advance(self):
        """
        Reads next command from input and makes it the current command.
        
        This should be called only if has_more_commands() returns true.
        Initially, there is no current command. The current command and next
        command are stored in order to determine whether a valid command
        follows the current one.
        """
        self._command = self._next_command
        self._read_next_command()

    def _read_next_command(self):
        """
        Reads the next command from the input.

        All comments and extra whitespaces are removed in the process.
        """
        while True:
            command = self._file.readline()
            # Check EOF
            if not command:
                self._next_command = None
                break
            # Remove comments and extra whitespace from line
            command = command[:command.find('//')].strip()
            # Read line until non-whitespace found
            if command:
                self._next_command = command
                break

    def command_type(self):
        """Returns the type of the current command."""
        if self._command.startswith('@'):
            return 'A_COMMAND'
        elif self._command.startswith('('):
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    def symbol(self):
        """Returns the symbol or constant @Xxx/(Xxx) of the current command."""
        return re.search(r'[(@]([a-zA-Z0-9_.$:]+)\)?', self._command).group(1)

    def dest(self):
        """Returns the 'dest' mnemonic in the current C-Instruction."""
        return self._parse_mnemonic('dest')

    def comp(self):
        """Returns the 'comp' mnemonic in the current C-Instruction."""
        return self._parse_mnemonic('comp')

    def jump(self):
        """Returns the 'jump' mnemonic in the current C-Instruction."""
        return self._parse_mnemonic('jump')

    def _parse_mnemonic(self, ftype):
        """Returns the field type from the given C-Instruction."""
        fields = self._split_c_instruction()
        if fields[ftype] not in Translate.CODES[ftype]:
            raise ParserError("Invalid {ftype}: {fields[ftype]}")
        return fields[ftype]

    def _split_c_instruction(self):
        """Parse the 3 different field types and stores them for retrieval."""
        fields = self._command.split('=', 1)
        if len(fields) > 1:
            dest, comp = fields
        else:
            dest, comp = None, fields[0]

        fields = comp.split(';', 1)
        if len(fields) > 1:
            comp, jump = fields
        else:
            comp, jump = fields[0], None
        
        return {'dest': dest, 'comp': comp, 'jump': jump}


# For parsing error exception; does nothing (meant for convention)
class ParserError(Exception):
    pass

