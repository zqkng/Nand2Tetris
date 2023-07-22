###############################################################################
# 06-assembler/assembler.py
# -------------------------
# The Assembler translates programs written in Hack assembly language into the
# binary code understood by the Hack hardware platform.
# It parses the assembly program in two passes:
#   In the first pass, the symbol table is initialized and L_COMMAND labels are
#   added to the symbol table.
#   For the second pass, it goes through the entire program, parsing each line
#   and translating the instructions as well as adding the variables it
#   encounters into the symbol table.
#
# To run: python assembler.py <program>.asm
#
###############################################################################

import re
import sys
from os import path
from parser import Parser
from code import Code
from symbol_table import SymbolTable
from symbol_table import SymbolTableBuilder


class Assembler:
    _WORD_SIZE = 16 # Words are 16-bits long

    def __init__(self, filename):
        self._parser = Parser(filename)
        self._symbol_table = SymbolTableBuilder(self._parser).build()
        self._parser.reset()

        self._assembler = open(self._get_filename(filename), 'w')
        self._assemble()

        self._parser.close()
        self._assembler.close()

    def _get_filename(self, asm_filename):
        """Converts .asm to .hack file extension."""
        hack_extension = ".hack"
        filename = re.compile(r'\.asm$', re.IGNORECASE).sub(hack_extension, asm_filename)
        if not filename.endswith(hack_extension):
            filename += hack_extension
        return filename

    def _assemble(self):
        """Translates each line in program from Hack Assembly to binary code."""
        while self._parser.has_more_commands():
            self._parser.advance()
            command_type = self._parser.command_type()
            if command_type == 'L_COMMAND':
                continue
            command = {'A_COMMAND': self._build_a_command, 'C_COMMAND': self._build_c_command,}[command_type]()
            self._assembler.write(command + '\n')
    
    def _build_a_command(self):
        """Parses 'A_COMMAND' types and returns corresponding constant or address of symbol."""
        symbol = self._parser.symbol()
        if symbol.isdigit():
            return self._get_a_constant(symbol)
        else:
            return self._get_a_address(symbol)

    def _get_a_constant(self, constant):
        """Returns the constant value for 'A_COMMAND' symbol."""
        max_size = self._WORD_SIZE - 1
        binary = self._convert_decimal_to_binary(constant)
        if len(binary) > max_size:
            raise AssemblerError(f"Constant {constant} is too large. Only {max_size} bits available.")
        # Pad with leading zeroes
        return f"0{'0' * (max_size - len(binary))}{binary}"

    def _convert_decimal_to_binary(self, num):
        binary = ''
        num = int(num)
        while True:
            binary = f"{num % 2}{binary}"
            num /= 2
            if num == 0:
                return binary

    def _get_a_address(self, symbol):
        """Returns the corresponding address for 'A_COMMAND' symbol."""
        if not self._symbol_table.contains(symbol):
            self._symbol_table.add_variable(symbol)
        address = self._symbol_table.get_address(symbol)
        return self._get_a_constant(address)

    def _build_c_command(self):
        """Returns corresponding binary code by looking up mnemonics for 'C_COMMAND'."""
        comp_code = Code.comp(self._parser.comp())
        dest_code = Code.dest(self._parser.dest())
        jump_code = Code.jump(self._parser.jump())
        return f"111{comp_code}{dest_code}{jump_code}"


# For assembler error exception; does nothing (just for convention)
class AssemblerError(Exception):
    pass


if __name__ == "__main__":
    Assembler(sys.argv[1])
