# -*- coding: utf-8 -*-
from __future__ import division         # Python2 需要额外import模块
from collections import OrderedDict
######################################################################
# 在之前的所有求值之中，我们都是直接在利用文法结构解释文本结构，然后就直接求值了  #
# 现在我们就先构建抽象语法树，然后再在语法树上面求值了。                      #
######################################################################

# Token types
# EOF(End-Of-File) 是指一个结束符，词法分析器解析到文本的结尾就会产生一个EOF
# 并且我们需要知道的是词法分析就是解释文本，并且为每一个Token打上tag，并且Token里面存放其真实的值
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MUL, DIV, LPARE, RPARA, EOF = 'INTEGER', 'PLUS', 'MINUS','MUL', 'DIV', 'LPARE', 'RPARA','EOF'       # tags 

ID, ASSIGN, SEMI, DOT, BEGIN, END = 'ID', 'ASSIGN', 'SEMI', 'DOT', 'BEGIN', 'END'

COLON, COMMA, FLOAT_DIV, INTEGER_DIV = 'COLON', 'COMMA', 'FLOAT_DIV', 'INTEGER_DIV'

VAR, PROGRAM, REAL = 'VAR', 'PROGRAM', 'REAL'

INTEGER_CONST, REAL_CONST = 'INTEGER_CONST', 'REAL_CONST'

# 定义Token
class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type = self.type, value = repr(self.value))

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'BEGIN': Token(BEGIN, 'BEGIN'),
    'END': Token(END, 'END'),
    'DIV': Token(INTEGER_DIV, 'DIV'),
    'PROGRAM': Token(PROGRAM, 'PROGRAM'),
    'VAR' : Token(VAR, 'VAR'),
    'INTEGER': Token(INTEGER, 'INTEGER'),
    'REAL': Token(REAL, 'REAL')
}

##########################################################
# Lexer code                                             #
##########################################################
class Lexer(object):
    # 如上所述，解释器首先就是处理文本
    def __init__(self, text):
        self.text = text
        self.pos = 0                # 当前处理到的字符位置
        self.current_token = None        # 当前解释得到的Token，初始状态是没有Token的
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
    
        self.pos += 1
        if self.pos == len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '}':
            self.advance()
        
        if self.current_char is None:
            self.error()
        
        self.advance()

    # def number(self):
    #     num = ''
    #     while self.current_char is not None and self.current_char.isdigit():
    #         num += self.current_char
    #         self.advance()
        
    #     return int(num)


    # 动态语言就是十分方便，一个函数可以返回不同类型的值
    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        flag = False  # 是否浮点数
        num = ''
        state = 0   # 自动机初始状态

        # 状态5是一个终止状态
        while self.current_char is not None:
            if state == 0:
                if self.current_char == '0':
                    num += self.current_char
                    self.advance()
                    state = 1
                elif self.current_char >= '1' and self.current_char <= '9':
                    num += self.current_char
                    self.advance()
                    state = 2
                else:
                    state = 5
            elif state == 1:
                if self.current_char == '.':
                    num += self.current_char
                    self.advance()
                    state = 3
                    flag = True    # 是浮点数
                else:
                    state = 5
            elif state == 2:
                if self.current_char.isdigit():
                    num += self.current_char
                    self.advance()
                    state = 2
                elif self.current_char == '.':
                    num += self.current_char
                    self.advance()
                    state = 3
                    flag = True    # 是浮点数
                else:
                    state = 5
            elif state == 3:
                if self.current_char.isdigit():
                    num += self.current_char
                    self.advance()
                    state = 4
                else:
                    state = 5
            elif state == 4:
                if self.current_char.isdigit():
                    num += self.current_char
                    self.advance()
                    state = 4
                else:
                    state = 5
            elif state == 5:
                break
        
        # 不在能够终止的状态
        if state == 3:
            self.error()
        
        if flag:
            return Token('REAL_CONST', float(num))
        else:
            return Token('INTEGER_CONST', int(num))

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text):
            return None
        else:
            return self.text[peek_pos]

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        # 大小写不敏感   Pascal 语言就是这般
        # result = result.upper()
        # 变量和关键字是需要分开的处理的
        return RESERVED_KEYWORDS.get(result, Token(ID, result))


    def get_next_token(self):
    
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespaces()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue
            
            if self.current_char.isdigit():
                return self.number()
            elif self.current_char.isalnum() or self.current_char == '_':
                return self._id()
            elif self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')
            elif self.current_char == '.':
                self.advance()
                return Token(DOT, '.')
            elif self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')
            elif self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            elif self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            elif self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            elif self.current_char == '/':
                self.advance()
                return Token(FLOAT_DIV, '/')
            elif self.current_char == '(':
                self.advance()
                return Token(LPARE, '(')
            elif self.current_char == ')':
                self.advance()
                return Token(RPARA, ')')
            elif self.current_char == ':':
                self.advance()
                return Token(COLON, ':')
            elif self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')
            else:
                print "Can't recognize this character % s" % self.current_char
                self.error()
        
        return Token(EOF, None)


##########################################################
#            Parser                                      #
##########################################################

# 抽象类
class AST(object):
    pass

# 二元运算符节点
class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

# 叶子节点
class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

# 一元运算符
class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Compound(AST):
    def __init__(self):
        self.children = []

class Assignment(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass

class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block

class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self):
        raise Exception('SyntaxError')

    def eat(self, token_type):
        print self.current_token
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            print 'SyntaxError！'
            self.lexer.error()

    def term(self):
        """term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            op = self.current_token
            if op.type == MUL:
                self.eat(MUL)
            elif op.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
            else:
                self.eat(FLOAT_DIV)
        
            node = BinOp(left=node, op=op, right=self.factor())

        return node

    def factor(self):
        """factor : PLUS factor
              | MINUS factor
              | INTEGER_CONST
              | REAL_CONST
              | LPAREN expr RPAREN
              | variable
        """
        token = self.current_token
        if token.type == LPARE:
            self.eat(LPARE)
            node = self.expr()
            self.eat(RPARA)
            return node
        elif token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        elif token.type == REAL_CONST:
            self.eat(REAL_CONST)
            return Num(token)
        elif token.type == ID:
            return self.variable()
        else:
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            else:
                self.error()
            
            return UnaryOp(token.type, self.factor())
            

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
            else:
                self.eat(MINUS)
            node = BinOp(left=node, op=op, right=self.term())
        
        if self.current_token.type == INTEGER:
            self.error()

        return node


    def program(self):
        """program : PROGRAM variable SEMI block DOT"""
        self.eat(PROGRAM)
        var_name = self.variable().value
        self.eat(SEMI)
        block = self.block()
        self.eat(DOT)

        return Program(var_name, block)

    def compound_statement(self):
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)
        
        return root
    
    def statement_list(self):
        node = self.statement()
        result = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            result.append(self.statement())
        
        if self.current_token.type == ID:
            self.error()

        return result


    def statement(self):

        if self.current_token.type == BEGIN:
            return self.compound_statement()
        elif self.current_token.type == ID:
            return self.assignment_statement()
        else:
            return self.empty()

    def assignment_statement(self):
        left = self.variable()
        op = self.current_token
        self.eat(ASSIGN)
        right = self.expr()

        return Assignment(left, op, right)

    def variable(self):
        token = self.current_token
        self.eat(ID)
        return Var(token)

    def empty(self):
        return NoOp()


    def block(self):
        """block : declarations compound_statement"""
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)

        return node

    def declarations(self):
        """declarations : VAR (variable_declaration SEMI)+
                    | empty
        """
        declarations = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                declarations.extend(self.variable_declaration())
                self.eat(SEMI)
        else:
            self.empty()

        return declarations

    def variable_declaration(self):
        """variable_declaration : ID (COMMA ID)* COLON type_spec"""
        var_nodes = [Var(self.current_token)]
        self.eat(ID)
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)
        
        self.eat(COLON)
        type_node = self.type_spec()
        var_declarations = [
            VarDecl(v_node, type_node) for v_node in var_nodes
        ]

        return var_declarations

    def type_spec(self):
        """type_spec : INTEGER
                 | REAL
        """
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
        else:
            self.eat(REAL)
        
        return Type(token)


    def parser(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        
        return node

###### 加入符号表
###### 符号表的作用是在程序解释之前 确保程序在解释的时候 符号的引用都是存在且正确的

# 符号需要有名字和类型
class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


# 符号也分为多种： 1、内建类型符号   2、新建变量名
class BuildinTypeSymbol(Symbol):
    def __init__(self, name):
        super(BuildinTypeSymbol, self).__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super(VarSymbol, self).__init__(name, type)

    def __str__(self):
        return '<{name}:{type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__

#### 定义好了基本的符号之后，我们就需要加入符号表了
### 我们可以往符号表里面加入符号(一般是在初次声明的时候),在其他地方遇到符号的时候我们都需要在符号表里面查找
class SymbolTable(object):
    def __init__(self):
        self._symbols = OrderedDict()
        self._init_builtin()

    def _init_builtin(self):
        self.define(BuildinTypeSymbol('INTEGER'))
        self.define(BuildinTypeSymbol('REAL'))
    
    def define(self, symbol):
        print 'Define %s' % symbol
        self._symbols[symbol.name] = symbol
    
    def look_up(self, name):
        print 'Look up %s' % name
        return self._symbols.get(name)

    def __str__(self):
        return 'Symbols: {symbols}'.format(symbols = [value for value in self._symbols.values()])

    __repr__ = __str__


###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit) # 动态语言的方便之处
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


## 建立了符号表这个基本的数据结构之后，我们就需要在解释整个程序之前先做 AST 的一次符号处理

class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symtab = SymbolTable()

    def visit_Program(self, node):
        self.visit(node.block)
    
    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)

        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.symtab.look_up(type_name)
        self.symtab.define(VarSymbol(node.var_node.value, type_symbol))

    def visit_Num(self, node):
        pass
    
    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assignment(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_NoOp(self, node):
        pass

    # def visit_Type

    def visit_Var(self, node):
        var_name = node.value
        if self.symtab.look_up(var_name) is None:
            raise NameError(repr(var_name))

    def print_symtab(self):
        print 'Symbol Table contents:'
        print self.symtab


class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        op = node.op
        if op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif op.type == INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        else:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        if node.op == PLUS:
            return self.visit(node.expr)
        else:
            return - self.visit(node.expr)


    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assignment(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        value =  self.GLOBAL_SCOPE.get(var_name)
        if value is None:
            raise NameError(repr(value))
        else:
            return value

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        pass

    def visit_Type(self, node):
        pass

    def interpreter(self):
        tree = self.parser.parser()
        # self.RPN(tree)
        # print ''

        # self.LISP(tree)
        # print ''

        symtab_bulider = SymbolTableBuilder()
        symtab_bulider.visit(tree)
        symtab_bulider.print_symtab()

        self.visit(tree)
        self.print_GLOBAL_SCOPE()

    # 后缀表达式
    def RPN(self, node):
        node_type = type(node).__name__
        if node_type == 'Num':
            print '%s ' % node.value ,
        else: 
            self.RPN(node.left)
            self.RPN(node.right)
            print '%s ' % node.op.value,

    # LISP 风格输出
    def LISP(self, node):
        node_type = type(node).__name__
        if node_type == 'Num':
            print '%s' % node.value,
        else: 
            print '(%s' % node.op.value,
            self.LISP(node.left)
            self.LISP(node.right)
            print ')',


    def print_GLOBAL_SCOPE(self):
        print 'Run-time GLOBAL_MEMORY contents:'
        print self.GLOBAL_SCOPE


def main():
    import sys
    text = open(sys.argv[1], 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpreter()


if __name__ == '__main__':
    main()
