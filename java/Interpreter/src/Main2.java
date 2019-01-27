import java.util.Scanner;
import java.util.Stack;

public class Main2 {

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);

        String line = in.nextLine();
        Stack<Character> stack = new Stack<>();
        for (int i = 0;i < line.length();++i) {
            if (line.charAt(i) != '#')
                stack.push(line.charAt(i));
            else if (!stack.isEmpty())
                System.out.print(stack.pop() + " ");
        }

        System.out.println();
    }
}
