###############################################################################
# 06-assembler/code.py
# --------------------
# The Code module translates Hack assembly language menmonics into binary codes.
#
###############################################################################

class Translate:
    """
    Store binary code translations/equivalents for Hack Assembly in a dictionary
    (as key-value pair based on field type).
    """

    CODES = { 
        'dest': {
            None:  '000',
            'M':   '001',
            'D':   '010',
            'MD':  '011',
            'A':   '100',
            'AM':  '101',
            'AD':  '110',
            'AMD': '111',
        },

        'comp': {
            '0':   '0101010',
            '1':   '0111111',
            '-1':  '0111010',
            'D':   '0001100',
            'A':   '0110000',
            '!D':  '0001101',
            '!A':  '0110001',
            '-D':  '0001111',
            '-A':  '0110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'D+A': '0000010',
            'D-A': '0010011',
            'A-D': '0000111',
            'D&A': '0000000',
            'D|A': '0010101',
            'M':   '1110000',
            '!M':  '1110001',
            '-M':  '1110011',
            'M+1': '1110111',
            'M-1': '1110010',
            'D+M': '1000010',
            'D-M': '1010011',
            'M-D': '1000111',
            'D&M': '1000000',
            'D|M': '1010101',
        },

        'jump': {
            None:  '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        },
    }


class Code:
    """
    Return the binary code of the specified field type (mnemonic).
    """

    @staticmethod
    def dest(mnemonic):
        return Translate.CODES['dest'][mnemonic]

    @staticmethod
    def comp(mnemonic):
        return Translate.CODES['comp'][mnemonic]

    @staticmethod
    def jump(mnemonic):
        return Translate.CODES['jump'][mnemonic]

