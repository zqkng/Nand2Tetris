###############################################################################
# 11-compiler-code-generation/vm_writer.py
# ----------------------------------------
# The VMWriter module outputs virtual machine commands using the
# Hack VM command syntax.
###############################################################################

import os
from symbol_table import SymbolTable

class VMWriter:
    
    @staticmethod
    def write_push(segment, index):
        """Returns a virtual machine `push` command.

        Arguments: 
        segment -- 'CONST' | 'ARG' | 'LOCAL' | 'STATIC' | 'THIS' | 'THAT' | 'POINTER' | 'TEMP'
        index (int)
        """
        return [f'push {segment} {index}']

    @staticmethod
    def write_pop(segment, index):
        """Returns a virtual machine `pop` command.

        Arguments: 
        segment -- 'CONST' | 'ARG' | 'LOCAL' | 'STATIC' | 'THIS' | 'THAT' | 'POINTER' | 'TEMP'
        index (int)
        """
        return [f'pop {segment} {index}']

    @staticmethod
    def write_operator(command):
        """Returns a virtual machine arithmetic/logical command.

        Argument:
        command -- 'ADD' | 'SUB' | 'NEG' | 'EQ' | 'GT' | 'LT' | 'AND' | 'OR' | 'NOT'
        """
        return [command]

    @staticmethod
    def write_label(label):
        """Returns a virtual machine `label` command.

        Argument: label (string)
        """
        return [f'label {label}']
    
    @staticmethod
    def write_goto(label):
        """Returns a virtual machine `goto` command.

        Argument: label (string)

        """
        return [f'goto {label}']
        
    @staticmethod
    def write_if(label):
        """Returns a virtual machine `if-goto` command.

        Argument: label (string)

        """
        return [f'if-goto {label}']

    @staticmethod
    def write_call(name, n_args):
        """Returns a virtual machine `call` command.

        Arguments:
        name (string)
        n_args -- number of arguments (int)
        """
        return [f'call {name} {n_args}']

    @staticmethod
    def write_function(name, n_locals):
        """Returns a virtual machine `function` command.

        Arguments:
        name (string)
        n_locals -- number of local variables (int)
        """
        return [f'function {name} {n_locals}']

    @staticmethod
    def write_return():
        """Returns a virtual machine `return` command."""
        return ['return']

