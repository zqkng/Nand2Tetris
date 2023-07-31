###############################################################################
# 08-vm-program-control/parser.py
# --------------------------------
# The Parser module handles the parsing of a single .vm file, and encapsulates
# access to the input code.
#
###############################################################################

from command_symbols import CommandSymbols


class Parser:
    """Reads VM commands, parses them, and provides convenient access to their components."""

    def __init__(self, filename):
        """Opens input file/stream and gets ready to parse it.
        
        Arguments: filename -- input file/stream       
        """
        self._file = open(filename)
        # For `has_more_commands()` to function properly,
        # must call `read_next_command()` to initialize, since `advance()` has
        # not been called yet andthere is no current command initially.
        self._read_next_command()

    def close(self):
        """Closes the input file/stream."""
        self._file.close()

    def has_more_commands(self):
        """Checks if there are more commands in input file. Returns: boolean"""
        return self._next_command != None

    def advance(self):
        """Reads next command from the input and makes it the current command. 
        
        Each command is parsed into three tokens: {command, arg1, arg2}
        and then stored.
        This should be called only if has_more_commands() is True.
        """
        self._parse_command(self._next_command)
        self._read_next_command()

    def _parse_command(self, command):
        """Splits full instruction into three tokens [command arg1 arg2]

        Arguments: command -- the full command to parse (string)
        """
        tokens = command.split()
        tokens = [s.lower() for s in tokens]
        # If < 2 arguments, use empty object ensure at least 3 objects in tokens
        tokens.extend([None, None])
        self._command, self._arg1, self._arg2 = tokens[:3]

    def _read_next_command(self):
        """Reads next command from input, and in doing so, removes whitespace and comments."""
        while True:
            command = self._file.readline()
            # Check EOF
            if not command:
                self._next_command = None
                break
            # Remove comments and extra whitespace from line if present
            command = command[:command.find('//')].strip()
            # Read line until non-whitespace found
            if command:
                self._next_command = command
                break
    
    def command_type(self):
        """Returns the type of the current VM command.
        
        C_ARITHMETICS is returned for all the arithmetic commands.
        """
        types = {'push': 'C_PUSH', 'pop': 'C_POP', 
                 'label': 'C_LABEL', 'goto': 'C_GOTO', 
                 'if-goto':'C_IF', 'function': 'C_FUNCTION', 
                 'return': 'C_RETURN', 'call':'C_CALL'
                 }
        # Add all arithmetic/logical commands to `types` dict 
        for command in CommandSymbols.all_commands():
            types[command] = 'C_ARITHMETIC'

        if self._command in types:
            return types[self._command]
        raise ParserError(f"Unknown Command: {self._command}")

    def arg1(self):
        """Returns the first argument of the current command.

        In the case of `C_ARITHMETIC`, the command itself (add, sub, etc.) is returned.
        This should not be called if the current command is `C_RETURN`.
        """
        if not self._arg1:
            raise ParserError(f"Missing first argument for {self.command_type()} command.")
        return self._arg1

    def arg2(self):
        """Returns the second argument of the current command.
        
        This should only be called if the current command is:
        `C_PUSH`, `C_POP`, `C_FUNCTION`, or `C_CALL`.
        """
        if not self.arg2:
            raise ParserError(f"Missing second argument for {self.command_type()} command.")
        return self._arg2

    def command(self):
        """Returns the current command."""
        return self._command


# For parsing error exception; null operation (nothing happens)
class ParserError(Exception):
    pass

