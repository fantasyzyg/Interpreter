package ast;
import static lexer.Lexer.Token;

/**
 *  Token (type, value)  ----> type 只是一个类型标签，value是其背后真实的字符值
 */
public class Var extends AST{
    private Token token;
    private String value;

    public Var(Token<String> token) {
        this.token = token;
        this.value = token.getValue();
    }

    public String getValue() {
        return value;
    }
}
