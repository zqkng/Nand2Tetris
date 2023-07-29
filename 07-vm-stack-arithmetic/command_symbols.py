###############################################################################
# 07-vm-stack-arithmetic/command_symbols.py
# ---------------------------------------------
# The CommandSymbols module manages the symbol translations for the
# nine arithmetic/logical commands.
#
###############################################################################


class CommandSymbols:
    # Symbols are stored in dictionaries within a dictionary
    # (as key-val pairs based on command type)
    _COMMAND_SYMBOLS = {
        'binary_compute': {
            'add': '+',
            'sub': '-',
            'and': '&',
            'or': '|',
            },

        'unary_compute': {
            'not': '!',
            'neg': '-',
            },

        'binary_logic': {
            'eq': 'JEQ',
            'gt': 'JGT',
            'lt': 'JLT',
            }
        }

    @classmethod
    def all_commands(cls):
        """Returns all the arithmetic commands."""
        commands = []
        for cmd_type in cls._COMMAND_SYMBOLS:
            for cmd in cls._COMMAND_SYMBOLS[cmd_type]:
                commands.append(cmd)
        return commands

    @classmethod
    def types(cls):
        """Returns all command types."""
        return cls._COMMAND_SYMBOLS.keys()

    @classmethod
    def type_commands(cls, cmd_type):
        """Returns all commands associated with a specific type."""
        return cls._COMMAND_SYMBOLS[cmd_type]

    @classmethod
    def symbol(cls, cmd_type, command):
        """Returns the symbol of a specific command."""
        return cls._COMMAND_SYMBOLS[cmd_type][command]

