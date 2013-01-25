/**
 * A program that prints the first 20 numbers in the Fibonacci sequence.
 *
 * (Example solution for Exercise 1.)
 *
 * @author Matthew Frazier <leafstormrush@gmail.com>
 */
public class Fibonacci {
    public static void main (String[] args) {
        // Print the first two terms specially.
        System.out.print("0, 1");

        int n;
        int n1 = 1;     // represents n - 1
        int n2 = 0;     // represents n - 2

        // We already printed 2, so we only need to loop 18 times.
        for (int i = 3; i <= 20; i++) {
            n = n1 + n2;
            System.out.print(", " + n);
            n2 = n1;
            n1 = n;
        }

        // Always have a newline at the end!
        // Otherwise, weird stuff can happen to your terminal prompt.
        System.out.println();
    }
}
