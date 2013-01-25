/**
 * Prints the first 20 numbers of the Fibonacci sequence.
 *
 * @author Matthias
 */
public class Fibonacci {
	public static void main(String[] args) {
		System.out.println("0");
		System.out.println("1");

		int n;
		int n2 = 0;
		int n1 = 1;

		for (int i = 0; i <= 17; i++) {
			n = n1 + n2;
			System.out.println(n);
			n2 = n1;
			n1 = n;
		}
		System.out.println();
	}
}
