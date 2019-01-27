package parser;

import ast.AST;
import ast.BinOp;
import ast.Num;
import lexer.Lexer;

public class Parser {
    private Lexer lexer;
    private Lexer.Token currentToken;

    public Parser(Lexer lexer) {
        this.lexer = lexer;
        this.currentToken = lexer.getNextToken();
    }

    private void error() {
        throw new IllegalArgumentException("语法错误！");
    }

    private void eat(Lexer.TYPE type) {
        System.out.println(currentToken);
        if (currentToken.getType() == type) {
            currentToken = lexer.getNextToken();
        } else
            error();
    }


    private AST factor() {
        Lexer.Token<Integer> token = currentToken;
        AST result;
        if (token.getType() == Lexer.TYPE.LPARA) {
            eat(Lexer.TYPE.LPARA);
            result = expr();
            eat(Lexer.TYPE.RPARA);
        } else {
            result = new Num(token);
            eat(Lexer.TYPE.INTEGER);
        }

        return result;
    }

    private AST term() {
        AST result = factor();
        while (currentToken.getType() == Lexer.TYPE.MUL || currentToken.getType() == Lexer.TYPE.DIV) {
            Lexer.Token token = currentToken;
            if (token.getType() == Lexer.TYPE.MUL) {
                eat(Lexer.TYPE.MUL);
            } else {
                eat(Lexer.TYPE.DIV);
            }

            result = new BinOp(result, token, factor());
        }

        return result;
    }

    /*
        文法如下：
            expr --> term ((PLUS | MINUS)term)*
            term --> factor ((MUL | DIV) factor)*
            factor --> INTEGER | (expr)
        开始符号为 expr , 优先级更高的应该放在更下面。

     */
    private AST expr() {
        AST result = term();

        while (currentToken.getType() == Lexer.TYPE.PLUS || currentToken.getType() == Lexer.TYPE.MINUS) {
            Lexer.Token token = currentToken;
            if (token.getType() == Lexer.TYPE.PLUS) {
                eat(Lexer.TYPE.PLUS);
            } else {
                eat(Lexer.TYPE.MINUS);
            }
            result = new BinOp(result, token, term());
        }

        if (currentToken.getType() == Lexer.TYPE.INTEGER)
            error();

        return result;
    }

    public AST parser() {
        return expr();
    }
}
