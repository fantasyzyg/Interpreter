package ast;
import static lexer.Lexer.Token;

/**
 *  Assignment --> variable = expr;
 */
public class Assignment extends AST{
    private AST left;
    private Token op;
    private AST right;

    public Assignment(AST left, Token op, AST right) {
        this.left = left;
        this.op = op;
        this.right = right;
    }

    public AST getLeft() {
        return left;
    }

    public Token getOp() {
        return op;
    }

    public AST getRight() {
        return right;
    }
}
