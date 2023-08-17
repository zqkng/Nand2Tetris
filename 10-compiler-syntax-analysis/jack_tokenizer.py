###############################################################################
# 10-compiler-syntax-analysis/jack_tokenizer.py
# ---------------------------------------------
# Handles the tokenizing (splitting program elements into tokens) of a single
# .jack file and encapsulates access to the input code.
###############################################################################

import os
import re

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
        
    _RE_SYMBOL = re.compile(f'[{re.escape(r"{}()[].,;+-*/&|<>=~")}]')
        
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
        (_RE_KEYWORD, 'KEYWORD'),
        (_RE_SYMBOL, 'SYMBOL'),
        (_RE_IDENTIFIER, 'IDENTIFIER'), 
        (_RE_INT_CONST, 'INT_CONST'), 
        (_RE_STRING_CONST, 'STRING_CONST')	   
    ]

    def __init__(self, filename):
        """Opens the input file/stream for tokenizing.

        Arguments: filename -- input file/stream
        """
	    self._file = open(filename, 'r')
        self._source = "".join(self._file.readlines())
        self._current_token = None
        self._token_type = ""
        self._size = len(self._source)
        self._pos = 0
        self._line = 0

    def close(self):
        """Closes the input/file stream."""
        self._file.close()
    
    def has_more_tokens(self):
        """Checks if there are more tokens in the input file. Returns: boolean"""
        return self._pos < self._size

    def advance(self):
        """Gets the next token from the input and makes it the current token. 

        This method should only be called if `has_more_tokens()` is True. 
        Initially, there is no current token.
        """
        self._read_next_token()
	    while self._current_token == None and self.has_more_tokens():
            self._read_next_token()

    def _read_next_token(self):
        """Read next token from input, ignoring whitespaces and comments.""" 
        match = None

        for regex, type in JackTokenizer._TOKEN_REGEX_TYPES:
            match = regex.match(self._source, self._pos)
            if match:
                if type: 
                    self._current_token = match.group(0).replace("\"", "")
                    self._token_type = type
                else:
                    self._current_token = None
                    self._token_type = ""
                break
        if match:
            self._pos += len(match.group(0))
            self._line += match.group(0).count(os.linesep)
        else:
            err_line = JackTokenizer._RE_END_OF_LINE.match(self._source, pos).group(0)
            raise LexicalError(f"ERROR - Line {line + 1}: {err_line}")

    def token_type(self):
        """Returns the type of the current token."""
        return self._token_type

    def keyword(self):
        """Returns the keyword which is the current token."""
        if self._token_type == 'KEYWORD':
            return self._current_token
        else:
            return ""

    def symbol(self):
        """Returns the character which is the current token."""
        if self._token_type == 'SYMBOL':
            return self._current_token
        else:
            return ""

    def identifier(self):
        """Returns the identifier which is the current token."""
        if self._token_type == 'IDENTIFIER':
            return self._current_token
        else:
            return ""

    def int_val(self):
        """Returns the integer value of the current token."""
        if self._token_type == 'INT_CONST':
            return self._current_token
        else:
            return ""

    def string_val(self):
        """Returns the string value of the current token."""
        if self._token_type == 'STRING_CONST':
            return self._current_token
        else:
            return ""
    
    def get_xml_token(self):
        type = self.token_type()
        if type == 'KEYWORD':
            return f"<keyword> {self.keyword()} </keyword>"
        elif type == 'SYMBOL':
            symbol = self.symbol()
            if symbol == '<':
                return "<symbol> &lt; </symbol>"
            elif symbol == '>':
                return "<symbol> &gt; </symbol>"
            elif symbol == '&':
                return "<symbol> &amp; </symbol>"
            else:
                return f"<symbol> {self.symbol()} </symbol>"
        elif type == 'IDENTIFIER':
            return f"<identifier> {self.identifier()} </identifier>"
        elif type == 'INT_CONST':
            return f"<integerConstant> {self.int_val()} </integerConstant>"
        elif  type == 'STRING_CONST':
            return f"<stringConstant> {self.string_val()} </stringConstant>"
        else:
            return ""
        
    def token(self):
        """Returns the current token."""
        return self._current_token
        

# For lexical error exception; null operation (nothing happens)
class LexicalError(Exception):
    pass

