package parser;

import ast.*;
import lexer.Lexer;

import java.util.ArrayList;
import java.util.List;

import static lexer.Lexer.TYPE.*;
import static lexer.Lexer.Token;

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
        if (token.getType() == LPARA) {
            eat(LPARA);
            result = expr();
            eat(RPARA);
        } else if (token.getType() == INTEGER){
            result = new Num(token);
            eat(INTEGER);
        } else if (token.getType() == ID) {
            return  avaliable();
        } else {
            if (token.getType() == PLUS)
                eat(PLUS);
            else if (token.getType() == MINUS)
                eat(MINUS);
            else
                error();
            result = new UnaryOp(token.getType(), factor());
        }

        return result;
    }

    private AST term() {
        AST result = factor();
        while (currentToken.getType() == MUL || currentToken.getType() == DIV) {
            Lexer.Token token = currentToken;
            if (token.getType() == MUL) {
                eat(MUL);
            } else {
                eat(DIV);
            }

            result = new BinOp(result, token, factor());
        }

        return result;
    }

    private AST expr() {
        AST result = term();

        while (currentToken.getType() == PLUS || currentToken.getType() == MINUS) {
            Lexer.Token token = currentToken;
            if (token.getType() == PLUS) {
                eat(PLUS);
            } else {
                eat(MINUS);
            }
            result = new BinOp(result, token, term());
        }

        if (currentToken.getType() == INTEGER)
            error();

        return result;
    }

    public AST parser() {
        AST node = program();
        if (currentToken.getType() != EOF)
            error();

        return node;
    }


    private AST program() {
        AST node = compoundStatement();
        eat(DOT);

        return node;
    }

    private AST compoundStatement() {
        eat(BEGIN);
        Compound node = new Compound();
        List<AST> children = statementList();
        for (AST child: children)
            node.getChildren().add(child);

        eat(END);

        return node;
    }

    private List<AST> statementList() {
        List<AST> result = new ArrayList<>();
        result.add(statement());

        while (currentToken.getType() != EOF && currentToken.getType() == SEMI) {
            eat(SEMI);
            result.add(statement());
        }

        if (currentToken.getType() == ID)
            error();

        return result;
    }

    private AST statement() {
        if (currentToken.getType() == BEGIN)
            return compoundStatement();
        else if (currentToken.getType() == ID)
            return assignmentStatement();
        else
            return empty();
    }

    private AST assignmentStatement() {
        AST left = avaliable();
        Token op = currentToken;
        eat(ASSIGN);
        AST right = expr();

        return new Assignment(left, op, right);
    }

    private AST avaliable() {
        Var var = new Var(currentToken);
        eat(ID);

        return var;
    }

    private AST empty() {
        return new NoOp();
    }
}
