###############################################################################
# 11-compiler-code-generation/jack_tokenizer.py
# ---------------------------------------------
# Handles the tokenizing (splitting program elements into tokens) of a single
# .jack file and encapsulates access to the input code.
###############################################################################

import os
import re

import syntax_elements as syntax


class JackTokenizer:
    """
    Splits input code into Jack-language tokens, as specified by the Jack grammar.
    All comments and whitespace is removed from input stream.
    """
 
    _RE_KEYWORD = re.compile(
        r"(?:"
        r"class|constructor|function|method|"
        r"field|static|var|int|char|boolean|"
        r"void|true|false|null|this|let|do|"
        r"if|else|while|return"
        r")(?=[^a-zA-Z0-9_])")
        
    _RE_SYMBOL = re.compile("[%s]" % (re.escape(r"{}()[].,;+-*/&|<>=~")))
        
    _RE_IDENTIFIER = re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*")
    
    _RE_INT_CONST = re.compile(r"\d+")
    
    _RE_STRING_CONST = re.compile(r"\"[^\"\r\n]*\"")
    
    _RE_WHITESPACE = re.compile(r"\s")
    
    _RE_INLINE_COMMENT = re.compile(r"//[^\n\r]*[^\n\r]")

    _RE_MULTILINE_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)

    _RE_END_OF_LINE = re.compile(r"[^\n\r]*")

    _TOKEN_REGEX_TYPES = [
        (_RE_WHITESPACE, None),
        (_RE_INLINE_COMMENT, None),
        (_RE_MULTILINE_COMMENT, None),
        (_RE_KEYWORD, syntax.Keyword),
        (_RE_SYMBOL, syntax.Symbol),
        (_RE_INT_CONST, syntax.IntegerConstant), 
        (_RE_STRING_CONST, syntax.StringConstant),	   
        (_RE_IDENTIFIER, syntax.Identifier)
    ]

    @staticmethod
    def tokenize(file):
        """Splits syntax elements within a Jack program file into tokens (terminal elements).

        Argument: file -- the Jack input file prepared for reading
        Returns: list of tokens
        """
        tokens = []
        pos = 0
        line_num = 0
        size = len(file)

        while pos < size:
            match = None
            current_token = None

            for regex, type in JackTokenizer._TOKEN_REGEX_TYPES:
                match = regex.match(file, pos)
                if match:
                    if type: current_token = type(match.group(0).replace("\"", ""))
                    break
            
            if match:
                pos += len(match.group(0))
                line_num += match.group(0).count(os.linesep)
                if current_token: tokens.append(current_token)
            else:
                err_line = JackTokenizer._RE_END_OF_LINE.match(file, pos).group(0)
                raise TokenizerError(f"ERROR - Line {line + 1}: {err_line}")
        
        return tokens


# For tokenizer error exception; null operation (nothing happens)
class TokenizerError(Exception):
    pass

