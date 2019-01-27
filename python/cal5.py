# -*- coding: utf-8 -*-

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
# Parser / Interpreter code                              #
##########################################################
class Interpreter(object):
    # 如上所述，解释器首先就是处理文本
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()


    def error(self):
        raise Exception('SyntaxError')


    # 语法分析过程中，有一个匹配过程，如果Token流不符合预期的结构文法，则会抛出错误，还是编译错误，这时就是语法错误了
    # 但是我们需要记住的是，如果匹配成功了，我们就需要继续向前了，直到EOF
    def eat(self, token_type):
        print self.current_token
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            print 'SyntaxError！'
            self.lexer.error()


    def term(self):
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            else:
                self.eat(DIV)
                result /= self.factor()

        return result
    

    def factor(self):
        token = self.current_token
        if token.type == LPARE:
            self.eat(LPARE)
            result = self.expr()
            self.eat(RPARA)
        else:
            result = token.value
            self.eat(INTEGER)

        return result

    '''
        加入了可以处理括号的文法
        更高优先级的应该在更下面，factor如果是一个括号保护起来的，那么还是可以作为一个基本的因子来处理

        文法如下：
            expr --> term ((PLUS | MINUS)term)*
            term --> factor ((MUL | DIV) factor)*
            factor --> INTEGER | (expr)
        开始符号为 expr , 优先级更高的应该放在更下面。
    '''
    def expr(self):
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            else:
                self.eat(MINUS)
                result -= self.term()

        # 如果接下来还是数字的话，也是一种错误
        if self.current_token.type == INTEGER:
            self.error()

        return result


def main():
    while True:
        try:
            text = raw_input('cal>')
        except EOFError:
            break
        if not text:
            continue
    
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        print interpreter.expr()

if __name__ == '__main__':
    main()
