/**
 * Prints Fibonacci stuff
 *
 * @author Robert
 */
public class Fibonacci{
public static void main(String[] args){
    System.out.print("0, 1");

    int n;
    int n_2=0;
    int n_1=1;

    for (int i=0; i<=17; i++) {
        n=n_1+n_2;
        System.out.print(", "+n);
        n_2=n_1;
        n_1=n;
    }
    System.out.println();
}
