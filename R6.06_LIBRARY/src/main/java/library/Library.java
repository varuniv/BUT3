
package library;

import java.util.*;


public class Library {
    public static List<Book> books = new ArrayList<>();
    public static Map<String, Borrower> loans = new HashMap<>();

   
    public static Book byIsbn(String isbn) {
        for (Book b : books) if (b.getIsbn().equals(isbn)) return b;
        return null;
    }

    public static boolean isBorrowed(String isbn) {
        return loans.containsKey(isbn);
    }
}
