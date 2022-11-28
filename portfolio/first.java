// import java.lang.annotation.Retention;

class first {
    public static void main(String[] args) {
        // int n = 4;
        // System.out.println("Hello world");
        int[] arr = {3, 8, 9, 5, 0};
        for (int i : arr) {
            System.out.print(i);
        }
        System.out.println("Separate");
        for( int i = 0 ; i < arr.length; i++) {
            System.out.print(arr[i]);
        }
    }
}