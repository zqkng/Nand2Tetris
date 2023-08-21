###############################################################################
# 11-compiler-code-generation/syntax_analyzer.py
# ----------------------------------------------
# The SyntaxAnalyzer module reads a list of tokens from a Jack program and
# determines its syntactic structure with respect to the Jack grammar.
###############################################################################

import os

from jack_grammar import JackGrammar
import syntax_elements as syntax


class SyntaxAnalyzer:
    
    def __init__(self, tokens):
        """Generates and calls the appropriate parser for each grammar rule specified in the Jack grammar."""
        self._size = len(tokens)
        self._tokens = tokens
  
        for rule in JackGrammar.RULES:
            function = getattr(self, f"{rule[1][0]}_parser")
            function(rule[0], rule[1][1:], rule[2])

    @staticmethod
    def parse(tokens):
        """Takes a list fo token and parses recursively from the top-down, starting with parse_Class."""
        syntax_analyzer = SyntaxAnalyzer(tokens)
        parser = getattr(syntax_analyzer, "parse_Class")
        parse_tree, index = parser(0)

        if index < len(tokens):
            raise ParserError("ERROR: Not all tokens parsed!")
        else:
            return parse_tree
 
    def get_parser(self, element, index):
        """Gets the parser as specified in JackGrammar.RULES."""
        if element.startswith("keyword"):
            return self.parse_Keyword(element[7:], index)
        elif element.startswith("symbol"):
            return self.parse_Symbol(element[6:], index)
        else:
            return getattr(self, f"parse_{element}")(index)

    def sequence_parser(self, name, sequence, syntax_structure):
        """Parses a sequence of tokens (for program structure, statements, expressions)."""
        def parser(self, index):
            try:
                result = []
                result.append(name)
                i = index
                for element in sequence:
                    res, i = self.get_parser(element, i)
                    result.append(res)
                return syntax_structure(result), i
            except ParserError as error:
                raise ParserError(f"Failed to parse: {name}{os.linesep}")

        setattr(SyntaxAnalyzer, f"parse_{name}", parser)

    def type_parser(self, name, options, syntax_structure):
        """Parses the grammar rule in which a choice must be specified (var types, declarations, and different types of statements."""
        def parser(self, index):
            i = index
            for element in options:
                try:
                    res, i = self.get_parser(element, i)
                    return syntax_structure([name, res]), i
                except ParserError as error:
                    pass
            raise ParserError(f"Failed to parse: {name}")
   
        setattr(SyntaxAnalyzer, f"parse_{name}", parser)

    def list_parser(self, name, item, syntax_structure):
        """Parses a list of tokens (parameters, expressions, etc.)."""
        def parser(self, index):
            result = []
            result.append(name)
            i = index
            try:
                while True:
                    res, i = self.get_parser(item[0], i)
                    result.append(res)
            except ParserError as error:
                return syntax_structure(result), i

        setattr(SyntaxAnalyzer, f"parse_{name}", parser)

    def optional_parser(self, name, item, syntax_structure):
        """Parses optional syntax elements within the grammar (parameters, expressions, etc.)."""
        def parser(self, index):
            result = []
            result.append(name)
            i = index
            try:
                res, i = self.get_parser(item[0], i)
                result.append(res)
                return syntax_structure(result), i
            except ParserError as error:
                return syntax_structure(result), i

        setattr(SyntaxAnalyzer, f"parse_{name}", parser)

    def parse_Keyword(self, keyword, index):
        """Returns keyword as class object."""
        token = self._get_next_token(index)
        if token and token.__class__.__name__ == "Keyword" and token.keyword == keyword:
            return syntax.Keyword(keyword), index + 1
        else:
            raise ParserError(f"Failed to parse KEYWORD: {keyword}")

    def parse_Symbol(self, symbol, index):
        """Returns symbol as class object."""
        token = self._get_next_token(index)
        if token and token.__class__.__name__ == "Symbol" and token.symbol == symbol:
            return syntax.Symbol(symbol), index + 1
        else:
            raise ParserError(f"Failed to parse SYMBOL: {symbol}")

    def parse_IntegerConstant(self, index):
        """Returns interger constant as class object."""
        token = self._get_next_token(index)
        if token and token.__class__.__name__ == "IntegerConstant":
            return syntax.IntegerConstant(token.integer_constant), index + 1
        else:
            raise ParserError(f"Failed to parse INTEGER CONSTANT: {token}")

    def parse_StringConstant(self, index):
        """Returns string constant as class object."""
        token = self._get_next_token(index)
        if token and token.__class__.__name__ == "StringConstant":
            return syntax.StringConstant(token.string_constant), index + 1
        else:
            raise ParserError(f"Failed to parse STRING CONSTANT: {token}")

    def parse_Identifier(self, index):
        """Returns an identifier as class object."""
        token = self._get_next_token(index)
        if token and token.__class__.__name__ == "Identifier":
            return syntax.Identifier(token.identifier), index + 1
        else:
            raise ParserError(f"Failed to parse IDENTIFIER: {token}")

    def _get_next_token(self, index):
        """Gets the next token from the list of tokens if there are more tokens."""
        return self._tokens[index] if index < self._size else None


# For tokenizer error exceptions; null operation (nothing happens)
class ParserError(Exception):
    pass

