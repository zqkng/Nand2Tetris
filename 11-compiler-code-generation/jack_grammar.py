###############################################################################
# 11-compiler-code-generation/jack_grammar.py
# --------------------------------------------
# The JackGrammar module describes and represents the syntax of the Jack
# programming language as specified in Figure 10.5
# <Complete grammar of the Jack language>.
#
# It encapsulates each grammar rule as a class object that maintains structure
# of code.
################################################################################

import syntax_elements as syntax


class JackGrammar:

    RULES = [       
        # 'class' ClassName '{' ClassVarDec* SubroutineDec* '}'
        ("Class", ["sequence", "keywordclass", "ClassName", "symbol{", "ClassVarDecs", "SubroutineDecs", "symbol}"],
         lambda x: syntax.Class(x[2], x[4], x[5])),

        ("ClassVarDecs", ["list", "ClassVarDec"],
         lambda x: x[1:]),

        ("SubroutineDecs", ["list", "SubroutineDec"],
         lambda x: x[1:]),

        # ('static' | 'field') Type VarName (',' VarName)* ';'
        ("ClassVarDec", ["sequence", "DecScope", "Type", "VarName", "CommaPrecededVarNames", "symbol;"],
         lambda x: syntax.ClassVarDec(x[1], x[2], [x[3]] + x[4])),

        ("DecScope", ["type", "keywordstatic", "keywordfield"],
         lambda x: x[1]),

        ("CommaPrecededVarNames", ["list", "CommaPrecededVarName"],
         lambda x: x[1:]),

        ("CommaPrecededVarName", ["sequence", "symbol,", "VarName"],
         lambda x: x[2]),

        # 'int' | 'char' | 'boolean' | ClassName
        ("Type", ["type", "keywordint", "keywordchar", "keywordboolean", "ClassName"],
         lambda x: syntax.VarType(x[1])),
        
        # ('constructor' | 'fnction' | 'method') ('void' | Type) SubroutineName '(' ParameterList ')' SubroutineBody
        ("SubroutineDec", ["sequence", "SubroutineType", "SubroutineReturnType", "SubroutineName", "symbol(", "ParameterList", "symbol)", "SubroutineBody"],
         lambda x: syntax.SubroutineDec(x[1], x[2], x[3], x[5], x[7])),
      
        ("SubroutineType", ["type", "keywordconstructor", "keywordfunction", "keywordmethod"],
         lambda x: x[1]),

        ("SubroutineReturnType", ["type", "keywordvoid", "Type"],
         lambda x: x[1]),
      
        # ((Type VarName) (',' Type VarName)*)?
        ("ParameterList", ["optional", "NonEmptyParameterList"],
         lambda x: x[1] if len(res) > 1 else []),
      
        ("NonEmptyParameterList", ["sequence", "Type", "VarName", "CommaPrecededTypedVarNames"],
         lambda x: [(x[1], x[2])] + x[3]),

        ("CommaPrecededTypedVarNames", ["list", "CommaPrecededTypedVarName"],
         lambda x: x[1:]),

        ("CommaPrecededTypedVarName", ["sequence", "symbol,", "Type", "VarName"],
         lambda x: (x[2], x[3])),
      
        # '{' VarDec* Statements '}'
        ("SubroutineBody", ["sequence", "symbol{", "VarDecs", "Statements", "symbol}"],
         lambda x: syntax.SubroutineBody(x[2], x[3])),

        ("VarDecs", ["list", "VarDec"],
         lambda x: x[1:]),

        # 'var' Type VarName (',' VarName)* ';'
        ("VarDec", ["sequence", "keywordvar", "Type", "VarName", "CommaPrecededVarNames", "symbol;"], 
         lambda x: syntax.VarDec(x[2], [x[3]] + x[4])),

        ("ClassName", ["sequence", "Identifier"], 
         lambda x: x[1]),
        
        ("SubroutineName", ["sequence", "Identifier"], 
         lambda x: x[1]),
        
        ("VarName", ["sequence", "Identifier"], 
         lambda x: x[1]),
      
        # statement*
        ("Statements", ["list", "Statement"], 
         lambda x: syntax.Statements(x[1:])),
      
        # LetStatement | IfStatement | WhileStatement | DoStatement | ReturnStatement
        ("Statement", ["type", "LetStatement", "IfStatement", "DoStatement", "WhileStatement", "ReturnStatement"], 
         lambda x: syntax.Statement(x[1])),

        ("LetStatement", ["type", "RegularLetStatement", "ArrayEntryLetStatement"],
         lambda x: syntax.LetStatement(x[1])),

        # 'let' VarName '=' Expression ';'
        ("RegularLetStatement", ["sequence", "keywordlet", "VarName", "symbol=", "Expression", "symbol;"], 
         lambda x: syntax.RegularLetStatement(x[2], x[4])),

        # 'let' VarName ('[' Expression ']')? '=' Expression ';'
        ("ArrayEntryLetStatement", ["sequence", "keywordlet", "ArrayVarName", "symbol=", "Expression", "symbol;"],
         lambda x: syntax.ArrayEntryLetStatement(x[2][0], x[2][1], x[4])),

        ("IfStatement", ["type", "IfElseStatement", "RegularIfStatement"],
         lambda x: syntax.IfStatement(x[1])),

        # 'if' '(' Expression ')' '{' Statements '}'
        ("RegularIfStatement", ["sequence", "keywordif", "symbol(", "Expression", "symbol)", "symbol{", "Statements", "symbol}"], 
         lambda x: syntax.RegularIfStatement(x[3], x[6])),
        
        # RegularIfStatement ('else' '{' statement ']')?)
        ("IfElseStatement", ["sequence", "RegularIfStatement", "keywordelse", "symbol{", "Statements", "symbol}"],
         lambda x: syntax.IfElseStatement(x[1].expression, x[1].statements, x[4])),

        # 'while' '(' Expression ')' '{' Statements '}'
        ("WhileStatement", ["sequence", "keywordwhile", "symbol(", "Expression", "symbol)", "symbol{", "Statements", "symbol}"],
         lambda x: syntax.WhileStatement(x[3], x[6])),

        # 'do' SubroutineCall ';'
        ("DoStatement", ["sequence", "keyworddo", "SubroutineCall", "symbol;"],
         lambda x: syntax.DoStatement(x[2])),
      
        ("ReturnStatement", ["type", "ReturnExpressionStatement", "ReturnToEndStatement"], 
         lambda x: syntax.ReturnStatement(x[1])),
      
        # 'return' Expression ';'
        ("ReturnExpressionStatement", ["sequence", "keywordreturn", "Expression", "symbol;"], 
         lambda x: syntax.ReturnExpressionStatement(x[2])),

        # 'return' ';'
        ("ReturnToEndStatement", ["sequence", "keywordreturn", "symbol;"], 
         lambda x: syntax.ReturnToEndStatement()),

        # Term (OpTerm)*
        ("Expression", ["sequence", "Term", "OpTerms"], 
         lambda x: syntax.Expression(x[1], x[2])),
        
        ("OpTerms", ["list", "OpTerm"], 
         lambda x: x[1:]),
        
        ("OpTerm", ["sequence", "Op", "Term"], 
         lambda x: (x[1], x[2])),
        
        ("Term", ["type", "IntegerConstant", "KeywordConstant", "StringConstant", "SubroutineCall", "ArrayVarName", "VarName", "ParenExpression", "UnaryOpTerm"],
         lambda x: syntax.Term(x[1])),
      
        ("ArrayVarName", ["sequence", "VarName", "symbol[", "Expression", "symbol]"], 
         lambda x: (x[1], x[3])),

        ("ParenExpression", ["sequence", "symbol(", "Expression", "symbol)"], 
         lambda x: x[2]),

        ("UnaryOpTerm", ["sequence", "UnaryOp", "Term"], 
         lambda x: syntax.UnaryOpTerm(x[1], x[2])),
      
        ("SubroutineCall", ["type", "FunctionCall", "MethodCall", "StaticMethodCall"], 
         lambda x: syntax.SubroutineCall(x[1])),

        ("FunctionCall", ["sequence", "SubroutineName", "symbol(", "ExpressionList", "symbol)"], 
         lambda x: syntax.FunctionCall(x[1], x[3])),

        ("MethodCall", ["sequence", "VarName", "symbol.", "SubroutineName", "symbol(", "ExpressionList", "symbol)"],
         lambda x: syntax.MethodCall(x[1], x[3], x[5])),

        ("StaticMethodCall", ["sequence", "ClassName", "symbol.", "SubroutineName", "symbol(", "ExpressionList", "symbol)"], 
         lambda x: syntax.StaticMethodCall(x[1], x[3], x[5])),

        ("ExpressionList", ["optional", "NonEmptyExpressionList"],
         lambda x: x[1] if len(res) > 1 else []),
      
        ("NonEmptyExpressionList", ["sequence", "Expression", "CommaPrecededExpressions"],
         lambda x: [x[1]] + x[2]),
        
        ("CommaPrecededExpressions", ["list", "CommaPrecededExpression"],
         lambda x: x[1:]),
        
        ("CommaPrecededExpression", ["sequence", "symbol,", "Expression"],
         lambda x: x[2]),
      
        ("Op", ["type", "symbol+", "symbol-", "symbol*", "symbol/", "symbol&", "symbol|", "symbol<", "symbol>", "symbol="],
         lambda x: syntax.Op(x[1])),
        
        ("UnaryOp", ["type", "symbol-", "symbol~"], 
         lambda x: syntax.UnaryOp(x[1])),
      
        ("KeywordConstant", ["type", "keywordtrue", "keywordfalse", "keywordnull", "keywordthis"], 
         lambda x: syntax.KeywordConstant(x[1]))        
    ]

