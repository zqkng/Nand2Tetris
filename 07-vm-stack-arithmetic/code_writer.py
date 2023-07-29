###############################################################################
# 07-vm-stack-arithmetic/code_writer.py
# -------------------------------------
# The CodeWriter module translates VM commands into Hack assembly code.
#
###############################################################################

import os
import re

from command_symbols import CommandSymbols


class CodeWriter:
    """Generates HACK assembly code from VM language commands."""
    
    # CONSTANT and STATIC segments handled as special case
    _VM_SEGMENTS = {
        # For each instance of running function
        'instance': {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            },
        # Shared by all functions in program
        'shared': {
            'pointer': 'THIS',
            'temp': 'R5'
            }
        }

    def __init__(self, vm_file):
        """Opens the output file/stream for writing."""
        self._output_file = open(self._get_filename(vm_file), 'w')
        self._label_count = 0

    def _get_filename(self, vm_file):
        """Checks whether .vm file or .asm file.
        
        Arguments: vm_file -- .vm file (string)
        Returns: .vm file with .asm extension
        """
        asm_extension = '.asm'
        filename = re.compile(r'\.vm$', re.IGNORECASE).sub(asm_extension, vm_file)
        if not filename.endswith(asm_extension):
            filename += asm_extension
        return filename

    def set_filename(self, vm_file):
        """Informs the code writer that the translation of a new VM file is started.
        
        Arguments:
        vm_file -- filename (string)
        """
        vm_file = os.path.basename(vm_file)
        self._vm_basename = re.compile(r'\.vm$', re.IGNORECASE).sub('', vm_file)
        
    def _write(self, string):
        """Writes string to output file (general)."""
        self._output_file.write(string + '\n')

    def _write_comment(self, comment):
        """Write comment to output file."""
        self._write(f"// {comment}")

    def _write_instruction(self, commands):
        """Writes instructions (list of commands) to output file.

        Each command is on newline; command indented unless it is a label.
        """
        commands = [[4*' ', ''][cmd.startswith('(')] + cmd for cmd in commands]
        self._write('\n'.join(commands))

    def write_command(self, command):
        """Writes the assembly code that is the translation of the given command.

        Arguments:
        command -- the command to translate and write to output file (string)
        """
        for cmd_type in CommandSymbols.types():
            if command in CommandSymbols.type_commands(cmd_type):
                self._write_comment(command)
                # Determine command type, then calls corresponding method
                write_method = getattr(self, f"_write_{cmd_type}")
                write_method(CommandSymbols.symbol(cmd_type, command))
                self._write('')    # Write newline
                break
        else:
            raise CodeWriterError(f"Unknown Command: {command}")
        
    def _write_binary_compute(self, symbol):
        """Writes the assembly code to compute a binary function (add, sub, and, or).
        
        Arguments: symbol -- corresponding operation symbol for the command (string)
        """
        self._pop_from_stack_to('D')
        self._pop_from_stack_to('A')
        self._write_instruction([f"D=A{symbol}D"]);
        self._push_to_stack_from('D')

    def _write_unary_compute(self, symbol):
        """Writes the assembly code to compute a unary function (neg, not).

        Arguments: symbol -- corresponding operation symbol for the command (string)
        """
        self._write_instruction(['@SP', 'A=M-1', f'M={symbol}M'])

    def _write_binary_logic(self, symbol):
        """Writes the assembly code to compute a binary function that returns a Boolean (eq, gt, lt).
        
        Arguments: symbol -- corresponding opration symbol for the command (string)
        """
        # Increment count for unique labels
        self._label_count += 1
        label = f"LABEL{self._label_count}"

        self._pop_from_stack_to('D')
        self._pop_from_stack_to('A')
        self._write_instruction(['D=A-D'])
        self._write_instruction([f'@{label}_TRUE', f'D;{symbol}'])
        self._push_boolean_to_stack(False)
        self._write_instruction([f'@{label}_FALSE', '0;JMP', f'({label}_TRUE)'])
        self._push_boolean_to_stack(True)
        self._write_instruction([f'({label}_FALSE)'])
        
    def _pop_from_stack_to(self, register):
        """Writes the assembly code for storing a value form RAM to register.
        
        Arguments: register -- the register to store the value (string)
        """
        self._write_instruction(['@SP', 'AM=M-1', f'{register}=M'])

    def _push_to_stack_from(self, register):
        """Writes the assembly code for storing a value from the register to RAM.

        Arguments: register -- the register to retrieve the value from to store into RAM (string)
        """
        self._write_instruction(['@SP', 'M=M+1', 'A=M-1', f'M={register}'])
    
    def _push_boolean_to_stack(self, boolean):
        """Writes the assembly code for storing a boolean value to RAM.
        
        Arguments: boolean -- the boolean value to store into RAM
        """
        self._write_instruction(['@SP', 'M=M+1', 'A=M-1', f'M={(0, -1)[boolean]}'])

    def write_push_pop(self, command, segment, index):
        """Writes the assembly code that is the translation of the given C_PUSH or C_POP command.

        Arguments:
        command -- 'C_PUSH' or 'C_POP'
        segment -- name of virtual memory segment (string)
        index -- nonnegative decimal that specifies location within memory segment (int)
        """
        # Join command with arguments
        full_command = ' '.join((command, segment, index))
        self._write_comment(full_command)

        if command == 'push' and segment == 'constant':
            self._push_constant(index)
        elif segment in self._VM_SEGMENTS['shared'].keys() + self._VM_SEGMENTS['instance'].keys():
            self._push_pop_variable(command, segment, index)
        elif segment == 'static':
            self._push_pop_static(command, index)
        else:
            raise CodeWriterError(f"Unknown Command: {full_command}")
        self._write('')    # Write newline

    def _push_constant(self, constant):
        """Writes the assembly code that corresponds to pushing a constant to the stack. 

        Constant stored in virtual CONSTANT segment.
        Arguments: constant -- the value to push to stack
        """
        self._write_instruction([f'@{constant}', 'D=A', '@SP', 'M=M+1', 'A=M-1', 'M=D'])
        
    def _push_pop_variable(self, command, segment, index):
        """Writes the assembly code that corresponds to push/pop variable to/from the specified vm segment.

        Arguments:
        command -- either 'push' or 'pop' command (string)
        segment -- the specified memory segment to be accessed (string)
        index -- the offset from the base address (integer)
        """
        if command == 'push':
            self._get_address('A', segment, index)
            self._write_instruction(['D=M'])
            self._push_to_stack_from('D')
        elif command == 'pop':
            self._get_address('D', segment, index)
            self._write_instruction(['@R13', 'M=D'])
            self._pop_from_stack_to('D')
            self._write_instruction(['@R13', 'A=M', 'M=D'])
        else:
            raise CodeWriterError(f"Unknown Command: {command}")

    def _get_address(self, register, segment, index):
        """Calculates the address and writes the necessary assembly code.
        
        Resulting address = segment[index] or base address + index
        Arguments:
        register -- the register to store the resulting address (string)
        segment -- the segment to be accessed for calculating base address (string)
        index -- the offset from base address (location within segment) (integer)
        """
        if segment in self._VM_SEGMENTS['instance']:
            base_addr = self._VM_SEGMENTS['instance'][segment]
            loc = 'M'
        elif segment in self._VM_SEGMENTS['shared']:
            base_addr = self._VM_SEGMENTS['shared'][segment]
            loc = 'A'

        self._write_instruction([f'@{index}', 'D=A', f'@{base_addr}', f'{register}={loc}+D'])

    def _push_pop_static(self, command, var):
        """Writes the assembly code that corresponds to push/pop static variables to STATIC vm segment.

        Arguments:
        command -- the memory access command, either 'push' or 'pop' (string)
        var -- the static variable symbol extension (Xxx.var)
        """
        symbol = f'{self._vm_basename}.{var}'
        if command == 'push':
            self._write_instruction([f'@{symbol}', 'D=M'])
            self._push_to_stack_from('D')
        elif command == 'pop':
            self._pop_from_stack_to('D')
            self._write_instruction([f'@{symbol}', 'M=D'])
        else:
            raise CodeWriterError(f"Unknown Command: {command}")

    def close(self):
        """Writes the assembly code corresponding to the end of a program."""
        self._write_comment("Infinite Loop (Terminator)")
        self._write_instruction(['(END)', '@END', '0;JMP'])
        # Close output file upon program end
        self._output_file.close()
        

# For code translation/writing error exceptions; null operation (nothing happens).
class CodeWriterError(Exception):
    pass

