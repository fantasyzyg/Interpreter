package ast;
import static lexer.Lexer.Token;

public class Num extends AST{
    private Token token;
    private Integer value;

    public Num(Token token) {
        this.token = token;
        this.value = (Integer) token.getValue();  // 强制转换
    }

    public int getValue() {
        return value;
    }
}
