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

    # 这个对于一个解释器来说是必须的，在前端部分进行词法分析或者语法分析时，遇到不符合规则的就会跑出错误，停止执行
    # 俗称就是语法错误，编译失败
    def error(self):
        raise Exception('Error parsing input')
    

    # 当前就是一个词法分析器了,但是还只是可以识别三种符号
    def get_next_token(self):

        # 处理空格
        while self.pos < len(self.text) and self.text[self.pos] == ' ':
            self.pos += 1

        # 到达text结尾，就直接返回一个EOF Token
        if self.pos > len(self.text) - 1:
            return Token(EOF, None)

        current_char = self.text[self.pos]
        # 一个数字 Token
        if current_char.isdigit():
            l = self.pos
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1

            return Token(INTEGER, int(self.text[l:self.pos]))
        elif current_char == '+':
            self.pos += 1
            return Token(PLUS, '+')
        elif current_char == '-':
            self.pos += 1
            return Token(MINUS, '-')

        # 抛出错误，因为无法识别该Token
        self.error()

    # 语法分析过程中，有一个匹配过程，如果Token流不符合预期的结构文法，则会抛出错误，还是编译错误，这时就是语法错误了
    # 但是我们需要记住的是，如果匹配成功了，我们就需要继续向前了，直到EOF
    def eat(self, token_type):
        # print self.current_token
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    
    def expr(self):

        # 在这里我们可以看到，Lexer是由Parser所驱动的，Parser就是去寻找解释一种结构，在下面就是去寻求一个 
        # a + b 的结构，但是如果解释不到的话，就会认为达不到预期，就会报错，也就是语法错误啦！
        # 就好像是，你说的话，我根本就听不懂~

        # 如果最后都是符合要求文法的，就会认为是没有语法错误了，就会开始直接求值或者是中间代码生成了。。

        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        right = self.current_token
        self.eat(INTEGER)

        self.eat(EOF)

        if op.type == PLUS:
            return left.value + right.value
        else:
            return left.value - right.value

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
