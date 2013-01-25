/**
 * Prints 20 Fibonacci numbers.
 *
 * @author Lina
 */
public class Fibonacci {
    public static void main(String[] args) {
        System.out.print("0, 1");

        int n;
        int n_2 = 0, n_1 = 1;

        for (int i = 1; i <= 18; i++) {
            n = n_1 + n_2;
            System.out.print(", " + n);
            n_2 = n_1;
            n_1 = n;
        }
        System.out.println();
    }
}
