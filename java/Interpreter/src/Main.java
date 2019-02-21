import interpreter.Interpreter;
import lexer.Lexer;
import parser.Parser;

import java.io.*;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) throws IOException {
        FileReader reader = new FileReader("src/assignments");
        BufferedReader bufferedReader = new BufferedReader(reader);

        StringBuilder text = new StringBuilder();
        String line;
        while ((line = bufferedReader.readLine()) != null) {
            text.append(line);
        }

        Lexer lexer = new Lexer(text.toString());
        Parser parser = new Parser(lexer);
        Interpreter interpreter = new Interpreter(parser);
        interpreter.interpreter();

        System.out.println(interpreter.GLOBAL_SCOPE);        // 作用域table
    }
}
