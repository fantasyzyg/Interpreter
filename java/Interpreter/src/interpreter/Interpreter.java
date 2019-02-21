package interpreter;

import ast.*;
import lexer.Lexer;
import parser.Parser;
import java.util.HashMap;
import java.util.Map;

public class Interpreter {
    private Parser parser;
    public Map<String, Integer> GLOBAL_SCOPE;

    public Interpreter(Parser parser) {
        this.parser = parser;
        GLOBAL_SCOPE = new HashMap<>();
    }

    public int interpreter() {
        AST tree = parser.parser();
//        RPN(tree);
//        System.out.println();
//        LISP(tree);
//        System.out.println();
        return visit(tree);
    }

    private int visit(AST node) {
        if (node.getClass() == Num.class)
            return ((Num)node).getValue();
        else if (node.getClass() == BinOp.class){
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
        } else if (node.getClass() == Compound.class) {
            Compound compound = (Compound)node;
            for (AST child: compound.getChildren()) {
                visit(child);
            }
        } else if (node.getClass() == NoOp.class) {
            return 0;
        } else if (node.getClass() == Assignment.class) {
            Assignment assignment = (Assignment)node;
            String variableName = ((Var)assignment.getLeft()).getValue();
            GLOBAL_SCOPE.put(variableName, visit(assignment.getRight()));
            return 0;
        } else if (node.getClass() == Var.class) {
            Var var = (Var)node;
            if (!GLOBAL_SCOPE.containsKey(var.getValue())) {
                throw new IllegalArgumentException(var.getValue() + " 不存在！");
            }

            return GLOBAL_SCOPE.get(var.getValue());
        } else {
            UnaryOp unaryOp = (UnaryOp)node;
            if (unaryOp.getOp() == Lexer.TYPE.PLUS)
                return visit(unaryOp.getExpr());
            else
                return - visit(unaryOp.getExpr());
        }

        return 0;
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
