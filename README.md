### 依据网上教程写的解释器
教程连接如下：https://ruslanspivak.com/lsbasi-part1/

### 什么是解释器？
> For the purpose of this series, let’s agree that if a translator translates a source program into machine language, it is a compiler. If a translator processes and executes the source program without translating it into machine language first, it is an interpreter. 

#### 就是说如果一个翻译器把源代码翻译成机器语言，就是一个编译器。如果并没有翻译成机器语言，而是直接处理了源代码并且进行了求值，就是一个解释器。


目的是去构建一个类Pascal语言的解析器（实现一大部分Pascal语言子集），Pascal语言的基础使用语法如下：

``` pascal
program factorial;

function factorial(n: integer): longint;
begin
    if n = 0 then
        factorial := 1
    else
        factorial := n * factorial(n - 1);
end;

var
    n: integer;

begin
    for n := 0 to 16 do
        writeln(n, '! = ', factorial(n));
end.
```

### *写解析器之前一般都是先写一个简单的算术表达式的解析器。对于一个简单的算术表达式，我们需要知道是如何被解释的，首先肯定是词法分析，词法分析器分割字符，形成字符流(Token)。*

#### A token is an object that has a type and a value 
#### The process of breaking the input string into tokens is called lexical analysis. 有时候简称 Lexer 或者 tokenizer。

我们还需要知道的是一个Token，是一个词素 Lexeme。

### 词法分析和语法分析到底是如何结合起来的呢？
首先我们需要知道的是语法分析需要的是一个Token流，而词法分析就是产生Token流，语法分析中的Parser是解释一个语法结构，每次都向Lexer索取Token去尽可能匹配得到的结构。

## Parser与Lexer的结合
> it finds the structure in the stream of tokens it gets from the get_next_token method and then it interprets the phrase that is has recognized, generating the result of the arithmetic expression.

### Parser
> The process of finding the structure in the stream of tokens, or put differently, the process of recognizing a phrase in the stream of tokens is called parsing. The part of an interpreter or compiler that performs that job is called a parser.

Parser也是可以理解为一个识别过程（Recognition）

语法分析需要用到语法规则图表，那什么是语法规则图表呢？
> What is a syntax diagram? A syntax diagram is a graphical representation of a programming language’s syntax rules. Basically, a syntax diagram visually shows you which statements are allowed in your programming language and which are not.

但是我们需要知道的是：语法分析需要识别句子结构，还是需要一种文法支持导向的。文法可以指导我们写代码。

文法有两个重要概念：产生式和终结符
产生式分成左右两个部分，由左边可以推导出右边，但是如果最后达到了终结符了，就不可以继续进行下去了。

去推断一个文本，首先是从一个开始符号开始，再根据右边的产生式一直识别下去，直到最后把整个文本给解释完毕！

> A grammar defines a language by explaining what sentences it can form. This is how you can derive an arithmetic expression using the grammar: first you begin with the start symbol expr and then repeatedly replace a non-terminal by the body of a rule for that non-terminal until you have generated a sentence consisting solely of terminals. Those sentences form a language defined by the grammar.

> If the grammar cannot derive a certain arithmetic expression, then it doesn’t support that expression and the parser will generate a syntax error when it tries to recognize the expression.

#### 什么是上下文无关文法呢？  context-free-grammer 
> 上下文无关文法（英语：context-free grammar，缩写为CFG），在计算机科学中，若一个形式文法 G = (N, Σ, P, S) 的产生式规则都取如下的形式：V -> w，则谓之。其中 V∈N ，w∈(N∪Σ)* 。上下文无关文法取名为“上下文无关”的原因就是因为字符 V 总可以被字串 w 自由替换，而无需考虑字符 V 出现的上下文。一个形式语言是上下文无关的，如果它是由上下文无关文法生成的（条目上下文无关语言）。上下文无关文法重要的原因在于它们拥有足够强的表达力来表示大多数程序设计语言的语法；实际上，几乎所有程序设计语言都是通过上下文无关文法来定义的。另一方面，上下文无关文法又足够简单，使得我们可以构造有效的分析算法来检验一个给定字串是否是由某个上下文无关文法产生的。例子可以参见 LR 分析器和 LL 分析器。BNF（巴克斯-诺尔范式）经常用来表达上下文无关文法。(摘自维基百科)

对于文法中的一些东西，我们需要知道的有结合性和运算符的优先级。有了这些，我们就可以解决很多二义性了。
那么对于有多个优先级的产生式又该是怎么写呢？

> Here are the rules for how to construct a grammar from the precedence table:
> For each level of precedence define a non-terminal. The body of a production for the non-terminal should contain arithmetic operators from that level and non-terminals for the next higher level of precedence.
> Create an additional non-terminal factor for basic units of expression, in our case, integers. The general rule is that if you have N levels of precedence, you will need N + 1 non-terminals in total: one non-terminal for each level plus one non-terminal for basic units of expression.

更高优先级的应该更往下，也就是说递归深度遍历的话，就是会更快得到处理。最后一个产生式应该是需要有终结符。

递归下降算法：可以理解为一种分治算法，每一次都去求值更小的结果，最后再重新整合。

抽象语法树和Parser Tree：

Parser Tree 是根据文法结构进行一步一步的展开，会显得十分臃肿，但是抽象语法树会展示求值的本质。

但是我们到底如何在抽象语法树中展示优先级呢？
> So far so good, but how do you encode operator precedence in an AST? In order to encode the operator precedence in AST, that is, to represent that “X happens before Y” you just need to put X lower in the tree than Y. 
在构建语法树时，把更高优先级的放在更下面。


### Lexer ---> Parser ---> Interpreter  Lexer 把Token流交给 Parser，Parser构建AST，最后Interpreter解释AST输出结果

> You can read that as “The parser gets tokens from the lexer and then returns the generated AST for the interpreter to traverse and interpret the input.”
> That’s it for today, but before wrapping up I’d like to talk briefly about recursive-descent parsers, namely just give them a definition because I promised last time to talk about them in more detail. So here you go: a recursive-descent parser is a top-down parser that uses a set of recursive procedures to process the input. Top-down reflects the fact that the parser begins by constructing the top node of the parse tree and then gradually constructs lower nodes.