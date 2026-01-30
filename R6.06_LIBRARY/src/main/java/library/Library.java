
package library;

import java.util.*;


public class Library {
    private static List<Book> books = new ArrayList<>();
    private static Map<String, Borrower> loans = new HashMap<>();

   
    public static void addBook(Book book) {
        books.add(book);
    }

    public static List<Book> getBooks() {
        return books;
    }

    public static void clearBooks() {
        books.clear();
    }
    public static void clearLoans() {
        loans.clear();
    }
    public static void clear() {
        books.clear();
        loans.clear();
    }
    
    public static Map<String, Borrower> getLoans() {
        return loans;
    }
    public static void addLoan(String isbn, Borrower borrower) {
        loans.put(isbn, borrower);
    }

    public static void removeLoan(String isbn) {
        loans.remove(isbn);
    }

    public static void borrowBook(String isbn, Borrower borrower) {
        loans.put(isbn, borrower);
    }

    public static void borrowBook(String isbn,String borrowerName) {
        loans.put(isbn, new Borrower(borrowerName));
    }   
    
    public static Book byIsbn(String isbn) {
        for (Book b : books) if (b.getIsbn().equals(isbn)) return b;
        return null;
    }

    public static boolean isBorrowed(String isbn) {
        return loans.containsKey(isbn);
    }


}
