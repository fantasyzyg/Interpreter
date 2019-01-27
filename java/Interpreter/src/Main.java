import interpreter.Interpreter;
import lexer.Lexer;
import parser.Parser;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);

        while (true) {
            try {
                System.out.print("cal>");
                String text = in.nextLine();
                if (text.length() == 0)
                    continue;

                Lexer lexer = new Lexer(text);
                Parser parser = new Parser(lexer);
                Interpreter interpreter = new Interpreter(parser);
                System.out.println(interpreter.interpreter());
            } catch (Exception e) {
                e.printStackTrace();
                break;
            }
        }

    }

}
