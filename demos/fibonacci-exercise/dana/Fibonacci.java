/**
 * Program that generates a LOT more than 20 numbers of the Fibonacci
 * sequence.
 *
 * @author Dana
 */
public class Fibonacci {
    public static void main (String[] argv) {
        System.out.print("0, 1");

        int n;
        int n_2 = 0, n_1 = 1;

        for (;;) {
            n = n_1 + n_2;
            System.out.print(", " + n);
            n_2 = n_1;
            n_1 = n;
        }
    }
}
