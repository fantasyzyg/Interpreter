package interpreter;

import ast.AST;
import ast.BinOp;
import ast.Num;
import parser.Parser;

public class Interpreter {
    private Parser parser;

    public Interpreter(Parser parser) {
        this.parser = parser;
    }

    public int interpreter() {
        AST tree = parser.parser();
        RPN(tree);
        System.out.println();
        LISP(tree);
        System.out.println();
        return visit(tree);
    }

    private int visit(AST node) {
        if (node.getClass() == Num.class)
            return ((Num)node).getValue();
        else {
            BinOp binOp = (BinOp)node;
            String op = (String) binOp.getOp().getValue();
            if (op == "+")
                return visit(binOp.getLeft()) + visit(binOp.getRight());
            else if (op == "-")
                return visit(binOp.getLeft()) - visit(binOp.getRight());
            else if (op == "*")
                return visit(binOp.getLeft()) * visit(binOp.getRight());
            else
                return visit(binOp.getLeft()) / visit(binOp.getRight());
        }
    }

    private void RPN(AST node) {
        if (node instanceof Num) {
            System.out.print(((Num)node).getValue() + " ");
        } else if (node instanceof BinOp) {
            BinOp binOp = (BinOp)node;
            RPN(binOp.getLeft());
            RPN(binOp.getRight());
            System.out.print(binOp.getOp().getValue() + " ");
        }
    }

    private void LISP(AST node) {
        if (node instanceof Num) {
            System.out.print(((Num)node).getValue() + " ");
        } else if (node instanceof BinOp) {
            BinOp binOp = (BinOp)node;
            System.out.print("("+binOp.getOp().getValue() + " ");
            LISP(binOp.getLeft());
            LISP(binOp.getRight());
            System.out.print(")");
        }
    }
}
