package ast;
import static lexer.Lexer.*;

public class BinOp extends AST{
    private AST left;
    private Token op;

    public AST getLeft() {
        return left;
    }

    public AST getRight() {
        return right;
    }

    private AST right;

    public BinOp(AST left, Token op, AST right) {
        this.left = left;
        this.op = op;
        this.right = right;
    }

    public Token getOp() {
        return op;
    }


}
