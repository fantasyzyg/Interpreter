# -*- coding: utf-8 -*-

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

# 定义Token
class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type = self.type, value = repr(self.value))

    def __repr__(self):
        return self.__str__()


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

    # def number(self):
    #     num = ''
    #     while self.current_char is not None and self.current_char.isdigit():
    #         num += self.current_char
    #         self.advance()
        
    #     return int(num)


    # 动态语言就是十分方便，一个函数可以返回不同类型的值
    def number(self):
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
            return float(num)
        else:
            return int(num)


    def get_next_token(self):
    
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespaces()
                continue
            
            if self.current_char.isdigit():
                return Token(INTEGER, self.number())
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
                return Token(DIV, '/')
            elif self.current_char == '(':
                self.advance()
                return Token(LPARE, '(')
            elif self.current_char == ')':
                self.advance()
                return Token(RPARA, ')')
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
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            op = self.current_token
            if op.type == MUL:
                self.eat(MUL)
            else:
                self.eat(DIV)
        
            node = BinOp(left=node, op=op, right=self.factor())

        return node

    def factor(self):
        token = self.current_token
        if token.type == LPARE:
            self.eat(LPARE)
            node = self.expr()
            self.eat(RPARA)
            return node
        else:
            self.eat(INTEGER)
            return Num(token)

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

    def parser(self):
        return self.expr()


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


class Interpreter(NodeVisitor):

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
        else:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value


    def interpreter(self):
        tree = self.parser.parser()
        self.RPN(tree)
        print ''

        self.LISP(tree)
        print ''

        return self.visit(tree)

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


def main():
    while True:
        try:
            text = raw_input('cal>')
        except EOFError:
            break
        if not text:
            continue
    
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        print interpreter.interpreter()

if __name__ == '__main__':
    main()
