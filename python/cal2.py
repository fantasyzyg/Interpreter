# -*- coding: utf-8 -*-

# Token types
# EOF(End-Of-File) 是指一个结束符，词法分析器解析到文本的结尾就会产生一个EOF
# 并且我们需要知道的是词法分析就是解释文本，并且为每一个Token打上tag，并且Token里面存放其真实的值
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS','EOF'       # tags 

# 定义Token
class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type = self.type, value = repr(self.value))

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    # 如上所述，解释器首先就是处理文本
    def __init__(self, text):
        self.text = text
        self.pos = 0       # 当前处理到的字符位置
        self.current_token = None  # 当前解释得到的Token，初始状态是没有Token的
        self.current_char = self.text[self.pos]

    # 这个对于一个解释器来说是必须的，在前端部分进行词法分析或者语法分析时，遇到不符合规则的就会跑出错误，停止执行
    # 俗称就是语法错误，编译失败
    def error(self):
        raise Exception('Error parsing input')


    # 它的使命就是每一次都会向前走一步，先去做一个探测，到达结尾就是EOF
    def advance(self):

        self.pos += 1
        if self.pos == len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    # 处理 空格
    def skip_whitespaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # 识别数字
    def integer(self):
        num = ''
        while self.current_char is not None and self.current_char.isdigit():
            num += self.current_char
            self.advance()
        
        return int(num)

    # 当前就是一个词法分析器了       无论词法还是语法分析过程中遇到无法识别的都会抛出错误
    def get_next_token(self):

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespaces()
                continue
            
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            elif self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            elif self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            else:
                self.error()
        
        return Token(EOF, None)

    # 语法分析过程中，有一个匹配过程，如果Token流不符合预期的结构文法，则会抛出错误，还是编译错误，这时就是语法错误了
    # 但是我们需要记住的是，如果匹配成功了，我们就需要继续向前了，直到EOF
    def eat(self, token_type):
        print self.current_token
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    
    # 十分简单的语法分析器
    # 下面是为了实现多个连续的加减
    def expr(self):

        self.current_token = self.get_next_token()
        res = self.current_token.value
        self.eat(INTEGER)

        while self.current_token.type != EOF:
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
            else:
                self.eat(MINUS)
            
            num = self.current_token.value
            self.eat(INTEGER)

            if op.type == PLUS:
                res += num
            else:
                res -= num
        
        self.eat(EOF)

        return res



if __name__ == '__main__':
    while True:
        try:
            text = raw_input('cal>')
        except EOFError:
            break
        if not text:
            continue
        
        interpreter = Interpreter(text)
        print interpreter.expr()
