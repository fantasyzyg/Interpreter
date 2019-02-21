package lexer;

import java.util.HashMap;
import java.util.Map;

import static lexer.Lexer.TYPE.*;

public class Lexer {
    private int pos;
    private String text;
    private Character current_char;

    private static Map<String, Token> RESERVED_KEYWORDS = new HashMap<>();

    static {
        RESERVED_KEYWORDS.put("BEGIN", new Token(BEGIN, "BEGIN"));
        RESERVED_KEYWORDS.put("END", new Token(END, "END"));
    }


    // 需要处理的Token类型
    public enum TYPE {
        INTEGER("INTEGER"),
        PLUS("PLUS"),
        MINUS("MINUS"),
        MUL("MUL"),
        DIV("DIV"),
        LPARA("LPARA"),
        RPARA("RPARA"),
        EOF("EOF"),

        // new key words
        BEGIN("BEGIN"),
        END("END"),
        ID("ID"),
        DOT("DOT"),
        ASSIGN("ASSIGN"),
        SEMI("SEMI");

        private String typeName;

        TYPE(String typeName) {
            this.typeName = typeName;
        }

        public String getTypeName() {
            return typeName;
        }

        @Override
        public String toString() {
            return typeName;
        }
    }

    // Token
    public static class Token<T> {
        private TYPE type;
        private T value;

        Token(TYPE type, T value) {
            this.type = type;
            this.value = value;
        }

        @Override
        public String toString() {
            return String.format("(%s, %s)", type, value);
        }

        public TYPE getType() {
            return type;
        }

        public T getValue() {
            return value;
        }
    }

    public Lexer(String text) {
        this.text = text;
        this.current_char = text.charAt(pos);    // 初始符号
    }

    // pos 前进一步
    private void advance() {
        ++pos;
        if (pos == text.length())
            current_char = null;
        else
            current_char = text.charAt(pos);
    }

//    // 处理整数或者浮点数
//    private Number number() {
//        StringBuilder sb = new StringBuilder();
//        boolean flag = false;   // 是否浮点数
//        int state = 0;       // 初始状态
//
//        while (current_char != null) {
//            if (state == 0) {
//                if (current_char == 0) {
//                    sb.append(current_char);
//                    advance();
//                    state = 1;
//                } else if (current_char >= '1' && current_char <= '9') {
//                    sb.append(current_char);
//                    advance();
//                    state = 2;
//                } else {
//                    state = 5;
//                }
//            } else if (state == 1) {
//                if (current_char == '.') {
//                    sb.append(current_char);
//                    advance();
//                    state = 3;
//                    flag = true;
//                } else {
//                    state = 5;
//                }
//            } else if (state == 2) {
//                if (Character.isDigit(current_char)) {
//                    sb.append(current_char);
//                    advance();
//                    state = 2;
//                } else if (current_char == '.') {
//                    sb.append(current_char);
//                    advance();
//                    state = 3;
//                    flag = true;
//                } else {
//                    state = 5;
//                }
//            } else if (state == 3) {
//                if (Character.isDigit(current_char)) {
//                    sb.append(current_char);
//                    advance();
//                    state = 4;
//                } else {
//                    state = 5;
//                }
//            } else if (state == 4) {
//                if (Character.isDigit(current_char)) {
//                    sb.append(current_char);
//                    advance();
//                    state = 4;
//                } else {
//                    state = 5;
//                }
//            } else if (state == 5) {
//                break;
//            }
//        }
//
//        // 不处于结束状态
//        if (state == 3)
//            error();
//
//        if (flag)
//            return Float.parseFloat(sb.toString());
//        else
//            return Integer.parseInt(sb.toString());
//    }

    private int integer() {
        StringBuilder sb = new StringBuilder();
        while (current_char != null && Character.isDigit(current_char)) {
            sb.append(current_char);
            advance();
        }

        return Integer.parseInt(sb.toString());
    }

    // 处理空格
    private void skipWhitespaces() {
        while (current_char != null && current_char == ' ')
            advance();
    }

    // 词法分析中抛出的错误  ---- 无法识别的符号
    private void error() {
        throw new IllegalArgumentException("无法识别的符号： " + current_char);
    }

    // 词法分析器
    public Token getNextToken() {

        while (current_char != null) {

            if (current_char == ' ') {
                skipWhitespaces();
                continue;
            }
            // skipWhitespaces();   // 这样写是不行的，虽然我们想到的是，能进入这个函数的就肯定还不是末尾，但是如果在句子末尾本来就是有空格的话，就会发生错误了。

            Character c;
            if (Character.isDigit(current_char)) {
                return new Token<>(TYPE.INTEGER, integer());
            } else if (Character.isLetter(current_char)) {
                return id();
            } else if (current_char == ':' && ((c = peek()) != null && c == '=')) {
                advance();
                advance();
                return new Token<>(ASSIGN, ":=");
            } else if (current_char == '+') {
                advance();
                return new Token<>(TYPE.PLUS, "+");
            } else if (current_char == ';') {
                advance();
                return new Token<>(SEMI, ";");
            } else if (current_char == '.') {
                advance();
                return new Token<>(DOT, ".");
            } else if (current_char == '-') {
                advance();
                return new Token<>(TYPE.MINUS, "-");
            } else if (current_char == '*') {
                advance();
                return new Token<>(TYPE.MUL, "*");
            } else if (current_char == '/') {
                advance();
                return new Token<>(TYPE.DIV, "/");
            } else if (current_char == '(') {
                advance();
                return new Token<>(TYPE.LPARA, "(");
            } else if (current_char == ')') {
                advance();
                return new Token<>(TYPE.RPARA, ")");
            } else
                error();       // 无法识别的符号
        }

        return new Token<String>(TYPE.EOF, null);
    }

    private Character peek() {
        int peekPos = pos + 1;
        if (peekPos >= text.length())
            return null;
        else
            return text.charAt(peekPos);
    }

    private Token id() {
        StringBuilder sb = new StringBuilder();
        while (current_char != null && Character.isLetter(current_char)) {
            sb.append(current_char);
            advance();
        }

        return RESERVED_KEYWORDS.containsKey(sb.toString())?RESERVED_KEYWORDS.get(sb.toString()) : new Token<>(ID, sb.toString());
    }
}
