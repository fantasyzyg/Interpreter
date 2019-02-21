package ast;
import static lexer.Lexer.TYPE;

public class UnaryOp extends AST{
    private TYPE op;

    public TYPE getOp() {
        return op;
    }

    public AST getExpr() {
        return expr;
    }

    private AST expr;

    public UnaryOp(TYPE op, AST expr) {
        this.op = op;
        this.expr = expr;
    }
}
