###############################################################################
# 06-assembler/symbol_table.py
# ----------------------------
# The SymbolTable module creates and maintains the corresponedence between
# symbols and their meaning (RAM and ROM addresses).
#
###############################################################################

class SymbolTable:

    def __init__(self):
        """
        Construct new symbol table, initialized with predefined symbols and
        pre-allocated RAM addresses (rather than just an empty table).
        """
        self._symbol_table = {
            'SP':     0,
            'LCL':    1,
            'ARG':    2,
            'THIS':   3,
            'THAT':   4,
            'SCREEN': 0x4000,
            'KBD':    0x6000,
        }
        # Add R0 - R15 to symbol table
        for i in range(16):
            self._symbol_table[f'R{i}'] = i
        # Set base address for variable symbols
        self._variable_addr = 16

    def add_entry(self, symbol, address):
        """Adds the pair (symbol, address) to symbol table."""
        self._symbol_table[symbol] = address

    def add_variable(self, symbol):
        """
        Adds variables to the symbol table, starting at base RAM address 16
        and then consecutive memory locations.
        """
        self.add_entry(symbol, self._variable_addr)
        self._variable_addr += 1

    def contains(self, symbol):
        """Determines whether the symbol table contains a specific symbol."""
        return symbol in self._symbol_table

    def get_address(self, symbol):
        """Returns the address associated with the given symbol."""
        return self._symbol_table[symbol]


class SymbolTableBuilder:
    """
    Builds the initial symbol table for the first pass.
    
    Only `L_COMMAND` types are added to the symbol table.
    """

    def __init__(self, parser):
        self._parser = parser

    def build(self):
        count = 0
        symbol_table = SymbolTable()

        while self._parser.has_more_commands():
            self._parser.advance()
            if self._parser.command_type() != 'L_COMMAND':
                count += 1
            else:
                symbol_table.add_entry(self._parser.symbol(), count)
        return symbol_table

